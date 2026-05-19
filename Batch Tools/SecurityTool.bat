@echo off
setlocal EnableDelayedExpansion
title Windows Security Toolkit v5.2 (Intelligence Edition)
color 0A

:: ===============================
:: PATHS
:: ===============================
set BASE=%~dp0
set LOGDIR=%BASE%logs
set LOGFILE=%LOGDIR%\security_log.txt
set ALERTS=%LOGDIR%\alerts.txt

if not exist "%LOGDIR%" mkdir "%LOGDIR%"

:: ===============================
:: MENU
:: ===============================
:MENU
cls
echo ======================================
echo     WINDOWS SECURITY TOOLKIT v5.2
echo ======================================
echo.
echo 1. Network Scan
echo 2. Process Scan 
echo 3. Startup Programs
echo 4. Scheduled Tasks
echo 5. DNS Cache 
echo 6. Users & Admins
echo 7. Firewall Status
echo.
echo 8. LIVE MONITOR MODE
echo 9. FULL SYSTEM SCAN
echo 10. PORT INTELLIGENCE 
echo A. RAT HUNT MODE
echo B. SYSTEM INFO REPORT
echo C. TEMP SCAN
echo D. SECURITY HEALTH CHECK
echo E. EXPORT FULL REPORT
echo F. SERVICE SCAN
echo G. AUTORUN CHECK
echo H. HIDDEN FILE SCAN
echo I. NETWORK ADAPTER INFO
echo J. SYSTEM RESOURCE SNAPSHOT
echo K. DOWNLOADS SECURITY CHECK
echo L. EVENT LOG CHECK 
echo M. CONNECTION MAP 
echo N. RISK SCORE ANALYSIS 
echo 0. EXIT
echo.
set /p choice=Enter choice:

if "%choice%"=="1" goto net
if "%choice%"=="2" goto proc
if "%choice%"=="3" goto startup
if "%choice%"=="4" goto tasks
if "%choice%"=="5" goto dns
if "%choice%"=="6" goto users
if "%choice%"=="7" goto firewall
if "%choice%"=="8" goto live
if "%choice%"=="9" goto full
if "%choice%"=="10" goto portintel
if /I "%choice%"=="A" goto rat
if /I "%choice%"=="B" goto sysinfo
if /I "%choice%"=="C" goto temp
if /I "%choice%"=="D" goto health
if /I "%choice%"=="E" goto export
if /I "%choice%"=="F" goto services
if /I "%choice%"=="G" goto autorun
if /I "%choice%"=="H" goto hidden
if /I "%choice%"=="I" goto netadapter
if /I "%choice%"=="J" goto resources
if /I "%choice%"=="K" goto downloads
if /I "%choice%"=="L" goto eventlog
if /I "%choice%"=="M" goto connmap
if /I "%choice%"=="N" goto risk
if "%choice%"=="0" exit

goto MENU

:: ===============================
:: LOG SYSTEM
:: ===============================
:log
echo [%date% %time%] %~1 >> "%LOGFILE%"
exit /b

:alert
echo [%date% %time%] ALERT: %~1 >> "%ALERTS%"
echo [!] %~1
exit /b

:: ===============================
:: 1. NETWORK
:: ===============================
:net
cls
call :log "Network Scan"
netstat -ano
pause
goto MENU

:: ===============================
:: 2. PROCESS
:: ===============================
:proc
cls
call :log "Process Scan"

tasklist
powershell -Command "Get-CimInstance Win32_Process | Select Name,ProcessId,ExecutablePath"
tasklist | findstr /i "powershell wscript cscript rundll32 regsvr32"

pause
goto MENU

:: ===============================
:: 3. STARTUP
:: ===============================
:startup
cls
call :log "Startup Scan"
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
pause
goto MENU

:: ===============================
:: 4. TASKS
:: ===============================
:tasks
cls
call :log "Scheduled Tasks"
schtasks /query /fo LIST /v
pause
goto MENU

:: ===============================
:: 5. DNS (FIXED CLEAN VIEW)
:: ===============================
:dns
cls
call :log "DNS Scan Clean"

echo === SAFE DOMAINS ===
ipconfig /displaydns | findstr /i "google microsoft cloudflare github windows"

echo.
echo === SUSPICIOUS PATTERNS ===
ipconfig /displaydns | findstr /i "temp appdata 4444 1337 unknown"

pause
goto MENU

:: ===============================
:: 6. USERS
:: ===============================
:users
cls
call :log "Users Scan"
net user
net localgroup administrators
pause
goto MENU

