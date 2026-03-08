import subprocess
import time
import threading
from youtube_api import get_subscribers

# Aapki Details
CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "77cs-jw6x-yfeu-m2ks-82d6"

def update_label_file():
    """Har 10 second mein bina stream roke subs update karega"""
    while True:
        subs = get_subscribers(CHANNEL_ID)
        with open("label.txt", "w") as f:
            f.write(f"LIVE SUBS: {subs}")
        time.sleep(10)

def start_stream():
    # Pehle default text file banayein
    with open("label.txt", "w") as f:
        f.write("Connecting...")

    # Background thread shuru karein
    threading.Thread(target=update_label_file, daemon=True).start()
    
    # Sahi YouTube RTMP URL (Standard Server 1)
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    # FFmpeg Command: Shorts Format (720x1280)
    command = [
        "ffmpeg",
        "-re",
        "-f", "lavfi", "-i", "color=c=purple:s=720x1280:r=25", # Purple background vertical
        "-f", "lavfi", "-i", "anullsrc=cl=stereo:sr=44100",    # Silent audio
        "-vf", "drawtext=reload=1:textfile=label.txt:fontcolor=white:fontsize=55:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6:boxborderw=15",
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-f", "flv", rtmp_url
    ]

    print("--- VERTICAL SHORTS STREAM STARTED ON RENDER ---")
    subprocess.run(command)

if __name__ == "__main__":
    start_stream()
