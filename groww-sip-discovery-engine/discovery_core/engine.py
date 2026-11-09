"""
engine.py - 4-stage AI Classification & Diagnosis Engine for Groww SIP User Feedback.
Uses Gemini 3.8 Flash with structured JSON output and deterministic heuristic fallbacks.
"""

import json
import re
from typing import Optional, Dict, Any, Tuple
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from discovery_core.schemas import (
    FailureCategory,
    InvestorTenure,
    CognitiveProfile,
    AnalysisResult,
    CATEGORY_LABELS,
)
from discovery_core.config import GEMINI_API_KEY, DEFAULT_MODEL


class LLMStructuredOutput(BaseModel):
    is_relevant: bool = Field(..., description="Whether feedback relates to SIP journey, mandates, returns, or drop-off")
    relevance_rationale: str = Field(..., description="1-sentence explanation of relevance decision")
    primary_category: Optional[str] = Field(None, description="One of the 7 FailureCategory enum strings")
    secondary_category: Optional[str] = Field(None, description="Optional secondary FailureCategory enum string")
    category_confidence: float = Field(0.0, description="Confidence score from 0.0 to 1.0")
    initial_motivation: str = Field("", description="Why user started SIP (e.g. compounding, tax, friend advice)")
    expectation_delta: str = Field("", description="How reality differed from expectation")
    primary_anxiety: str = Field("", description="Core emotional stressor or confusion")
    coping_behavior: str = Field("", description="Reactive action taken e.g. cancelled mandate, paused, redeemed")
    churn_imminence_score: int = Field(1, description="1 (low risk) to 5 (definite churn/cancelled)")
    product_solvability_score: int = Field(1, description="1 (unsolvable via UI/UX) to 5 (directly solvable in Growth)")
    key_quote: str = Field("", description="Short verbatim excerpt encapsulating pain point")
    product_opportunity: str = Field("", description="Target product intervention area")


SYSTEM_PROMPT = """You are an expert Principal Product Manager on the Growth Team at GROWW (India's leading mutual fund & investment platform).
Your task is to analyze user feedback, forum discussions, and reviews from first-time mutual fund investors to diagnose why they pause, cancel, or let their monthly SIPs lapse in their first 12 months.

Strict constraints:
- Do NOT recommend specific stocks or funds.
- Do NOT encourage FOMO or urgency.
- The 7 grounded failure categories are:
  1. BANK_MANDATE_PENALTY_SHOCK: E-mandate bounce fees (Rs 250-500 NACH penalty by bank), delayed salary crediting past debit date, autopay authorization bugs.
  2. RETURN_ILLUSION_DISILLUSION: Flat or negative returns in months 3-9 leading to disillusionment ('FD is better than MF', 'I am losing money').
  3. CASHFLOW_RIGID_ANXIETY: Rigid monthly debit dates clash with variable income, emergency expenses, fear of account dipping below minimum balance.
  4. METRIC_METAPHOR_CONFUSION: XIRR vs Absolute returns confusion, panic when NAV dips even if units accumulated, ELSS lock-in surprises.
  5. QUIET_DISENGAGE_HABIT_FADE: No perceived tangible milestone in months 4-10; app opened less frequently; SIP feels like an invisible recurring drain with no dopamine.
  6. EXTERNAL_DRAFT_PANIC_PULL: Advice from elder, family, or social media panic causing user to stop equity SIP and switch to gold/FD.
  7. GOAL_DETACHMENT_LIQUIDATION: SIP started without a life goal; liquidated for short-term impulse spending (gadgets, vacations).

Evaluate the user text rigorously and output structured JSON adhering to the schema.
"""


