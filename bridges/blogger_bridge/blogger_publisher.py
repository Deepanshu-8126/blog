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

import time
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
    Publishes an article directly to Google Blogger with auto-retry on 429 rate limits.
    
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

    # HARD LOCK: Block expiring telesco.pe mobile preview thumbnails
    if featured_image and "telesco.pe" in featured_image.lower():
        featured_image = None

    # Prepend responsive featured image / emblem
    final_content = content_html
    if featured_image and featured_image.startswith("http") and featured_image not in content_html:
        is_emblem_or_logo = any(k in featured_image.lower() for k in ["logo", "emblem", "seal", "symbol", "badge", "wikimedia"])
        if is_emblem_or_logo:
            img_tag = (
                f'<div class="separator" style="clear: both; text-align: center; margin: 15px auto 25px auto; max-width: 580px; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); padding: 25px 20px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">'
                f'<img border="0" src="{featured_image}" alt="{title}" style="max-height: 180px; max-width: 80%; object-fit: contain; margin: 0 auto; display: block; filter: drop-shadow(0 2px 5px rgba(0,0,0,0.08));" />'
                f'<div style="font-size: 12px; color: #64748b; font-weight: 600; margin-top: 10px; letter-spacing: 0.5px; text-transform: uppercase;">Official Verified Logo & Notice</div>'
                f'</div>\n\n'
            )
        else:
            img_tag = (
                f'<div class="separator" style="clear: both; text-align: center; margin-bottom: 25px;">'
                f'<img border="0" src="{featured_image}" alt="{title}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);" />'
                f'</div>\n\n'
            )
        final_content = img_tag + final_content

    # Append official Telegram & WhatsApp channel community footer if not already present
    if "whatsapp.com/channel" not in final_content:
        is_deals_blog = str(blog_id) == "834082955272949961" or any(l in ["Deals", "Loot", "Offers", "Shopping"] for l in (labels or []))
        is_sarkari_blog = str(blog_id) == "1366151638291560024" or any(l in ["Sarkari Result", "Exams & Results", "Admit Card", "Exam Alert"] for l in (labels or []))

        if is_deals_blog:
            footer_html = (
                f'\n\n<div class="uniquedigit-community-box" style="margin: 40px auto 20px auto; padding: 24px 20px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 16px; border: 1px solid #334155; color: #ffffff; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
                f'<div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin-bottom: 8px;">🔥 Never Miss a 0-Minute Price Glitch!</div>'
                f'<p style="margin: 0 auto 18px auto; max-width: 580px; color: #cbd5e1; font-size: 14px; line-height: 1.6;">Amazon & Flipkart par lightning deals, price errors aur festive loots kuch hi minutes ke liye aate hain. Instant notifications paane ke liye humare official channels join karein:</p>'
                f'<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; margin-bottom: 12px;">'
                f'<a href="https://t.me/uniquedigit_deals" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #0088cc 0%, #006699 100%); color: #ffffff; text-decoration: none; padding: 12px 26px; border-radius: 9999px; font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0,136,204,0.4);">'
                f'✈️ Join Telegram Deals Channel (@uniquedigit_deals)'
                f'</a>'
                f'<a href="https://whatsapp.com/channel/0029Vb90gso4dTnKKpcf7M1E" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #25d366 0%, #128c7e 100%); color: #ffffff; text-decoration: none; padding: 12px 26px; border-radius: 9999px; font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(37,211,102,0.4);">'
                f'🟢 Join WhatsApp Alerts Channel'
                f'</a>'
                f'</div>'
                f'<div style="font-size: 11px; color: #94a3b8; margin-top: 10px;">'
                f'⚡ 100% Verified Deals • Zero Spam • Direct Store Buying Links'
                f'</div>'
                f'</div>\n'
            )
        elif is_sarkari_blog:
            footer_html = (
                f'\n\n<div class="uniquedigit-community-box" style="margin: 40px auto 20px auto; padding: 24px 20px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 16px; border: 1px solid #334155; color: #ffffff; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
                f'<div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin-bottom: 8px;">📢 Sarkari Result & Exam Direct Alerts!</div>'
                f'<p style="margin: 0 auto 18px auto; max-width: 580px; color: #cbd5e1; font-size: 14px; line-height: 1.6;">Admit cards, exam dates, answer keys aur scorecards ki sabse fast updates seedhe apne phone par paayein. Join karein humare official broadcast channels:</p>'
                f'<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; margin-bottom: 12px;">'
                f'<a href="https://t.me/uniquedigit_deals" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #0088cc 0%, #006699 100%); color: #ffffff; text-decoration: none; padding: 12px 26px; border-radius: 9999px; font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0,136,204,0.4);">'
                f'✈️ Telegram Exam & Deal Alerts'
                f'</a>'
                f'<a href="https://whatsapp.com/channel/0029Vb90gso4dTnKKpcf7M1E" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #25d366 0%, #128c7e 100%); color: #ffffff; text-decoration: none; padding: 12px 26px; border-radius: 9999px; font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(37,211,102,0.4);">'
                f'🟢 Join WhatsApp Channel Alert'
                f'</a>'
                f'</div>'
                f'<div style="font-size: 11px; color: #94a3b8; margin-top: 10px;">'
                f'Direct Official Portals • Verified Cutoffs • No Fake News'
                f'</div>'
                f'</div>\n'
            )
        else:
            footer_html = (
                f'\n\n<div class="uniquedigit-community-box" style="margin: 40px auto 20px auto; padding: 24px 20px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 16px; border: 1px solid #334155; color: #ffffff; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif;">'
                f'<div style="font-size: 22px; font-weight: 800; color: #38bdf8; margin-bottom: 8px;">⚡ UniqueDigit Community & Deal Alerts</div>'
                f'<p style="margin: 0 auto 18px auto; max-width: 580px; color: #cbd5e1; font-size: 14px; line-height: 1.6;">Latest AI tools updates, tech guides aur exclusive shopping loots ki real-time notifications paane ke liye join karein:</p>'
                f'<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; margin-bottom: 12px;">'
                f'<a href="https://t.me/uniquedigit_deals" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #0088cc 0%, #006699 100%); color: #ffffff; text-decoration: none; padding: 12px 26px; border-radius: 9999px; font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(0,136,204,0.4);">'
                f'✈️ Join Telegram Alerts Channel'
                f'</a>'
                f'<a href="https://whatsapp.com/channel/0029Vb90gso4dTnKKpcf7M1E" target="_blank" rel="noopener noreferrer" style="background: linear-gradient(135deg, #25d366 0%, #128c7e 100%); color: #ffffff; text-decoration: none; padding: 12px 26px; border-radius: 9999px; font-weight: 700; font-size: 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(37,211,102,0.4);">'
                f'🟢 Join WhatsApp Alerts Channel'
                f'</a>'
                f'</div>'
                f'</div>\n'
            )
        final_content = final_content + footer_html

    # Prepare Blogger API body
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": final_content,
        "labels": labels or ["Trending", "UniqueDigit"]
    }

    max_retries = 2
    for attempt in range(max_retries + 1):
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
            err_str = str(e)
            if ("429" in err_str or "rateLimitExceeded" in err_str or "quota" in err_str.lower()) and attempt < max_retries:
                wait_time = 12 * (attempt + 1)
                print(f"⚠️ [Blogger 429 Quota/Rate Limit]: Waiting {wait_time}s before retry {attempt+1}/{max_retries}...")
                time.sleep(wait_time)
                continue
            print(f"❌ [Blogger Error]: {e}")
            return {"success": False, "error": err_str}

if __name__ == "__main__":
    # Test connection
    s, bid = get_blogger_service()
    if s and bid:
        print(f"✅ Blogger Service Ready! Blog ID: {bid}")
    else:
        print("⚠️ Blogger Service not yet authenticated. Run blogger_auth.py first.")
