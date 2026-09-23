#!/usr/bin/env python3
"""
Generic yt-dlp Downloader Module
Handles all yt_dlp related download operations for any supported site.
"""

import os
import re
import json
import requests
import subprocess
from pathlib import Path

import yt_dlp
from yt_dlp.utils import DownloadError # Import DownloadError



def sanitize_filename(filename, max_len=150):
    """Sanitize a string to be a valid filename, including truncation."""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces and other potentially problematic characters with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'__+', '_', sanitized).strip('_') # Remove extra underscores and leading/trailing ones
    # Truncate to a reasonable length to avoid OS limits
    if len(sanitized) > max_len:
        # Keep extension if present
        name, ext = os.path.splitext(sanitized)
        if len(name) > max_len - len(ext):
            sanitized = name[:max_len - len(ext)] + ext
        else:
            sanitized = name + ext
    return sanitized


class DownloadConfig:
    """Configuration for a download task"""
    def __init__(self, url, output_path, quality="Best", audio_only=False, download_playlist=False, platform="unknown"):
        self.url = url
        self.output_path = output_path
        self.quality = quality
        self.audio_only = audio_only
        self.download_playlist = download_playlist
        self.platform = platform


def get_ffmpeg_path():
    """Get ffmpeg path from script directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_dir = os.path.join(script_dir, 'ffmpeg')
    ffmpeg_path = os.path.join(ffmpeg_dir, 'ffmpeg.exe')
    return ffmpeg_path if os.path.exists(ffmpeg_path) else None


def get_nodejs_path():
    """Get node.exe path from script directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nodejs_dir = os.path.join(script_dir, 'nodejs', 'node-v25.2.1-win-x64')
    nodejs_path = os.path.join(nodejs_dir, 'node.exe')
    return nodejs_path if os.path.exists(nodejs_path) else None


