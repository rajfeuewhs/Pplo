import requests

# Aapki API Key yahan set hai
API_KEY = "AIzaSyB1kbXAnaSOc_Oxu6n7DJD-jwMABDqGMtk"

def get_subscribers(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["statistics"]["subscriberCount"]
        return "0"
    except Exception:
        return "Updating..."
