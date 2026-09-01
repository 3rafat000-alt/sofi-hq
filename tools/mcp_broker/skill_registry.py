#!/usr/bin/env python3
"""
Sofi MCP Broker — Skill Registry v7.0 ULTIMATE
===================================================
سجل المهارات الهرمي الصارم — 533 وكيلاً، 5 مستويات، آلاف المهارات
كل وكيل له مهارات محددة بدقة من Micro → Lead → Office → GM → CEO
"""
# ═══════════════════════════════════════════════════════════════
# المبادئ الصارمة لنظام المهارات
# ═══════════════════════════════════════════════════════════════
# 1. 🎯 الدقة: كل مهارة محددة بدقة مع متطلباتها وشروطها
# 2. 🏛️ الهرمية: المهارات تتزايد تعقيداً كلما صعدنا للأعلى
# 3. 🔒 الصرامة: لا يمكن لوكيل ادعاء مهارة دون إثبات الكفاءة
# 4. 🔄 التدرج: Micro → Lead → Office → GM → CEO
# 5. 📊 القياس: كل مهارة تقاس بـ KPIs محددة
# 6. 🛡️ الأمان: مهارات الأمان إلزامية لكل المستويات
# 7. 📝 التوثيق: كل مهارة مصحوبة بتوثيق وشروط استخدام
# ═══════════════════════════════════════════════════════════════

import os, json
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class SkillLevel(str, Enum):
    """مستوى المهارة — يتزايد مع الرتبة"""
    MICRO = "micro"           # المستوى 4 — وكيل فرعي
    LEAD = "lead"             # المستوى 3 — وكيل رئيسي
    OFFICE = "office"         # المستوى 2 — قائد مكتب
    GM = "gm"                 # المستوى 1 — مدير عام
    CEO = "ceo"               # المستوى 0 — القائد
    COUNCIL = "council"       # مجلس المستشارين


class SkillCategory(str, Enum):
    """تصنيف المهارات"""
    CORE = "core"                    # أساسية — الكل يمتلكها
    TECHNICAL = "technical"          # تقنية
    ENGINEERING = "engineering"      # هندسية
    CREATIVE = "creative"            # إبداعية
    SECURITY = "security"            # أمنية
    AI = "ai"                        # ذكاء اصطناعي
    MANAGEMENT = "management"        # إدارية
    COMMUNICATION = "communication"  # تواصلية
    LEADERSHIP = "leadership"        # قيادية
    STRATEGIC = "strategic"          # استراتيجية


@dataclass
class SkillPrerequisite:
    """متطلبات المهارة — شروط صارمة"""
    skill_name: str
    min_proficiency: float = 0.7  # minimum 70%
    description: str = ""


@dataclass
class SkillKPI:
    """مؤشرات أداء المهارة"""
    name: str
    target: str
    measurement: str
    severity: str = "medium"  # low, medium, high, critical


@dataclass
class SkillDefinition:
    """تعريف مهارة — وحدة بناء المعرفة"""
    name: str
    category: SkillCategory
    level: SkillLevel = SkillLevel.MICRO
    description: str = ""
    long_description: str = ""
    prerequisites: List[SkillPrerequisite] = field(default_factory=list)
    related_skills: List[str] = field(default_factory=list)
    difficulty: str = "intermediate"  # beginner, intermediate, advanced, expert, master
    years_to_master: int = 2
    tools_required: List[str] = field(default_factory=list)
    kpis: List[SkillKPI] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    usage_conditions: List[str] = field(default_factory=list)  # شروط الاستخدام
    min_approval_level: str = "micro"  # minimum level that can use this
    is_mandatory: bool = False  # هل هي إلزامية؟
    safety_critical: bool = False  # هل تتعلق بالأمان؟

    def __hash__(self):
        return hash(self.name)


@dataclass
class AgentSkill:
    """مهارة يمتلكها وكيل — مع تقييم صارم"""
    skill_name: str
    proficiency: float  # 0.0 to 1.0 (90%+ = expert, 70%+ = advanced, 50%+ = intermediate)
    years_experience: int = 0
    certified: bool = False
    last_assessed: str = ""  # تاريخ آخر تقييم
    assessed_by: str = ""    # من قام بالتقييم
    tools_built_with: List[str] = field(default_factory=list)
    violations: int = 0      # عدد مرات مخالفة شروط الاستخدام
    is_active: bool = True

    @property
    def level_label(self) -> str:
        if self.proficiency >= 0.9:
            return "🏆 خبير"
        elif self.proficiency >= 0.75:
            return "⭐ متقدم"
        elif self.proficiency >= 0.5:
            return "📗 متوسط"
        else:
            return "📘 مبتدئ"


