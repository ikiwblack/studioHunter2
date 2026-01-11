@echo off
title Hunter V2 Server
echo [1/2] Mengaktifkan Virtual Environment...
call venv\Scripts\activate

echo [2/2] Menjalankan FastAPI Server...
python -m uvicorn app.main:app --reload

pause