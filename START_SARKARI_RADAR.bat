@echo off
title SARKARI & EXAM RESULT RADAR 24/7
echo ==========================================================
echo 🚀 SARKARI RESULT & SCHEME RADAR (Auto-Publisher Engine)
echo Target Blog: all-sarkari-result-2k0.blogspot.com
echo ==========================================================
cd /d "%~dp0"
python pipelines/sarkari_radar_engine.py 3
pause
