@echo off
title Google Blogger 1-Click Authentication
color 0B
cd /d "%~dp0bridges\blogger_bridge"

echo =====================================================================
echo  Google Blogger API 1-Click Authenticator
echo =====================================================================
echo.
echo Starting Google OAuth flow...
echo A browser window will open. Please log in and allow permissions.
echo.
python blogger_auth.py
echo.
pause
