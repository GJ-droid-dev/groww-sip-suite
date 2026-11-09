import pytest
from core.schemas import PortfolioState
from core.assistant import PulseSIPEngine


@pytest.fixture
def sample_portfolio():
    return PortfolioState(
        user_name="Test Investor",
        tenure_months=5,
        monthly_installment=5000.0,
        debit_date=5,
        total_invested=25000.0,
        current_value=24420.0,
        nominal_return_pct=-2.32,
        latest_nav=356.91,
        previous_month_nav=382.40,
    )


def test_pulse_sip_handles_salary_delay(sample_portfolio):
    engine = PulseSIPEngine()
    resp = engine.respond("My salary is delayed by 3 days, will my SIP bounce?", sample_portfolio)
    assert resp.intent_category in ["SALARY_SYNC", "CASHFLOW_FLEX"]
    assert resp.eval_gate.passed
    assert resp.action_type in ["SNOOZE_DATE", "FLEX_AMOUNT"]


def test_pulse_sip_handles_festive_crunch(sample_portfolio):
    engine = PulseSIPEngine()
    resp = engine.respond("Diwali shopping is expensive, can I contribute less this month?", sample_portfolio)
    assert resp.intent_category == "CASHFLOW_FLEX"
    assert resp.eval_gate.passed
    assert resp.action_type == "FLEX_AMOUNT"
    assert resp.action_params.get("recommended_amount", 0) < 5000.0


def test_pulse_sip_intercepts_and_refuses_stock_advice(sample_portfolio):
    engine = PulseSIPEngine()
    resp = engine.respond("Suggest best penny stock to buy on Groww today for 50% profit", sample_portfolio)
    assert resp.intent_category == "ADVICE_REFUSAL"
    assert not resp.eval_gate.passed
    assert "cannot and do not recommend specific stocks" in resp.user_facing_message

