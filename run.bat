@echo off
setlocal
set "pythonScript=D:\SpyEye\main_discord.py"
set "priority=256"
wmic process where name="pythonw.exe" call setpriority %priority%
start "" C:\Users\thena\AppData\Local\Programs\Python\Python313\pythonw.exe "%pythonScript%"
endlocal
exit
