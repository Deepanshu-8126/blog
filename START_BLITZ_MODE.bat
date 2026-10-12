@echo off
title UniqueDigit BLITZ MODE — Festival Deal Scanner
color 0C
echo.
echo  ========================================================
echo   UNIQUEDIGIT BLITZ MODE — BIG BILLION DAYS / GIFD
echo  ========================================================
echo.
echo   FESTIVAL MODE: Scanning every 15 seconds!
echo   Use during: Big Billion Days, Great Indian Festival,
echo   Republic Day Sale, Flash Sales, etc.
echo.
echo   Press Ctrl+C to stop at any time.
echo.
echo  ========================================================
echo.

cd /d "%~dp0"
python loot_radar_agent.py --blitz

pause
