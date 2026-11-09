import re
import hashlib
from typing import Set, Tuple, Optional
from core.schemas import UnifiedSIPRecord, SourceType, InvestorTenure


class PIIScrubber:
    """Regex-based PII scrubber tailored for Indian financial feedback."""

    EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    # Indian phone numbers: +91, 0, or bare 10-digit starting with 6,7,8,9
    PHONE_REGEX = re.compile(r"(?:\+91[-\s]?|0)?[6-9]\d{9}\b")
    # Indian PAN card pattern: 5 uppercase letters, 4 digits, 1 uppercase letter
    PAN_REGEX = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE)
    # Bank Account numbers: 9 to 18 consecutive digits
    ACCOUNT_REGEX = re.compile(r"\b\d{9,18}\b")
    # Folio numbers: common formats e.g. 1234567/89 or 10-12 digits with slash/hyphen
    FOLIO_REGEX = re.compile(r"\bfolio(?:\s+no\.?|\s+number)?\s*[:#-]?\s*[0-9A-Z/-]{6,16}\b", re.IGNORECASE)

    @classmethod
    def scrub(cls, text: str) -> str:
        if not text:
            return ""
        scrubbed = cls.EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
        scrubbed = cls.PHONE_REGEX.sub("[REDACTED_PHONE]", scrubbed)
        scrubbed = cls.PAN_REGEX.sub("[REDACTED_PAN]", scrubbed)
        scrubbed = cls.FOLIO_REGEX.sub("[REDACTED_FOLIO]", scrubbed)
        scrubbed = cls.ACCOUNT_REGEX.sub("[REDACTED_ACCOUNT]", scrubbed)
        return scrubbed.strip()


class Deduplicator:
    """SHA-256 deduplicator based on normalized canonical text."""

    def __init__(self):
        self.seen_hashes: Set[str] = set()

    @staticmethod
    def compute_hash(text: str) -> str:
        # Normalize text for hashing: lowercase, strip punctuation, collapse whitespace
        normalized = re.sub(r"[^\w\s]", "", text.lower())
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def is_duplicate(self, text: str) -> Tuple[bool, str]:
        record_hash = self.compute_hash(text)
        if record_hash in self.seen_hashes:
            return True, record_hash
        self.seen_hashes.add(record_hash)
        return False, record_hash


def infer_tenure_hint(text: str) -> InvestorTenure:
    """Heuristic tenure extractor from raw feedback text."""
    lower = text.lower()
    if re.search(r"\b(?:1st|first)\s+(?:month|installment|instalment)\b", lower) or re.search(r"\bmonth\s+1\b", lower):
        return InvestorTenure.MONTH_1
    if re.search(r"\b(?:2|3|two|three)\s+months?\b", lower) or re.search(r"\bmonth\s+(?:2|3)\b", lower) or re.search(r"\bsecond\s+(?:month|installment)\b", lower):
        return InvestorTenure.MONTHS_2_3
    if re.search(r"\b(?:4|5|6|four|five|six)\s+months?\b", lower) or re.search(r"\bmonth\s+(?:4|5|6)\b", lower) or "half year" in lower or "6m" in lower:
        return InvestorTenure.MONTHS_4_6
    if re.search(r"\b(?:7|8|9|seven|eight|nine)\s+months?\b", lower) or re.search(r"\bmonth\s+(?:7|8|9)\b", lower):
        return InvestorTenure.MONTHS_7_9
    if re.search(r"\b(?:10|11|12|ten|eleven|twelve)\s+months?\b", lower) or re.search(r"\bmonth\s+(?:10|11|12)\b", lower) or "1 year" in lower or "one year" in lower:
        return InvestorTenure.MONTHS_10_12
    if re.search(r"\b(?:2|3|4|5)\s+years?\b", lower):
        return InvestorTenure.YEAR_1_PLUS
    return InvestorTenure.UNSPECIFIED


def normalize_record(
    raw_text: str,
    source: SourceType,
    timestamp: str,
    deduplicator: Deduplicator,
    user_tenure_hint: Optional[InvestorTenure] = None,
    inferred_segment: str = "general_first_timer",
    status: str = "active",
) -> Optional[UnifiedSIPRecord]:
    """Scrub PII, deduplicate, and assemble UnifiedSIPRecord."""
    scrubbed_text = PIIScrubber.scrub(raw_text)
    if not scrubbed_text or len(scrubbed_text) < 15:
        return None

    is_dup, record_hash = deduplicator.is_duplicate(scrubbed_text)
    if is_dup:
        return None

    tenure = user_tenure_hint or infer_tenure_hint(scrubbed_text)

    return UnifiedSIPRecord(
        record_id=f"rec_{record_hash[:12]}",
        source=source,
        timestamp=timestamp,
        raw_text=scrubbed_text,
        user_tenure_hint=tenure,
        inferred_segment=inferred_segment,
        status=status,
    )
