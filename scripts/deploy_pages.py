import os, sys, subprocess
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv('d:/affi;ate/.env')

print("[1/2] Deploying d:/affi;ate/dist to Cloudflare Pages...")
res = subprocess.run(
    ["npx", "wrangler", "pages", "deploy", "d:/affi;ate/dist", "--project-name", "uniquedigit-viral-hub"],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    shell=True
)

print(res.stdout)
if res.stderr:
    print("[STDERR]", res.stderr)
print("[EXIT CODE]", res.returncode)
