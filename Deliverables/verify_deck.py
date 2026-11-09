import os
import sys
import pymupdf

def audit_presentation_pdf(pdf_path):
    print("=" * 60)
    print("AUDITING GROWW CAPSTONE PRESENTATION DECK")
    print(f"Path: {pdf_path}")
    print("=" * 60)

    if not os.path.exists(pdf_path):
        print(f"FAIL: File does not exist: {pdf_path}")
        return False

    file_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"File Size: {file_size_mb:.2f} MB (Limit: < 40.0 MB)")
    if file_size_mb >= 40.0:
        print("FAIL: File size exceeds 40 MB!")
        return False

    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    print(f"Total Slides: {total_pages} (Requirement: Exactly 10)")
    if total_pages != 10:
        print(f"FAIL: Expected 10 slides, got {total_pages}!")
        return False

    # Check metadata for anonymity
    meta = doc.metadata
    print(f"Metadata Author: {meta.get('author')}")
    print(f"Metadata Title:  {meta.get('title')}")

    # Fellow names to check for (e.g. user OS name 'jangr', or fellow personal names)
    banned_terms = ["jangr", "fellow name", "student name"]
    violations = []
    font_issues = []

    for page_idx in range(total_pages):
        page = doc[page_idx]
        text_page = page.get_text("dict")
        blocks = text_page.get("blocks", [])

        slide_texts = []
        for b in blocks:
            if b.get("type") == 0: # text block
                for line in b.get("lines", []):
                    for span in line.get("spans", []):
                        txt = span.get("text", "").strip()
                        size = span.get("size", 0.0)
                        if txt:
                            slide_texts.append((txt, size))
                            # Check font size floor: strict >= 13.9pt (allow 0.1 rounding margin for PDF transforms)
                            if size < 13.5:
                                font_issues.append((page_idx + 1, txt, size))
                            # Check anonymity
                            for banned in banned_terms:
                                if banned.lower() in txt.lower():
                                    violations.append((page_idx + 1, banned, txt))

        print(f"Slide {page_idx + 1:2d}: {len(slide_texts)} text spans checked. Min font size on slide: {min((s[1] for s in slide_texts), default=0):.1f} pt")

    print("-" * 60)
    passed = True
    if violations:
        print(f"FAIL: Found {len(violations)} anonymity violations:")
        for v in violations:
            print(f"  Slide {v[0]}: banned term '{v[1]}' in '{v[2]}'")
        passed = False
    else:
        print("PASS: 100% Anonymous (No banned author/fellow names detected)")

    if font_issues:
        print(f"FAIL: Found {len(font_issues)} text spans with font size < 14pt:")
        for issue in font_issues[:10]:
            print(f"  Slide {issue[0]}: size={issue[2]:.1f}pt text='{issue[1]}'")
        passed = False
    else:
        print("PASS: Strictly >= 14pt across all text spans on all 10 slides")

    print("-" * 60)
    if passed:
        print("OVERALL VERDICT: ALL AUDIT CHECKS PASSED SUCCESSFULLY! (10/10)")
    else:
        print("OVERALL VERDICT: AUDIT FAILED - PLEASE FIX ISSUES ABOVE")
    print("=" * 60)
    return passed

if __name__ == "__main__":
    pdf_file = "c:/Users/jangr/Documents/NextLeap/Project/Project2/Deliverables/NL_Groww.pdf"
    success = audit_presentation_pdf(pdf_file)
    sys.exit(0 if success else 1)

