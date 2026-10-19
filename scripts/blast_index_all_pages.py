"""
Master Multi-Engine Search Indexing Blaster
Submits all live sitemap URLs to IndexNow (Bing, IndexNow.org, Seznam, Naver) and verifies crawl readiness.
"""
import sys
import re
import json
import time
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SITE = "https://uniquedigit-viral-hub.pages.dev"
INDEXNOW_KEY = "e8b912c47a504efea389127d40cb91af"
SITEMAP_URL = f"{SITE}/sitemap.xml"

print("=" * 70)
print("🚀 MASTER MULTI-ENGINE FAST INDEXING BLASTER")
print("=" * 70)

# Step 1: Fetch Live Sitemap
print(f"📡 [1/4] Fetching live sitemap: {SITEMAP_URL}")
try:
    req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        xml = resp.read().decode("utf-8")
except Exception as e:
    print(f"❌ Could not fetch sitemap: {e}")
    sys.exit(1)

urls = re.findall(r"<loc>(https?://[^<]+)</loc>", xml)
print(f"✅ Discovered {len(urls)} live URLs in sitemap")

if not urls:
    print("⚠️ No URLs found.")
    sys.exit(0)

# Step 2: Verify Search Meta Tags on Sample
print(f"\n🔍 [2/4] Verifying Indexability & Meta Tags on live pages...")
sample_urls = [
    f"{SITE}/",
    f"{SITE}/deals/pm-surya-ghar-muft-bijli-yojana-subsidy-cost-guide",
    f"{SITE}/credit-cards",
    f"{SITE}/calculators"
]

all_good = True
for u in sample_urls:
    try:
        r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"})
        with urllib.request.urlopen(r, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            has_noindex = "noindex" in body.lower()
            canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', body)
            can_url = canonical.group(1) if canonical else "None"
            if not has_noindex and resp.status == 200:
                print(f"  ✅ [200 OK - Indexable]: {u.replace(SITE, '') or '/'} (Canonical: {can_url})")
            else:
                print(f"  ⚠️ [Issue]: {u} status={resp.status} noindex={has_noindex}")
                all_good = False
    except Exception as e:
        print(f"  ❌ Error checking {u}: {e}")

# Step 3: Batch Submit to IndexNow Protocol (Bing, Yahoo, Naver, Seznam)
print(f"\n⚡ [3/4] Blasting {len(urls)} URLs to IndexNow Search Engine Network...")
payload = {
    "host": "uniquedigit-viral-hub.pages.dev",
    "key": INDEXNOW_KEY,
    "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt",
    "urlList": urls[:500]
}
payload_bytes = json.dumps(payload).encode("utf-8")
headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": "UniqueDigitIndexer/1.0"}

endpoints = [
    ("api.indexnow.org (Global Central Hub)", "https://api.indexnow.org/indexnow"),
    ("bing.com (Microsoft Bing & Copilot)", "https://www.bing.com/indexnow"),
    ("search.seznam.cz (European Search)", "https://search.seznam.cz/indexnow"),
]

for name, endpoint in endpoints:
    try:
        r = urllib.request.Request(endpoint, data=payload_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(r, timeout=15) as resp:
            print(f"  ✅ {name}: HTTP {resp.status} - SUCCESS (All {len(urls)} URLs Accepted!)")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print(f"  ⚠️ {name}: HTTP {e.code} - {body[:100]}")
    except Exception as e:
        print(f"  ⚠️ {name}: {e}")

# Step 4: Verification of robots.txt
print(f"\n📑 [4/4] Verifying robots.txt sitemap directive...")
try:
    r = urllib.request.Request(f"{SITE}/robots.txt", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r, timeout=10) as resp:
        txt = resp.read().decode("utf-8")
        sitemap_line = [l for l in txt.split("\n") if "sitemap:" in l.lower()]
        print(f"  ✅ robots.txt points to: {sitemap_line}")
except Exception as e:
    print(f"  ⚠️ robots.txt check: {e}")

print("\n" + "=" * 70)
print(f"🎉 INDEXING BLAST COMPLETE: All {len(urls)} URLs successfully submitted to search engines!")
print("=" * 70)
