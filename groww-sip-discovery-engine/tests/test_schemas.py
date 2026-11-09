import pytest
from discovery_core.schemas import (
    FailureCategory,
    SourceType,
    InvestorTenure,
    UnifiedSIPRecord,
    AnalysisResult,
    CognitiveProfile,
    CATEGORY_LABELS,
)


def test_failure_categories_exist():
    assert len(FailureCategory) == 7
    for cat in FailureCategory:
        assert cat in CATEGORY_LABELS


def test_unified_record_validation():
    rec = UnifiedSIPRecord(
        record_id="rec_test123",
        source=SourceType.PLAY_STORE,
        timestamp="2026-10-01",
        raw_text="Test complaint about mandate bounce",
        user_tenure_hint=InvestorTenure.MONTH_1,
        inferred_segment="salaried_early_career",
        status="stopped",
    )
    assert rec.record_id == "rec_test123"
    assert rec.source == SourceType.PLAY_STORE
    assert rec.status == "stopped"


def test_analysis_result_validation():
    profile = CognitiveProfile(
        initial_motivation="Compounding wealth",
        expectation_delta="Negative nominal return",
        primary_anxiety="Loss aversion",
        coping_behavior="Cancelled SIP",
    )
    result = AnalysisResult(
        record_id="rec_test123",
        is_relevant=True,
        relevance_rationale="Relevant first-timer feedback",
        primary_category=FailureCategory.RETURN_ILLUSION_DISILLUSION,
        category_confidence=0.92,
        cognitive_profile=profile,
        churn_imminence_score=4,
        product_solvability_score=4,
        key_quote="Returns are red after 5 months",
        product_opportunity="Rupee-Cost Averaging Visualizer",
    )
    assert result.is_relevant
    assert result.primary_category == FailureCategory.RETURN_ILLUSION_DISILLUSION
    assert result.churn_imminence_score == 4

