#!/usr/bin/env python3
"""
Sofi MCP Broker — Agent Network
===================================
طوبولوجيا شبكة الوكلاء — التوجيه، التسجيل، الاكتشاف
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class NetworkTopology:
    """طوبولوجيا الشبكة الكاملة"""
    version: str = "7.0.0"
    total_agents: int = 533
    levels: Dict[int, str] = field(default_factory=lambda: {
        0: "executive (CEO)",
        1: "management (GM)",
        2: "office_lead",
        3: "lead_agent",
        4: "micro_agent"
    })
    offices: List[str] = field(default_factory=lambda: [
        "engineering", "creative", "quality", "ai_data"
    ])


class AgentNetwork:
    """شبكة الوكلاء — تعارف، توجيه، اكتشاف"""
    
    def __init__(self):
        self.topology = NetworkTopology()
        self.nodes: Dict[str, Dict] = {}  # agent_id -> node info
        self.connections: Dict[str, Set[str]] = {}  # agent_id -> connected agents
        self.office_groups: Dict[str, List[str]] = {
            "engineering": [],
            "creative": [],
            "quality": [],
            "ai_data": []
        }
        self.level_groups: Dict[int, List[str]] = {i: [] for i in range(5)}
    
    def register_node(self, agent_id: str, name: str, title: str,
                       office: str, level: int, skills: List[str]) -> Dict:
        """تسجيل عقدة في الشبكة"""
        node = {
            "agent_id": agent_id,
            "name": name,
            "title": title,
            "office": office,
            "level": level,
            "skills": skills,
            "status": "online",
            "registered_at": datetime.now().isoformat(),
            "last_heartbeat": datetime.now().isoformat(),
            "tools_built": 0,
            "tasks_completed": 0,
            "consultations_participated": 0
        }
        self.nodes[agent_id] = node
        
        # تجميع حسب المكتب
        if office in self.office_groups:
            self.office_groups[office].append(agent_id)
        
        # تجميع حسب المستوى
        if level in self.level_groups:
            self.level_groups[level].append(agent_id)
        
        # اتصالات افتراضية حسب الهيكل التنظيمي
        self.connections[agent_id] = set()
        self._setup_default_connections(agent_id, level, office)
        
        return node
    
    def _setup_default_connections(self, agent_id: str, level: int, office: str):
        """إنشاء اتصالات افتراضية حسب الهيكل"""
        # رؤساء
        if level == 4:  # Micro → Lead
            leads = self.level_groups.get(3, [])
            for lead_id in leads:
                if self.nodes.get(lead_id, {}).get("office") == office:
                    self.connections[agent_id].add(lead_id)
                    if lead_id not in self.connections:
                        self.connections[lead_id] = set()
                    self.connections[lead_id].add(agent_id)
        
        elif level == 3:  # Lead → Office Lead
            office_leads = self.level_groups.get(2, [])
            for ol_id in office_leads:
                if self.nodes.get(ol_id, {}).get("office") == office:
                    self.connections[agent_id].add(ol_id)
                    if ol_id not in self.connections:
                        self.connections[ol_id] = set()
                    self.connections[ol_id].add(agent_id)
        
        # زملاء في نفس المكتب
        colleagues = self.office_groups.get(office, [])
        for col_id in colleagues:
            if col_id != agent_id:
                self.connections[agent_id].add(col_id)
    
    def connect_agents(self, agent_a: str, agent_b: str):
        """ربط وكيلين مباشرة"""
        if agent_a not in self.connections:
            self.connections[agent_a] = set()
        if agent_b not in self.connections:
            self.connections[agent_b] = set()
        self.connections[agent_a].add(agent_b)
        self.connections[agent_b].add(agent_a)
    
    def find_path(self, from_agent: str, to_agent: str) -> List[str]:
        """إيجاد أقصر طريق بين وكيلين (BFS)"""
        if from_agent not in self.nodes or to_agent not in self.nodes:
            return []
        
        visited = {from_agent}
        queue = [[from_agent]]
        
        while queue:
            path = queue.pop(0)
            current = path[-1]
            
            if current == to_agent:
                return path
            
            for neighbor in self.connections.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        
        return []
    
    def find_agents_by_skill(self, skill: str, office: str = None) -> List[Dict]:
        """البحث عن وكلاء بمهارة محددة"""
        results = []
        for agent_id, node in self.nodes.items():
            if skill in node["skills"]:
                if office and node["office"] != office:
                    continue
                results.append(node)
        return results
    
    def get_office_network(self, office: str) -> Dict:
        """شبكة مكتب محدد"""
        members = self.office_groups.get(office, [])
        return {
            "office": office,
            "total_members": len(members),
            "members": [self.nodes.get(mid, {}) for mid in members],
            "connections": sum(len(self.connections.get(mid, set())) for mid in members)
        }
    
    def get_network_stats(self) -> Dict:
        """إحصائيات الشبكة"""
        return {
            "total_nodes": len(self.nodes),
            "total_connections": sum(len(c) for c in self.connections.values()),
            "nodes_by_level": {str(k): len(v) for k, v in self.level_groups.items()},
            "nodes_by_office": {k: len(v) for k, v in self.office_groups.items()},
            "avg_connections": sum(len(c) for c in self.connections.values()) / max(len(self.nodes), 1)
        }
    
    def remove_node(self, agent_id: str):
        """إزالة عقدة من الشبكة"""
        self.nodes.pop(agent_id, None)
        
        # إزالة من المجموعات
        for group in self.office_groups.values():
            if agent_id in group:
                group.remove(agent_id)
        for group in self.level_groups.values():
            if agent_id in group:
                group.remove(agent_id)
        
        # إزالة الاتصالات
        self.connections.pop(agent_id, None)
        for conns in self.connections.values():
            conns.discard(agent_id)
