import sys
import os
import re
import json
import subprocess
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv("d:/affi;ate/.env")
env = os.environ.copy()

UPDATES = {
    "4b5e00ea-372c-4aab-9a22-1d72da03ae0b": {
        "title": "'Am I Insane to Leave Rs 95 LPA Job at 23?': The Great Tech Salary vs Mental Health Dilemma Decoded",
        "summary": "A viral career confession about walking away from a lucrative Rs 95 LPA package has ignited a nationwide debate on corporate burnout, tax reality, and long-term career stability."
    },
    "d8a88350-f1ac-43d4-911f-472742c31cd2": {
        "title": "JEE Main 2026 Expected Result Schedule: Student Grievances, Ground Reality & Official NTA Advisory",
        "summary": "Analysis of JEE Main 2026 result timelines, addressing student concerns over delays, server readiness, and category-wise expected percentile cutoffs."
    },
    "574ace01-3006-4b45-b7ca-ef966e7182b6": {
        "title": "Laid Off After 10 Years? How a Senior Professional Secured a Rs 1.5 Cr Global Remote Role Using Modern AI Stack",
        "summary": "Discover the exact AI portfolio, automated skill matching, and mock interview tools leveraged to land a high-compensation global remote contract from India."
    },
    "ed6e4a2c-cd68-4b6d-b042-04343960d5a2": {
        "title": "7 Essential Audience Intelligence Tools for 2026: AI-Powered Social Listening for Indian Creators",
        "summary": "Discover 7 AI-powered audience intelligence and social listening platforms for 2026 to extract high-intent search queries and trend signals for creators."
    },
    "95fc10f8-beb5-490d-9667-439fe67490fb": {
        "title": "Gen Z’s Festive Shopping Playbook 2026: Smart Price-Glitch Tracking, Card Stacking & Real Steal Deals",
        "summary": "Discover how modern digital shoppers maximize festive sales across top platforms using automated price trackers, coupon stacking, and zero-mark-up hacks."
    },
    "70a11d48-e30f-4a41-9e89-76af9b57016b": {
        "title": "The Truth Behind the 90% Food App Discount: How Viral Stacking Codes Actually Work",
        "summary": "Investigating the viral claims of 90% savings on food delivery platforms: breaking down restaurant partner coupons, payment gateway perks, and real savings."
    },
    "4bcb32d6-3371-4a52-af6a-b122aa1bf07a": {
        "title": "The Indian Founder's Software Playbook: Top High-ROI SaaS Deals & Cloud Tool Stacks for 2026",
        "summary": "A comprehensive curation of essential small business software discounts, lifetime cloud licenses, and billing solutions tailored for Indian startup founders."
    },
    "50b3880a-21cc-4cf6-baf0-1cd9e67d0be1": {
        "title": "From Web Fiction to Hollywood Hits: Top Adapted Stories & Best Budget E-Reader Stacks",
        "summary": "Explore the most gripping web fiction series successfully optioned for major films, paired with smart subscription guides and e-reader discounts."
    },
    "d49d9798-6b7d-4942-a081-62f6240f55dc": {
        "title": "Beyond Board Exam Scores: Transforming 50s Percentage Into High-Paying Tech & Design Careers",
        "summary": "Why board percentages don't define your future: real-world career roadmaps in tech, product design, and digital media for students navigating exam pressure."
    },
    "af525663-1619-4644-8907-b5cfb4862990": {
        "title": "Online Cart Glitches & Checkout Drops: Why Smart Shoppers Need Real-Time Cash Tracking Tools",
        "summary": "When major e-commerce nodes experience server throttling, learn how automated price-drop trackers and browser extensions ensure you never miss cashback savings."
    },
    "4882385a-70d7-464e-bac3-474bc9701c5b": {
        "title": "Comprehensive Clinical Review of 400,000 Patient Logs on GLP-1: Side Effects & Indian Dietary Protocols",
        "summary": "Analyzing long-term user experiences on GLP-1 weight-loss medications: identifying reported side effects and examining sustainable, balanced Indian nutritional alternatives."
    },
    "87db3cba-aece-4b87-b634-7d2203b297cd": {
        "title": "Modern Men's Style Playbook 2026: Everyday Wardrobe Mistakes Indian Women Notice & How to Upgrade",
        "summary": "Upgrade your daily wardrobe: timeless sartorial rules covering tailoring, breathable fabrics, and versatile footwear designed for the modern Indian man."
    },
    "d1fec7e6-4d46-49d4-b59c-6578d39ea90b": {
        "title": "Metro Living on a Rs 30,000 Budget: Bengaluru Cost Blueprint & High-Protein Meal Prep Strategy",
        "summary": "How young professionals can comfortably thrive in Bengaluru on a Rs 30,000 monthly income: practical rent splits, commute hacks, and a nutritious home-cooked meal plan."
    },
    "be9b4660-39d3-4d04-b8ba-170ca94bd816": {
        "title": "Educational Search Engine Optimization 2026: How Indian Exam Portals Can Recover Organic Visibility",
        "summary": "Deep dive into search engine ranking shifts for government exam queries in India, and how independent educational publishers can reclaim organic authority."
    },
    "f6fc0b32-e7e2-4fc4-9755-ab7b5e44cdbc": {
        "title": "API Access Shifts & Feed Lockdowns: How Indian Indie Developers Can Build Resilient AI Data Pipelines",
        "summary": "As major public forums and platforms restrict RSS and open endpoints, here is how indie developers and data engineers can maintain robust news and trend pipelines."
    },
    "69d3966e-dba0-481f-a748-041f9997e834": {
        "title": "Workplace Protections in Food & Hospitality: Legal Rights, Notice Norms & Restaurant Best Practices",
        "summary": "Understanding essential labor standards, trial period regulations, and fair treatment protocols for restaurant staff, alongside an authentic homestyle cooking masterclass."
    },
    "b017b936-af89-4d88-987c-e127c895f94e": {
        "title": "From Web Forums to Silver Screen: 5 Viral Internet Fiction Stories That Landed Major Studio Deals",
        "summary": "How crowdsourced digital fiction captivated Hollywood producers: a breakdown of 5 acclaimed web-origin stories adapted into must-watch feature films."
    }
}

sql_file = "C:/Users/Deepanshu/cleanup_reddit.sql"
statements = []
for pid, data in UPDATES.items():
    t_esc = data["title"].replace("'", "''")
    s_esc = data["summary"].replace("'", "''")
    statements.append(f"UPDATE posts SET title = '{t_esc}', summary = '{s_esc}' WHERE id = '{pid}';")

with open(sql_file, "w", encoding="utf-8") as f:
    f.write("\n".join(statements) + "\n")

print(f"Wrote {len(statements)} update statements to {sql_file}")

# Execute via wrangler --file
cmd = ["npx", "wrangler", "d1", "execute", "uniquedigit-db", "--remote", f"--file={sql_file}"]
res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", shell=True, env=env, cwd="C:/Users/Deepanshu")
print("Return code:", res.returncode)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
