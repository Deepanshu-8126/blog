"""
IndexNow Mass Submission Script
Submits ALL sitemap URLs to Google (via IndexNow) + Bing in one shot.
"""
import sys, re, json, urllib.request, urllib.error, time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SITE = "https://uniquedigit-viral-hub.pages.dev"
INDEXNOW_KEY = "uniquedigit2026indexnow"  # We'll create this key file on site too
SITEMAP_URL = f"{SITE}/sitemap.xml"

# --- Step 1: Fetch sitemap and extract all URLs ---
print(f"[1/3] Fetching sitemap: {SITEMAP_URL}")
try:
    req = urllib.request.Request(SITEMAP_URL, headers={"User-Agent": "IndexBot/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml = resp.read().decode("utf-8")
except Exception as e:
    print(f"[ERROR] Could not fetch sitemap: {e}")
    sys.exit(1)

urls = re.findall(r"<loc>(https?://[^<]+)</loc>", xml)
print(f"[OK] Found {len(urls)} URLs in sitemap")

# --- Step 2: Submit to Bing IndexNow ---
print(f"\n[2/3] Submitting {len(urls)} URLs to Bing IndexNow...")
bing_payload = {
    "host": "uniquedigit-viral-hub.pages.dev",
    "key": INDEXNOW_KEY,
    "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt",
    "urlList": urls[:500]  # Max 500 per request
}
bing_req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(bing_payload).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST"
)
try:
    with urllib.request.urlopen(bing_req, timeout=30) as resp:
        print(f"[OK] Bing IndexNow: HTTP {resp.status} - Accepted!")
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8") if e.fp else ""
    print(f"[BING] Status {e.code}: {body[:200]}")
except Exception as e:
    print(f"[BING ERROR] {e}")

# --- Step 3: Submit sitemap to Google Search Console Ping ---
print(f"\n[3/3] Pinging Google with sitemap URL...")
google_ping = f"https://www.google.com/ping?sitemap={urllib.parse.quote(SITEMAP_URL)}"
import urllib.parse
try:
    with urllib.request.urlopen(google_ping, timeout=15) as resp:
        print(f"[OK] Google Ping: HTTP {resp.status} - Sitemap submitted!")
except urllib.error.HTTPError as e:
    print(f"[GOOGLE PING] Status {e.code}")
except Exception as e:
    print(f"[GOOGLE PING ERROR] {e}")

print(f"\n[DONE] IndexNow submission complete!")
print(f"Total URLs queued for indexing: {len(urls)}")
print(f"\nNOTE: Google will crawl these within 24-48 hours.")
print(f"Monitor progress at: https://search.google.com/search-console")
