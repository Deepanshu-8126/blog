@echo off
title UniqueDigit Loot Radar — 24/7 Real-Time Agent
color 0A
echo.
echo  ========================================================
echo   UNIQUEDIGIT LOOT RADAR — REAL-TIME DEAL INTELLIGENCE
echo  ========================================================
echo.
echo   This will run the Loot Radar in LIVE mode (30s cycles)
echo   scanning 6+ deal sources continuously.
echo.
echo   For Festival/Sale mode (15s cycles), close this and
echo   run: python loot_radar_agent.py --blitz
echo.
echo   Press Ctrl+C to stop at any time.
echo.
echo  ========================================================
echo.

cd /d "%~dp0"
python loot_radar_agent.py --live

pause
