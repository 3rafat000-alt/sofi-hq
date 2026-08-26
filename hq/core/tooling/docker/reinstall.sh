#!/usr/bin/env bash
# (comment)
# (comment)
set -euo pipefail

echo "done"
systemctl disable --now docker.service docker.socket containerd.service 2>/dev/null || true
pkill -9 dockerd 2>/dev/null || true
export DEBIAN_FRONTEND=noninteractive
apt-get purge -y 'docker*' 'containerd*' 'runc' 2>/dev/null || true
apt-get autoremove -y >/dev/null
rm -rf /var/lib/docker /var/lib/containerd /etc/docker /run/containerd
echo "done"

echo "done"
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list
apt-get update -qq
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "done"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
install -m 0644 "$SCRIPT_DIR/daemon.json" /etc/docker/daemon.json
groupadd -f docker
usermod -aG docker es3dlll          # (comment)
systemctl enable --now docker
sleep 2
docker info >/dev/null && echo "done"
echo "done"