class DiscoveryEngine:
    """Core AI diagnostic engine with dual LLM and heuristic fallback execution."""

    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model
        self.client = None
        if self.api_key and not self.api_key.startswith("your-"):
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[DiscoveryEngine] Warning: Could not initialize Gemini client: {e}")

    def analyze(self, text: str, record_id: str = "rec_custom") -> AnalysisResult:
        """Run 4-stage diagnosis on input text using LLM, with deterministic fallback."""
        if self.client:
            try:
                prompt = f"Analyze the following user feedback regarding mutual fund SIPs:\n\n\"\"\"\n{text}\n\"\"\""
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=LLMStructuredOutput,
                        temperature=0.1,
                    ),
                )
                if response.text:
                    parsed = LLMStructuredOutput.model_validate_json(response.text)
                    return self._map_llm_output_to_result(record_id, parsed, text)
            except Exception as e:
                print(f"[DiscoveryEngine] LLM invocation failed ({e}), falling back to heuristic engine.")

        # Heuristic fallback engine
        return self._heuristic_analyze(text, record_id)

    def _map_llm_output_to_result(
        self, record_id: str, parsed: LLMStructuredOutput, raw_text: str
    ) -> AnalysisResult:
        primary_cat = None
        if parsed.primary_category:
            try:
                primary_cat = FailureCategory(parsed.primary_category)
            except ValueError:
                primary_cat = None

        secondary_cat = None
        if parsed.secondary_category:
            try:
                secondary_cat = FailureCategory(parsed.secondary_category)
            except ValueError:
                secondary_cat = None

        profile = None
        if parsed.is_relevant:
            profile = CognitiveProfile(
                initial_motivation=parsed.initial_motivation or "Wealth creation / habit",
                expectation_delta=parsed.expectation_delta or "Unmet growth expectations",
                primary_anxiety=parsed.primary_anxiety or "Loss aversion / penalty fear",
                coping_behavior=parsed.coping_behavior or "Paused or stopped installment",
            )

        return AnalysisResult(
            record_id=record_id,
            is_relevant=parsed.is_relevant,
            relevance_rationale=parsed.relevance_rationale,
            primary_category=primary_cat,
            secondary_category=secondary_cat,
            category_confidence=round(parsed.category_confidence, 2),
            cognitive_profile=profile,
            churn_imminence_score=parsed.churn_imminence_score,
            product_solvability_score=parsed.product_solvability_score,
            key_quote=parsed.key_quote or raw_text[:120],
            product_opportunity=parsed.product_opportunity or "Targeted growth intervention",
        )

    def _heuristic_analyze(self, text: str, record_id: str) -> AnalysisResult:
        """Deterministic heuristic ruleset for offline analysis & resilience."""
        lower = text.lower()

        # Relevance check
        sip_keywords = ["sip", "mutual fund", "installment", "instalment", "mandate", "autopay", "nav", "xirr", "portfolio", "redeem", "elss", "groww"]
        is_relevant = any(kw in lower for kw in sip_keywords)
        if not is_relevant:
            return AnalysisResult(
                record_id=record_id,
                is_relevant=False,
                relevance_rationale="No indicators of mutual fund or SIP investment journey detected.",
                churn_imminence_score=1,
                product_solvability_score=1,
                key_quote=text[:80],
                product_opportunity="N/A",
            )

        # Categorization heuristics with regex word boundaries
        cat = FailureCategory.RETURN_ILLUSION_DISILLUSION
        confidence = 0.85
        imminence = 3
        solvability = 4
        opp = "Expectation framing & SIP milestone architecture"

        if re.search(r"\b(?:bounce|penalty|nach|mandate failed|charged|fees?|deducted twice)\b", lower):
            cat = FailureCategory.BANK_MANDATE_PENALTY_SHOCK
            imminence = 5
            solvability = 5
            opp = "Smart Balance Buffer & Salary-Synced Debit Windows"
        elif re.search(r"\b(?:rigid|change date|delay|skip|freelance|emergency|minimum balance)\b", lower):
            cat = FailureCategory.CASHFLOW_RIGID_ANXIETY
            imminence = 4
            solvability = 5
            opp = "Flexible Micro-Skip & Adaptive Debit Scheduling"
        elif re.search(r"\b(?:xirr|units|jargon|what does|confusing numbers|elss locked)\b", lower):
            cat = FailureCategory.METRIC_METAPHOR_CONFUSION
            imminence = 3
            solvability = 5
            opp = "Visual Unit Accumulation & Contextual Demystification"
        elif re.search(r"\b(?:haven't opened|forgot|subscription|detached|months later|no motivation)\b", lower):
            cat = FailureCategory.QUIET_DISENGAGE_HABIT_FADE
            imminence = 4
            solvability = 4
            opp = "Consistency Streaks & Affirmative Habit Milestones"
        elif re.search(r"\b(?:uncle|father|colleague|news|war|crash|gold|fd)\b", lower):
            cat = FailureCategory.EXTERNAL_DRAFT_PANIC_PULL
            imminence = 4
            solvability = 3
            opp = "Educational Peer Context & Volatility Mental Models"
        elif re.search(r"\b(?:vacation|iphone|goa|shopping|redeemed|withdrew|no goal)\b", lower):
            cat = FailureCategory.GOAL_DETACHMENT_LIQUIDATION
            imminence = 5
            solvability = 4
            opp = "Goal-Linked Buckets & Intentional Locking"
        elif re.search(r"\b(?:red|loss|minus|fd gives|profit is only|decreasing)\b", lower):
            cat = FailureCategory.RETURN_ILLUSION_DISILLUSION
            imminence = 4
            solvability = 4
            opp = "Rupee Cost Averaging Visualizer & Return Reality Anchor"

        return AnalysisResult(
            record_id=record_id,
            is_relevant=True,
            relevance_rationale="User describes firsthand friction or sentiment regarding mutual fund SIP.",
            primary_category=cat,
            secondary_category=None,
            category_confidence=confidence,
            cognitive_profile=CognitiveProfile(
                initial_motivation="Long-term wealth creation / savings habit",
                expectation_delta="Early friction or unexpected cognitive/financial hurdle",
                primary_anxiety=CATEGORY_LABELS[cat],
                coping_behavior="Considering pausing or discontinuing SIP",
            ),
            churn_imminence_score=imminence,
            product_solvability_score=solvability,
            key_quote=text[:120],
            product_opportunity=opp,
        )
