from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class PortfolioState(BaseModel):
    user_name: str = "Aarav Sharma"
    tenure_months: int = 5
    scheme_name: str = "Parag Parikh Flexi Cap Fund - Direct Growth"
    monthly_installment: float = 5000.0
    debit_date: int = 5
    linked_bank: str = "HDFC Bank (Salary Account ****1234)"
    total_invested: float = 25000.0
    current_value: float = 24420.0
    nominal_return_pct: float = -2.32
    nominal_return_abs: float = -580.0
    total_units_accumulated: float = 68.42
    latest_nav: float = 356.91
    previous_month_nav: float = 382.40
    streak_count: int = 5
    streak_tier: str = "Silver Habit Streak"
    status: str = "Active"


class EvalGateVerdict(BaseModel):
    passed: bool = Field(..., description="Whether the interaction passed all compliance gates")
    violation_detected: bool = Field(default=False)
    violation_type: Optional[str] = Field(None, description="STOCK_ADVICE_REQUEST, URGENCY_FOMO, HALLUCINATION")
    explanation: str = Field(..., description="Audit rationale for evaluator")
    safety_score: float = Field(default=1.0, ge=0.0, le=1.0)
    safe_fallback_used: bool = Field(default=False)


class AssistantResponse(BaseModel):
    intent_category: str = Field(..., description="CASHFLOW_FLEX, SALARY_SYNC, DIP_EDUCATION, ADVICE_REFUSAL, GENERAL")
    user_facing_message: str = Field(..., description="Empathetic, clear, non-advisory message for the user")
    action_type: str = Field(default="NONE", description="FLEX_AMOUNT, SNOOZE_DATE, REFRAME_DIP, FALLBACK")
    action_params: Dict[str, Any] = Field(default_factory=dict)
    unit_accumulation_insight: Optional[str] = None
    eval_gate: EvalGateVerdict

