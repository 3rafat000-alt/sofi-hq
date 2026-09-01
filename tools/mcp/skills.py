#!/usr/bin/env python3
"""
🧬 Sofi Skills MCP — سجل المهارات لكل الوكلاء
يوفر معلومات عن المهارات المسجلة للوكلاء مع إمكانية البحث
"""

import sys, os, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from tools.mcp.base import SofiBaseMCP

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "../../agents/sofi_skill_registry.json")

class SkillsMCP(SofiBaseMCP):
    def __init__(self):
        super().__init__("🧬 sofi-skills", "7.0.0", tools=[
            {
                "name": "skill_registry",
                "description": "🧬 سجل المهارات — 70 تعريفاً، 20 وكيلاً مسجلاً، 4 مكاتب",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "office": {
                            "type": "string", "enum": ["engineering", "creative", "quality", "ai_data"],
                            "description": "المكتب (اختياري — يعرض الكل إذا لم تحدد)"
                        }
                    }
                }
            },
            {
                "name": "agent_skills",
                "description": "🔍 عرض مهارات وكيل معين",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_id": {
                            "type": "string",
                            "description": "معرف الوكيل (architect, builder, security, ...)"
                        }
                    },
                    "required": ["agent_id"]
                }
            },
            {
                "name": "find_agents_by_skill",
                "description": "🎯 البحث عن وكلاء يمتلكون مهارة محددة",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": "اسم المهارة (python_programming, laravel_core, ...)"
                        },
                        "min_proficiency": {
                            "type": "number",
                            "description": "الحد الأدنى للكفاءة (0.0 - 1.0, افتراضي: 0.5)"
                        }
                    },
                    "required": ["skill_name"]
                }
            },
            {
                "name": "skill_stats",
                "description": "📊 إحصائيات المهارات الكاملة — عدد الوكلاء المسجلين، المهارات، التوزيع",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ])
    
    def _get_registry(self):
        """جلب السجل مع تحميل البيانات المخزنة"""
        from tools.mcp_broker.skill_registry import SkillRegistry
        registry = SkillRegistry()
        registry.load(REGISTRY_PATH)
        return registry
    
    async def handle_tool_call(self, name: str, arguments: dict) -> dict:
        registry = self._get_registry()
        
        if name == "skill_registry":
            office = arguments.get("office")
            if office:
                data = registry.get_office_skills_summary(office)
            else:
                data = registry.get_all_skills_hierarchy()
            return self._text_result(json.dumps(data, indent=2, ensure_ascii=False))
        
        elif name == "agent_skills":
            agent_id = arguments.get("agent_id")
            if not agent_id:
                return self._text_error("❌ يرجى تحديد agent_id")
            
            skills = registry.get_agent_skills(agent_id)
            if not skills:
                # Try finding partial match
                all_agents = registry.agent_skills
                matches = {aid: s for aid, s in all_agents.items() if agent_id in aid}
                if matches:
                    result = {}
                    for aid, s in matches.items():
                        result[aid] = {
                            skill_name: {
                                "proficiency": skill.proficiency,
                                "level": skill.level_label,
                                "certified": skill.certified,
                                "years_experience": skill.years_experience,
                                "active": skill.is_active
                            }
                            for skill_name, skill in s.items()
                        }
                    return self._text_result(json.dumps(result, indent=2, ensure_ascii=False))
                return self._text_error(f"❌ وكيل '{agent_id}' غير موجود")
            
            result = {
                skill_name: {
                    "proficiency": skill.proficiency,
                    "level": skill.level_label,
                    "certified": skill.certified,
                    "years_experience": skill.years_experience,
                    "active": skill.is_active
                }
                for skill_name, skill in skills.items()
            }
            return self._text_result(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif name == "find_agents_by_skill":
            skill_name = arguments.get("skill_name")
            min_prof = arguments.get("min_proficiency", 0.5)
            agents = registry.find_agents_by_skill(skill_name, min_prof)
            
            result = {
                "skill": skill_name,
                "min_proficiency": min_prof,
                "agents_found": len(agents),
                "agents": agents
            }
            
            # Add proficiency details
            details = {}
            for agent_id in agents:
                prof = registry.get_agent_proficiency(agent_id, skill_name)
                details[agent_id] = f"{prof:.0%}"
            result["proficiencies"] = details
            
            return self._text_result(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif name == "skill_stats":
            stats = registry.get_stats()
            
            # إضافة معلومات إضافية
            by_office = {"engineering": 0, "creative": 0, "quality": 0, "ai_data": 0}
            for agent_id in registry.agent_skills:
                # تحديد المكتب من اسم الوكيل
                for office in by_office:
                    if office in agent_id or any(
                        a["agent_id"] == agent_id 
                        for agents_list in [self._get_office_agents(office)]
                        for a in agents_list
                    ):
                        by_office[office] += 1
                        break
            
            stats["agents_by_office"] = by_office
            stats["registry_file"] = REGISTRY_PATH
            
            return self._text_result(json.dumps(stats, indent=2, ensure_ascii=False))
        
        return self._text_error(f"أداة غير معروفة: {name}")
    
    def _get_office_agents(self, office: str):
        """قائمة وكلاء مكتب معين"""
        mapping = {
            "engineering": ["architect", "builder", "db_engineer", "devops", "eng_assistant"],
            "creative": ["brand_designer", "ui_designer", "motion", "ux_research", "a11y"],
            "quality": ["security", "tester", "reviewer", "red_hacker", "recon"],
            "ai_data": ["assistant", "documenter", "release", "prompt_engineer", "auto_engineer"]
        }
        return [{"agent_id": aid} for aid in mapping.get(office, [])]

asyncio.run(SkillsMCP().run())
