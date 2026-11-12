"""
Semantic Router for HALO RAG Studio.

Maps queries to candidate notebook documents within the 15-file verified corpus.
"""

import re
from typing import Any, Dict, List, Set, Tuple


class RouteResult:
    def __init__(
        self,
        target_doc_ids: List[str],
        category: str,
        confidence: float,
        reasoning: str
    ):
        self.target_doc_ids = target_doc_ids
        self.category = category
        self.confidence = confidence
        self.reasoning = reasoning

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_doc_ids": self.target_doc_ids,
            "category": self.category,
            "confidence": round(self.confidence, 4),
            "reasoning": self.reasoning
        }


class SemanticRouter:
    """
    Directs queries to target source notebooks based on domain keywords and category matches.
    """

    DOMAIN_KEYWORDS: Dict[str, Tuple[List[str], List[str]]] = {
        "Cognitive & Neuroscience": (
            ["mozak", "dopamin", "amigdala", "prefrontalni", "kontrola", "navike", "neuro"],
            ["01", "10", "13"]
        ),
        "Enterprise AI Transformation": (
            ["digital", "engineering", "see", "enterprise", "transformacija", "arhitektura"],
            ["02", "12"]
        ),
        "Autonomous OS & Systems": (
            ["openclaw", "sovereign", "agentic os", "operativni", "koyeb", "discord"],
            ["03"]
        ),
        "Antigravity IDE & Tooling": (
            ["antigravity", "ide", "editor", "mission control", "subagent", "agy", "browser agent"],
            ["04"]
        ),
        "Deterministic RAG Architecture": (
            ["codymaster", "deterministic rag", "rule of 3", "dual-brain", "pajplajn", "hallucination"],
            ["05"]
        ),
        "Behavioral Psychology & TMT": (
            ["prokrastinacija", "tmt", "odlaganje", "motivacija", "impulsivnost", "odlaganj"],
            ["06"]
        ),
        "NotebookLM & Prompt Engineering": (
            ["notebooklm", "custom prompts", "gemini 3", "prompting", "audio overview", "grounding"],
            ["07", "09"]
        ),
        "Autonomous Social Agents": (
            ["linkedin", "franklin", "automatizacija", "lead", "outreach", "social"],
            ["08"]
        ),
        "Neuroplasticity & Silva Method": (
            ["silva", "nlp", "neuroplasticnost", "alfa", "meditacija", "sidrenje"],
            ["10"]
        ),
        "Spatial Computing & UI 2026": (
            ["ui", "ux", "spatial", "prostorno", "interfejs", "2026", "dizajn"],
            ["11"]
        ),
        "Deep Learning Foundations": (
            ["duboko ucenje", "deep learning", "neuronske", "cnn", "transformer", "backpropagation"],
            ["12"]
        ),
        "Strategic Decision Making": (
            ["odlucivanje", "7 koraka", "strategija", "odluka", "evaluacija", "prioriteti"],
            ["13"]
        ),
        "Personal Brand & Inbound Funnel": (
            ["licni brend", "inbound", "funnel", "monetizacija", "pozicioniranje", "marketing"],
            ["14", "15"]
        )
    }

    def route_query(self, query: str) -> RouteResult:
        q_tokens = set(re.findall(r"\w+", query.lower()))
        best_category = "General Knowledge"
        best_doc_ids: List[str] = []
        highest_matches = 0

        for cat, (keywords, doc_ids) in self.DOMAIN_KEYWORDS.items():
            matches = sum(1 for kw in keywords if any(kw in t for t in q_tokens) or kw in query.lower())
            if matches > highest_matches:
                highest_matches = matches
                best_category = cat
                best_doc_ids = doc_ids

        if highest_matches > 0:
            confidence = min(0.95, 0.60 + 0.10 * highest_matches)
            return RouteResult(
                target_doc_ids=best_doc_ids,
                category=best_category,
                confidence=confidence,
                reasoning=f"Matched {highest_matches} domain keywords for category '{best_category}'"
            )

        # Fallback to broad search across core documentation
        return RouteResult(
            target_doc_ids=["01", "04", "05"],
            category="Broad Discovery",
            confidence=0.40,
            reasoning="No high-confidence domain keywords matched; routing to foundational architecture notebooks"
        )
