import subprocess
import time
import threading
import os
from flask import Flask
from youtube_api import get_subscribers

# Aapki Details
CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = "77cs-jw6x-yfeu-m2ks-82d6"

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Stream Status: ACTIVE</h1>"

def update_label_file():
    while True:
        try:
            subs = get_subscribers(CHANNEL_ID)
            with open("label.txt", "w") as f:
                f.write(f"LIVE SUBS: {subs}")
        except:
            pass
        time.sleep(15)

def run_ffmpeg():
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    
    command = [
        "ffmpeg",
        "-re",
        "-f", "lavfi", "-i", "color=c=purple:s=720x1280:r=20",
        "-f", "lavfi", "-i", "anullsrc",
        "-vf", "drawtext=reload=1:textfile=label.txt:fontcolor=white:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-f", "flv", rtmp_url
    ]
    subprocess.run(command)

if __name__ == "__main__":
    if not os.path.exists("label.txt"):
        with open("label.txt", "w") as f:
            f.write("Loading...")
    
    threading.Thread(target=update_label_file, daemon=True).start()
    threading.Thread(target=run_ffmpeg, daemon=True).start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
