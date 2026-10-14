import os, sys, glob, re

sys.stdout.reconfigure(encoding='utf-8')

workflow_files = glob.glob('.github/workflows/*.yml')
print(f"Found {len(workflow_files)} workflow files in .github/workflows:")

for wf in workflow_files:
    print(f"\n--- Checking: {wf} ---")
    with open(wf, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check basic structure
    has_name = bool(re.search(r'^name:', content, re.M))
    has_on = bool(re.search(r"^('on'|on):", content, re.M))
    has_jobs = bool(re.search(r'^jobs:', content, re.M))
    print(f"  Header elements: name={has_name}, on={has_on}, jobs={has_jobs}")

    # Check cron expressions
    crons = re.findall(r"cron:\s*['\"]([^'\"]+)['\"]", content)
    print(f"  Cron schedules: {crons}")

    # Check triggers
    has_dispatch = 'workflow_dispatch:' in content
    has_push = 'push:' in content
    print(f"  Triggers: push={has_push}, workflow_dispatch={has_dispatch}, schedule={bool(crons)}")

    # Check python scripts called
    scripts = re.findall(r"python\s+([a-zA-Z0-9_\-/\.]+)", content)
    print(f"  Executed scripts: {scripts}")
    for sc in scripts:
        if sc.endswith('.py'):
            exists = os.path.exists(sc)
            print(f"    - {sc}: {'✅ Exists' if exists else '❌ MISSING!'}")

print("\n--- Summary: Checking requirements.txt ---")
if os.path.exists("requirements.txt"):
    print("requirements.txt exists ✅")
else:
    print("requirements.txt missing ❌")
