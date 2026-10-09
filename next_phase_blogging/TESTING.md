# Testing Protocol & Zero-Regression Verification Spec

**Document:** `next_phase_blogging/TESTING.md`  
**Purpose:** Pre-Flight & Continuous Quality Assurance Suite for UniqueDigit Media Platform  
**Target:** 100% Zero-Regression, Zero Broken Images, Zero Silent Pipeline Failures

---

## 1. Automated Test Suite Overview

Every production build and autonomous pipeline execution must pass four validation gates:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        QUALITY ASSURANCE GATES                         │
├─────────────────┬──────────────────┬─────────────────┬────────────────┤
│ Gate 1: Code &  │ Gate 2: Media &  │ Gate 3: Ingest  │ Gate 4: Edge   │
│ TypeScript      │ Image 200 Assert │ Deduplication   │ Caching        │
├─────────────────┼──────────────────┼─────────────────┼────────────────┤
│ • astro check   │ • HEAD HTTP 200  │ • Levenshtein   │ • /img proxy   │
│ • npm run build │ • Aspect Ratio   │ • Safe Content  │ • Cloudflare   │
│ • Zero Warnings │ • No 429/404s    │ • Category Tag  │   Cache HIT    │
└─────────────────┴──────────────────┴─────────────────┴────────────────┘
```

---

## 2. Gate 1: Build & Type Integrity

Executed before any deployment commit:
```bash
# 1. Astro Syntax & Type Check
npx astro check

# 2. Production SSR Server Compilation
npm run build
```
* **Success Criteria:** Exit code `0`. Zero TypeScript diagnostic errors. Server bundle compiled in under 5.0 seconds.

---

## 3. Gate 2: Automated Media & HTTP 200 Assertions

Every image ingested by the pipeline or listed in `CATEGORY_FALLBACK_IMAGES` is verified using a Python test harness:

```python
# tests/test_images.py
import urllib.request

IMAGE_TARGETS = [
    "https://upload.wikimedia.org/wikipedia/en/d/d9/Drishyam-_The_Conclusion_poster.jpg",
    "https://upload.wikimedia.org/wikipedia/en/a/a1/Stree_2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/e/ef/Tradtional_Thali.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/2a/Credit_Card_Chip_%2834684294971%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/b/b0/Beach_asana_class%2C_Plage_Pereire%2C_Arcachon%2C_2015.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/3f/AMD_Ryzen_7_1800X.jpg"
]

def test_remote_images_status():
    headers = {"User-Agent": "UniqueDigitBot/2.0 (contact: info@uniquedigit.in)"}
    for url in IMAGE_TARGETS:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as res:
            assert res.status == 200, f"Failed image URL: {url}"
            content_type = res.headers.get("Content-Type", "")
            assert "image" in content_type, f"Non-image MIME type {content_type} for {url}"
            print(f"✅ Verified: {url[:60]}... ({content_type})")

if __name__ == "__main__":
    test_remote_images_status()
```

---

## 4. Gate 3: Deduplication & Relevancy Engine Test

Validates that Agent Alpha rejects duplicate and near-duplicate trending stories:

```python
# tests/test_dedup.py
import re

def compute_similarity(q1: str, q2: str) -> float:
    w1 = set(re.findall(r'[a-zA-Z0-9]+', q1.lower()))
    w2 = set(re.findall(r'[a-zA-Z0-9]+', q2.lower()))
    if not w1 or not w2:
        return 0.0
    return len(w1.intersection(w2)) / len(w1.union(w2))

def test_dedup_rejection():
    existing = "Drishyam 3: The Conclusion Box Office Collection Nears 400 Crore Worldwide"
    duplicate_candidate = "Drishyam 3 Box Office Collection Hits 400 Crore"
    novel_candidate = "IPL 2026 Mega Auction Live Team Updates"

    assert compute_similarity(existing, duplicate_candidate) > 0.40, "Deduplication similarity trigger failed"
    assert compute_similarity(existing, novel_candidate) < 0.10, "False positive deduplication on novel topic"
    print("✅ Deduplication logic verified.")

if __name__ == "__main__":
    test_dedup_rejection()
```

---

## 5. Gate 4: Edge Proxy Caching & Fallback Redirection

Tests the Cloudflare Worker `/img?url=` route:
1. **Valid Image Request:**
   * Input: `/img?url=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fen%2Fd%2Fd9%2FDrishyam-_The_Conclusion_poster.jpg`
   * Assertion: HTTP `200 OK`, `Cache-Control: public, max-age=604800, s-maxage=2592000, immutable`, `Content-Type: image/jpeg`.
2. **Invalid / 404 Image Request:**
   * Input: `/img?url=https%3A%2F%2Fupload.wikimedia.org%2Fnonexistent_asset_404.jpg`
   * Assertion: HTTP `302 Found` redirecting directly to `/images/ai_tools.jpg` (or designated category fallback). **Zero 500/502 error codes returned to browser.**

---

## 6. Pre-Commit Checklist

Before pushing any feature branch or workflow update:
- [x] Run `npm run build` locally.
- [x] Verify YAML syntax in `.github/workflows/daily.yml` with quoted `'on':`.
- [x] Run `python -m pytest` or run test harnesses.
- [x] Assert all modified cards feature both ambient blur backdrop and `object-contain` foreground.
- [x] Verify that legal affiliate disclosure is present on all template outputs.
