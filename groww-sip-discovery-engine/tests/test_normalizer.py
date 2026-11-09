import pytest
from discovery_core.schemas import SourceType, InvestorTenure
from discovery_core.normalizer import PIIScrubber, Deduplicator, infer_tenure_hint, normalize_record


def test_pii_scrubber_redacts_indian_pii():
    text = (
        "My phone number is 9876543210 and email is rahul.sharma@gmail.com. "
        "My PAN is ABCDE1234F and bank account 123456789012. Folio no 9876543/21."
    )
    scrubbed = PIIScrubber.scrub(text)
    assert "[REDACTED_PHONE]" in scrubbed
    assert "[REDACTED_EMAIL]" in scrubbed
    assert "[REDACTED_PAN]" in scrubbed
    assert "[REDACTED_ACCOUNT]" in scrubbed
    assert "[REDACTED_FOLIO]" in scrubbed
    assert "9876543210" not in scrubbed
    assert "rahul.sharma@gmail.com" not in scrubbed


def test_deduplicator_filters_duplicates():
    dedup = Deduplicator()
    text1 = "Started SIP 5 months ago, returns are red."
    text2 = "Started SIP 5 months ago, returns are red!"
    text3 = "Different complaint about mandate bounce."

    is_dup1, h1 = dedup.is_duplicate(text1)
    is_dup2, h2 = dedup.is_duplicate(text2)
    is_dup3, h3 = dedup.is_duplicate(text3)

    assert not is_dup1
    assert is_dup2  # text2 is canonical duplicate of text1
    assert not is_dup3


def test_infer_tenure_hint():
    assert infer_tenure_hint("First installment debited") == InvestorTenure.MONTH_1
    assert infer_tenure_hint("Been investing for 2 months") == InvestorTenure.MONTHS_2_3
    assert infer_tenure_hint("Month 5 update on my SIP") == InvestorTenure.MONTHS_4_6
    assert infer_tenure_hint("After 8 months I stopped") == InvestorTenure.MONTHS_7_9
    assert infer_tenure_hint("Completing 1 year of investing") == InvestorTenure.MONTHS_10_12
    assert infer_tenure_hint("Random post without tenure") == InvestorTenure.UNSPECIFIED

