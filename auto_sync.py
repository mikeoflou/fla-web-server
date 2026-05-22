import subprocess
import json
import os
import yt_dlp
import sys

# --- 1. SET THE PATHS ---
current_folder = os.getcwd()
# Ensuring the Python Scripts folder is in the path for Whisper/FFmpeg
python_scripts_path = r'C:\Users\mikeo\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts'
os.environ["PATH"] += os.pathsep + current_folder + os.pathsep + python_scripts_path

# --- 2. CONFIGURATION ---
# Target: Chosen Road - Brethren We Have Met To Worship
YOUTUBE_URL = "https://www.youtube.com/watch?v=a2tK2xAqxZM" 
AUDIO_FILE = "temp_audio.mp3"
OUTPUT_DIR = "sync_output"

# --- 3. THE PROCESS ---
print("\n" + "!"*30)
print("STARTING WHISPER AUTO-SYNC")
print("!"*30 + "\n")

# 1. Download Audio
if os.path.exists(AUDIO_FILE): os.remove(AUDIO_FILE)
print(f"--- Step 1: Downloading from YouTube ---")
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
    'outtmpl': 'temp_audio', 
    'ffmpeg_location': current_folder, 
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([YOUTUBE_URL])

# 2. Run Whisper AI
print(f"\n--- Step 2: AI is listening (This takes 1-2 minutes) ---")
if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

# Using 'base' model for a good balance of speed and accuracy
cmd = ["python", "-m", "whisper", AUDIO_FILE, "--model", "base", "--output_dir", OUTPUT_DIR, "--output_format", "json"]

print(f"Executing: {' '.join(cmd)}")
result = subprocess.run(cmd)

# 3. Format and Output
if result.returncode == 0:
    json_path = os.path.join(OUTPUT_DIR, "temp_audio.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n" + "="*50)
        print("COPY INTO JASON.HTML:")
        print("="*50 + "\n")
        
        for segment in data.get('segments', []):
            start_time = round(segment["start"], 2)
            text = segment["text"].strip()
            # This matches your Flask template exactly
            print(f'<p class="lyric-line" data-time="{start_time}">{text}</p>')
        
        print("\n" + "="*50)
    else:
        print(f"Error: Whisper finished but {json_path} was not found.")
else:
    print(f"Whisper Error: Ensure you ran 'pip install openai-whisper' first.")
    