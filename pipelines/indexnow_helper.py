"""
IndexNow Helper Module
Allows any crawler/pipeline to instantly notify Bing and IndexNow search engines
when a new article, deal, or sarkari update is published.
"""
import sys, requests

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

INDEXNOW_HOST = "uniquedigit-viral-hub.pages.dev"
INDEXNOW_KEY = "e8b912c47a504efea389127d40cb91af"
INDEXNOW_KEY_LOCATION = f"https://{INDEXNOW_HOST}/{INDEXNOW_KEY}.txt"

def submit_url_to_indexnow(url_or_urls):
    """
    Submits a URL or list of URLs to IndexNow (Bing, Yandex, Seznam, etc.)
    for instantaneous indexing.
    """
    if isinstance(url_or_urls, str):
        urls = [url_or_urls]
    else:
        urls = list(url_or_urls)

    if not urls:
        return False

    payload = {
        "host": INDEXNOW_HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": INDEXNOW_KEY_LOCATION,
        "urlList": urls[:500]
    }

    try:
        res = requests.post(
            "https://api.indexnow.org/indexnow",
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10
        )
        if res.status_code in (200, 202):
            print(f"[IndexNow OK] Instant indexing queued ({len(urls)} URL(s), HTTP {res.status_code}): {urls[0]}")
            return True
        else:
            print(f"[IndexNow WARN] HTTP {res.status_code}: {res.text[:120]}")
            return False
    except Exception as e:
        print(f"[IndexNow ERR]: {e}")
        return False
