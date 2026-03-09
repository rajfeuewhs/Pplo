import subprocess
import time
import threading
import os
from flask import Flask
from youtube_api import get_subscribers

# Details
CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "77cs-jw6x-yfeu-m2ks-82d6" 

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Status: 24/7 Ultra-Lite Stream Active</h1>"

def update_label():
    while True:
        try:
            subs = get_subscribers(CHANNEL_ID)
            with open("label.txt", "w") as f:
                f.write(f" LIVE SUBS: {subs} | GOAL: 50 ")
        except:
            pass
        time.sleep(30) # CPU bachane ke liye bada gap

def run_ffmpeg():
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    
    # Static Image Input (Sabse Lite)
    bg_input = "-f lavfi -i color=c=purple:s=720x1280:r=5"
    if os.path.exists("bg.jpg"):
        bg_input = "-loop 1 -i bg.jpg"

    command = [
        "ffmpeg", "-re",
        *bg_input.split(),
        "-f", "lavfi", "-i", "anullsrc", # No heavy audio processing
        "-vf", (
            "drawtext=reload=1:textfile=label.txt:fontcolor=white:fontsize=70:"
            "x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6"
        ),
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-r", "5",               # Sirf 5 FPS
        "-g", "10",              
        "-b:v", "500k",          # Low bitrate
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-f", "flv", 
        rtmp_url
    ]
    
    while True:
        print("--- Starting Ultra-Lite Render Stream ---")
        subprocess.run(command)
        time.sleep(5) 

if __name__ == "__main__":
    if not os.path.exists("label.txt"):
        with open("label.txt", "w") as f:
            f.write("Loading...")
    threading.Thread(target=update_label, daemon=True).start()
    threading.Thread(target=run_ffmpeg, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
