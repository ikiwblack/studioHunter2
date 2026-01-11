@echo off
title Port 8000 Killer
color 0c

echo ========================================
echo   MENCARI PROSES DI PORT 8000...
echo ========================================

:: Mencari PID (Process ID) yang mendengarkan di port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    set PID=%%a
)

:: Cek apakah PID ditemukan
if defined PID (
    echo [+] Menemukan proses dengan PID: %PID%
    echo [+] Mematikan proses...
    taskkill /f /pid %PID%
    echo.
    echo ========================================
    echo   BERHASIL! PORT 8000 SEKARANG BEBAS.
    echo ========================================
) else (
    echo [!] Tidak ada proses yang berjalan di port 8000.
    echo ========================================
)

timeout /t 3
pause