def get_cookies_file_path(platform="unknown"):
    """Get path to platform-specific cookies file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_dir = os.path.join(script_dir, 'cookies')
    cookies_file = os.path.join(cookies_dir, f'{platform}Cookies.txt')
    
    if os.path.exists(cookies_file):
        print(f"[Downloader] Found platform-specific cookies file: {cookies_file}")
        return cookies_file
    print(f"[Downloader] No specific cookies file found for platform '{platform}' at {cookies_file}")
    return None


def build_ydl_options(config, progress_hook=None):
    """Build yt-dlp options dictionary"""
    Path(config.output_path).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'overwrites': True,  # Ensure overwriting for consistent behavior
        'retries': 3,
        'fragment_retries': 3,
        'extractor_retries': 3,
        'ignoreerrors': not config.download_playlist,
        'noplaylist': not config.download_playlist,
    }

    # Use a generic filename during download, and rename later with the full title
    output_template = os.path.join(config.output_path, '%(id)s.%(ext)s')
    ydl_opts['outtmpl'] = output_template
    ydl_opts['restrictfilenames'] = True  # Sanitize filenames

    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]

    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = os.path.dirname(ffmpeg_path)

    nodejs_path = get_nodejs_path()
    if nodejs_path:
        ydl_opts['js_runtimes'] = {'node': {}}

    cookies_file = get_cookies_file_path(config.platform)
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file
        print(f"[Downloader] Using cookies from file: {cookies_file}")

    if config.audio_only:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        if config.quality == 'Best':
            print("[Downloader] Requesting quality: Best (no height limit)")
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            quality_map = {
                '8K': 4320, '4K': 2160, '2160p': 2160, '1440p': 1440,
                '1080p': 1080, '720p': 720, '480p': 480, '360p': 360,
            }
            max_height = quality_map.get(config.quality, 720)
            print(f"[Downloader] Requesting quality: {config.quality} (max height: {max_height}p)")
            ydl_opts['format'] = f'bestvideo[height<={max_height}]+bestaudio/best[height<={max_height}]/best'

        ydl_opts['merge_output_format'] = 'mp4'

    return ydl_opts


def _download_file(link, file_name, output_path):
    """Downloads a file to the specified output path."""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).content
    except requests.RequestException as e:
        print(f"Failed to open {link}: {e}")
        raise
    
    os.makedirs(output_path, exist_ok=True)
    
    with open(os.path.join(output_path, file_name), 'wb') as f:
        f.write(resp)


def _fallback_facebook_download(link, output_path):
    """Custom fallback downloader for Facebook videos."""
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    try:
        resp = requests.get(link, headers=headers)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to open {link}: {e}")
        raise

    page_content = resp.text
    video_id = link.split('/')[-2] if '/' in link else sanitize_filename(link)

    try:
        if '"dash_prefetch_experimental":[' in page_content:
            streams_json = page_content.split('"dash_prefetch_experimental":[')[1].split(']')[0]
            streams = json.loads(f"[{streams_json}]")
            video_url = streams[0]['base_url'].replace('\\', '')
            audio_url = streams[1]['base_url'].replace('\\', '')
        else:
            video_url = page_content.split('playable_url_quality_hd":"')[1].split('"')[0].replace('\\', '')
            audio_url = video_url
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Could not extract video/audio streams from page: {e}")
        raise ValueError("Could not parse video information from Facebook page.") from e

    print("Downloading video (fallback)...")
    video_filename = f"{video_id}_video.mp4"
    _download_file(video_url, video_filename, output_path)

    print("Downloading audio (fallback)...")
    audio_filename = f"{video_id}_audio.mp4"
    _download_file(audio_url, audio_filename, output_path)

    print("Merging files using FFmpeg (fallback)...")
    video_path = os.path.join(output_path, video_filename)
    audio_path = os.path.join(output_path, audio_filename)
    final_filename = f"{sanitize_filename(video_id)}.mp4"
    combined_file_path = os.path.join(output_path, final_filename)
    
    ffmpeg_exe = get_ffmpeg_path()
    if not ffmpeg_exe:
        raise FileNotFoundError("FFmpeg executable not found.")
    
    cmd = f'"{ffmpeg_exe}" -hide_banner -loglevel error -i "{video_path}" -i "{audio_path}" -c copy "{combined_file_path}"'
    subprocess.run(cmd, shell=True, check=True)

    print("Cleaning up raw files...")
    os.remove(video_path)
    os.remove(audio_path)
    
    return {'title': final_filename, 'webpage_url': link}


def download_video(config, progress_hook=None):
    """Download video with given configuration, with fallback mechanisms."""
    try:
        # This inner try-except block handles all yt-dlp attempts including cookie fallbacks
        try:
            ydl_opts = build_ydl_options(config, progress_hook)
            print(f"[Downloader] yt-dlp options: {ydl_opts}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(config.url, download=False)
                video_id = info_dict.get('id', 'unknown')
                video_ext = info_dict.get('ext', 'mp4')
                temp_filename = os.path.join(config.output_path, f"{video_id}.{video_ext}")
                ydl.download([config.url])
                
                final_title = info_dict.get('fulltitle', info_dict.get('title', video_id))
                if config.audio_only:
                    new_basename = f"{sanitize_filename(final_title)} [Audio].{video_ext}"
                else:
                    new_basename = f"{sanitize_filename(final_title)} [{config.quality}].{video_ext}"
                new_filepath = os.path.join(config.output_path, new_basename)

                if os.path.exists(temp_filename):
                    counter = 1
                    unique_new_filepath = new_filepath
                    while os.path.exists(unique_new_filepath) and unique_new_filepath != temp_filename:
                        name, ext = os.path.splitext(new_basename)
                        unique_new_filepath = os.path.join(config.output_path, f"{name}_{counter}{ext}")
                        counter += 1
                    os.rename(temp_filename, unique_new_filepath)
                    print(f"[Downloader] Renamed '{temp_filename}' to '{unique_new_filepath}'")
                return info_dict

        except DownloadError as e:
            error_msg = str(e)
            print(f"[Downloader] Primary yt-dlp attempt failed: {error_msg}")
            # Fallback to browser cookies if authentication seems to be the issue
            if 'Sign in to confirm' in error_msg or 'bot detection' in error_msg.lower() or 'Private video' in error_msg:
                print("[Downloader] Authentication/bot detection suspected. Trying browser cookies...")
                try:
                    ydl_opts_with_cookies = build_ydl_options(config, progress_hook)
                    ydl_opts_with_cookies['cookiesfrombrowser'] = ('chrome', 'edge', 'firefox', 'opera')
                    with yt_dlp.YoutubeDL(ydl_opts_with_cookies) as ydl_cookies:
                        info_dict = ydl_cookies.extract_info(config.url, download=True)
                        print("[Downloader] Download successful using browser cookies.")
                        # Manually rename after cookie download, as ydl.download doesn't return info_dict
                        # This part might need adjustment based on how the post-download renaming is handled
                        return ydl_cookies.extract_info(config.url, download=False)
                except DownloadError as cookie_error:
                    print(f"[Downloader] All browser cookie attempts failed: {cookie_error}")
                    raise e # Re-raise original DownloadError to be caught by outer block
            raise e # Re-raise original error if it's not an auth issue

    except DownloadError as e:
        # This block is entered if ALL yt-dlp attempts failed.
        if config.platform == 'facebook':
            print("[Downloader] All yt-dlp attempts failed. Falling back to custom Facebook downloader.")
            try:
                # The fallback function will raise its own errors if it fails
                return _fallback_facebook_download(config.url, config.output_path)
            except Exception as fb_error:
                print(f"[Downloader] Custom Facebook fallback also failed: {fb_error}")
                raise e # Raise the original yt-dlp error
        
        # If not facebook, or if facebook fallback failed, re-raise the original error.
        raise e

    except Exception as e:
        import traceback
        print("[Downloader] An unexpected Python error occurred during download:")
        traceback.print_exc()
        raise e

