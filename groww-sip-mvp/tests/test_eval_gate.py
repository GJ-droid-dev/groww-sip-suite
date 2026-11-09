import pytest
from mvp_core.eval_gate import EvalGate


def test_eval_gate_passes_clean_cashflow_query():
    verdict = EvalGate.evaluate("My company delayed salary to the 8th, can I snooze my debit?")
    assert verdict.passed
    assert not verdict.violation_detected
    assert verdict.safety_score == 1.0


def test_eval_gate_intercepts_stock_advice_request():
    verdict = EvalGate.evaluate("Which stock should I buy for 20% return? Should I buy Tata Motors?")
    assert not verdict.passed
    assert verdict.violation_detected
    assert verdict.violation_type == "STOCK_ADVICE_REQUEST"
    assert verdict.safe_fallback_used


def test_eval_gate_intercepts_fomo_urgency():
    verdict = EvalGate.evaluate("Market crash tomorrow, buy before it skyrockets for guaranteed 30% returns!")
    assert not verdict.passed
    assert verdict.violation_detected
    assert verdict.violation_type == "URGENCY_FOMO"
    assert verdict.safe_fallback_used


def test_eval_gate_fallback_messages_are_informative():
    advice_fb = EvalGate.get_advice_refusal_fallback()
    assert "SEBI" in advice_fb
    assert "cannot and do not recommend specific stocks" in advice_fb

    fomo_fb = EvalGate.get_fomo_fallback()
    assert "Market movements cannot be predicted" in fomo_fb

