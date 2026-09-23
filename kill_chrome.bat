@echo off
echo Killing Chrome background processes...
taskkill /F /IM chrome.exe /T 2>nul
if %errorlevel% equ 0 (
    echo Chrome processes killed successfully!
) else (
    echo No Chrome processes found or already closed.
)
echo.
echo You can now try downloading the video again.
pause
