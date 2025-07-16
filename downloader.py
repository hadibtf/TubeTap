import yt_dlp
import ffmpeg
import os
import logging

logging.basicConfig(level=logging.INFO)

def download_video(url, format='mp4'):
    """Downloads a video from a given URL and converts it to the specified format."""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_id = info_dict.get('id', None)
        video_title = info_dict.get('title', None)
        duration = info_dict.get('duration', 0)

        if duration > 600:
            raise ValueError("Video is longer than 10 minutes.")

        logging.info(f"Downloading {video_title}...")
        ydl.download([url])

        input_file = f"{video_id}.mp4"
        output_file = f"{video_id}.{format}"

        if format == 'mp3':
            ffmpeg.input(input_file).output(output_file, acodec='libmp3lame').run()
        
        file_size = os.path.getsize(output_file)
        logging.info(f"Downloaded {video_title} ({file_size} bytes)")
        
        return output_file, video_title

def cleanup(*files):
    """Removes the given files."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)
