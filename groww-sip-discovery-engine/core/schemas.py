from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class FailureCategory(str, Enum):
    BANK_MANDATE_PENALTY_SHOCK = "BANK_MANDATE_PENALTY_SHOCK"
    RETURN_ILLUSION_DISILLUSION = "RETURN_ILLUSION_DISILLUSION"
    CASHFLOW_RIGID_ANXIETY = "CASHFLOW_RIGID_ANXIETY"
    METRIC_METAPHOR_CONFUSION = "METRIC_METAPHOR_CONFUSION"
    QUIET_DISENGAGE_HABIT_FADE = "QUIET_DISENGAGE_HABIT_FADE"
    EXTERNAL_DRAFT_PANIC_PULL = "EXTERNAL_DRAFT_PANIC_PULL"
    GOAL_DETACHMENT_LIQUIDATION = "GOAL_DETACHMENT_LIQUIDATION"


CATEGORY_LABELS: Dict[FailureCategory, str] = {
    FailureCategory.BANK_MANDATE_PENALTY_SHOCK: "Bank Mandate & Penalty Shock",
    FailureCategory.RETURN_ILLUSION_DISILLUSION: "Return Illusion & Early Disillusionment",
    FailureCategory.CASHFLOW_RIGID_ANXIETY: "Rigid Debit Schedule & Cashflow Anxiety",
    FailureCategory.METRIC_METAPHOR_CONFUSION: "Metric & Jargon Confusion (XIRR/NAV)",
    FailureCategory.QUIET_DISENGAGE_HABIT_FADE: "Quiet Disengagement & Habit Fade",
    FailureCategory.EXTERNAL_DRAFT_PANIC_PULL: "External Social Draft & Panicked Shift",
    FailureCategory.GOAL_DETACHMENT_LIQUIDATION: "Goal Detachment & Impulse Liquidation",
}

CATEGORY_DESCRIPTIONS: Dict[FailureCategory, str] = {
    FailureCategory.BANK_MANDATE_PENALTY_SHOCK: (
        "E-mandate bounce fees (₹250-500 NACH penalty by bank), delayed salary crediting "
        "causing failed auto-debits, confusing auto-pay authorization states, or duplicate debits."
    ),
    FailureCategory.RETURN_ILLUSION_DISILLUSION: (
        "Flat or negative nominal returns in months 3-9 leading to disillusionment. Investor expects "
        "steady monthly growth like an FD and feels 'mutual funds are a scam' or 'I am losing money'."
    ),
    FailureCategory.CASHFLOW_RIGID_ANXIETY: (
        "Fixed monthly deduction dates causing friction when unexpected expenses hit, salary dates vary, "
        "or fear of bank account balance dropping below minimum average requirement."
    ),
    FailureCategory.METRIC_METAPHOR_CONFUSION: (
        "Inability to interpret XIRR vs Absolute returns, confusing NAV fluctuations with capital loss, "
        "or misunderstanding units accumulation and expense ratio calculations."
    ),
    FailureCategory.QUIET_DISENGAGE_HABIT_FADE: (
        "Lack of positive feedback loops or tangible milestones in months 4-10. App usage drops to zero, "
        "and user silently views the SIP as a passive friction or budget leakage until cancelling."
    ),
    FailureCategory.EXTERNAL_DRAFT_PANIC_PULL: (
        "Outside influence (family elder, friends, sensationalist YouTube/social media videos) urging the "
        "user to stop equity investments and move funds back to bank FDs, physical gold, or crypto during market dips."
    ),
    FailureCategory.GOAL_DETACHMENT_LIQUIDATION: (
        "SIP started generically without linking to any tangible life goal or milestone. As soon as a short-term "
        "desire arises (vacation, gadget, festival spending), the accumulated balance is liquidated and the SIP paused."
    ),
}


class SourceType(str, Enum):
    PLAY_STORE = "PLAY_STORE"
    APP_STORE = "APP_STORE"
    REDDIT = "REDDIT"
    FORUM = "FORUM"
    YOUTUBE = "YOUTUBE"


class InvestorTenure(str, Enum):
    MONTH_1 = "MONTH_1"
    MONTHS_2_3 = "MONTHS_2_3"
    MONTHS_4_6 = "MONTHS_4_6"
    MONTHS_7_9 = "MONTHS_7_9"
    MONTHS_10_12 = "MONTHS_10_12"
    YEAR_1_PLUS = "YEAR_1_PLUS"
    UNSPECIFIED = "UNSPECIFIED"


class UnifiedSIPRecord(BaseModel):
    record_id: str = Field(..., description="Unique deterministic SHA-256 identifier")
    source: SourceType
    timestamp: str = Field(..., description="ISO 8601 or date string of feedback")
    raw_text: str = Field(..., description="Sanitized, PII-scrubbed text")
    user_tenure_hint: InvestorTenure = Field(default=InvestorTenure.UNSPECIFIED)
    inferred_segment: str = Field(default="general_first_timer")
    status: str = Field(default="active", description="active, paused, stopped, considering_stop")


class CognitiveProfile(BaseModel):
    initial_motivation: str = Field(..., description="Initial anchor or trigger to start SIP")
    expectation_delta: str = Field(..., description="How reality diverged from initial expectations")
    primary_anxiety: str = Field(..., description="Core fear, confusion, or stress experienced")
    coping_behavior: str = Field(..., description="Workaround or reactive behavior adopted")


class AnalysisResult(BaseModel):
    record_id: str
    is_relevant: bool = Field(..., description="Whether this feedback pertains to first-time SIP journey/drop-off")
    relevance_rationale: str
    primary_category: Optional[FailureCategory] = None
    secondary_category: Optional[FailureCategory] = None
    category_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    cognitive_profile: Optional[CognitiveProfile] = None
    churn_imminence_score: int = Field(default=1, ge=1, le=5, description="1=Curious/Healthy, 5=Definite Churn/Lapse")
    product_solvability_score: int = Field(default=1, ge=1, le=5, description="1=Unsolvable via UI/UX, 5=Directly Fixable in Growth Product")
    key_quote: str = Field(default="", description="Verbatim customer quote exemplifying the pain point")
    product_opportunity: str = Field(default="", description="Target product intervention area")


class GoldenSetItem(BaseModel):
    item_id: str
    text: str
    source: SourceType
    true_relevant: bool
    true_category: Optional[FailureCategory] = None
    true_tenure: InvestorTenure = InvestorTenure.UNSPECIFIED
    human_rationale: str
    predicted_category: Optional[FailureCategory] = None
    is_match: Optional[bool] = None
    evaluation_notes: Optional[str] = None

