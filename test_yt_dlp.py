import yt_dlp
import os

url = "https://www.facebook.com/reel/1097113862285129"
script_dir = os.path.dirname(os.path.abspath(__file__))
cookiefile = os.path.join(script_dir, 'cookies', 'facebookCookies.txt')

# Ensure the directories exist
os.makedirs(os.path.join(script_dir, 'cookies'), exist_ok=True)
os.makedirs(os.path.join(script_dir, 'downloads', 'video'), exist_ok=True)


ydl_opts = {
    'verbose': True, # This is key for debugging
    'overwrites': True,
    'retries': 3,
    'fragment_retries': 3,
    'extractor_retries': 3,
    'ignoreerrors': False, # Set to False to get full traceback
    'noplaylist': True,
    'outtmpl': os.path.join(script_dir, 'downloads', 'video', '%(title)s [Best].%(ext)s'),
    'restrictfilenames': True,
    'ffmpeg_location': os.path.join(script_dir, 'ffmpeg'),
    'js_runtimes': {'node': {}},
    'cookiefile': cookiefile,
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4'
}

print(f"Testing yt-dlp with URL: {url}")
print(f"Using cookiefile: {cookiefile}")
print(f"yt-dlp options: {ydl_opts}")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        print("Successfully extracted info (download=False):")
        print(info_dict)
except Exception as e:
    print(f"An error occurred during yt-dlp info extraction: {e}")
    import traceback
    traceback.print_exc()

