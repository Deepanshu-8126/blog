#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================================================================
🚀 MASTER 24/7 AUTO-PILOT CRON RUNNER (Autonomous Viral Newsroom & Deals Engine)
========================================================================================
Orchestrates the entire multi-radar ecosystem on a hands-free schedule:
1. Sentinel Quality Audit: Verifies affiliate tags (Amazon tag 'uniquedigi0c6-21', EarnKaro), media purity, and D1 connection
2. Sarkari & Exam Radar: Fetches latest government recruitment & yojana updates into D1
3. Current Affairs & Daily GK: Pulls fresh national developments
4. IndexNow Instant Ping: Automatically notifies Bing and search engines of fresh URLs

Usage:
  python scripts/run_auto_pilot.py --once        # Run a single complete cycle
  python scripts/run_auto_pilot.py --interval 3600 # Run continuously every hour
========================================================================================
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}", flush=True)

def run_step(step_name: str, script_path: str, args: list = None) -> bool:
    log(f"▶️ Starting: {step_name} ({script_path})")
    cmd = [sys.executable, str(ROOT_DIR / script_path)]
    if args:
        cmd.extend(args)
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180
        )
        if res.returncode == 0:
            log(f"✅ [SUCCESS] {step_name}")
            # Print last few lines of output
            lines = [l for l in res.stdout.strip().split("\n") if l.strip()]
            for l in lines[-4:]:
                print(f"    {l}", flush=True)
            return True
        else:
            log(f"⚠️ [WARNING] {step_name} exited with code {res.returncode}")
            if res.stderr:
                err_lines = [l for l in res.stderr.strip().split("\n") if l.strip()]
                for l in err_lines[-3:]:
                    print(f"    [ERR] {l}", flush=True)
            return False
    except subprocess.TimeoutExpired:
        log(f"⏰ [TIMEOUT] {step_name} exceeded 180s limit")
        return False
    except Exception as e:
        log(f"❌ [EXCEPTION] {step_name}: {e}")
        return False

def execute_full_cycle():
    log("=" * 70)
    log("🚀 EXECUTING AUTONOMOUS AUTO-PILOT PIPELINE CYCLE")
    log("=" * 70)

    # Step 1: Master Sentinel Health & Integrity Audit
    sentinel_ok = run_step("Sentinel Quality Audit", "pipelines/master_sentinel_agent.py")

    # Step 2: Sarkari & Yojana Fresh News Ingestion
    run_step("Sarkari & Yojana Radar", "pipelines/sarkari_radar_engine.py")

    # Step 3: Current Affairs & National Intelligence
    if (ROOT_DIR / "pipelines" / "current_affairs_radar_agent.py").exists():
        run_step("Current Affairs Desk", "pipelines/current_affairs_radar_agent.py")

    # Step 4: IndexNow Instant Search Engine Submission
    run_step("IndexNow Mass Notification", "scripts/submit_indexnow.py")

    log("=" * 70)
    log("🎉 AUTO-PILOT CYCLE COMPLETED!")
    log("=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Master Auto-Pilot Pipeline Runner")
    parser.add_argument("--once", action="store_true", help="Execute single cycle and exit")
    parser.add_argument("--interval", type=int, default=3600, help="Loop interval in seconds (default: 3600s / 1 hour)")
    args = parser.parse_args()

    if args.once:
        execute_full_cycle()
    else:
        log(f"🔁 Master Auto-Pilot Daemon active! Running every {args.interval} seconds ({args.interval // 60} mins)...")
        while True:
            try:
                execute_full_cycle()
            except Exception as e:
                log(f"Unexpected loop error: {e}")
            log(f"💤 Sleeping for {args.interval}s until next auto-pilot sweep...\n")
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
