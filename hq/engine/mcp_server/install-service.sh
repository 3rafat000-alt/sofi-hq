## FILE: hq/engine/mcp_server/install-service.sh
#!/usr/bin/env bash
set -e
# SOFI MCP — تثبيت الخدمة الدائمة (systemd user — تعمل بعد إعادة التشغيل)
DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE="$HOME/.config/systemd/user/sofi-mcp.service"
echo "🔧 تثبيت خدمة SOFI MCP الدائمة..."
mkdir -p ~/.config/systemd/user

# Create service file if not exists (or overwrite)
cat > "$SERVICE" <<'EOS'
[Unit]
Description=SOFI HQ Local MCP Server — Ticket Bus + Memory (Law 2/3/4/7) — localhost:8765
Documentation=file:///home/es3dlll/Desktop/SOFI/hq/engine/mcp_server/README.md
After=network.target network-online.target
Wants=network-online.target
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
Type=simple
WorkingDirectory=/home/es3dlll/Desktop/SOFI/hq/engine/mcp_server
Environment=PYTHONPATH=/home/es3dlll/Desktop/SOFI
EnvironmentFile=-/home/es3dlll/Desktop/SOFI/hq/engine/mcp_server/.env
ExecStart=/bin/bash /home/es3dlll/Desktop/SOFI/hq/engine/mcp_server/start-prod.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=3
TimeoutStopSec=10
KillMode=mixed
StandardOutput=append:/home/es3dlll/Desktop/SOFI/hq/engine/mcp_server/data/server.log
StandardError=append:/home/es3dlll/Desktop/SOFI/hq/engine/mcp_server/data/server.log
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=tmpfs
ReadWritePaths=/home/es3dlll/Desktop/SOFI/hq/engine/mcp_server/data /home/es3dlll/Desktop/SOFI/hq/brain
MemoryMax=500M
CPUQuota=100%

[Install]
WantedBy=default.target
EOS

echo "✅ تم إنشاء $SERVICE"

# Enable linger (يضمن التشغيل بعد إعادة التشغيل حتى بدون تسجيل دخول)
if command -v loginctl &>/dev/null; then
  if [ "$(loginctl show-user "$USER" -p Linger --value 2>/dev/null)" != "yes" ]; then
    echo "🔑 تفعيل linger..."
    loginctl enable-linger "$USER" 2>&1 || sudo loginctl enable-linger "$USER" || true
  fi
  echo "✅ Linger: $(loginctl show-user "$USER" -p Linger --value)"
fi

# Reload and enable
systemctl --user daemon-reload
systemctl --user enable sofi-mcp.service
systemctl --user restart sofi-mcp.service
sleep 3
systemctl --user status sofi-mcp.service --no-pager | head -n 30
echo ""
echo "🔍 فحص الصحة..."
KEY=$(grep -E "^SOFI_MCP_API_KEY" "$DIR/.env" 2>/dev/null | cut -d= -f2 | tr -d ' '); KEY=${KEY:-dev-key-change-me}
if curl -sf -H "X-API-Key: $KEY" http://127.0.0.1:8765/health | python3 -m json.tool | head -n 15; then
  echo "✅ الخدمة تعمل وستعود تلقائياً بعد إعادة التشغيل"
else
  echo "⚠️ فشل فحص الصحة — راجع: journalctl --user -u sofi-mcp.service --since '1 min ago'"
  exit 1
fi
echo ""
echo "📋 أوامر الإدارة:"
echo "  systemctl --user status sofi-mcp.service    # الحالة"
echo "  systemctl --user restart sofi-mcp.service   # إعادة تشغيل"
echo "  systemctl --user stop sofi-mcp.service      # إيقاف"
echo "  journalctl --user -u sofi-mcp.service -f    # السجلات الحية"
echo "  tail -f hq/engine/mcp_server/data/server.log # سجل الخادم"
