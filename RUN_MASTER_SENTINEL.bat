@echo off
title MASTER SENTINEL AGENT (System Watchdog)
echo ==========================================================
echo 🛡️ MASTER SENTINEL AGENT (360 Quality Guardian)
echo Auditing: Affiliate Tags, Anti-Slop, Real Emblems, Blogger
echo ==========================================================
cd /d "%~dp0"
python pipelines/master_sentinel_agent.py
pause
