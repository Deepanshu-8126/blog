import sys
import os
import subprocess
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

load_dotenv("d:/affi;ate/.env")
env = os.environ.copy()

sql_file = "C:/Users/Deepanshu/scrub_body_reddit.sql"
sql_query = """
UPDATE posts 
SET body_md = REPLACE(
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(body_md, 'Reddit', 'Consumer Community'),
                    'reddit', 'community'
                ),
                'Redditors', 'Community members'
            ),
            'redditors', 'community members'
        ),
        'Redditor', 'Community contributor'
    ),
    'r/', 'community/'
)
WHERE body_md LIKE '%reddit%' OR body_md LIKE '%Reddit%';
"""

with open(sql_file, "w", encoding="utf-8") as f:
    f.write(sql_query)

cmd = ["npx", "wrangler", "d1", "execute", "uniquedigit-db", "--remote", f"--file={sql_file}"]
res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", shell=True, env=env, cwd="C:/Users/Deepanshu")
print("Return code:", res.returncode)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
