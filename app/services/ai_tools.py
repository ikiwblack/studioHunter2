import os
import whisper
from moviepy import VideoFileClip

class AITools:
    def __init__(self):
        # Memuat model Whisper saat class diinisialisasi
        # 'base' cukup cepat untuk CPU, gunakan 'tiny' jika ingin lebih cepat lagi
        self.model = None
        self.model_name = "base"

    def _load_model(self):
        if self.model is None:
            print(f"INFO: Memuat model Whisper AI ({self.model_name})...")
            self.model = whisper.load_model(self.model_name)

    def generate_subtitles(self, video_path):
        """
        Mengekstrak audio dari video dan mengubahnya menjadi teks dengan timestamp.
        """
        try:
            self._load_model()
            
            # 1. Ekstrak audio sementara agar Whisper bisa memproses lebih cepat
            # Namun Whisper sebenarnya bisa membaca file video langsung
            print(f"INFO: Mentranskripsi video {video_path}...")
            
            # Jalankan transkripsi
            result = self.model.transcribe(video_path, verbose=False)
            
            # 2. Format hasil menjadi list of dict yang bisa dibaca editor.js
            subtitles = []
            for segment in result['segments']:
                subtitles.append({
                    "text": segment['text'].strip(),
                    "start": round(segment['start'], 2),
                    "end": round(segment['end'], 2),
                    "fontSize": 30,
                    "color": "#ffffff",
                    "x": 0.5, # Default tengah
                    "y": 0.8  # Default bawah (posisi subtitle)
                })
            
            return subtitles

        except Exception as e:
            print(f"AI Error: {str(e)}")
            return []

# Inisialisasi instance tunggal
ai_service = AITools()