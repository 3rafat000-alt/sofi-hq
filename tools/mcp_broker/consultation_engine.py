#!/usr/bin/env python3
"""
Sofi MCP Broker — Consultation Engine
=========================================
محرك التشاور العميق بين الوكلاء — نقاش، تحليل، تصويت، توصيات
"""

import asyncio
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ConsultationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VOTING = "voting"
    COMPLETED = "completed"
    TIMEOUT = "timeout"


class VoteChoice(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"
    NEEDS_MORE_INFO = "needs_more_info"


@dataclass
class ConsultantOpinion:
    """رأي مستشار في جلسة تشاور"""
    agent_id: str
    agent_name: str
    vote: VoteChoice = VoteChoice.ABSTAIN
    reasoning: str = ""
    alternative_suggestions: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    confidence: float = 0.5  # 0.0 to 1.0


@dataclass
class ConsultationSession:
    """جلسة تشاور كاملة"""
    id: str = ""
    topic: str = ""
    initiator: str = ""
    participants: List[str] = field(default_factory=list)
    status: ConsultationStatus = ConsultationStatus.PENDING
    opinions: Dict[str, ConsultantOpinion] = field(default_factory=dict)
    debate_rounds: List[Dict] = field(default_factory=list)
    final_recommendation: str = ""
    consensus_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str = ""


class ConsultationEngine:
    """محرك التشاور — يدير جلسات النقاش والتصويت"""
    
    def __init__(self):
        self.active_sessions: Dict[str, ConsultationSession] = {}
        self.completed_sessions: List[ConsultationSession] = []
    
    async def start_consultation(self, topic: str, initiator: str,
                                   participants: List[str]) -> ConsultationSession:
        """بدء جلسة تشاور جديدة"""
        import uuid
        session = ConsultationSession(
            id=str(uuid.uuid4())[:8],
            topic=topic,
            initiator=initiator,
            participants=participants,
            status=ConsultationStatus.IN_PROGRESS
        )
        self.active_sessions[session.id] = session
        
        print(f"\n{'='*60}")
        print(f"🏛️  جلسة تشاور: {topic}")
        print(f"   المبادر: {initiator}")
        print(f"   المشاركون: {', '.join(participants)}")
        print(f"{'='*60}")
        
        return session
    
    async def submit_opinion(self, session_id: str, agent_id: str,
                              agent_name: str, vote: VoteChoice,
                              reasoning: str, confidence: float = 0.7) -> bool:
        """تقديم رأي في جلسة تشاور"""
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        opinion = ConsultantOpinion(
            agent_id=agent_id,
            agent_name=agent_name,
            vote=vote,
            reasoning=reasoning,
            confidence=confidence
        )
        session.opinions[agent_id] = opinion
        
        print(f"\n  💬  {agent_name}: {vote.value}")
        print(f"       {reasoning[:100]}...")
        
        return True
    
    async def run_debate_round(self, session_id: str) -> Dict:
        """تشغيل جولة نقاش"""
        session = self.active_sessions.get(session_id)
        if not session:
            return {"error": "session not found"}
        
        round_data = {
            "round": len(session.debate_rounds) + 1,
            "discussions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # محاكاة نقاش بين المستشارين
        for agent_id, opinion in session.opinions.items():
            for other_id, other_opinion in session.opinions.items():
                if agent_id != other_id and opinion.vote != other_opinion.vote:
                    discussion = {
                        "from": opinion.agent_name,
                        "to": other_opinion.agent_name,
                        "point": f"اختلاف في الرأي: {opinion.vote.value} vs {other_opinion.vote.value}"
                    }
                    round_data["discussions"].append(discussion)
        
        session.debate_rounds.append(round_data)
        return round_data
    
    async def calculate_consensus(self, session_id: str) -> float:
        """حساب درجة التوافق"""
        session = self.active_sessions.get(session_id)
        if not session or not session.opinions:
            return 0.0
        
        votes = [o.vote for o in session.opinions.values()]
        approves = sum(1 for v in votes if v == VoteChoice.APPROVE)
        total = len(votes)
        
        session.consensus_score = approves / max(total, 1)
        return session.consensus_score
    
    async def finalize(self, session_id: str) -> ConsultationSession:
        """إنهاء جلسة التشاور"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        await self.calculate_consensus(session_id)
        
        # توليد التوصية النهائية
        if session.consensus_score >= 0.8:
            session.final_recommendation = "✅ توافق قوي — موصى به للمتابعة"
            session.status = ConsultationStatus.COMPLETED
        elif session.consensus_score >= 0.5:
            session.final_recommendation = "🔄 توافق متوسط — يحتاج تحسينات قبل المتابعة"
            session.status = ConsultationStatus.VOTING
        else:
            session.final_recommendation = "❌ لا يوجد توافق — يحتاج إعادة تقييم كاملة"
            session.status = ConsultationStatus.COMPLETED
        
        session.completed_at = datetime.now().isoformat()
        
        self.completed_sessions.append(session)
        del self.active_sessions[session_id]
        
        print(f"\n{'='*60}")
        print(f"🏁  نهاية جلسة التشاور")
        print(f"   الموضوع: {session.topic}")
        print(f"   التوافق: {session.consensus_score:.0%}")
        print(f"   التوصية: {session.final_recommendation}")
        print(f"{'='*60}")
        
        return session
    
    def get_session(self, session_id: str) -> Optional[ConsultationSession]:
        return self.active_sessions.get(session_id) or \
               next((s for s in self.completed_sessions if s.id == session_id), None)
    
    def get_stats(self) -> dict:
        return {
            "active_sessions": len(self.active_sessions),
            "completed_sessions": len(self.completed_sessions),
            "total_participants": sum(len(s.participants) for s in self.completed_sessions)
        }
