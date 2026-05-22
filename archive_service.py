import subprocess
import datetime
import os

def download_today_sermon():
    # 1. Create a clean date name (e.g., sermon_2026-05-17.mp4)
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # 2. Point this to your actual Flask project's static video folder
    output_dir = "/var/www/ehbc/static/videos/"
    output_file = os.path.join(output_dir, f"latest_sermon.mp4")

    # The church's YouTube stream URL
    youtube_url = "https://www.youtube.com/@easternheightsbaptistchurc6595/streams"

    try:
        print("Starting sermon archive download...")
        # Downloads the most recent video from the stream tab at 720p HD quality
        subprocess.run([
            'yt-dlp',
            '--playlist-items', '1',
            '-f', 'bestvideo[height<=720]+bestaudio[ext=m4a]/best[height<=720]',
            '-o', output_file,
            youtube_url
        ], check=True)
        print("Download complete! Overwrote the previous week's video successfully.")
    except Exception as e:
        print(f"Error downloading video: {e}")

if __name__ == "__main__":
    download_today_sermon()