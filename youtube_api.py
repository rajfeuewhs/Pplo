import requests

[span_2](start_span)API_KEY = "AIzaSyB1kbXAnaSOc_Oxu6n7DJD-jwMABDqGMtk"[span_2](end_span)

def get_subscribers(channel_id):
    [span_3](start_span)url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}"[span_3](end_span)
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            [span_4](start_span)return data["items"][0]["statistics"]["subscriberCount"][span_4](end_span)
        return "0"
    except Exception:
        return "Updating..."
