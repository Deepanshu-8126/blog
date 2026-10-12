#!/usr/bin/env python3
"""
=============================================================================
GOOGLE BLOGGER V3 PRODUCTION PUBLISHER MODULE
=============================================================================
Takes humanized articles with HD images and publishes them directly to Blogger
via official Google Blogger API v3 (0% Ban Risk, 50,000 Quota/Day, Unlimited).
=============================================================================
"""

import os
import sys
import json
import requests

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            getattr(sys.stdout, "reconfigure")(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            getattr(sys.stderr, "reconfigure")(encoding="utf-8")
    except Exception:
        pass

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

TOKENS_FILE = os.path.join(os.path.dirname(__file__), "tokens.json")

def get_blogger_service():
    """Builds an authenticated Google Blogger API client using refresh token."""
    client_id = os.getenv("BLOGGER_CLIENT_ID", "")
    client_secret = os.getenv("BLOGGER_CLIENT_SECRET", "")
    refresh_token = os.getenv("BLOGGER_REFRESH_TOKEN", "")
    blog_id = os.getenv("BLOGGER_BLOG_ID", "")

    # Fallback to tokens.json if not in .env
    if not refresh_token and os.path.exists(TOKENS_FILE):
        try:
            with open(TOKENS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                client_id = client_id or data.get("client_id")
                client_secret = client_secret or data.get("client_secret")
                refresh_token = refresh_token or data.get("refresh_token")
                blog_id = blog_id or data.get("blog_id")
        except Exception:
            pass

    if not refresh_token or not client_id or not client_secret:
        return None, None

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/blogger"]
    )

    # Refresh token if needed
    if not creds.valid:
        creds.refresh(Request())

    service = build("blogger", "v3", credentials=creds)
    return service, blog_id

def publish_to_blogger(title, content_html, labels=None, is_draft=False, featured_image=None, target_blog_id=None):
    """
    Publishes an article directly to Google Blogger.
    
    Args:
        title (str): Post title.
        content_html (str): Complete rich HTML content with subheadings & images.
        labels (list): Category tags (e.g. ['Tech', 'Deals', 'India']).
        is_draft (bool): True to save as draft, False to publish immediately.
        featured_image (str): Optional top image URL to prepend.
        target_blog_id (str): Optional blog ID override to target specific niche blogs.
    
    Returns:
        dict: Result with post ID and live Blogger URL.
    """
    service, default_blog_id = get_blogger_service()
    blog_id = target_blog_id or default_blog_id
    if not service or not blog_id:
        return {"success": False, "error": "Blogger credentials not configured or incomplete"}

    # HARD LOCK: Block pollinations.ai or AI-generated cartoon images
    if featured_image and "pollinations.ai" in featured_image.lower():
        featured_image = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=1200&h=630&fit=crop"

    # Prepend responsive featured image if provided
    final_content = content_html
    if featured_image and featured_image.startswith("http") and featured_image not in content_html:
        img_tag = (
            f'<div class="separator" style="clear: both; text-align: center; margin-bottom: 25px;">'
            f'<img border="0" src="{featured_image}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" />'
            f'</div>\n\n'
        )
        final_content = img_tag + final_content

    # Prepare Blogger API body
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": final_content,
        "labels": labels or ["Trending", "UniqueDigit"]
    }

    try:
        post = service.posts().insert(
            blogId=blog_id,
            body=body,
            isDraft=is_draft
        ).execute()

        post_url = post.get("url", "")
        post_id = post.get("id", "")
        print(f"🎉 [Blogger Published]: {title} -> {post_url}")
        return {
            "success": True,
            "post_id": post_id,
            "url": post_url
        }
    except Exception as e:
        print(f"❌ [Blogger Error]: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Test connection
    s, bid = get_blogger_service()
    if s and bid:
        print(f"✅ Blogger Service Ready! Blog ID: {bid}")
    else:
        print("⚠️ Blogger Service not yet authenticated. Run blogger_auth.py first.")
