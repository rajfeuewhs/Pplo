import subprocess
import time
import os
from youtube_api import get_subscribers

CHANNEL_ID = "UCr5ik3Qjslqnl6DB8XwJxDg"
STREAM_KEY = os.getenv("STREAM_KEY")
SUB_GOAL = 50

def run_ffmpeg():
    # GitHub ka network fast hai, direct RTMP bilkul sahi chalega
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    
    # Label file setup
    def update_text():
        try:
            subs = get_subscribers(CHANNEL_ID)
            with open("subs.txt", "w") as f:
                f.write(str(subs))
        except:
            pass

    update_text() # Initial fetch

    command = [
        "ffmpeg", "-re", "-loop", "1", "-i", "bg.jpg",
        "-f", "lavfi", "-i", "anullsrc",
        "-vf", (
            "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
            "drawbox=y=(h-400)/2:w=w:h=400:color=black@0.4:t=fill,"
            "drawtext=text='LIVE SUBSCRIBERS':fontcolor=yellow:fontsize=50:x=(w-text_w)/2:y=(h-text_h)/2-120,"
            "drawtext=reload=1:textfile=subs.txt:fontcolor=white:fontsize=180:x=(w-text_w)/2:y=(h-text_h)/2,"
            f"drawtext=text='TARGET GOAL\: {SUB_GOAL}':fontcolor=cyan:fontsize=45:x=(w-text_w)/2:y=(h-text_h)/2+130"
        ),
        "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "2500k",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-f", "flv", rtmp_url
    ]
    
    # background thread to update sub count every 30s
    def timer_task():
        while True:
            time.sleep(30)
            update_text()
            
    import threading
    threading.Thread(target=timer_task, daemon=True).start()
    
    subprocess.run(command)

if __name__ == "__main__":
    run_ffmpeg()
