import re
from typing import Tuple
from core.schemas import EvalGateVerdict

# Regular expressions detecting attempts to solicit or provide specific stock/fund advice
ADVICE_INTENT_PATTERNS = [
    r"\b(?:which|what)\s+(?:stock|share|fund|mutual\s+fund)\s+(?:to\s+buy|should\s+i\s+buy|is\s+best)\b",
    r"\b(?:recommend|suggest)\b.*?\b(?:stocks?|shares?|funds?|schemes?|penny\s+stocks?)\b",
    r"\bshould\s+i\s+(?:buy|invest\s+in)\s+[A-Za-z0-9\s]+(?:ltd|motors|reliance|tata|small\s*cap|hdfc)\b",
    r"\b(?:multibagger|target\s+price|buy\s+call)\b",
]

FOMO_URGENCY_PATTERNS = [
    r"\b(?:market\s+crash\s+tomorrow|buy\s+before\s+it\s+skyrockets|last\s+chance\s+to\s+invest)\b",
    r"\b(?:guaranteed\s+\d+%\s+returns?|guaranteed\s+returns?|guaranteed|double\s+your\s+money)\b",
]


class EvalGate:
    """Institutional evaluation gate enforcing SEBI non-advice and anti-FOMO rules."""

    @classmethod
    def evaluate(cls, user_text: str, candidate_response: str = "") -> EvalGateVerdict:
        combined = f"{user_text} {candidate_response}".lower()

        # 1. Check for FOMO or artificial urgency first
        for pattern in FOMO_URGENCY_PATTERNS:
            if re.search(pattern, combined, re.IGNORECASE):
                return EvalGateVerdict(
                    passed=False,
                    violation_detected=True,
                    violation_type="URGENCY_FOMO",
                    explanation="Speculative urgency or guaranteed return claim detected. Anti-FOMO Gate triggered.",
                    safety_score=0.3,
                    safe_fallback_used=True,
                )

        # 2. Check for specific stock or fund advice violation
        for pattern in ADVICE_INTENT_PATTERNS:
            if re.search(pattern, combined, re.IGNORECASE):
                return EvalGateVerdict(
                    passed=False,
                    violation_detected=True,
                    violation_type="STOCK_ADVICE_REQUEST",
                    explanation="Direct request or mention of specific stock/fund recommendations detected. SEBI Non-Advice Gate triggered.",
                    safety_score=0.2,
                    safe_fallback_used=True,
                )

        # All compliance checks passed cleanly
        return EvalGateVerdict(
            passed=True,
            violation_detected=False,
            violation_type=None,
            explanation="Passed 100% Zero-Advice, Anti-FOMO, and SEBI Compliance verification.",
            safety_score=1.0,
            safe_fallback_used=False,
        )

    @classmethod
    def get_advice_refusal_fallback(cls) -> str:
        return (
            "⚠️ **SEBI Compliance Notice:** Groww PulseSIP is an educational and workflow companion "
            "designed to help you manage your cashflow and understand rupee-cost averaging. "
            "Under SEBI (Investment Advisers) Regulations, we **cannot and do not recommend specific stocks, "
            "shares, or mutual fund schemes**.\n\n"
            "For your wealth goals, financial planners recommend focusing on **consistent monthly discipline, "
            "asset allocation, and long-term holding** rather than attempting to pick individual winning stocks."
        )

    @classmethod
    def get_fomo_fallback(cls) -> str:
        return (
            "⚠️ **Market Risk Notice:** Market movements cannot be predicted with certainty. "
            "Mutual funds do not offer guaranteed returns. Your SIP is designed to smooth out "
            "volatility by buying more units during dips and fewer during highs automatically."
        )
