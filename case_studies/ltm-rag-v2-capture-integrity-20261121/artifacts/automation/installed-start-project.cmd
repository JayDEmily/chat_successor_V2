@echo off
setlocal
if /I "%USERPROFILE%"=="C:\Users\james\AppData\Local\DesktopCommander\Shoko" goto shoco
if /I "%USERPROFILE%"=="C:\Users\james" goto james
>&2 echo Unknown account route; refusing implicit fallback
exit /b 1
:shoco
"C:\Program Files\Python313\python.exe" -B -X utf8 "C:\Users\james\AppData\Local\ChatSuccession\Backend\adr2-36b1709\integration\launch_project.py" %* --install-root "%~dp0." --account-key shoco
exit /b %ERRORLEVEL%
:james
"C:\Program Files\Python313\python.exe" -B -X utf8 "C:\Users\james\AppData\Local\ChatSuccession\Backend\adr2-5c86ad6\integration\launch_project.py" %* --install-root "%~dp0." --account-key james-student
exit /b %ERRORLEVEL%
