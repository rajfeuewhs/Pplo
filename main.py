import subprocess
import time
import threading
import os
from flask import Flask
from youtube_api import get_subscribers

# Details
CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = os.getenv("STREAM_KEY", "77cs-jw6x-yfeu-m2ks-82d6") 
SUB_GOAL = 50 

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Render Anti-Block Stream: ACTIVE</h1>"

def update_label():
    while True:
        try:
            subs = get_subscribers(CHANNEL_ID)
            with open("subs.txt", "w") as f:
                f.write(str(subs))
        except:
            pass
        time.sleep(30)

def run_ffmpeg():
    # RTMPS (Secure Port 443) use kar rahe hain bypass ke liye
    rtmps_url = f"rtmps://a.rtmps.youtube.com:443/live2/{STREAM_KEY}"
    
    bg_input = "-f lavfi -i color=c=purple:s=720x1280:r=5"
    if os.path.exists("bg.jpg"):
        bg_input = "-loop 1 -i bg.jpg"

    command = [
        "ffmpeg", "-re",
        *bg_input.split(),
        "-f", "lavfi", "-i", "anullsrc",
        "-vf", (
            "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
            "drawbox=y=(h-400)/2:w=w:h=400:color=black@0.4:t=fill,"
            "drawtext=text='LIVE SUBSCRIBERS':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2-120,"
            "drawtext=reload=1:textfile=subs.txt:fontcolor=white:fontsize=180:x=(w-text_w)/2:y=(h-text_h)/2,"
            f"drawtext=text='TARGET GOAL\: {SUB_GOAL}':fontcolor=cyan:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+130"
        ),
        "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
        "-r", "5", "-g", "10", "-b:v", "500k", "-pix_fmt", "yuv420p", 
        "-c:a", "aac", "-f", "flv", 
        rtmps_url
    ]
    
    while True:
        print("--- Connecting via Port 443 (Secure) ---")
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
