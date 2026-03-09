import subprocess
import time
import threading
import os
from flask import Flask
from youtube_api import get_subscribers

# Details
CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = os.getenv("STREAM_KEY") 
SUB_GOAL = 50 

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Pro Text Stream: ACTIVE</h1>"

def update_label():
    while True:
        try:
            subs = get_subscribers(CHANNEL_ID)
            with open("label.txt", "w") as f:
                f.write(f" LIVE SUBS: {subs} | GOAL: {50} ")
        except Exception as e:
            print(f"Update Error: {e}")
        time.sleep(15)

def run_ffmpeg():
    # Direct IP address if DNS fails
    rtmp_url = f"rtmp://199.223.232.122/live2/{STREAM_KEY}"
    
    # Static Image Input (Best for Render 24/7)
    bg_input = "-f lavfi -i color=c=purple:s=720x1280:r=15"
    if os.path.exists("bg.jpg"):
        bg_input = "-loop 1 -i bg.jpg"

    command = [
        "ffmpeg", "-re",
        *bg_input.split(),
        "-f", "lavfi", "-i", "anullsrc",
        "-vf", (
            "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
            # TEXT IMPROVEMENT: Big Font (120) + Black Shadow (Glow)
            "drawtext=reload=1:textfile=label.txt:fontcolor=white:fontsize=120:"
            "x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.5:boxborderw=25"
        ),
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-g", "30", "-b:v", "2000k", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-f", "flv", 
        # TLR Verify false to fix rtmps issues
        "-tls_verify", "0",
        rtmp_url
    ]
    subprocess.run(command)

if __name__ == "__main__":
    if not os.path.exists("label.txt"):
        with open("label.txt", "w") as f:
            f.write("Fetching Subs...")
    threading.Thread(target=update_label, daemon=True).start()
    threading.Thread(target=run_ffmpeg, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