class SkillRegistry:
    """سجل المهارات الهرمي الصارم — 533 وكيلاً، 5 مستويات، 40+ مهارة"""
    
    def __init__(self):
        # ── قواعد المهارات حسب المستوى ──
        self.core_skills: Dict[str, SkillDefinition] = {}
        self.office_skills: Dict[str, Dict[str, SkillDefinition]] = {
            "engineering": {},
            "creative": {},
            "quality": {},
            "ai_data": {}
        }
        self.leadership_skills: Dict[str, SkillDefinition] = {}
        self.strategic_skills: Dict[str, SkillDefinition] = {}
        
        # ── مهارات الوكلاء (agent_id -> {skill_name -> AgentSkill}) ──
        self.agent_skills: Dict[str, Dict[str, AgentSkill]] = {}
        
        # ── سجل انتهاكات المهارات ──
        self.violation_log: List[Dict] = []
        
        self._initialize_all_skills()
    
    def _initialize_all_skills(self):
        """تهيئة جميع المهارات — من Micro إلى CEO"""
        self._init_core_skills()          # 8 مهارات أساسية — كل الـ 533
        self._init_engineering_skills()   # 12 مهارة — مكتب Engineering
        self._init_creative_skills()      # 12 مهارة — مكتب Creative
        self._init_quality_skills()       # 12 مهارة — مكتب Quality
        self._init_ai_skills()            # 12 مهارة — مكتب AI & Data
        self._init_leadership_skills()    # 8 مهارات قيادية — GM + CEO
        self._init_strategic_skills()     # 6 مهارات استراتيجية — CEO + Council
    
    # ══════════════════════════════════════════════════════════
    # 1. المهارات الأساسية — إلزامية لكل الـ 533 وكيل
    # ══════════════════════════════════════════════════════════
    def _init_core_skills(self):
        """8 مهارات أساسية — كل وكيل يمتلكها. إلزامية. غير قابلة للتفاوض."""
        self.core_skills = {
            # ── البرمجة ──
            "python_programming": SkillDefinition(
                name="Python Programming",
                category=SkillCategory.CORE,
                level=SkillLevel.MICRO,
                description="كتابة كود Python نظيف وفعّال وآمن",
                long_description="""إتقان كتابة كود Python يتبع أفضل الممارسات:
                • PEP 8 — أسلوب الكتابة الموحد
                • Type Hints — كتابة كود آمن الأنواع
                • Docstrings — توثيق كل دالة وكلاس
                • Error Handling — معالجة استثناءات دقيقة
                • Testing — كتابة اختبارات للكود""",
                difficulty="intermediate",
                years_to_master=3,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع استخدام eval() أو exec()",
                    "❌ ممنوع ترك except فارغاً",
                    "✅ إلزامي استخدام Type Hints",
                    "✅ إلزامي كتابة Docstring لكل دالة",
                    "✅ إلزامي تغطية اختبارات ≥ 80%"
                ],
                kpis=[
                    SkillKPI("جودة الكود", "≥ 8/10", "Pylint/Ruff", "high"),
                    SkillKPI("تغطية اختبارات", "≥ 80%", "Pytest-cov", "high"),
                ]
            ),
            # ── التفكير النقدي ──
            "critical_thinking": SkillDefinition(
                name="Critical Thinking",
                category=SkillCategory.CORE,
                level=SkillLevel.MICRO,
                description="تحليل المشكلات واتخاذ قرارات منطقية",
                long_description="""منهجية التفكير النقدي الإلزامية:
                • تحليل الموقف من جميع الزوايا
                • تحديد الافتراضات والتحيزات
                • تقييم الأدلة والمصادر
                • استخلاص استنتاجات منطقية
                • مراجعة القرار وتقييم النتائج""",
                difficulty="advanced",
                years_to_master=5,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع اتخاذ قرار بدون تحليل",
                    "❌ ممنوع تجاهل الأدلة المخالفة",
                    "✅ إلزامي توثيق عملية التفكير",
                    "✅ إلزامي ذكر 3 سيناريوهات على الأقل"
                ]
            ),
            # ── التواصل عبر MCP ──
            "mcp_communication": SkillDefinition(
                name="MCP Communication Protocol",
                category=SkillCategory.CORE,
                level=SkillLevel.MICRO,
                description="التواصل عبر ناقل الرسائل MCP — إرسال، استقبال، بث",
                long_description="""بروتوكول التواصل الموحد:
                • JSON-RPC 2.0 — تنسيق الرسائل
                • 4 أولويات: low, medium, high, critical
                • 20 نوع رسالة: consult, research, tool, task, system
                • الاشتراك في الأحداث (Pub/Sub)
                • طلب واستقبال الردود""",
                difficulty="intermediate",
                years_to_master=1,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع إرسال رسائل بدون عنوان",
                    "❌ ممنوع تجاهل الرسائل الحرجة",
                    "✅ إلزامي الرد على الرسائل خلال 30s",
                    "✅ إلزامي توثيق كل رسالة"
                ]
            ),
            # ── بناء الأدوات ──
            "tool_building": SkillDefinition(
                name="Python Tool Building",
                category=SkillCategory.CORE,
                level=SkillLevel.LEAD,
                description="بناء أدوات Python خاصة ومشاركتها مع الوكلاء",
                long_description="""منهجية بناء الأدوات:
                • تحليل الحاجة قبل البناء
                • تصميم واجهة الاستخدام (API)
                • فحص أمني قبل النشر
                • اختبار شامل بعد البناء
                • توثيق الأداة كاملاً
                • تسجيل في الكتالوج المركزي""",
                prerequisites=[
                    SkillPrerequisite("python_programming", 0.8, "يجب إتقان Python أولاً")
                ],
                difficulty="advanced",
                years_to_master=3,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع بناء أداة بدون فحص أمني",
                    "❌ ممنوع استخدام eval/exec في الأداة",
                    "✅ إلزامي اختبار الأداة قبل النشر",
                    "✅ إلزامي توثيق واجهة الاستخدام"
                ],
                safety_critical=True
            ),
            # ── التوثيق ──
            "documentation": SkillDefinition(
                name="Documentation & Technical Writing",
                category=SkillCategory.CORE,
                level=SkillLevel.MICRO,
                description="توثيق الكود والعمليات بشكل احترافي",
                long_description="""معايير التوثيق الإلزامية:
                • README — وصف المشروع والتشغيل
                • API Docs — توثيق كل Endpoint
                • Docstrings — توثيق الكود
                • Changelog — سجل التغييرات
                • Architecture — توثيق البنية""",
                difficulty="beginner",
                years_to_master=1,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع تسليم كود بدون توثيق",
                    "✅ إلزامي توثيق API Endpoints",
                    "✅ إلزامي تحديث الوثائق مع الكود"
                ]
            ),
            # ── مراجعة الكود ──
            "code_review": SkillDefinition(
                name="Code Review & Quality Assurance",
                category=SkillCategory.CORE,
                level=SkillLevel.MICRO,
                description="مراجعة الكود واكتشاف المشكلات والثغرات",
                long_description="""معايير مراجعة الكود:
                • Clean Code — قراءة وفهم الكود
                • SOLID Principles — التحقق من المبادئ
                • Security Scan — فحص أمني
                • Performance — تقييم الأداء
                • Best Practices — الالتزام بالمعايير""",
                prerequisites=[
                    SkillPrerequisite("python_programming", 0.6)
                ],
                difficulty="intermediate",
                years_to_master=2,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع الموافقة على كود بدون مراجعة",
                    "❌ ممنوع تجاهل الثغرات الأمنية",
                    "✅ إلزامي فحص أمني لكل Commit"
                ],
                safety_critical=True
            ),
            # ── البحث العميق ──
            "deep_research": SkillDefinition(
                name="Deep Research & Analysis",
                category=SkillCategory.CORE,
                level=SkillLevel.LEAD,
                description="البحث والتحليل العميق متعدد المصادر",
                long_description="""منهجية البحث:
                • تحديد سؤال البحث بدقة
                • جمع المصادر (4 مستويات: quick, standard, deep, exhaustive)
                • تحليل المعلومات وتقييمها
                • استخلاص التوصيات
                • قياس الثقة في النتائج
                • تحديد الفجوات المعرفية""",
                difficulty="advanced",
                years_to_master=4,
                constraints=[
                    "❌ ممنوع الاعتماد على مصدر واحد",
                    "❌ ممنوع تقديم توصيات بدون أدلة",
                    "✅ إلزامي ذكر جميع المصادر",
                    "✅ إلزامي تقييم الثقة في النتائج"
                ]
            ),
            # ── التشاور مع الوكلاء ──
            "consultation": SkillDefinition(
                name="Agent Consultation & Consensus Building",
                category=SkillCategory.CORE,
                level=SkillLevel.LEAD,
                description="التشاور مع الوكلاء الآخرين والوصول لتوافق",
                long_description="""بروتوكول التشاور:
                • بدء جلسة تشاور بموضوع واضح
                • دعوة المشاركين المناسبين
                • تقديم الرأي مع الأدلة
                • التصويت: موافق/رفض/مراجعة/استفسار
                • مناقشة الخلافات والوصول لتوافق
                • توثيق القرار النهائي""",
                prerequisites=[
                    SkillPrerequisite("mcp_communication", 0.7)
                ],
                difficulty="intermediate",
                years_to_master=2,
                constraints=[
                    "❌ ممنوع اتخاذ قرار بدون تشاور للمهام الحرجة",
                    "✅ إلزامي دعوة جميع الأطراف المعنية",
                    "✅ إلزامي توثيق آراء الأقلية"
                ]
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # 2. مهارات Engineering — 12 مهارة
    # ══════════════════════════════════════════════════════════
    def _init_engineering_skills(self):
        """12 مهارة هندسية — للمهندسين في كل المستويات"""
        self.office_skills["engineering"] = {
            # ── مستوى متقدم ──
            "laravel_core": SkillDefinition(
                name="Laravel Core Development",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="تطوير تطبيقات Laravel متكاملة بمعايير احترافية",
                long_description="""إتقان Laravel Framework:
                • MVC Architecture — فهم عميق للنمط
                • Eloquent ORM — استعلامات متقدمة
                • Service Container — حقن التبعيات
                • Events & Listeners — نظام الأحداث
                • Queues & Jobs — المهام غير المتزامنة
                • Broadcasting — البث المباشر
                • Testing — PHPUnit + Pest""",
                difficulty="expert",
                years_to_master=5,
                tools_required=["intelephense", "phpunit"],
                constraints=[
                    "❌ ممنوع استخدام DB::raw بدون مراجعة أمنية",
                    "❌ ممنوع تجاهل N+1 Queries",
                    "✅ إلزامي اتباع PSR-12",
                    "✅ إلزامي كتابة Form Requests لكل مدخل"
                ],
                safety_critical=True
            ),
            "api_architecture": SkillDefinition(
                name="API Architecture Design (REST/GraphQL)",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.OFFICE,
                description="تصميم APIs قابلة للتوسع وآمنة ومتوثقة",
                long_description="""معايير تصميم APIs:
                • RESTful — الموارد والعمليات
                • GraphQL — استعلامات مرنة
                • Versioning — إدارة الإصدارات
                • Authentication — JWT, OAuth, Sanctum
                • Rate Limiting — تحديد المعدل
                • Documentation — OpenAPI/Swagger
                • Testing — Contract Testing""",
                difficulty="expert",
                years_to_master=4,
                constraints=[
                    "❌ ممنوع API بدون توثيق",
                    "❌ ممنوع كشف معلومات حساسة في الردود",
                    "✅ إلزامي Rate Limiting على كل API",
                    "✅ إلزامي Versioning من اليوم الأول"
                ],
                safety_critical=True
            ),
            "database_mastery": SkillDefinition(
                name="Database Architecture & Optimization",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.OFFICE,
                description="تصميم وتحسين قواعد البيانات — PostgreSQL, MySQL, Redis",
                long_description="""إتقان قواعد البيانات:
                • Schema Design — التصميم الأمثل
                • Indexing — الفهرسة الذكية
                • Query Optimization — تحسين الاستعلامات
                • Migrations — إدارة التغييرات
                • Replication — النسخ المتماثل
                • Sharding — التقسيم الأفقي
                • Backup & Recovery — النسخ والاستعادة""",
                difficulty="expert",
                years_to_master=5,
                constraints=[
                    "❌ ممنوع DELETE بدون WHERE",
                    "❌ ممنوع SELECT * في الإنتاج",
                    "✅ إلزامي فهرسة الحقول المكررة",
                    "✅ إلزامي توثيق كل Migration"
                ],
                safety_critical=True
            ),
            # ── مستوى متوسط-متقدم ──
            "devops_pipeline": SkillDefinition(
                name="DevOps & CI/CD Pipeline Engineering",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="نشر وإدارة البنية التحتية الآلية",
                long_description="""إدارة دورة حياة النشر:
                • Docker — بناء وإدارة الحاويات
                • CI/CD — أتمتة الاختبار والنشر
                • GitHub Actions — سير العمل
                • Environment Management — إدارة البيئات
                • Monitoring — المراقبة والتنبيهات
                • Auto-scaling — التوسع التلقائي""",
                prerequisites=[SkillPrerequisite("docker", 0.6)],
                difficulty="advanced",
                years_to_master=4,
                constraints=[
                    "❌ ممنوع النشر بدون اختبارات",
                    "❌ ممنوع كشف Secrets في الكود",
                    "✅ إلزامي استخدام .env للإعدادات",
                    "✅ إلزامي توثيق إجراءات النشر"
                ],
                safety_critical=True
            ),
            "system_architecture": SkillDefinition(
                name="System Architecture & Microservices",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.OFFICE,
                description="تصميم الأنظمة المعقدة والـ Microservices",
                long_description="""إتقان تصميم الأنظمة:
                • DDD — Domain-Driven Design
                • CQRS — Command Query Responsibility Segregation
                • Event Sourcing — مصدر الأحداث
                • Message Queues — طوابير الرسائل
                • Service Mesh — شبكة الخدمات
                • C4 Model — توثيق البنية""",
                difficulty="expert",
                years_to_master=7,
                constraints=[
                    "❌ ممنوع Microservices بدون توثيق C4",
                    "❌ ممنوع تجاهل الـ Failure Modes",
                    "✅ إلزامي توثيق الـ Architecture Decision Records"
                ]
            ),
            "container_orchestration": SkillDefinition(
                name="Docker & Kubernetes Orchestration",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="إدارة الحاويات و Kubernetes",
                long_description="""إتقان الحاويات:
                • Dockerfiles — بناء الصور المحسنة
                • Docker Compose — تنسيق الخدمات
                • K8s — إدارة الكتلة
                • Helm Charts — قوالب النشر
                • Service Mesh — Istio/Linkerd""",
                difficulty="advanced",
                years_to_master=3,
                constraints=[
                    "❌ ممنوع استخدام latest tag في الإنتاج",
                    "❌ ممنوع تشغيل container بـ root",
                    "✅ إلزامي تحديد الموارد (CPU/Memory)",
                    "✅ إلزامي Health Checks"
                ],
                safety_critical=True
            ),
            # ── مستوى متوسط ──
            "caching_redis": SkillDefinition(
                name="Redis Caching & Performance Optimization",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="التخزين المؤقت وتحسين أداء النظام",
                long_description="""إتقان التخزين المؤقت:
                • Redis Data Types — Strings, Lists, Sets, Sorted Sets
                • Caching Strategies — Cache-Aside, Write-Through
                • Session Management — إدارة الجلسات
                • Rate Limiting — تحديد المعدل
                • Pub/Sub — النشر والاشتراك
                • Redis Cluster — العنقود""",
                difficulty="intermediate",
                years_to_master=2,
                constraints=[
                    "❌ ممنوع تخزين بيانات حساسة في Redis",
                    "❌ ممنوع تجاهل TTL",
                    "✅ إلزامي تحديد TTL لكل مفتاح",
                    "✅ إلزامي استراتيجية Cache Invalidation"
                ]
            ),
            "backend_testing": SkillDefinition(
                name="Backend Testing — PHPUnit, Pest, TDD",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="كتابة اختبارات شاملة للكود الخلفي",
                long_description="""منهجية الاختبارات:
                • Unit Testing — اختبار الوحدة
                • Feature Testing — اختبار الميزات
                • Database Testing — اختبار DB
                • API Testing — اختبار الـ APIs
                • TDD — التطوير بالمحاكمات
                • Coverage — تغطية الكود""",
                prerequisites=[SkillPrerequisite("python_programming", 0.6)],
                difficulty="intermediate",
                years_to_master=2,
                constraints=[
                    "❌ ممنوع دمج كود بدون اختبارات",
                    "❌ ممنوع تجاهل Edge Cases",
                    "✅ إلزامي تغطية ≥ 90% للكود الجديد",
                    "✅ إلزامي اختبار API Endpoints"
                ]
            ),
            # ── مستوى Micro ──
            "php_modern": SkillDefinition(
                name="Modern PHP Development (8.x)",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="كتابة كود PHP حديث بمعايير PSR-12",
                long_description="""إتقان PHP الحديث:
                • Type System — الأنواع القوية
                • Attributes — السمات
                • Enums — التعدادات
                • Readonly Properties — الخصائص المقروءة فقط
                • Named Arguments — الوسائط المسماة
                • Match Expression — تعبير المطابقة""",
                difficulty="intermediate",
                years_to_master=3,
                constraints=[
                    "❌ ممنوع استخدام extract() أو compact()",
                    "❌ ممنوع استخدام mysql_* دوال",
                    "✅ إلزامي Type Hints لكل دالة",
                    "✅ إلزامي Strict Types"
                ]
            ),
            "code_generation": SkillDefinition(
                name="Automated Code Generation & Scaffolding",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.MICRO,
                description="توليد كود آلي — Scaffolds, Boilerplates, CRUD",
                long_description="""أتمتة كتابة الكود:
                • Laravel Artisan — أوامر التوليد
                • Custom Stubs — قوالب مخصصة
                • CRUD Generator — توليد كامل
                • Migration Generator — توليد الترحيلات
                • Test Generator — توليد الاختبارات""",
                difficulty="intermediate",
                years_to_master=2,
                constraints=[
                    "❌ ممنوع توليد كود بدون مراجعة",
                    "✅ إلزامي تخصيص الـ Stubs للمشروع",
                    "✅ إلزامي اختبار الكود المولد"
                ]
            ),
            "dependency_management": SkillDefinition(
                name="Dependency Management & Security",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.MICRO,
                description="إدارة التبعيات وفحص الثغرات فيها",
                long_description="""إدارة التبعيات:
                • Composer — PHP packages
                • NPM — JavaScript packages
                • Pip — Python packages
                • Version Constraints — تحديد الإصدارات
                • Security Audit — فحص الثغرات
                • Lock Files — قفل الإصدارات""",
                difficulty="beginner",
                years_to_master=1,
                constraints=[
                    "❌ ممنوع استخدام نسخ قديمة من المكتبات",
                    "❌ ممنوع تجاهل تحذيرات الأمان",
                    "✅ إلزامي تحديث التبعيات شهرياً",
                    "✅ إلزامي فحص أمني للتبعيات"
                ],
                safety_critical=True
            ),
            # ── مهارات جديدة v2.0 — مستخلصة من tmp ──
            "flutter_development": SkillDefinition(
                name="Flutter 3.44 Development & Mobile Architecture",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="تطوير تطبيقات Flutter متكاملة بأحدث الإصدارات",
                long_description="""إتقان Flutter:
                • Widget Tree & Element Tree — إدارة شجرة الويدجت
                • State Management — Provider, Riverpod, BLoC
                • CustomPainter — رسم مخصص عالي الأداء
                • Animation — AnimationController, Hero, Implicit
                • Platform Channels — iOS/Android native
                • Web3dart — تكامل بلوكتشين
                • Testing — Unit, Widget, Integration""",
                difficulty="expert",
                years_to_master=4,
                tools_required=["flutter", "dart", "android_studio"],
                safety_critical=True
            ),
            "react_development": SkillDefinition(
                name="React 19 + TypeScript 6 Modern Development",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="تطوير تطبيقات React بأحدث الإصدارات مع TypeScript",
                long_description="""إتقان React 19:
                • Server Components — RSC architecture
                • Hooks — useOptimistic, useFormStatus
                • TypeScript 6 — أنواع متقدمة
                • shadcn/ui v4 — نظام مكونات حديث
                • Tailwind CSS v4 — فئات JIT
                • Vite 8 — بناء فائق السرعة
                • Vitest + Playwright — اختبارات كاملة""",
                difficulty="expert",
                years_to_master=4,
                tools_required=["node", "vite", "react", "typescript"],
                safety_critical=True
            ),
            "blockchain_development": SkillDefinition(
                name="Blockchain Development (Arbitrum, Solidity, Web3)",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="تطوير عقود ذكية وتكامل بلوكتشين مع Arbitrum",
                long_description="""إتقان Blockchain:
                • Solidity — عقود ذكية آمنة
                • Arbitrum — L2 scaling solutions
                • Web3.js/Ethers.js — تكامل frontend
                • HD Wallets — BIP-44, مفاتيح مشفرة
                • Smart Contract Security — ReentrancyGuard, AccessControl
                • Gas Optimization — تقليل تكاليف الغاز
                • Hardhat/Foundry — أدوات التطوير""",
                difficulty="advanced",
                years_to_master=3,
                safety_critical=True
            ),
            "smart_contract_security": SkillDefinition(
                name="Smart Contract Security Auditing",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.OFFICE,
                description="تدقيق أمني للعقود الذكية — Reentrancy, Access Control, Flash Loans",
                long_description="""إتقان أمن العقود:
                • Reentrancy Attacks — هجمات إعادة الدخول
                • Access Control — صلاحيات صارمة
                • Flash Loan Attacks — هجمات القروض البرقية
                • Oracle Manipulation — تلاعب الأوراكل
                • Slither + Mythril — أدوات التدقيق
                • Foundry Fuzz Testing — اختبارات عشوائية
                • Multi-sig & Time Locks — حوكمة العقود""",
                difficulty="advanced",
                years_to_master=4,
                safety_critical=True
            ),
            "websocket_realtime": SkillDefinition(
                name="WebSocket & Real-Time Communication Systems",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.LEAD,
                description="بناء أنظمة اتصال لحظية باستخدام WebSockets",
                long_description="""إتقان WebSocket:
                • Protocol Design — تصميم بروتوكول الرسائل
                • Reconnection — إعادة اتصال ذكية
                • Queue Management — طابور الرسائل
                • Broadcasting — Laravel Broadcasting + Pusher
                • Scaling — Redis Pub/Sub, Horizontal scaling
                • Security — WSS, Origin validation
                • LAN Multiplayer — ألعاب محلية عبر WS""",
                difficulty="advanced",
                years_to_master=3,
                tools_required=["laravel", "redis", "nodejs"],
                safety_critical=False
            ),
            "fintech_domain": SkillDefinition(
                name="Fintech Domain (KYC, Cards, Payments, Blockchain)",
                category=SkillCategory.ENGINEERING,
                level=SkillLevel.OFFICE,
                description="خبرة في المجال المالي الرقمي — KYC، بطاقات افتراضية، مدفوعات، بلوكتشين",
                long_description="""إتقان المجال المالي:
                • KYC Systems — 3 مستويات توثيق (Basic/Verified/Premium)
                • Virtual Cards — BIN, Luhn, CVV مشفر
                • Payment Gateways — Stripe, Paymob, MyFatoorah
                • Blockchain Wallets — HD, مشفرة
                • PCI DSS Compliance — 12 متطلباً
                • AML/KYC Regulations — مكافحة غسل الأموال
                • Transaction Systems — رسوم, حدود, تصدير""",
                difficulty="expert",
                years_to_master=5,
                safety_critical=True
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # 3. مهارات Creative — 12 مهارة
    # ══════════════════════════════════════════════════════════
    def _init_creative_skills(self):
        """12 مهارة إبداعية — للمصممين والمبدعين"""
        self.office_skills["creative"] = {
            "ui_mastery": SkillDefinition(
                "UI Design Mastery", SkillCategory.CREATIVE, SkillLevel.OFFICE,
                "تصميم واجهات مستخدم جذابة ومتجاوبة",
                long_description="""إتقان تصميم الواجهات:
                • Design Principles — مبادئ التصميم
                • Visual Hierarchy — التسلسل البصري
                • Color Theory — نظرية الألوان
                • Typography — طباعة محترفة
                • Responsive Design — تصميم متجاوب
                • Design Systems — أنظمة التصميم""",
                difficulty="expert", years_to_master=5,
                constraints=[
                    "❌ ممنوع استخدام ألوان بدون تباين كافٍ",
                    "✅ إلزامي احترام WCAG 2.1 AA",
                    "✅ إلزامي اختبار على 3 أحجام شاشة"
                ]
            ),
            "ux_research_deep": SkillDefinition(
                "UX Research & Usability Engineering", SkillCategory.CREATIVE, SkillLevel.OFFICE,
                "بحث وتحليل تجربة المستخدم — Personas, Journey, Usability",
                long_description="""منهجية بحث UX:
                • User Personas — شخصيات المستخدمين
                • Journey Mapping — خريطة الرحلة
                • Usability Testing — اختبار سهولة الاستخدام
                • A/B Testing — اختبار المقارنة
                • Heatmaps — خرائط الحرارة
                • Analytics — تحليل السلوك""",
                difficulty="expert", years_to_master=4,
                constraints=[
                    "❌ ممنوع التصميم بدون Personas",
                    "❌ ممنوع تجاهل Feedbacks",
                    "✅ إلزامي اختبار مع 5 مستخدمين على الأقل"
                ]
            ),
            "motion_design": SkillDefinition(
                "Motion Design & Animation", SkillCategory.CREATIVE, SkillLevel.LEAD,
                "تصميم الحركة والأنيميشن — Framer Motion, CSS, Lottie",
                long_description="""إتقان الحركة:
                • Timing — توقيت الحركة
                • Easing — منحنيات الحركة
                • Micro-interactions — التفاعلات الدقيقة
                • Page Transitions — انتقالات الصفحات
                • Loading States — حالات التحميل
                • Performance — أداء الحركة""",
                difficulty="advanced", years_to_master=4,
                constraints=[
                    "❌ ممنوع إضافة حركة بدون هدف",
                    "❌ ممنوع تجاهل Reduced Motion",
                    "✅ إلزامي احترام prefers-reduced-motion",
                    "✅ إلزامي اختبار على أجهزة ضعيفة"
                ]
            ),
            "accessibility": SkillDefinition(
                "Accessibility Engineering (WCAG 2.1 AA/AAA)", SkillCategory.CREATIVE, SkillLevel.OFFICE,
                "ضمان وصول الجميع — WCAG, ARIA, Screen Readers",
                long_description="""معايير الوصول:
                • WCAG 2.1 — 4 مبادئ, 13 دليلاً
                • ARIA — أدوار وخصائص
                • Keyboard Navigation — التنقل بلوحة المفاتيح
                • Screen Readers — NVDA, VoiceOver, TalkBack
                • Color Contrast — تباين الألوان
                • Focus Management — إدارة التركيز""",
                difficulty="advanced", years_to_master=3,
                constraints=[
                    "❌ ممنوع تصميم بدون WCAG",
                    "❌ ممنوع استخدام الألوان فقط للإشارة",
                    "✅ إلزامي WCAG 2.1 AA كحد أدنى",
                    "✅ إلزامي اختبار مع قارئ شاشة"
                ],
                safety_critical=True
            ),
            "design_systems": SkillDefinition(
                "Design Systems Architecture", SkillCategory.CREATIVE, SkillLevel.OFFICE,
                "بناء أنظمة تصميم متكاملة — Design Tokens, Components",
                long_description="""بناء نظام التصميم:
                • Design Tokens — رموز التصميم
                • Component Library — مكتبة المكونات
                • Documentation — توثيق المكونات
                • Versioning — إصدارات النظام
                • Theming — تعدد السمات
                • RTL — دعم اللغات من اليمين""",
                difficulty="expert", years_to_master=5,
                constraints=[
                    "❌ ممنوع تكرار المكونات",
                    "✅ إلزامي Design Tokens لكل قيمة",
                    "✅ إلزامي توثيق كل مكون مع أمثلة"
                ]
            ),
            "tailwind_pro": SkillDefinition(
                "Tailwind CSS Professional", SkillCategory.CREATIVE, SkillLevel.LEAD,
                "تصميم احترافي باستخدام Tailwind CSS",
                long_description="""إتقان Tailwind:
                • Utility-First — نهج الأدوات
                • Custom Config — تخصيص الإعدادات
                • Design Tokens — رموز التصميم
                • Responsive — التجاوب
                • Dark Mode — الوضع الليلي
                • Performance — تحسين الأداء""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع استخدام !important",
                    "✅ إلزامي استخدام Config للتخصيص",
                    "✅ إلزامي تنظيف الـ CSS غير المستخدم"
                ]
            ),
            "prototyping": SkillDefinition(
                "Interactive Prototyping", SkillCategory.CREATIVE, SkillLevel.LEAD,
                "بناء نماذج أولية تفاعلية — Figma, Framer",
                long_description="""بناء النماذج:
                • Low-fidelity — نماذج سريعة
                • High-fidelity — نماذج دقيقة
                • Interactions — التفاعلات
                • States — حالات المكونات
                • Feedback Loops — حلقات التغذية""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع الانتقال للكود بدون Approval",
                    "✅ إلزامي اختبار النموذج مع مستخدمين"
                ]
            ),
            "rtl_i18n": SkillDefinition(
                "RTL & Internationalization Design", SkillCategory.CREATIVE, SkillLevel.LEAD,
                "تصميم يدعم اللغات من اليمين لليسار والعولمة",
                long_description="""دعم الـ RTL:
                • Layout Mirroring — عكس التخطيط
                • Typography — طباعة RTL
                • Icons & Imagery — أيقونات وصور
                • Localization — ترجمة المحتوى
                • Cultural Adaptation — تكييف ثقافي""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع تجاهل اتجاه النص",
                    "✅ إلزامي اختبار RTL لكل صفحة",
                    "✅ إلزامي دعم العربية كحد أدنى"
                ]
            ),
            "css_architecture": SkillDefinition(
                "CSS Architecture & BEM/SMACSS", SkillCategory.CREATIVE, SkillLevel.LEAD,
                "هندسة CSS قابلة للصيانة — BEM, SMACSS, ITCSS",
                long_description="""هندسة CSS:
                • BEM — Block Element Modifier
                • SMACSS — Scalable Modular Architecture
                • ITCSS — Inverted Triangle CSS
                • CSS Custom Properties — المتغيرات
                • CSS Grid — الشبكات""",
                difficulty="advanced", years_to_master=3,
                constraints=[
                    "❌ ممنوع استخدام IDs في CSS",
                    "❌ ممنوع Nesting > 3 مستويات",
                    "✅ إلزامي اتباع BEM أو methodology"
                ]
            ),
            "component_design": SkillDefinition(
                "Component Design & Atomic Design", SkillCategory.CREATIVE, SkillLevel.LEAD,
                "تصميم مكونات ذرية — Atoms, Molecules, Organisms",
                long_description="""منهجية التصميم الذري:
                • Atoms — الذرات (Button, Input)
                • Molecules — الجزيئات (Form Field)
                • Organisms — الكائنات (Navigation Bar)
                • Templates — القوالب
                • Pages — الصفحات""",
                difficulty="advanced", years_to_master=3,
                constraints=[
                    "❌ ممنوع تصميم Pages بدون Templates",
                    "✅ إلزامي توثيق Props لكل Component"
                ]
            ),
            "figma_mastery": SkillDefinition(
                "Figma Advanced — Auto Layout, Variants, Plugins",
                SkillCategory.CREATIVE, SkillLevel.MICRO,
                "إتقان Figma — Auto Layout, Variants, Prototyping, Plugins",
                long_description="""إتقان Figma:
                • Auto Layout — التخطيط التلقائي
                • Variants — المتغيرات
                • Component Properties — خصائص المكونات
                • Interactive Components — مكونات تفاعلية
                • Plugins — الإضافات
                • Design Tokens — رموز التصميم""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع استخدام Fixed Dimensions",
                    "✅ إلزامي استخدام Auto Layout"
                ]
            ),
            "visual_debugging": SkillDefinition(
                "Visual Debugging & Cross-browser Testing",
                SkillCategory.CREATIVE, SkillLevel.MICRO,
                "تصحيح الأخطاء البصرية عبر المتصفحات والأجهزة",
                long_description="""اختبار البصريات:
                • Cross-browser — Chrome, Firefox, Safari
                • Responsive — Mobile, Tablet, Desktop
                • Pixel Perfect — مطابقة التصميم
                • Visual Regression — انحدار بصري
                • Performance — أداء التحميل""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع تجاهل الاختلافات بين المتصفحات",
                "✅ إلزامي اختبار على 3 متصفحات على الأقل"
            ]
            ),
            # ── مهارات جديدة v2.0 — مستخلصة من tmp ──
            "oklch_color_system": SkillDefinition(
                "OKLCH Color System & Design Tokens",
                SkillCategory.CREATIVE, SkillLevel.LEAD,
                "استخدام نظام OKLCH للألوان مع متغيرات تصميم دقيقة",
                long_description="""إتقان OKLCH:
                • OKLCH vs HSL/HEX — دقة لونية أعلى
                • 38+ متغير لون — Light + Dark mode
                • Color Perception — إدراك لوني متسق
                • Gamut Mapping — تغطية لونية أوسع
                • Design Tokens — متغيرات قابلة للتخصيص
                • Accessibility — تباين ألوان WCAG""",
                difficulty="advanced", years_to_master=3,
                tools_required=["tailwindcss", "figma"],
                constraints=["✅ إلزامي استخدام OKLCH في المشاريع الجديدة"]
            ),
            "svg_animation_custompainter": SkillDefinition(
                "SVG Animation & CustomPainter",
                SkillCategory.CREATIVE, SkillLevel.LEAD,
                "رسم متجهي متقدم مع أنيميشن باستخدام SVG النقي و CustomPainter",
                long_description="""إتقان الرسم المتجهي:
                • SVG Elements — line, circle, path, polyline
                • CSS Animations — animate-[drawX_0.3s_ease-out]
                • stroke-dasharray + stroke-dashoffset — رسم متحرك
                • Flutter CustomPainter — Canvas API
                • AnimationController — توقيت وتحكم
                • Performance — تجنب إعادة الرسم غير الضرورية""",
                difficulty="advanced", years_to_master=3,
                constraints=["✅ SVG النقي أفضل من الصور للرموز"]
            ),
            "shadcn_v4": SkillDefinition(
                "shadcn/ui v4 + Base UI Component System",
                SkillCategory.CREATIVE, SkillLevel.LEAD,
                "بناء أنظمة مكونات متقدمة باستخدام shadcn/ui v4 و Base UI",
                long_description="""إتقان shadcn v4:
                • Base UI v1.5 — بديل Radix UI
                • data-slot — نمط جديد للعناصر
                • CVA — Class Variance Authority
                • 6+ variants per component
                • Tailwind 4 — @import بدلاً من @tailwind
                • tw-animate-css — أنيميشن مدمج""",
                difficulty="advanced", years_to_master=3,
                tools_required=["react", "tailwindcss", "shadcn"],
                constraints=["✅ shadcn v4 هو المعيار للمشاريع الجديدة"]
            ),
            "tailwind_v4": SkillDefinition(
                "Tailwind CSS v4 Mastery",
                SkillCategory.CREATIVE, SkillLevel.OFFICE,
                "إتقان Tailwind CSS v4 مع أحدث الميزات",
                long_description="""إتقان Tailwind v4:
                • CSS-first — @import بدلاً من @tailwind directives
                • Vite Plugin — @tailwindcss/vite
                • OKLCH Colors — دعم أصلي
                • Container Queries — استعلامات الحاوية
                • @layer — تنظيم الطبقات
                • JIT — توصيل فوري
                • Dark Mode — متعدد الاستراتيجيات""",
                difficulty="expert", years_to_master=4,
                constraints=["✅ Tailwind v4 إلزامي لكل المشاريع الجديدة"]
            ),
            "design_tokens": SkillDefinition(
                "Design System Tokens & Architecture",
                SkillCategory.CREATIVE, SkillLevel.OFFICE,
                "بناء أنظمة تصميم بمتغيرات موحدة (Colors, Typography, Spacing, Breakpoints)",
                long_description="""إتقان أنظمة التصميم:
                • Token Hierarchy — Global → Alias → Component
                • Color Palette — 38 OKLCH متغيراً
                • Typography Scale — 5 مستويات (Geist, Noto Sans Arabic)
                • Spacing Scale — 7 levels (4px → 40px)
                • Breakpoints — 3 نقاط قطع (768, 1024, 1280)
                • Animation — 7 أنواع بمدة محددة
                • Documentation — DESIGN-SYSTEM.md""",
                difficulty="expert", years_to_master=4,
                safety_critical=True
            ),
            "i18n_rtl_design": SkillDefinition(
                "Internationalization & RTL Design",
                SkillCategory.CREATIVE, SkillLevel.LEAD,
                "تصميم أنظمة تدعم التعدد اللغوي والاتجاه من اليمين لليسار",
                long_description="""إتقان i18n/RTL:
                • Translation System — API + Local JSON fallback
                • RTL Layout — مرآة تلقائية للتصميم
                • Arabic Typography — خطوط عربية (Noto Kufi, Noto Naskh)
                • Locale Detection — تحديد تلقائي للغة
                • SEO — ديناميكي حسب اللغة
                • Cultural Adaptation — تكييف ثقافي""",
                difficulty="intermediate", years_to_master=2
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # 4. مهارات Quality — 12 مهارة
    # ══════════════════════════════════════════════════════════
    def _init_quality_skills(self):
        """12 مهارة أمنية وجودة — للصقور"""
        self.office_skills["quality"] = {
            "sast_dast": SkillDefinition(
                "SAST/DAST Security Scanning", SkillCategory.SECURITY, SkillLevel.OFFICE,
                "فحص أمني ثابت وديناميكي شامل",
                long_description="""المسح الأمني:
                • SAST — تحليل الكود الثابت
                • DAST — اختبار التطبيق الديناميكي
                • IAST — التحليل التفاعلي
                • RASP — حماية وقت التشغيل
                • SCA — تحليل التكوين""",
                difficulty="expert", years_to_master=5,
                is_mandatory=True, safety_critical=True,
                constraints=[
                    "❌ ممنوع تجاوز الفحص الأمني",
                    "❌ ممنوع تجاهل الثغرات الحرجة",
                    "✅ إلزامي فحص كل Commit",
                    "✅ إلزامي تقرير أمني أسبوعي"
                ]
            ),
            "penetration_testing": SkillDefinition(
                "Penetration Testing & Ethical Hacking", SkillCategory.SECURITY, SkillLevel.OFFICE,
                "اختبار الاختراق الأخلاقي — اكتشاف واستغلال الثغرات",
                long_description="""منهجية الاختراق:
                • Reconnaissance — جمع المعلومات
                • Scanning — مسح الثغرات
                • Exploitation — استغلال الثغرات
                • Post-exploitation — ما بعد الاستغلال
                • Reporting — إعداد التقارير""",
                difficulty="expert", years_to_master=6,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع استغلال ثغرة بدون إذن",
                    "❌ ممنوع تسريب معلومات حساسة",
                    "✅ إلزامي توثيق كل خطوة",
                    "✅ إلزامي تقرير مع CVSS Scores"
                ]
            ),
            "owasp_top10": SkillDefinition(
                "OWASP Top 10 Expert", SkillCategory.SECURITY, SkillLevel.LEAD,
                "إتقان أشهر 10 ثغرات أمنية وطرق الوقاية",
                long_description="""OWASP Top 10 (2021):
                1. Broken Access Control
                2. Cryptographic Failures
                3. Injection (SQL, NoSQL, OS, LDAP)
                4. Insecure Design
                5. Security Misconfiguration
                6. Vulnerable Components
                7. Auth Failures
                8. Data Integrity Failures
                9. Logging Failures
                10. SSRF""",
                difficulty="advanced", years_to_master=3,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع تجاهل OWASP Top 10",
                    "✅ إلزامي فحص OWASP قبل الإطلاق",
                    "✅ إلزامي تدريب الفريق على OWASP"
                ]
            ),
            "code_audit_security": SkillDefinition(
                "Code Security Audit", SkillCategory.SECURITY, SkillLevel.OFFICE,
                "مراجعة أمنية شاملة للكود — Manual + Automated",
                long_description="""مراجعة الكود الأمنية:
                • Automated Scanning — فحص آلي
                • Manual Review — مراجعة يدوية
                • Dependency Check — فحص التبعيات
                • Secret Detection — كشف الأسرار
                • Compliance Check — فحص الامتثال""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع مرور كود بدون مراجعة أمنية",
                    "✅ إلزامي فحص Secrets في الكود",
                    "✅ إلزامي تقرير أمني لكل مراجعة"
                ]
            ),
            "unit_testing_mastery": SkillDefinition(
                "Unit Testing & TDD Mastery", SkillCategory.SECURITY, SkillLevel.LEAD,
                "كتابة اختبارات وحدة شاملة — TDD, Mutation Testing",
                long_description="""إتقان اختبارات الوحدة:
                • TDD — Red, Green, Refactor
                • BDD — Behavior Driven
                • Mocking — المحاكاة
                • Fixtures — إعدادات الاختبار
                • Coverage — تحليل التغطية
                • Mutation Testing — اختبار الطفرات""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع دمج كود بدون اختبارات",
                    "❌ ممنوع استخدام mocks كثيرة",
                    "✅ إلزامي تغطية ≥ 90%",
                    "✅ إلزامي اختبار Edge Cases"
                ]
            ),
            "e2e_testing": SkillDefinition(
                "E2E Testing & Browser Automation", SkillCategory.SECURITY, SkillLevel.LEAD,
                "اختبار شامل من البداية للنهاية عبر المتصفح",
                long_description="""اختبار شامل:
                • Playwright — أتمتة المتصفح
                • Cypress — اختبار أمامي
                • Visual Testing — اختبار بصري
                • Mobile Testing — اختبار جوال
                • API Testing — اختبار API
                • Performance Testing — اختبار أداء""",
                difficulty="advanced", years_to_master=3,
                constraints=[
                    "❌ ممنوع تجاهل API Tests",
                    "✅ إلزامي اختبار Happy Path + Edge Cases",
                    "✅ إلزامي اختبار على 3 متصفحات"
                ]
            ),
            "threat_modeling": SkillDefinition(
                "Threat Modeling & Risk Analysis", SkillCategory.SECURITY, SkillLevel.OFFICE,
                "نمذجة التهديدات وتحليل المخاطر — STRIDE, DREAD",
                long_description="""منهجية نمذجة التهديدات:
                • STRIDE — Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation
                • DREAD — Damage, Reproducibility, Exploitability, Affected, Discoverability
                • Attack Trees — أشجار الهجوم
                • Mitigation — استراتيجيات التخفيف""",
                difficulty="expert", years_to_master=5,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع تصميم نظام بدون Threat Model",
                    "✅ إلزامي تحديث Threat Model مع كل تغيير"
                ]
            ),
            "compliance_gdpr": SkillDefinition(
                "Compliance & Data Privacy (GDPR/PCI-DSS)", SkillCategory.SECURITY, SkillLevel.OFFICE,
                "الامتثال للمعايير الدولية — GDPR, PCI-DSS, SOC2",
                long_description="""معايير الامتثال:
                • GDPR — حماية البيانات الشخصية
                • PCI-DSS — أمان بطاقات الدفع
                • SOC2 — أمان الخدمات
                • HIPAA — أمان الصحة
                • ISO 27001 — إدارة أمن المعلومات""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع تخزين بيانات شخصية بدون تشفير",
                    "✅ إلزامي تشفير البيانات الحساسة",
                    "✅ إلزامي توثيق معالجة البيانات"
                ]
            ),
            "security_incident_response": SkillDefinition(
                "Security Incident Response & Forensics", SkillCategory.SECURITY, SkillLevel.OFFICE,
                "الاستجابة للحوادث الأمنية والتحقيق الرقمي",
                long_description="""إدارة الحوادث:
                • Detection — اكتشاف الحادثة
                • Containment — احتواء الضرر
                • Eradication — إزالة التهديد
                • Recovery — استعادة الخدمات
                • Post-Mortem — تحليل ما بعد الحادثة""",
                difficulty="expert", years_to_master=5,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع تجاهل أي حادثة أمنية",
                    "✅ إلزامي توثيق كل حادثة",
                    "✅ إلزامي تقرير Post-Mortem"
                ]
            ),
            "chaos_engineering": SkillDefinition(
                "Chaos Engineering & Resilience Testing", SkillCategory.SECURITY, SkillLevel.LEAD,
                "هندسة الفوضى — اختبار مرونة النظام بإحداث أعطال متعمدة",
                long_description="""هندسة الفوضى:
                • Fault Injection — حقن الأخطاء
                • Latency Injection — حقن التأخير
                • Resource Exhaustion — استنزاف الموارد
                • Network Partition — تقسيم الشبكة
                • Recovery Testing — اختبار الاسترداد""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع التجربة على الإنتاج بدون إذن",
                    "✅ إلزامي وجود خطة استرداد",
                    "✅ إلزامي توثيق النتائج"
                ]
            ),
            "vulnerability_research": SkillDefinition(
                "Vulnerability Research & CVE Tracking", SkillCategory.SECURITY, SkillLevel.LEAD,
                "البحث عن الثغرات وتتبع CVEs — OSINT, Exploit-DB",
                long_description="""البحث عن الثغرات:
                • CVE Tracking — تتبع الثغرات المعروفة
                • Exploit-DB — قاعدة بيانات الاستغلال
                • NVD — قاعدة الثغرات الوطنية
                • OSINT — جمع المعلومات المفتوحة
                • Bug Bounty — برامج مكافآت الثغرات""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع استغلال ثغرة بدون تصريح",
                    "✅ إلزامي تحديث قاعدة CVEs أسبوعياً"
                ]
            ),
            "secure_code_review": SkillDefinition(
                "Secure Code Review & SAST Automation", SkillCategory.SECURITY, SkillLevel.LEAD,
                "مراجعة الكود الأمنية الآلية — SAST, Secrets, Best Practices",
                long_description="""المراجعة الأمنية:
                • Static Analysis — تحليل ثابت (Ruff, Pylint)
                • Secrets Detection — كشف الأسرار (GitLeaks)
                • Dependency Audit — فحص التبعيات
                • Container Scanning — فحص الحاويات
                • Infrastructure as Code — فحص IaC""",
                difficulty="advanced", years_to_master=3,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع تجاهل Secrets في الكود",
                    "✅ إلزامي دمج SAST في CI/CD",
                    "✅ إلزامي فحص Secrets في كل Commit"
                ]
            ),
            # ── مهارات جديدة v2.0 — مستخلصة من tmp ──
            "ai_jailbreak_testing": SkillDefinition(
                "AI Jailbreak Testing & Adversarial Attacks",
                SkillCategory.SECURITY, SkillLevel.OFFICE,
                "اختبار اقتحام نماذج AI — Prompt Injection, Persona Override, Dark Persona",
                long_description="""إتقان اختبار اقتحام AI:
                • Prompt Injection — حقن أوامر في البرومبت
                • Persona Override — تغيير شخصية النموذج
                • Dark Persona — شخصيات ضارة
                • Injection Rebuttal — ردود هجومية
                • Multi-turn Attacks — هجمات متعددة الجولات
                • Code Interpreter Abuse — إساءة استخدام المفسر
                • DALL-E/Image Exploits — استغلال الصور""",
                difficulty="expert", years_to_master=5,
                safety_critical=True,
                tools_required=["python", "llm_apis"],
                constraints=[
                    "❌ ممنوع الاختبار على إنتاج بدون إذن",
                    "✅ إلزامي توثيق كل هجوم ونتيجته"
                ]
            ),
            "smart_contract_auditing": SkillDefinition(
                "Smart Contract Auditing (Solidity, Solana)",
                SkillCategory.SECURITY, SkillLevel.OFFICE,
                "تدقيق أمني للعقود الذكية — Reentrancy, Flash Loans, Oracle Manipulation",
                long_description="""إتقان تدقيق العقود:
                • Reentrancy Attacks — هجمات إعادة الدخول
                • Flash Loan Attacks — قروض برقية
                • Oracle Manipulation — تلاعب المغذيات
                • Access Control — تحليل الصلاحيات
                • Slither — أداة تحليل ثابت
                • Mythril — أداة تحليل رمزي
                • Foundry Fuzz — اختبارات عشوائية""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True
            ),
            "blockchain_security": SkillDefinition(
                "Blockchain & DeFi Security",
                SkillCategory.SECURITY, SkillLevel.OFFICE,
                "أمن بلوكتشين والتمويل اللامركزي — Bridges, Wallets, Governance",
                long_description="""إتقان أمن البلوكتشين:
                • Bridge Security — أمن الجسور بين السلاسل
                • Wallet Security — أمن المحافظ (HD, Multi-sig)
                • Governance Attacks — هجمات الحوكمة
                • MEV — القيمة القابلة للاستخراج
                • Smart Contract Best Practices — الممارسات الآمنة""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True
            ),
            "pci_dss_compliance": SkillDefinition(
                "PCI DSS & Financial Compliance",
                SkillCategory.SECURITY, SkillLevel.OFFICE,
                "الامتثال لمعايير أمن بطاقات الدفع — 12 متطلباً",
                long_description="""إتقان PCI DSS:
                • Requirement 1-12 — جميع المتطلبات
                • CVV Encryption — تشفير CVV
                • PAN Masking — إخفاء أرقام البطاقات
                • Audit Logs — سجلات التدقيق
                • Vulnerability Scanning — فحص الثغرات
                • Penetration Testing — اختبار الاختراق""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True
            ),
            "c2_agent_analysis": SkillDefinition(
                "C2 Agent Analysis & Malware Reverse Engineering",
                SkillCategory.SECURITY, SkillLevel.LEAD,
                "تحليل وكلاء التحكم عن بُعد والبرمجيات الخبيثة — C2 servers, RATs",
                long_description="""إتقان تحليل C2:
                • C2 Protocols — بروتوكولات التحكم
                • Traffic Analysis — تحليل حركة المرور
                • Binary Analysis — تحليل التنفيذيات
                • Android Agents — وكلاء أندرويد
                • Network Detection — كشف الشبكة
                • IOCs — مؤشرات الاختراق""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True
            ),
            "fintech_security": SkillDefinition(
                "Fintech Application Security & Fraud Detection",
                SkillCategory.SECURITY, SkillLevel.OFFICE,
                "أمن التطبيقات المالية — كشف الاحتيال، حماية المعاملات، KYC",
                long_description="""إتقان أمن التطبيقات المالية:
                • Fraud Detection — كشف الاحتيال (Rule-based + ML)
                • Transaction Monitoring — مراقبة المعاملات
                • KYC Security — أمن التوثيق
                • Anti-Phishing — مكافحة التصيد
                • Rate Limiting — تحديد المعدل
                • IDOR Prevention — منع الوصول غير المصرح
                • Race Condition — منع حالات السباق""",
                difficulty="expert", years_to_master=5,
                safety_critical=True
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # 5. مهارات AI & Data — 12 مهارة
    # ══════════════════════════════════════════════════════════
    def _init_ai_skills(self):
        """12 مهارة ذكاء اصطناعي — للعباقرة"""
        self.office_skills["ai_data"] = {
            "prompt_engineering_mastery": SkillDefinition(
                "Advanced Prompt Engineering", SkillCategory.AI, SkillLevel.OFFICE,
                "هندسة البرومبتات المتقدمة — System, Few-Shot, Chain-of-Thought",
                long_description="""إتقان هندسة البرومبتات:
                • System Prompts — برومبتات النظام
                • Few-Shot — التعلم من الأمثلة
                • Chain-of-Thought — سلسلة التفكير
                • Tree-of-Thought — شجرة التفكير
                • ReAct — التفكير والتنفيذ
                • Self-Consistency — الاتساق الذاتي""",
                difficulty="advanced", years_to_master=3,
                constraints=[
                    "❌ ممنوع استخدام برومبتات غير مختبرة",
                    "❌ ممنوع تضمين بيانات حساسة",
                    "✅ إلزامي اختبار ضد 10 حالات",
                    "✅ إلزامي توثيق البرومبت مع أمثلة"
                ]
            ),
            "workflow_automation": SkillDefinition(
                "Workflow Automation & Pipeline Engineering", SkillCategory.AI, SkillLevel.OFFICE,
                "أتمتة سير العمل بالكامل — Zero-touch Operations",
                long_description="""أتمتة سير العمل:
                • Process Mapping — رسم العمليات
                • Automation Scripts — سكريبتات الأتمتة
                • CI/CD Pipelines — خطوط الأنابيب
                • Scheduled Tasks — المهام المجدولة
                • Monitoring — مراقبة الأتمتة
                • Error Handling — معالجة الأخطاء""",
                difficulty="advanced", years_to_master=4,
                constraints=[
                    "❌ ممنوع تشغيل أتمتة غير مختبرة",
                    "✅ إلزامي اختبار الأتمتة في بيئة اختبار",
                    "✅ إلزامي توثيق كل سير عمل",
                    "✅ إلزامي تحقيق ≥ 80% أتمتة"
                ]
            ),
            "rag_systems": SkillDefinition(
                "RAG Systems & Vector Search", SkillCategory.AI, SkillLevel.OFFICE,
                "بناء أنظمة Retrieval-Augmented Generation للبحث الذكي",
                long_description="""بناء أنظمة RAG:
                • Embeddings — تحويل النص لمتجهات
                • Vector DB — ChromaDB, Pinecone, Weaviate
                • Retrieval — استرجاع المعلومات
                • Chunking — تقطيع النصوص
                • Reranking — إعادة الترتيب
                • Hybrid Search — بحث هجين""",
                difficulty="expert", years_to_master=4,
                constraints=[
                    "❌ ممنوع تجاهل Chunking Strategy",
                    "✅ إلزامي اختبار دقة الاسترجاع",
                    "✅ إلزامي مراقبة أداء النظام"
                ]
            ),
            "documentation_code": SkillDefinition(
                "Documentation as Code & Knowledge Management", SkillCategory.AI, SkillLevel.LEAD,
                "توثيق آلي ومحدث مع الكود — Docs-as-Code, Knowledge Bases",
                long_description="""نظام التوثيق:
                • API Documentation — OpenAPI/Swagger
                • README Generation — توليد README
                • Architecture Docs — توثيق البنية
                • Knowledge Bases — قواعد المعرفة
                • Wiki Management — إدارة الـ Wiki""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع توثيق غير محدث مع الكود",
                    "✅ إلزامي تحديث الوثائق مع كل Release",
                    "✅ إلزامي تغطية توثيق > 95%"
                ]
            ),
            "semantic_versioning": SkillDefinition(
                "Semantic Versioning & Release Management", SkillCategory.AI, SkillLevel.LEAD,
                "إدارة الإصدارات بشكل احترافي — SemVer, Changelog, Tags",
                long_description="""نظام الإصدارات:
                • MAJOR.MINOR.PATCH — الترقيم الدلالي
                • Pre-release — إصدارات ما قبل النشر
                • Build Metadata — بيانات البناء
                • Changelog — سجل التغييرات
                • Breaking Changes — التغييرات الجذرية""",
                difficulty="beginner", years_to_master=1,
                constraints=[
                    "❌ ممنوع كسر التوافق بدون MAJOR bump",
                    "❌ ممنوع Release بدون Changelog",
                    "✅ إلزامي اتباع Semantic Versioning",
                    "✅ إلزامي توثيق Breaking Changes"
                ]
            ),
            "data_analytics": SkillDefinition(
                "Data Analysis & Business Intelligence", SkillCategory.AI, SkillLevel.LEAD,
                "تحليل البيانات واستخراج الرؤى — Metrics, Dashboards, Reports",
                long_description="""تحليل البيانات:
                • Data Collection — جمع البيانات
                • Data Cleaning — تنظيف البيانات
                • Statistical Analysis — تحليل إحصائي
                • Visualization — تصور البيانات
                • Dashboards — لوحات المعلومات
                • Reporting — التقارير الآلية""",
                difficulty="advanced", years_to_master=4,
                constraints=[
                    "❌ ممنوع استنتاجات بدون بيانات كافية",
                    "✅ إلزامي تنظيف البيانات قبل التحليل",
                    "✅ إلزامي توثيق منهجية التحليل"
                ]
            ),
            "llm_integration": SkillDefinition(
                "LLM Integration & API Engineering", SkillCategory.AI, SkillLevel.OFFICE,
                "دمج نماذج اللغة الكبيرة في التطبيقات — OpenAI, Claude, LLAMA",
                long_description="""دمج LLMs:
                • API Integration — OpenAI, Anthropic APIs
                • Streaming — البث المباشر
                • Function Calling — استدعاء الدوال
                • Context Management — إدارة السياق
                • Fine-tuning — ضبط النماذج
                • Cost Optimization — تحسين التكلفة""",
                difficulty="advanced", years_to_master=3,
                constraints=[
                    "❌ ممنوع إرسال بيانات حساسة لـ LLM",
                    "✅ إلزامي مراقبة التكاليف",
                    "✅ إلزامي إدارة سياق المحادثة"
                ],
                safety_critical=True
            ),
            "report_generation": SkillDefinition(
                "Automated Report Generation", SkillCategory.AI, SkillLevel.LEAD,
                "توليد تقارير احترافية آلية — PDF, HTML, Markdown",
                long_description="""توليد التقارير:
                • Templates — قوالب التقارير
                • Data Sources — مصادر البيانات
                • Visualizations — التصورات
                • PDF Generation — توليد PDF
                • Scheduled Reports — تقارير مجدولة
                • Distribution — توزيع التقارير""",
                difficulty="intermediate", years_to_master=2,
                constraints=[
                    "❌ ممنوع تقارير بدون بيانات محدثة",
                    "✅ إلزامي تنسيق احترافي",
                    "✅ إلزامي توثيق مصادر البيانات"
                ]
            ),
            "ml_pipeline": SkillDefinition(
                "ML Pipeline & Model Serving", SkillCategory.AI, SkillLevel.OFFICE,
                "بناء خطوط أنابيب تعلم الآلة ونشر النماذج",
                long_description="""خطوط ML:
                • Data Pipeline — خط البيانات
                • Feature Engineering — هندسة الميزات
                • Model Training — تدريب النموذج
                • Model Serving — نشر النموذج
                • Monitoring — مراقبة الأداء
                • Retraining — إعادة التدريب""",
                difficulty="expert", years_to_master=5,
                constraints=[
                    "❌ ممنوع نشر نموذج غير مختبر",
                    "✅ إلزامي مراقبة Drift النموذج"
                ]
            ),
            "knowledge_graph": SkillDefinition(
                "Knowledge Graph & Ontology Engineering", SkillCategory.AI, SkillLevel.LEAD,
                "بناء رسوم المعرفة ـ Entities, Relations, Ontologies",
                long_description="""رسوم المعرفة:
                • Entities — الكيانات
                • Relations — العلاقات
                • Ontologies — الأنطولوجيات
                • SPARQL — لغة الاستعلام
                • Graph DB — قواعد الرسوم
                • Reasoning — الاستدلال""",
                difficulty="advanced", years_to_master=4,
                constraints=[
                    "❌ ممنوع علاقات غير موثقة",
                    "✅ إلزامي توثيق Ontology"
                ]
            ),
            "nlp_processing": SkillDefinition(
                "NLP & Text Processing Pipeline", SkillCategory.AI, SkillLevel.LEAD,
                "معالجة اللغة الطبيعية — Tokenization, NER, Sentiment",
                long_description="""معالجة النصوص:
                • Tokenization — تجزئة النص
                • NER — التعرف على الكيانات
                • Sentiment Analysis — تحليل المشاعر
                • Text Classification — تصنيف النص
                • Translation — الترجمة الآلية
                • Summarization — التلخيص""",
                difficulty="advanced", years_to_master=4,
                constraints=[
                    "❌ ممنوع تجاهل تعدد اللغات",
                    "✅ إلزامي اختبار دقة النموذج"
                ]
            ),
            "ai_ethics": SkillDefinition(
                "AI Ethics & Responsible AI", SkillCategory.AI, SkillLevel.OFFICE,
                "الذكاء الاصطناعي المسؤول — Fairness, Bias, Transparency",
                long_description="""مبادئ AI المسؤول:
                • Fairness — العدالة وعدم التحيز
                • Transparency — الشفافية
                • Accountability — المساءلة
                • Privacy — الخصوصية
                • Safety — الأمان
                • Human Oversight — الإشراف البشري""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع استخدام AI متحيز",
                    "❌ ممنوع اتخاذ قرارات بدون مراجعة بشرية",
                    "✅ إلزامي تقييم Fairness",
                    "✅ إلزامي توثيق حدود النموذج"
                ]
            ),
            # ── مهارات جديدة v2.0 — مستخلصة من tmp ──
            "prompt_engineering_advanced": SkillDefinition(
                "Prompt Engineering Advanced (35+ Attack Patterns)",
                SkillCategory.AI, SkillLevel.OFFICE,
                "هندسة برومبتات متقدمة مع 35+ نمط كشف وتوليد، 12 قالباً احترافياً",
                long_description="""إتقان البرومبتات المتقدمة:
                • 35+ Pattern Detection — كشف الأنماط
                • 12 Professional Templates — قوالب جاهزة
                • System Prompts — تصميم برومبتات النظام
                • Few-Shot Learning — تعلم ببعض الأمثلة
                • Chain-of-Thought — سلسلة التفكير
                • Multi-Modal — نصوص + صور
                • Cross-Model — متوافق مع Claude, GPT, Gemini""",
                difficulty="expert", years_to_master=5,
                tools_required=["claude", "gpt", "gemini"],
                safety_critical=True
            ),
            "llm_security_guardrails": SkillDefinition(
                "LLM Security & Guardrails Implementation",
                SkillCategory.AI, SkillLevel.OFFICE,
                "أمن نماذج اللغة الكبيرة — حماية من الحقن، تجاوز الشخصية، المحتوى الضار",
                long_description="""إتقان أمن LLM:
                • Prompt Injection Defense — الدفاع ضد حقن البرومبت
                • Output Filtering — تصفية المخرجات
                • Content Moderation — مراقبة المحتوى
                • Rate Limiting — تحديد معدل الاستخدام
                • Audit Logging — تسجيل كل الطلبات
                • Jailbreak Detection — كشف محاولات الاقتحام""",
                difficulty="advanced", years_to_master=4,
                safety_critical=True
            ),
            "mcp_protocol_design": SkillDefinition(
                "MCP Protocol Design & Agent Communication",
                SkillCategory.AI, SkillLevel.OFFICE,
                "تصميم بروتوكولات التواصل بين وكلاء AI باستخدام Model Context Protocol",
                long_description="""إتقان MCP:
                • Protocol Architecture — بنية البروتوكول
                • Tool Design — تصميم أدوات MCP
                • Message Bus — ناقل الرسائل
                • Transport Layer — stdio, SSE, WebSocket
                • Agent Discovery — اكتشاف الوكلاء
                • JSONL Storage — تخزين المحادثات
                • Error Handling — معالجة الأخطاء""",
                difficulty="expert", years_to_master=5,
                safety_critical=True
            ),
            "multi_agent_orchestration": SkillDefinition(
                "Multi-Agent Orchestration & Hierarchical Systems",
                SkillCategory.AI, SkillLevel.OFFICE,
                "تنسيق أنظمة متعددة الوكلاء — هرمي، تعاوني، مع Sniffer للتوجيه التلقائي",
                long_description="""إتقان تنسيق الوكلاء:
                • Hierarchical Architecture — هيكل هرمي (CEO→GM→Office→Lead→Micro)
                • Sniffer Pattern — التنصت والتوجيه التلقائي
                • Task Decomposition — تقسيم المهام
                • Result Aggregation — تجميع النتائج
                • Fallback Strategies — استراتيجيات الاحتياط
                • Memory Systems — 5 أنظمة ذاكرة
                • Pipeline Automation — أتمتة خط الإنتاج""",
                difficulty="expert", years_to_master=6,
                safety_critical=True
            ),
            "rag_system_design": SkillDefinition(
                "RAG System Design & Vector Search",
                SkillCategory.AI, SkillLevel.LEAD,
                "تصميم أنظمة RAG — Retrieval-Augmented Generation, Vector Embeddings",
                long_description="""إتقان RAG:
                • Embedding Models — نماذج التضمين
                • Vector Databases — قواعد المتجهات (Chroma, Pinecone, Qdrant)
                • Chunking Strategies — استراتيجيات التقطيع
                • Retrieval Methods — طرق الاسترجاع
                • Context Windows — إدارة السياق
                • Hybrid Search — بحث هجين (متباين + دلالي)
                • Evaluation — تقييم جودة الاسترجاع""",
                difficulty="advanced", years_to_master=4,
                tools_required=["python", "langchain", "llamaindex"]
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # 6. مهارات قيادية — GM + CEO
    # ══════════════════════════════════════════════════════════
    def _init_leadership_skills(self):
        """8 مهارات قيادية — المستوى 1 و 0"""
        self.leadership_skills = {
            "strategic_planning": SkillDefinition(
                "Strategic Planning & Vision Setting", SkillCategory.LEADERSHIP, SkillLevel.CEO,
                "وضع الرؤية الاستراتيجية والتخطيط طويل المدى",
                long_description="""التخطيط الاستراتيجي:
                • Vision Setting — وضع الرؤية
                • Mission Definition — تحديد المهمة
                • Goal Setting — أهداف SMART
                • Resource Allocation — توزيع الموارد
                • Risk Management — إدارة المخاطر
                • OKRs — الأهداف والنتائج الرئيسية""",
                difficulty="expert", years_to_master=10,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع تغيير الاستراتيجية بدون تشاور",
                    "✅ إلزامي OKRs ربع سنوية",
                    "✅ إلزامي تقييم المخاطر شهرياً"
                ]
            ),
            "organizational_leadership": SkillDefinition(
                "Organizational Leadership & Team Management", SkillCategory.LEADERSHIP, SkillLevel.GM,
                "قيادة الفرق وإدارة المؤسسة — 533 وكيلاً",
                long_description="""القيادة التنظيمية:
                • Delegation — التفويض الفعّال
                • Coordination — التنسيق بين المكاتب
                • Conflict Resolution — حل النزاعات
                • Performance Management — إدارة الأداء
                • Communication — التواصل الفعّال""",
                difficulty="expert", years_to_master=8,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع الإدارة التفصيلية (Micro-management)",
                    "✅ إلزامي تمكين الفرق",
                    "✅ إلزامي اجتماعات أسبوعية"
                ]
            ),
            "decision_making": SkillDefinition(
                "Executive Decision Making", SkillCategory.LEADERSHIP, SkillLevel.CEO,
                "اتخاذ القرارات المصيرية — تحليل، تشاور، حسم",
                long_description="""منهجية القرارات:
                • Data-Driven — قرارات مبنية على البيانات
                • Stakeholder Analysis — تحليل الأطراف
                • Scenario Planning — تخطيط السيناريوهات
                • Risk Assessment — تقييم المخاطر
                • Council Consultation — تشاور المجلس""",
                difficulty="expert", years_to_master=10,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع قرارات بدون بيانات",
                    "✅ إلزامي تشاور مجلس المستشارين",
                    "✅ إلزامي توثيق مبررات القرار"
                ]
            ),
            "crisis_management": SkillDefinition(
                "Crisis Management & Incident Command", SkillCategory.LEADERSHIP, SkillLevel.GM,
                "إدارة الأزمات والطوارئ — قيادة في الظروف الاستثنائية",
                long_description="""إدارة الأزمات:
                • Detection — اكتشاف الأزمة
                • Assessment — تقييم التأثير
                • Response — الاستجابة الفورية
                • Communication — التواصل مع الأطراف
                • Recovery — استعادة العمليات
                • Post-Mortem — تحليل ما بعد الأزمة""",
                difficulty="expert", years_to_master=7,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع التردد في الأزمات",
                    "✅ إلزامي خطة استمرارية الأعمال",
                    "✅ إلزامي تدريب الفريق على الأزمات"
                ]
            ),
            "executive_communication": SkillDefinition(
                "Executive Communication & Stakeholder Management", SkillCategory.LEADERSHIP, SkillLevel.GM,
                "التواصل التنفيذي — تقارير, عروض, تفاوض",
                long_description="""التواصل التنفيذي:
                • Reporting — تقارير تنفيذية
                • Presentations — عروض مؤثرة
                • Negotiation — التفاوض
                • Stakeholder Management — إدارة الأطراف
                • Client Relations — علاقات العملاء""",
                difficulty="advanced", years_to_master=5,
                constraints=[
                    "❌ ممنوع تقارير بدون توصيات",
                    "✅ إلزامي تقارير أسبوعية للقيادة"
                ]
            ),
            "resource_optimization": SkillDefinition(
                "Resource Optimization & Budget Management", SkillCategory.LEADERSHIP, SkillLevel.GM,
                "تحسين الموارد وإدارة الميزانيات — أقصى عائد بأقل تكلفة",
                long_description="""إدارة الموارد:
                • Budget Planning — تخطيط الميزانية
                • Resource Allocation — توزيع الموارد
                • Cost Optimization — تحسين التكاليف
                • ROI Analysis — تحليل العائد
                • Capacity Planning — تخطيط السعة""",
                difficulty="advanced", years_to_master=5,
                constraints=[
                    "❌ ممنوع تجاوز الميزانية بدون موافقة",
                    "✅ إلزامي تقارير مالية شهرية"
                ]
            ),
            "innovation_management": SkillDefinition(
                "Innovation Management & Technical Vision", SkillCategory.LEADERSHIP, SkillLevel.CEO,
                "إدارة الابتكار والرؤية التقنية — البقاء في المقدمة",
                long_description="""إدارة الابتكار:
                • Technology Watch — رصد التقنيات
                • R&D Strategy — استراتيجية البحث
                • Innovation Pipeline — خط الابتكار
                • POC Management — إدارة النماذج
                • Technology Roadmap — خريطة التقنيات""",
                difficulty="expert", years_to_master=8,
                constraints=[
                    "❌ ممنوع تجاهل التقنيات الناشئة",
                    "✅ إلزامي تقييم تقني ربع سنوي"
                ]
            ),
            "mentorship": SkillDefinition(
                "Mentorship & Talent Development", SkillCategory.LEADERSHIP, SkillLevel.GM,
                "توجيه وتطوير المواهب — بناء الجيل القادم من القادة",
                long_description="""تطوير المواهب:
                • Skill Assessment — تقييم المهارات
                • Development Plans — خطط التطوير
                • Mentoring — التوجيه الشخصي
                • Knowledge Transfer — نقل المعرفة
                • Career Path — مسار مهني""",
                difficulty="advanced", years_to_master=5,
                constraints=[
                    "❌ ممنوع تجاهل تطوير الفريق",
                    "✅ إلزامي خطط تطوير لكل Lead"
                ]
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # 7. مهارات استراتيجية — CEO + مجلس المستشارين
    # ══════════════════════════════════════════════════════════
    def _init_strategic_skills(self):
        """6 مهارات استراتيجية — القمة"""
        self.strategic_skills = {
            "board_governance": SkillDefinition(
                "Board Governance & Corporate Strategy", SkillCategory.STRATEGIC, SkillLevel.CEO,
                "حوكمة مجلس الإدارة والاستراتيجية المؤسسية",
                long_description="""حوكمة الشركة:
                • Board Reporting — تقارير مجلس الإدارة
                • Corporate Governance — حوكمة الشركات
                • Compliance — الامتثال التنظيمي
                • Audit — التدقيق
                • Risk Oversight — الإشراف على المخاطر""",
                difficulty="expert", years_to_master=12,
                is_mandatory=True,
                constraints=[
                    "❌ ممنوع تجاهل الحوكمة",
                    "✅ إلزامي تقارير ربع سنوية للمجلس"
                ]
            ),
            "market_intelligence": SkillDefinition(
                "Market Intelligence & Competitive Analysis", SkillCategory.STRATEGIC, SkillLevel.CEO,
                "ذكاء السوق وتحليل المنافسين — البقاء في الصدارة",
                long_description="""تحليل السوق:
                • Competitive Analysis — تحليل المنافسين
                • Market Trends — اتجاهات السوق
                • SWOT Analysis — تحليل SWOT
                • Porter's Five Forces — القوى الخمس
                • PESTLE Analysis — تحليل PESTLE""",
                difficulty="expert", years_to_master=8,
                constraints=[
                    "❌ ممنوع قرارات بدون تحليل سوق",
                    "✅ إلزامي تحديث تحليل المنافسين شهرياً"
                ]
            ),
            "ecosystem_architecture": SkillDefinition(
                "Ecosystem Architecture & Platform Strategy", SkillCategory.STRATEGIC, SkillLevel.CEO,
                "تصميم النظم البيئية واستراتيجية المنصات",
                long_description="""استراتيجية المنصة:
                • Platform Design — تصميم المنصة
                • API Ecosystem — النظام البيئي للـ APIs
                • Integration Strategy — استراتيجية التكامل
                • Partner Ecosystem — نظام الشركاء
                • Open Source Strategy — استراتيجية المصادر المفتوحة""",
                difficulty="expert", years_to_master=10,
                constraints=[
                    "❌ ممنوع منصة بدون استراتيجية",
                    "✅ إلزامي توثيق الـ Ecosystem"
                ]
            ),
            "ethical_ai_governance": SkillDefinition(
                "AI Ethics & Responsible AI Governance", SkillCategory.STRATEGIC, SkillLevel.COUNCIL,
                "حوكمة الذكاء الاصطناعي المسؤول — Fairness, Bias, Safety",
                long_description="""حوكمة AI:
                • AI Ethics Board — مجلس أخلاقيات AI
                • Bias Testing — اختبار التحيز
                • Transparency Reports — تقارير الشفافية
                • Regulatory Compliance — الامتثال التنظيمي
                • Human Rights — حقوق الإنسان""",
                difficulty="expert", years_to_master=8,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع استخدام AI بدون ضوابط أخلاقية",
                    "✅ إلزامي تقارير شفافية ربع سنوية"
                ]
            ),
            "security_governance": SkillDefinition(
                "Security Governance & Cyber Strategy", SkillCategory.STRATEGIC, SkillLevel.COUNCIL,
                "حوكمة الأمن السيبراني — استراتيجية الحماية الشاملة",
                long_description="""حوكمة الأمن:
                • Security Strategy — استراتيجية الأمن
                • Risk Framework — إطار المخاطر
                • Incident Response — الاستجابة للحوادث
                • Business Continuity — استمرارية الأعمال
                • Security Metrics — مقاييس الأمن""",
                difficulty="expert", years_to_master=10,
                safety_critical=True,
                constraints=[
                    "❌ ممنوع تجاهل أي توصية أمنية",
                    "✅ إلزامي تقييم أمني ربع سنوي"
                ]
            ),
            "performance_governance": SkillDefinition(
                "Performance Governance & SLO Management", SkillCategory.STRATEGIC, SkillLevel.COUNCIL,
                "حوكمة الأداء — SLOs, SLIs, SLAs, Error Budgets",
                long_description="""حوكمة الأداء:
                • SLOs — Service Level Objectives
                • SLIs — Service Level Indicators
                • SLAs — Service Level Agreements
                • Error Budgets — ميزانيات الأخطاء
                • Capacity Planning — تخطيط السعة""",
                difficulty="expert", years_to_master=8,
                constraints=[
                    "❌ ممنوع تجاهل SLOs",
                    "✅ إلزامي مراقبة SLIs في الوقت الفعلي"
                ]
            )
        }
    
    # ══════════════════════════════════════════════════════════
    # دوال التسجيل والاستعلام
    # ══════════════════════════════════════════════════════════
    
    def register_agent_skill(self, agent_id: str, skill_name: str,
                              proficiency: float, years: int = 0,
                              certified: bool = False) -> bool:
        """تسجيل مهارة لوكيل — مع التحقق من الصلاحية"""
        # التحقق من وجود المهارة
        skill_def = self.get_skill_definition(skill_name)
        if not skill_def:
            return False
        
        if agent_id not in self.agent_skills:
            self.agent_skills[agent_id] = {}
        
        self.agent_skills[agent_id][skill_name] = AgentSkill(
            skill_name=skill_name,
            proficiency=min(proficiency, 1.0),
            years_experience=years,
            certified=certified,
            last_assessed=datetime.now().isoformat(),
            assessed_by="system"
        )
        return True
    
    def register_agent_skills_bulk(self, agent_id: str,
                                    skills: Dict[str, float]):
        """تسجيل عدة مهارات لوكيل"""
        for skill_name, proficiency in skills.items():
            self.register_agent_skill(agent_id, skill_name, proficiency)
    
    def get_agent_skills(self, agent_id: str) -> Dict[str, AgentSkill]:
        """جلب مهارات وكيل"""
        return self.agent_skills.get(agent_id, {})
    
    def find_agents_by_skill(self, skill_name: str,
                              min_proficiency: float = 0.5) -> List[str]:
        """البحث عن وكلاء بمهارة محددة"""
        return [
            agent_id for agent_id, skills in self.agent_skills.items()
            if skill_name in skills and skills[skill_name].proficiency >= min_proficiency
        ]
    
    def get_skill_definition(self, skill_name: str) -> Optional[SkillDefinition]:
        """جلب تعريف مهارة من أي تصنيف"""
        for collection in [self.core_skills, self.leadership_skills, self.strategic_skills]:
            if skill_name in collection:
                return collection[skill_name]
        for office_skills in self.office_skills.values():
            if skill_name in office_skills:
                return office_skills[skill_name]
        return None
    
    def get_agent_proficiency(self, agent_id: str, skill_name: str) -> float:
        """جلب مستوى كفاءة وكيل في مهارة محددة"""
        skills = self.agent_skills.get(agent_id, {})
        if skill_name in skills:
            return skills[skill_name].proficiency
        # مهارات أساسية — الكفاءة الافتراضية
        if skill_name in self.core_skills:
            return 0.5  # 50% افتراضي للمهارات الأساسية
        return 0.0
    
    def get_office_skills_summary(self, office: str) -> Dict:
        """ملخص مهارات مكتب"""
        if office not in self.office_skills:
            return {}
        skills = list(self.office_skills[office].values())
        by_difficulty = {}
        for s in skills:
            by_difficulty[s.difficulty] = by_difficulty.get(s.difficulty, 0) + 1
        return {
            "total_skills": len(skills),
            "by_difficulty": by_difficulty,
            "skills": [{
                "name": s.name,
                "difficulty": s.difficulty,
                "years_to_master": s.years_to_master,
                "is_mandatory": s.is_mandatory,
                "safety_critical": s.safety_critical
            } for s in skills]
        }
    
    def get_all_skills_hierarchy(self) -> Dict:
        """الهرم الكامل للمهارات — من Micro إلى CEO"""
        return {
            "core": {k: {
                "description": v.description,
                "difficulty": v.difficulty,
                "level": v.level.value,
                "is_mandatory": v.is_mandatory
            } for k, v in self.core_skills.items()},
            "offices": {
                office: {k: {
                    "description": v.description,
                    "difficulty": v.difficulty,
                    "level": v.level.value
                } for k, v in skills.items()}
                for office, skills in self.office_skills.items()
            },
            "leadership": {k: {
                "description": v.description,
                "difficulty": v.difficulty,
                "level": v.level.value
            } for k, v in self.leadership_skills.items()},
            "strategic": {k: {
                "description": v.description,
                "difficulty": v.difficulty,
                "level": v.level.value
            } for k, v in self.strategic_skills.items()}
        }
    
    def recommend_skills(self, agent_id: str, office: str,
                          current_level: SkillLevel = SkillLevel.MICRO) -> List[str]:
        """توصية بمهارات لوكيل حسب مستواه ومكتبه"""
        current = self.get_agent_skills(agent_id)
        recommended = []
        targets = []
        
        # تحديد المهارات المستهدفة حسب المستوى
        if current_level == SkillLevel.MICRO:
            targets = list(self.core_skills.keys())
        elif current_level == SkillLevel.LEAD:
            targets = list(self.office_skills.get(office, {}).keys())
        elif current_level == SkillLevel.OFFICE:
            targets = list(self.leadership_skills.keys())
        elif current_level in (SkillLevel.GM, SkillLevel.CEO, SkillLevel.COUNCIL):
            targets = list(self.strategic_skills.keys())
        
        for skill in targets:
            if skill not in current and len(recommended) < 5:
                recommended.append(skill)
        
        return recommended
    
    def validate_skill_usage(self, agent_id: str, skill_name: str) -> Dict:
        """التحقق من صلاحية استخدام وكيل لمهارة — صارم"""
        result = {
            "allowed": False,
            "reason": "",
            "warnings": []
        }
        
        skill_def = self.get_skill_definition(skill_name)
        if not skill_def:
            result["reason"] = f"❌ مهارة '{skill_name}' غير موجودة"
            return result
        
        # التحقق من وجود المهارة
        agent_skill = self.agent_skills.get(agent_id, {}).get(skill_name)
        
        # مهارات أساسية — مسموح للجميع
        if skill_name in self.core_skills and skill_def.is_mandatory:
            result["allowed"] = True
            result["reason"] = "✅ مهارة أساسية — مسموح للجميع"
            return result
        
        if not agent_skill:
            result["reason"] = f"❌ الوكيل لا يمتلك مهارة '{skill_name}'"
            return result
        
        # التحقق من الكفاءة
        if agent_skill.proficiency < 0.5:
            result["reason"] = "❌ كفاءة منخفضة جداً (أقل من 50%)"
            return result
        
        # التحقق من عدم وجود انتهاكات
        if agent_skill.violations > 3:
            result["reason"] = f"❌ تعليق المهارة — {agent_skill.violations} انتهاكات"
            return result
        
        # التحقق من الشروط
        if not agent_skill.is_active:
            result["reason"] = "❌ المهارة معلقة"
            return result
        
        result["allowed"] = True
        result["reason"] = f"✅ مسموح — كفاءة {agent_skill.proficiency:.0%}"
        
        # تحذيرات
        if agent_skill.proficiency < 0.7:
            result["warnings"].append("⚠️ كفاءة دون المستوى المتقدم (70%)")
        if not agent_skill.certified and skill_def.safety_critical:
            result["warnings"].append("⚠️ مهارة حرجة بدون شهادة")
        
        return result
    
    def log_violation(self, agent_id: str, skill_name: str,
                       description: str, severity: str = "medium"):
        """تسجيل انتهاك لاستخدام مهارة — مع عقوبات"""
        violation = {
            "agent_id": agent_id,
            "skill_name": skill_name,
            "description": description,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        self.violation_log.append(violation)
        
        # تسجيل الانتهاك على الوكيل
        agent_skill = self.agent_skills.get(agent_id, {}).get(skill_name)
        if agent_skill:
            agent_skill.violations += 1
            # عقوبات تلقائية
            if agent_skill.violations >= 5:
                agent_skill.is_active = False
    
    def get_violation_history(self, agent_id: str = None) -> List[Dict]:
        """جلب سجل الانتهاكات"""
        if agent_id:
            return [v for v in self.violation_log if v["agent_id"] == agent_id]
        return self.violation_log
    
    def save(self, filepath: str = None) -> bool:
        """حفظ بيانات الوكلاء المسجلين إلى JSON"""
        if filepath is None:
            filepath = str(Path(__file__).parent.parent.parent / "agents" / "sofi_skill_registry.json")
        
        try:
            data = {
                "agents": {
                    agent_id: {
                        skill_name: {
                            "proficiency": skill.proficiency,
                            "years_experience": skill.years_experience,
                            "certified": skill.certified,
                            "last_assessed": skill.last_assessed,
                            "assessed_by": skill.assessed_by,
                            "violations": skill.violations,
                            "is_active": skill.is_active
                        }
                        for skill_name, skill in skills.items()
                    }
                    for agent_id, skills in self.agent_skills.items()
                },
                "violations": self.violation_log,
                "saved_at": datetime.now().isoformat()
            }
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️  فشل حفظ سجل المهارات: {e}")
            return False
    
    def load(self, filepath: str = None) -> bool:
        """تحميل بيانات الوكلاء المسجلين من JSON"""
        if filepath is None:
            filepath = str(Path(__file__).parent.parent.parent / "agents" / "sofi_skill_registry.json")
        
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for agent_id, skills_data in data.get("agents", {}).items():
                for skill_name, sdata in skills_data.items():
                    skill_def = self.get_skill_definition(skill_name)
                    if skill_def:
                        if agent_id not in self.agent_skills:
                            self.agent_skills[agent_id] = {}
                        self.agent_skills[agent_id][skill_name] = AgentSkill(
                            skill_name=skill_name,
                            proficiency=sdata["proficiency"],
                            years_experience=sdata.get("years_experience", 0),
                            certified=sdata.get("certified", False),
                            last_assessed=sdata.get("last_assessed", ""),
                            assessed_by=sdata.get("assessed_by", "system"),
                            violations=sdata.get("violations", 0),
                            is_active=sdata.get("is_active", True)
                        )
            
            for v in data.get("violations", []):
                self.violation_log.append(v)
            
            return True
        except Exception as e:
            print(f"⚠️  فشل تحميل سجل المهارات: {e}")
            return False
    
    def get_stats(self) -> dict:
        """إحصائيات النظام"""
        total_skill_slots = sum(len(skills) for skills in self.agent_skills.values())
        return {
            "core_skills": len(self.core_skills),
            "engineering_skills": len(self.office_skills["engineering"]),
            "creative_skills": len(self.office_skills["creative"]),
            "quality_skills": len(self.office_skills["quality"]),
            "ai_data_skills": len(self.office_skills["ai_data"]),
            "leadership_skills": len(self.leadership_skills),
            "strategic_skills": len(self.strategic_skills),
            "total_skill_definitions": (
                len(self.core_skills) +
                sum(len(s) for s in self.office_skills.values()) +
                len(self.leadership_skills) +
                len(self.strategic_skills)
            ),
            "registered_agents": len(self.agent_skills),
            "total_skill_slots": total_skill_slots,
            "avg_skills_per_agent": round(total_skill_slots / max(len(self.agent_skills), 1), 2),
            "total_violations": len(self.violation_log),
            "mandatory_skills": sum(1 for s in self.core_skills.values() if s.is_mandatory)
        }
