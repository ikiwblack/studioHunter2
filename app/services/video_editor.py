import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import moviepy.video.fx as vfx

# Konfigurasi ImageMagick (Sesuaikan path ini dengan PC Anda)
os.environ["IMAGEMAGICK_BINARY"] = r"%PATH%\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

def edit_video(input_path, output_path, settings):
    """
    Memproses video menggunakan MoviePy 2.2.1
    settings: dict berisi 'texts' (list) dan 'volume' (float)
    """
    video = None
    final_video = None
    
    try:
        # 1. Muat Video Utama
        video = VideoFileClip(input_path)
        
        # 2. Atur Volume Video
        volume_level = settings.get('volume', 1.0)
        if volume_level == 0:
            video = video.without_audio()
        else:
            video = video.with_volume_scaling(volume_level)

        layers = [video]

        # 3. Tambahkan Layer Teks
        for t in settings.get('texts', []):
            # Hitung posisi piksel berdasarkan rasio (0.0 - 1.0) dari frontend
            # MoviePy 2.x menggunakan koordinat top-left untuk positioning manual
            pos_x = t.get('x', 0.5) * video.w
            pos_y = t.get('y', 0.5) * video.h

            txt_clip = (TextClip(
                text=t['text'],
                font_size=t.get('fontSize', 40),
                color=t.get('color', 'white'),
                font="Arial-Bold", # Pastikan font ini terinstall di Windows
                method='caption',
                size=(video.w * 0.8, None) # Bungkus teks agar tidak keluar layar
            )
            .with_duration(video.duration)
            .with_start(0)
            .with_position((pos_x, pos_y)))

            layers.append(txt_clip)

        # 4. Gabungkan Semua Layer
        final_video = CompositeVideoClip(layers)

        # 5. Render ke File MP4
        # Menggunakan preset 'ultrafast' agar preview render lebih cepat
        final_video.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac", 
            fps=24,
            preset="ultrafast",
            threads=4
        )
        
        return True

    except Exception as e:
        print(f"MoviePy Error: {str(e)}")
        return False
    
    finally:
        # Tutup semua clip agar memori tidak penuh (leak)
        if video: video.close()
        if final_video: final_video.close()