# 🧪 STUDIOHUNTER - [EKSPERIMENTAL] WINDOWS10 V E N V🚀

> **PERINGATAN:** Proyek ini berstatus **EKSPERIMENTAL**.
> Fitur AI dan rendering MoviePy 2.2.1 sedang dalam tahap pengujian intensif. Gunakan untuk tujuan pengembangan dan riset.
StudioHunter adalah aplikasi pengeditan video berbasis web yang dibangun menggunakan **FastAPI** dan **MoviePy 2.2.1**. Aplikasi ini dirancang untuk memudahkan penambahan elemen visual dan teks interaktif dengan dukungan teknologi **AI Whisper** untuk pembuatan subtitle otomatis.

## 🚀 Fitur Utama

- **Drag-and-Drop Editor**: Menambahkan teks dan elemen visual langsung di atas preview video dengan posisi yang presisi.
- **AI Auto-Subtitle**: Transkripsi suara video menjadi teks secara otomatis menggunakan model OpenAI Whisper.
- **Audio Control**: Pengaturan volume video asli dan dukungan untuk integrasi musik latar.
- **Modern UI**: Antarmuka berbasis Dark Mode yang responsif dan intuitif.

## 🛠️ Struktur Proyek

hunter/
├── app/
│   ├── main.py                 # Endpoint API & Routing FastAPI
│   ├── templates/              # File HTML (UI)
│   ├── static/                 
│   │   ├── css/                # Styling (style.css)
│   │   ├── js/                 # Logika Frontend (editor.js)
│   │   ├── uploads/            # Penyimpanan video mentah
│   │   └── exports/            # Hasil render video (.mp4)
│   └── services/               
│       ├── video_editor.py     # Mesin MoviePy 2.2.1
│       └── ai_tools.py         # Integrasi Whisper AI
├── requirements.txt            # Daftar library Python
└── README.md                   # Panduan instalasi


📦 Instalasi
1. Prasyarat Sistem
  >    Python 3.9+

  >    ImageMagick: Wajib diinstal untuk memproses teks pada video.

  >    Windows: Pastikan saat instalasi mencentang opsi "Install legacy utilities (convert.exe)".

  >    FFmpeg: Dibutuhkan untuk pemrosesan audio/video (biasanya terinstal otomatis).

2. Setup Lingkungan

# Masuk ke folder proyek
    cd hunter

# Buat virtual environment
    python -m venv venv

# Aktivasi venv (Windows)
    venv\Scripts\activate

# Instal dependensi
    pip install -r requirements.txt

3. Konfigurasi Path
  Buka app/services/video_editor.py dan sesuaikan path ImageMagick Anda:

  os.environ["IMAGEMAGICK_BINARY"] = r"%PATH%\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"


🏃 Cara Menjalankan
  Jalankan server pengembangan dengan perintah berikut:

    python -m uvicorn app.main:app --reload

Buka browser dan akses: http://127.0.0.1:8000

📝 Catatan Penting
- Rendering: Proses render menggunakan CPU. Kecepatan bergantung pada durasi video dan jumlah layer teks.

- Model AI: Saat pertama kali menjalankan fitur subtitle, aplikasi akan mengunduh model Whisper (base) sebesar ~140MB secara otomatis.

- run_server.bat (Memulai server Otomatis)

- kill_server8000 (Kill Port 8000)


# DEDICATED TO PRABO.GO & Gib.Run Framework 


