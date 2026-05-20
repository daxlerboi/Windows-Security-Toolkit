@echo off
setlocal EnableDelayedExpansion
title RAT Detection & Network Analyzer 
color 0A

:: =========================
:: ADMIN CHECK
:: =========================
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo [!] Run as ADMIN for full accuracy
    echo ------------------------------------------
)

:: =========================
:: LOG SETUP
:: =========================
set LOGDIR=%~dp0logs
set LOGFILE=%LOGDIR%\rat_scan_log.txt

if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo ========================================== > "%LOGFILE%"
echo        RAT DETECTION REPORT v5           >> "%LOGFILE%"
echo ========================================== >> "%LOGFILE%"
echo Date: %date% %time% >> "%LOGFILE%"
echo. >> "%LOGFILE%"

set /a RISK=0

echo ==========================================
echo        RAT DETECTION SCANNER v5
echo ==========================================
echo.

:: =========================
:: SAFE CONNECTION SCAN (FIXED PARSING)
:: =========================
echo [1] Active Connections (Clean View)
echo ------------------------------------------

for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr ESTABLISHED') do (
    set LADDR=%%a
    set FADDR=%%b
    set PID=%%e

    echo !LADDR! -> !FADDR! PID: !PID!

    :: Ignore IPv6 parsing issues safely
    echo !FADDR! | findstr ":" >nul
    if !errorlevel! EQU 0 (
        rem IPv6 detected - skip risk scoring (prevents false alarms)
    ) else (
        echo !FADDR! | findstr "127.0.0.1 192.168. 10. 172." >nul
        if !errorlevel! NEQ 0 (
            echo [!] External connection: !FADDR!
            set /a RISK+=1
        )
    )
)

echo.

:: =========================
:: LISTENING PORTS
:: =========================
echo [2] Listening Ports
echo ------------------------------------------
netstat -ano | findstr LISTENING

echo.

:: =========================
:: SUSPICIOUS PORT CHECK (SAFE VERSION)
:: =========================
echo [3] Suspicious Port Scan
echo ------------------------------------------

set PORTS=4444 5555 1337 31337 9001

for %%p in (%PORTS%) do (
    netstat -ano | findstr "%%p" >nul
    if !errorlevel! EQU 0 (
        echo [WARNING] Suspicious port activity: %%p
        set /a RISK+=1
    )
)

echo.

:: =========================
:: PROCESS SNAPSHOT (SAFE REPLACEMENT FOR WMIC)
:: =========================
echo [4] Process Snapshot (Basic Check)
echo ------------------------------------------

tasklist > "%LOGDIR%\process_list.txt"
type "%LOGDIR%\process_list.txt"

:: Check suspicious execution locations (basic heuristic)
findstr /i "temp appdata \\downloads" "%LOGDIR%\process_list.txt" >nul
if !errorlevel! EQU 0 (
    echo [!] Suspicious process location pattern detected
    set /a RISK+=2
)

echo.

:: =========================
:: STARTUP CHECK (WMIC SAFE FALLBACK)
:: =========================
echo [5] Startup Entries
echo ------------------------------------------

wmic startup get caption,command >nul 2>&1
if !errorlevel! NEQ 0 (
    echo [!] WMIC not available (Windows modern build)
    echo Use PowerShell: Get-CimInstance Win32_StartupCommand
    set /a RISK+=0
) else (
    wmic startup get caption,command
)

echo.

:: =========================
:: RDP STATUS
:: =========================
echo [6] Remote Desktop Status
echo ------------------------------------------
reg query "HKLM\System\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections

echo.

:: =========================
:: RISK SCORING
:: =========================
echo ==========================================
echo               SUMMARY
echo ==========================================

if !RISK! GEQ 5 (
    echo [CRITICAL] HIGH RISK DETECTED
) else if !RISK! GEQ 3 (
    echo [WARNING] MEDIUM RISK DETECTED
) else (
    echo [OK] LOW RISK - No strong indicators
)

echo.
echo Total Risk Score: !RISK!
echo Log saved: %LOGFILE%
echo ==========================================
pause