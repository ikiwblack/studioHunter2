import yt_dlp
import os
import uuid
import logging

# Konfigurasi logging untuk memantau proses download
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProvider:
    def __init__(self, temp_dir="app/static/temp"):
        self.temp_dir = temp_dir
        # Pastikan folder temp ada
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def fetch_and_download(self, url):
        """
        Mengunduh video dari URL dan mengembalikan info untuk Editor.
        """
        file_id = str(uuid.uuid4())
        # Lokasi penyimpanan sementara dengan ID unik
        output_template = os.path.join(self.temp_dir, f"{file_id}.%(ext)s")

        ydl_opts = {
            # Pilih format terbaik yang bertipe mp4 agar lancar di browser & MoviePy
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            # User Agent untuk meniru browser asli agar tidak diblokir
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        try:
            logger.info(f"Memulai unduhan dari URL: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Ambil info tanpa download dulu untuk verifikasi
                info = ydl.extract_info(url, download=True)
                
                # Mendapatkan path asli file (karena ekstensi bisa .mp4, .mkv, dll)
                actual_filename = ydl.prepare_filename(info)
                
                # Jika format bukan mp4, MoviePy terkadang kesulitan, 
                # namun yt-dlp sudah kita arahkan ke mp4 di atas.
                
                return {
                    "status": "success",
                    "title": info.get('title', 'Video Tanpa Judul'),
                    "duration": info.get('duration'),
                    "thumbnail": info.get('thumbnail'),
                    "file_path": actual_filename, # Digunakan oleh MoviePy (backend)
                    "video_url": f"/static/temp/{os.path.basename(actual_filename)}" # Digunakan oleh Preview (frontend)
                }

        except Exception as e:
            logger.error(f"Gagal mengunduh video: {str(e)}")
            return {
                "status": "error", 
                "message": "Gagal mengambil video. Pastikan link valid atau coba lagi nanti."
            }

# Inisialisasi global agar bisa dipanggil di main.py
video_provider = VideoProvider()