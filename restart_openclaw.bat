@echo off
net stop openclaw
timeout /t 2 /nobreak >nul
net start openclaw
echo Done. Press any key to exit.
pause >nul