:: ===============================
:: 7. FIREWALL
:: ===============================
:firewall
cls
call :log "Firewall Check"
netsh advfirewall show allprofiles
pause
goto MENU

:: ===============================
:: 8. LIVE MONITOR
:: ===============================
:live
cls
echo LIVE MONITOR (CTRL+C to stop)
:loop
netstat -ano | findstr ESTABLISHED
timeout /t 3 >nul
goto loop

:: ===============================
:: 9. FULL SCAN
:: ===============================
:full
cls
call :log "FULL SCAN"

netstat -ano >> "%LOGFILE%"
tasklist >> "%LOGFILE%"
powershell -Command "Get-CimInstance Win32_Process | Select Name,ProcessId,ExecutablePath" >> "%LOGFILE%"
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run >> "%LOGFILE%"
schtasks /query /fo LIST /v >> "%LOGFILE%"

call :alert "Full scan completed"
pause
goto MENU

:: ===============================
:: 10. PORT INTELLIGENCE
:: ===============================
:portintel
cls
call :log "Port Intelligence"

netstat -ano | findstr LISTENING
netstat -ano | findstr ESTABLISHED

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ESTABLISHED') do (
    echo PID: %%a
    tasklist /fi "PID eq %%a"
)

pause
goto MENU

:: ===============================
:: A. RAT HUNT
:: ===============================
:rat
cls
call :log "RAT Hunt"

netstat -ano | findstr ":4444"
netstat -ano | findstr ":1337"
tasklist | findstr /i "powershell wscript cscript"
pause
goto MENU

:: ===============================
:: B. SYSTEM INFO
:: ===============================
:sysinfo
cls
systeminfo
pause
goto MENU

:: ===============================
:: C. TEMP SCAN
:: ===============================
:temp
cls
dir %temp%
dir %temp% | findstr /i ".exe"
pause
goto MENU

:: ===============================
:: D. HEALTH CHECK
:: ===============================
:health
cls
netsh advfirewall show allprofiles
net user
pause
goto MENU

:: ===============================
:: E. EXPORT
:: ===============================
:export
cls
set REPORT=%LOGDIR%\full_report.txt

echo SECURITY REPORT > "%REPORT%"
netstat -ano >> "%REPORT%"
tasklist >> "%REPORT%"

call :alert "Report exported"
pause
goto MENU

:: ===============================
:: F. SERVICES
:: ===============================
:services
cls
net start
pause
goto MENU

:: ===============================
:: G. AUTORUN
:: ===============================
:autorun
cls
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
pause
goto MENU

:: ===============================
:: H. HIDDEN FILES
:: ===============================
:hidden
cls
dir C:\ /a:h | more
pause
goto MENU

:: ===============================
:: I. NETWORK ADAPTER
:: ===============================
:netadapter
cls
ipconfig /all
route print
pause
goto MENU

:: ===============================
:: J. RESOURCES
:: ===============================
:resources
cls
wmic cpu get loadpercentage
wmic OS get FreePhysicalMemory,TotalVisibleMemorySize
tasklist
pause
goto MENU

:: ===============================
:: K. DOWNLOADS
:: ===============================
:downloads
cls
dir "%USERPROFILE%\Downloads" | findstr /i ".exe .bat .js"
pause
goto MENU

:: ===============================
:: L. EVENT LOG (SAFE FIX)
:: ===============================
:eventlog
cls
call :log "Event Log Check"

wevtutil qe System /c:10 /f:text
wevtutil qe Application /c:10 /f:text
pause
goto MENU

:: ===============================
:: M. CONNECTION MAP (NEW)
:: ===============================
:connmap
cls
call :log "Connection Map"

for /f "tokens=5" %%a in ('netstat -ano ^| findstr ESTABLISHED') do (
    echo ===== PID %%a =====
    tasklist /fi "PID eq %%a"
)
pause
goto MENU

:: ===============================
:: N. RISK SCORE (NEW)
:: ===============================
:risk
cls
set /a score=0

netstat -ano | findstr ":4444" >nul && set /a score+=40
netstat -ano | findstr ":1337" >nul && set /a score+=30
tasklist | findstr /i "powershell wscript" >nul && set /a score+=10

echo === RISK SCORE: %score% ===

if %score% GEQ 50 (
    echo HIGH RISK
) else if %score% GEQ 20 (
    echo MEDIUM RISK
) else (
    echo LOW RISK
)

pause
goto MENU