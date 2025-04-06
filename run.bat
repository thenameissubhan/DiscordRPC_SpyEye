@echo off
setlocal

:: Path to your Python script
set "pythonScript=D:\SpyEye\main_discord.py"

:: Path to your pythonw.exe
set "pythonExe=C:\Users\thena\AppData\Local\Programs\Python\Python313\pythonw.exe"

:: Start the Python script silently (no console window)
start "" "%pythonExe%" "%pythonScript%"

:: Set priority to High using PowerShell
powershell -Command "Get-Process -Name 'pythonw' | ForEach-Object { $_.PriorityClass = 'High' }"

endlocal
exit
