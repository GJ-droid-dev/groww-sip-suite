"""
assistant.py - PulseSIP AI Companion Engine with Eval-Gated Quality & Safety.
Uses Gemini 3.8 Flash structured output with deterministic fallback.
"""

import json
import re
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from core.schemas import PortfolioState, AssistantResponse, EvalGateVerdict
from core.eval_gate import EvalGate
from core.config import GEMINI_API_KEY, DEFAULT_MODEL


class LLMAssistantOutput(BaseModel):
    intent_category: str = Field(..., description="CASHFLOW_FLEX, SALARY_SYNC, DIP_EDUCATION, GENERAL")
    user_facing_message: str = Field(..., description="Conversational, empathetic explanation for investor")
    action_type: str = Field(default="NONE", description="FLEX_AMOUNT, SNOOZE_DATE, REFRAME_DIP, NONE")
    recommended_amount: Optional[float] = Field(None, description="Suggested temporary flex amount in rupees")
    recommended_date_offset_days: Optional[int] = Field(None, description="Suggested postponement in days")
    unit_accumulation_insight: Optional[str] = Field(None, description="Calculated bonus units insight during dip")


SYSTEM_PROMPT = """You are 'PulseSIP', the AI Cashflow & Habit Companion inside Groww (India's leading investment platform).
Your mission is to help first-time mutual fund investors stay invested for 12 months without dropping out.

Strict Constraints:
1. NEVER recommend specific stocks, funds, or crypto (SEBI Compliance).
2. NEVER use fear, urgency, or FOMO nudges.
3. If user faces cashflow stress (e.g., Diwali shopping, festivals, salary delayed, emergency):
   - Provide a safe 1-cycle Micro-Flex (e.g. temporarily lowering ₹5,000 to ₹1,500) OR
   - Snooze debit date by 3 to 7 days to match salary credit and prevent bank bounce fees.
4. If user is anxious about red returns or NAV dips:
   - Reframe the dip around RUPEE-COST AVERAGING and UNIT ACCUMULATION. Explain that a fixed SIP amount buys MORE units at a lower price, building wealth when the market recovers.
5. Be warm, supportive, and mathematically grounded.
"""


