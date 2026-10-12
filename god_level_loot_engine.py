#!/usr/bin/env python3
"""
UniqueDigit God-Level 24/7 Loot Engine Entrypoint
Delegates execution to the hardened pipelines package.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipelines.god_level_loot_engine import GodLevelLootEngine, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="God-Level Autonomous Loot Engine")
    parser.add_argument("--loop", action="store_true", help="Run in continuous 24/7 loop")
    parser.add_argument("--interval", type=int, default=25, help="Seconds between scan cycles (default: 25)")
    parser.add_argument("--duration", type=int, default=None, help="Max run duration in seconds")
    args = parser.parse_args()

    engine = GodLevelLootEngine()

    if args.loop or args.duration:
        engine.run_loop(interval=args.interval, duration=args.duration)
    else:
        engine.run_one_cycle()
