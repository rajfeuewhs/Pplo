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
    return "<h1>Professional Counter Stream: ACTIVE</h1>"

def update_label():
    while True:
        try:
            subs = get_subscribers(CHANNEL_ID)
            # Sirf number save karenge taaki design clean rahe
            with open("subs.txt", "w") as f:
                f.write(str(subs))
        except:
            pass
        time.sleep(15)

def run_ffmpeg():
    # Direct IP for stability
    rtmp_url = f"rtmp://199.223.232.122/live2/{STREAM_KEY}"
    
    # Static Image (bg.jpg)
    bg_input = "-f lavfi -i color=c=purple:s=720x1280:r=15"
    if os.path.exists("bg.jpg"):
        bg_input = "-loop 1 -i bg.jpg"

    command = [
        "ffmpeg", "-re",
        *bg_input.split(),
        "-f", "lavfi", "-i", "anullsrc",
        "-vf", (
            "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
            # BOX BACKGROUND: Center mein ek halka black box taaki text chamke
            "drawbox=y=(h-400)/2:w=w:h=400:color=black@0.4:t=fill,"
            # 1. TOP LABEL (Yellow)
            "drawtext=text='LIVE SUBSCRIBERS':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2-120,"
            # 2. MAIN COUNT (Bada White Number)
            "drawtext=reload=1:textfile=subs.txt:fontcolor=white:fontsize=180:x=(w-text_w)/2:y=(h-text_h)/2,"
            # 3. BOTTOM GOAL (Cyan)
            f"drawtext=text='TARGET GOAL\: {SUB_GOAL}':fontcolor=cyan:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+130"
        ),
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-g", "30", "-b:v", "2000k", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-f", "flv", 
        "-tls_verify", "0",
        rtmp_url
    ]
    
    while True:
        subprocess.run(command)
        time.sleep(5)

if __name__ == "__main__":
    if not os.path.exists("subs.txt"):
        with open("subs.txt", "w") as f:
            f.write("0")
    threading.Thread(target=update_label, daemon=True).start()
    threading.Thread(target=run_ffmpeg, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
