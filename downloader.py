import yt_dlp
import os
import logging

logging.basicConfig(level=logging.INFO)

def _download(url, ydl_opts):
    """Common download logic."""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_id = info_dict.get('id', None)
        video_title = info_dict.get('title', 'video')
        duration = info_dict.get('duration', 0)

        if duration > 600:  # 10 minutes
            raise ValueError("Video is longer than 10 minutes.")

        logging.info(f"Downloading {video_title}...")
        ydl.download([url])
        
        # yt-dlp might save with a different extension
        output_filename = ydl.prepare_filename(info_dict)
        base, _ = os.path.splitext(output_filename)
        
        return f"{base}.mp3", video_title, f"{base}.mp4"

def download_mp3(url):
    """Downloads audio from a YouTube URL as an MP3 file."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
        "cookiefile": "cookies.txt"
    }
    output_file, video_title, _ = _download(url, ydl_opts)
    return output_file, video_title

def download_mp4(url):
    """Downloads a video from a YouTube URL as an MP4 file."""
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(id)s.%(ext)s',
        'noplaylist': True,
        "cookiefile": "cookies.txt"
    }
    _, video_title, output_file = _download(url, ydl_opts)
    # The actual downloaded file might have a different extension, let's find it
    base, _ = os.path.splitext(output_file)
    
    # Check for common extensions
    for ext in ['.mp4', '.mkv', '.webm']:
        if os.path.exists(base + ext):
            return base + ext, video_title
            
    raise FileNotFoundError("Could not find the downloaded video file.")


def cleanup(*files):
    """Removes the given files."""
    for file in files:
        try:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Removed {file}")
        except OSError as e:
            logging.error(f"Error removing file {file}: {e}")