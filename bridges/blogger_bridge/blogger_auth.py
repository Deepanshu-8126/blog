#!/usr/bin/env python3
"""
=============================================================================
GOOGLE BLOGGER 1-CLICK OAUTH AUTHENTICATION & BLOG DISCOVERY
=============================================================================
Connects your Google Cloud credentials, generates permanent refresh tokens,
and auto-discovers your Blog ID.
=============================================================================
"""

import os
import sys
import json
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Set UTF-8
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            getattr(sys.stdout, "reconfigure")(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            getattr(sys.stderr, "reconfigure")(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET", "")

if not CLIENT_ID or not CLIENT_SECRET:
    CLIENT_ID = input("Enter Google Client ID: ").strip()
    CLIENT_SECRET = input("Enter Google Client Secret: ").strip()

SCOPES = ["https://www.googleapis.com/auth/blogger"]
TOKENS_FILE = os.path.join(os.path.dirname(__file__), "tokens.json")

def authenticate():
    print("=" * 65)
    print("🔐 GOOGLE BLOGGER AUTHENTICATION SETUP")
    print("=" * 65)

    client_config = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080/"]
        }
    }

    try:
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    except Exception:
        client_config = {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:8080/"]
            }
        }
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)

    print("\n👉 A browser tab will open automatically.")
    print("👉 Sign in with your Google account and click 'Continue / Allow'.")
    print("👉 If you see 'Google hasn't verified this app', click 'Advanced' -> 'Go to app (unsafe)' to proceed.\n")

    creds = flow.run_local_server(port=8080, prompt="consent", access_type="offline")

    print("\n✅ Authentication successful!")

    # Connect to Blogger API and discover user's blogs
    blogger = build("blogger", "v3", credentials=creds)
    blogs_result = blogger.blogs().listByUser(userId="self").execute()

    items = blogs_result.get("items", [])
    if not items:
        print("⚠️ No Blogger blogs found for this account. Make sure a blog exists at blogger.com!")
        return

    print("\n=======================================================")
    print("🎉 YOUR BLOGGER BLOGS FOUND:")
    print("=======================================================")
    primary_blog = items[0]
    for idx, b in enumerate(items, 1):
        print(f"[{idx}] Name: {b.get('name')}")
        print(f"    ID:   {b.get('id')}")
        print(f"    URL:  {b.get('url')}\n")

    # Save credentials & blog info
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": creds.refresh_token,
        "blog_id": primary_blog.get("id"),
        "blog_name": primary_blog.get("name"),
        "blog_url": primary_blog.get("url")
    }

    with open(TOKENS_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)

    # Also update .env file
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as ef:
            env_content = ef.read()

        def update_or_add_env(key, val, text):
            if f"{key}=" in text:
                return "\n".join([f"{key}={val}" if l.startswith(f"{key}=") else l for l in text.splitlines()])
            return text.rstrip() + f"\n{key}={val}\n"

        env_content = update_or_add_env("BLOGGER_BLOG_ID", primary_blog.get("id"), env_content)
        env_content = update_or_add_env("BLOGGER_CLIENT_ID", CLIENT_ID, env_content)
        env_content = update_or_add_env("BLOGGER_CLIENT_SECRET", CLIENT_SECRET, env_content)
        if creds.refresh_token:
            env_content = update_or_add_env("BLOGGER_REFRESH_TOKEN", creds.refresh_token, env_content)

        with open(env_path, "w", encoding="utf-8") as ef:
            ef.write(env_content)

    print("=======================================================")
    print(f"🔒 Configuration saved to .env & {TOKENS_FILE}")
    print(f"🚀 Primary Blog Locked: {primary_blog.get('name')} (ID: {primary_blog.get('id')})")
    print("=======================================================")
    print("💡 CRITICAL: To prevent this token from expiring in 7 days:")
    print("1. Go to https://console.cloud.google.com/apis/credentials/consent")
    print("2. Under 'Publishing status', click 'PUBLISH APP' (Move from Testing to Production).")
    print("3. Once in Production, Google refresh tokens NEVER expire!")
    print("=======================================================\n")

if __name__ == "__main__":
    authenticate()
