import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

PHRASES = [
    'radar', 'telemetry', 'recomput', 'autonomous', 'verified buyer',
    'intelligence portal', 'viral intelligence', 'bot active', 'engine',
    'glitch', 'live wire', 'wire corroborated', 'hype board', 'signal',
    'desk active', 'hubs connected', 'direct action', 'tested across',
    '0-minute', 'live discount radar', 'deal radar', 'precision vector',
    'multi-signal', 'real-time multi', 'peer-reviewed', 'clinical & ayush',
    'national telemetry', 'hourly off-peak', 'price glitch', 'automated radar',
    'unbiased', 'rockstar wire', 'vice city intelligence', 'hype score',
    'curated intelligence', 'algorithmic', 'bot', 'sensor'
]

matches = []
for root, dirs, files in os.walk('src'):
    for f in files:
        if f.endswith('.astro'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as fh:
                for idx, line in enumerate(fh, 1):
                    s = line.strip()
                    if s.startswith('//') or s.startswith('import ') or s.startswith('<!--') or s.startswith('*'):
                        continue
                    low = s.lower()
                    for ph in PHRASES:
                        if ph in low:
                            # Filter out false positives like 'signal' in a variable name or target='_blank'
                            if ph == 'signal' and ('signal' in s and not any(w in low for w in ['multi-signal', 'signal score', 'signal intel'])):
                                continue
                            if ph == 'engine' and ('pipeline' in low or 'template' in low or 'script' in low):
                                continue
                            matches.append((filepath, idx, ph, s))
                            break

print(f"Total matching lines found: {len(matches)}")
for path, line_no, ph, content in matches:
    print(f"[{ph}] {path}:{line_no} -> {content}")
