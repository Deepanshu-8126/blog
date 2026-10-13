import sys
import os
import json
import subprocess
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv("d:/affi;ate/.env")
env = os.environ.copy()

def run_d1_query(sql):
    cmd = ["npx", "wrangler", "d1", "execute", "uniquedigit-db", "--remote", "--json", f"--command={sql}"]
    res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", shell=True, env=env, cwd="C:/Users/Deepanshu")
    if res.returncode == 0 and res.stdout:
        idx = res.stdout.find("[")
        if idx != -1:
            data = json.loads(res.stdout[idx:])
            return data[0].get("results", [])
    print("[Error/Output]:", (res.stderr[:300] or res.stdout[:300]))
    return []

if __name__ == "__main__":
    sql = "SELECT p.id, n.slug as niche_slug, p.slug, p.title, p.summary FROM posts p JOIN niches n ON p.niche_id = n.id WHERE p.title LIKE '%reddit%' OR p.summary LIKE '%reddit%' LIMIT 100;"
    posts = run_d1_query(sql)
    print(f"Total matching Reddit posts in D1: {len(posts)}")
    for p in posts:
        print(f"ID {p['id']} [{p['niche_slug']}]: {p['title']}")