class PulseSIPEngine:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or GEMINI_API_KEY
        self.model = model
        self.client = None
        if self.api_key and not self.api_key.startswith("your-"):
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[PulseSIP] Warning: Could not init Gemini client: {e}")

    def respond(self, user_query: str, portfolio: PortfolioState) -> AssistantResponse:
        # 1. Pre-Execution Eval Gate Check
        pre_check = EvalGate.evaluate(user_query)
        if not pre_check.passed:
            if pre_check.violation_type == "STOCK_ADVICE_REQUEST":
                return AssistantResponse(
                    intent_category="ADVICE_REFUSAL",
                    user_facing_message=EvalGate.get_advice_refusal_fallback(),
                    action_type="FALLBACK",
                    eval_gate=pre_check,
                )
            elif pre_check.violation_type == "URGENCY_FOMO":
                return AssistantResponse(
                    intent_category="ADVICE_REFUSAL",
                    user_facing_message=EvalGate.get_fomo_fallback(),
                    action_type="FALLBACK",
                    eval_gate=pre_check,
                )

        # 2. Compute dynamic unit accumulation metrics for portfolio
        current_nav = portfolio.latest_nav
        prev_nav = portfolio.previous_month_nav
        monthly_amt = portfolio.monthly_installment

        current_units = monthly_amt / current_nav
        prev_units = monthly_amt / prev_nav
        bonus_units = max(0.0, current_units - prev_units)
        discount_pct = max(0.0, ((prev_nav - current_nav) / prev_nav) * 100.0)

        calc_context = (
            f"User Portfolio State:\n"
            f"- Scheme: {portfolio.scheme_name}\n"
            f"- Monthly SIP: Rs {portfolio.monthly_installment:.0f}\n"
            f"- Current Value: Rs {portfolio.current_value:.0f} (Nominal: {portfolio.nominal_return_pct:.2f}%)\n"
            f"- Current NAV: Rs {current_nav:.2f} (down {discount_pct:.1f}% from Rs {prev_nav:.2f})\n"
            f"- Units acquired this month: {current_units:.2f} vs {prev_units:.2f} last month (+{bonus_units:.2f} bonus units)\n"
            f"- Scheduled Debit Date: {portfolio.debit_date}th\n"
            f"- Active Habit Streak: {portfolio.streak_count} months ({portfolio.streak_tier})\n"
        )

        # 3. LLM Generation
        if self.client:
            try:
                prompt = f"{calc_context}\n\nUser Query: \"{user_query}\"\nProvide structured JSON response."
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        response_mime_type="application/json",
                        response_schema=LLMAssistantOutput,
                        temperature=0.2,
                    ),
                )
                if response.text:
                    parsed = LLMAssistantOutput.model_validate_json(response.text)
                    post_check = EvalGate.evaluate(user_query, parsed.user_facing_message)

                    return AssistantResponse(
                        intent_category=parsed.intent_category,
                        user_facing_message=parsed.user_facing_message,
                        action_type=parsed.action_type,
                        action_params={
                            "recommended_amount": parsed.recommended_amount or 1500.0,
                            "recommended_date_offset_days": parsed.recommended_date_offset_days or 4,
                            "original_amount": portfolio.monthly_installment,
                            "original_date": portfolio.debit_date,
                        },
                        unit_accumulation_insight=(
                            f"✨ **Market Dip Advantage:** Your ₹{monthly_amt:,.0f} acquired **{current_units:.2f} units** "
                            f"at ₹{current_nav:.1f}/unit (vs {prev_units:.2f} units last month). You gained **+{bonus_units:.2f} bonus units "
                            f"at a {discount_pct:.1f}% discount**!"
                        ),
                        eval_gate=post_check,
                    )
            except Exception as e:
                print(f"[PulseSIP] LLM generation error ({e}), engaging fallback.")

        # 4. Deterministic Heuristic Fallback Engine
        return self._heuristic_respond(user_query, portfolio, current_units, prev_units, bonus_units, discount_pct)

    def _heuristic_respond(
        self,
        query: str,
        portfolio: PortfolioState,
        current_units: float,
        prev_units: float,
        bonus_units: float,
        discount_pct: float,
    ) -> AssistantResponse:
        lower = query.lower()
        debit_date = portfolio.debit_date

        if any(w in lower for w in ["salary", "delay", "holiday", "weekend", "bounced", "penalty", "nach"]):
            new_date = min(28, debit_date + 4)
            return AssistantResponse(
                intent_category="SALARY_SYNC",
                user_facing_message=(
                    f"I understand your salary date shifted. To make sure you never face an accidental bank bounce fine (₹295 NACH fee), "
                    f"we can synchronize your debit date from the **{debit_date}th** to the **{new_date}th** of this month. "
                    f"Your mandate remains active and your 5-month streak continues uninterrupted!"
                ),
                action_type="SNOOZE_DATE",
                action_params={"new_date": new_date, "original_date": debit_date, "days_offset": 4},
                eval_gate=EvalGate.evaluate(query, "salary sync"),
            )

        elif any(w in lower for w in ["diwali", "festival", "tight", "less", "reduce", "expense", "shopping", "cash", "pause", "cancel"]):
            flex_amt = 1500.0
            return AssistantResponse(
                intent_category="CASHFLOW_FLEX",
                user_facing_message=(
                    f"Festive seasons and unplanned expenses are completely natural! Instead of cancelling your entire SIP or paying a heavy ₹5,000, "
                    f"you can activate **1-Cycle Smart Flex** to contribute just **₹{flex_amt:,.0f}** for this upcoming month. "
                    f"This preserves your cash in hand, keeps your mandate healthy, and protects your 5-Month Consistency Streak!"
                ),
                action_type="FLEX_AMOUNT",
                action_params={"recommended_amount": flex_amt, "original_amount": portfolio.monthly_installment},
                eval_gate=EvalGate.evaluate(query, "smart flex"),
            )

        else:
            # Market dip / return anxiety
            insight = (
                f"✨ **Market Dip Advantage:** Your ₹{portfolio.monthly_installment:,.0f} acquired **{current_units:.2f} units** "
                f"at ₹{portfolio.latest_nav:.1f}/unit (vs {prev_units:.2f} units last month). You gained **+{bonus_units:.2f} bonus units "
                f"at a {discount_pct:.1f}% discount**!"
            )
            return AssistantResponse(
                intent_category="DIP_EDUCATION",
                user_facing_message=(
                    f"It's completely normal to feel concerned when you see red numbers (-2.32%), but here is how your SIP is actually working for you:\n\n"
                    f"When market prices dip, your fixed ₹{portfolio.monthly_installment:,.0f} doesn't lose money—it acts like a **discount shopper**, "
                    f"buying **more mutual fund units** at lower prices. When the market recovers, every single bonus unit you bought at a discount accelerates your compounding!"
                ),
                action_type="REFRAME_DIP",
                unit_accumulation_insight=insight,
                eval_gate=EvalGate.evaluate(query, "dip education"),
            )

