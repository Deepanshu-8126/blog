"""
========================================================================================
🚀 REAL-TIME SEARCH INTENT & AUTOCOMPLETE ENGINE (India High-Volume Intent Hunter)
========================================================================================
Bypasses broken wire feeds and random foreign trends (like Mexican football or obscure news).
Directly extracts what 50 Crore Indians are typing into Google Search right now!
Uses:
- Real Google Search Autocomplete API (gl=in, hl=hi/en)
- Curated High-Volume Indian Seed Matrix across all niches:
  * Sarkari Results, Admit Cards, Cutoffs & Recruitment
  * Welfare Yojanas, Scholarships, DBT & Subsidies
  * Tech, 5G Mobiles, Laptops & Buying Guides
  * Personal Finance, Zero-Balance Accounts & Credit Cards
========================================================================================
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

# High-Intent Seed Matrices (Top Search Demands in India)
HIGH_INTENT_SEEDS = {
    "sarkari": [
        "sarkari result 2026",
        "up police constable re exam",
        "admit card 2026 download",
        "ssc gd answer key 2026",
        "ctet admit card 2026",
        "rrb alp exam date 2026",
        "up board time table 2026",
        "neet ug 2026 application form",
        "bteup result 2026 odd semester",
        "railway group d vacancy 2026",
        "kumaun university admit card",
        "ccsu exam date sheet 2026"
    ],
    "yojanas": [
        "pm kisan beneficiary status 2026",
        "pm surya ghar yojana apply online",
        "ladli behna yojana 2026 list",
        "free silai machine yojana online form",
        "ayushman card online apply download",
        "up scholarship status check 2026",
        "subhash chandra bose scholarship 2026",
        "ration card new list 2026 check"
    ],
    "finance": [
        "best lifetime free credit card without income proof",
        "best zero balance savings account online open 2026",
        "sbi cashback credit card apply online",
        "kotak 811 account opening without video kyc"
    ],
    "tech": [
        "best 5g phone under 15000 in 2026",
        "best 5g gaming phone under 20000",
        "best student laptop under 40000",
        "best anc tws earbuds under 2000"
    ]
}

def fetch_google_autocomplete(query: str, lang: str = "hi", gl: str = "in") -> list:
    """
    Fetches real-time suggestions that Indian users actually see in the Google Search Bar.
    """
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://suggestqueries.google.com/complete/search?client=chrome&hl={lang}&gl={gl}&q={encoded}"
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if len(data) > 1 and isinstance(data[1], list):
                # Clean and filter queries
                results = []
                for item in data[1]:
                    clean = item.strip()
                    # Filter out raw URLs or junk
                    if len(clean) >= 8 and not clean.startswith("http") and not clean.startswith("www."):
                        results.append(clean)
                return results
    except Exception as e:
        pass
    return []

def get_high_intent_search_topics(category="sarkari", max_topics=5) -> list:
    """
    Returns curated, high-velocity search queries matching genuine Indian user demand.
    Each topic includes:
      - search_keyword: The exact phrase people type into Google
      - entity: Detected board / department / product
      - intent: admit_card | result | yojana | tech | finance
      - official_portal: Official portal URL (if known)
    """
    seeds = HIGH_INTENT_SEEDS.get(category, HIGH_INTENT_SEEDS["sarkari"])
    all_suggestions = []
    seen = set()

    # Authority and portal mapping
    PORTAL_MAP = {
        "up police": ("Uttar Pradesh Police Recruitment Board (UPPRPB)", "https://uppbpb.gov.in"),
        "pm kisan": ("PM Kisan Samman Nidhi Portal", "https://pmkisan.gov.in"),
        "pm surya ghar": ("PM Surya Ghar National Portal", "https://pmsuryaghar.gov.in"),
        "ssc": ("Staff Selection Commission (SSC)", "https://ssc.gov.in"),
        "ctet": ("Central Teacher Eligibility Test (CTET)", "https://ctet.nic.in"),
        "uptet": ("Uttar Pradesh Teacher Eligibility Test (UPTET)", "https://updeled.gov.in"),
        "up board": ("Uttar Pradesh Madhyamik Shiksha Parishad (UPMSP)", "https://upmsp.edu.in"),
        "mp board": ("Madhya Pradesh Board of Secondary Education (MPBSE)", "https://mpbse.nic.in"),
        "bteup": ("Board of Technical Education UP", "https://bteup.ac.in"),
        "ladli behna": ("Ladli Behna Yojana Portal MP", "https://cmladlibehna.mp.gov.in"),
        "silai machine": ("PM Vishwakarma Yojana Free Silai Machine", "https://pmvishwakarma.gov.in"),
        "ayushman": ("National Health Authority (Ayushman Bharat)", "https://beneficiary.nha.gov.in"),
        "up scholarship": ("UP Scholarship Official Portal", "https://scholarship.up.gov.in"),
        "rrb": ("Railway Recruitment Board (RRB)", "https://indianrailways.gov.in"),
        "railway": ("Railway Recruitment Board (RRB)", "https://indianrailways.gov.in"),
        "group d": ("Railway Recruitment Cell (RRC Group D)", "https://indianrailways.gov.in"),
        "neet": ("National Testing Agency (NEET)", "https://exams.nta.ac.in/NEET"),
        "jee": ("National Testing Agency (JEE)", "https://jeemain.nta.ac.in"),
        "upsc": ("Union Public Service Commission (UPSC)", "https://upsc.gov.in"),
        "ibps": ("Institute of Banking Personnel Selection (IBPS)", "https://ibps.in"),
        "lucknow university": ("University of Lucknow", "https://lkouniv.ac.in"),
        "kumaun": ("Kumaun University Nainital", "https://kunainital.ac.in"),
        "ccsu": ("Chaudhary Charan Singh University Meerut", "https://ccsuniversity.ac.in")
    }

    for seed in seeds:
        suggestions = fetch_google_autocomplete(seed, lang="hi")
        if not suggestions:
            suggestions = fetch_google_autocomplete(seed, lang="en")
        
        for s in suggestions:
            lower = s.lower()
            if lower not in seen:
                seen.add(lower)
                
                # Determine entity and portal
                matched_entity = "Sarkari Central Portal"
                matched_portal = "https://uniquedigit-viral-hub.pages.dev"
                for key, (ent, portal) in PORTAL_MAP.items():
                    if key in lower:
                        matched_entity = ent
                        matched_portal = portal
                        break
                
                # Determine intent with correct precedence (Vacancy BEFORE Result)
                if any(w in lower for w in ["vacancy", "bharti", "recruitment", "online form", "notification"]):
                    intent = "Recruitment / Bharti"
                elif any(w in lower for w in ["admit card", "hall ticket", "roll number"]):
                    intent = "Admit Card"
                elif any(w in lower for w in ["answer key", "response sheet"]):
                    intent = "Answer Key"
                elif any(w in lower for w in ["time table", "date sheet", "exam date"]):
                    intent = "Exam Schedule"
                elif any(w in lower for w in ["result", "scorecard", "merit list", "cutoff"]):
                    intent = "Result / Cutoff"
                elif any(w in lower for w in ["beneficiary status", "kist", "subsidy", "list", "apply"]):
                    intent = "Yojana & Scheme"
                elif any(w in lower for w in ["credit card", "zero balance", "account opening"]):
                    intent = "Banking & Finance"
                else:
                    intent = "Sarkari Alert"

                all_suggestions.append({
                    "search_keyword": s,
                    "entity": matched_entity,
                    "portal": matched_portal,
                    "intent": intent,
                    "source": "Google Autocomplete (High Volume Search Intent)"
                })

    # Return top unique topics up to max_topics
    return all_suggestions[:max_topics]

if __name__ == "__main__":
    topics = get_high_intent_search_topics("sarkari", max_topics=6)
    print(f"✅ Extracted {len(topics)} High-Volume Search Intent Topics:")
    for t in topics:
        print(f"  📌 Keyword: '{t['search_keyword']}'")
        print(f"     Entity: {t['entity']} | Intent: {t['intent']} | Portal: {t['portal']}\n")
