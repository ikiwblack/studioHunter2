import os
import json
import uuid
import shutil
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

# Pastikan Anda sudah membuat file ini di folder app/services/
from app.services.video_editor import edit_video 

app = FastAPI()

# --- KONFIGURASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
EXPORT_DIR = os.path.join(BASE_DIR, "static", "exports")

# Buat folder jika belum ada
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# --- MOUNTING STATIC & TEMPLATES ---
# Ini kunci agar CSS, JS, dan Video Preview bisa diakses browser
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/")
async def index(request: Request):
    """Menampilkan halaman utama editor."""
    return templates.TemplateResponse("editor.html", {"request": request})

@app.post("/render")
async def render_endpoint(
    video: UploadFile = File(...), 
    settings: str = Form(...)
):
    """
    Endpoint untuk menerima video mentah dan instruksi editing,
    lalu memprosesnya menggunakan MoviePy.
    """
    try:
        # 1. Parse pengaturan dari string JSON (dikirim oleh editor.js)
        edit_settings = json.loads(settings)
        
        # 2. Simpan video mentah ke folder uploads dengan nama unik
        file_id = str(uuid.uuid4())[:8]
        input_filename = f"input_{file_id}_{video.filename}"
        input_path = os.path.join(UPLOAD_DIR, input_filename)
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # 3. Tentukan nama file hasil render
        output_filename = f"result_{file_id}.mp4"
        output_path = os.path.join(EXPORT_DIR, output_filename)

        # 4. Jalankan mesin MoviePy
        # Fungsi ini harus menerima path video, data teks, dan volume
        success = edit_video(input_path, output_path, edit_settings)

        if success:
            return JSONResponse({
                "status": "success",
                "filename": output_filename,
                "download_url": f"/static/exports/{output_filename}"
            })
        else:
            raise HTTPException(status_code=500, detail="Gagal memproses video")

    except Exception as e:
        print(f"Error pada Backend: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"status": "error", "message": str(e)}
        )

# Jalankan dengan: uvicorn app.main:app --reload