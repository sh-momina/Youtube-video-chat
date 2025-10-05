import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """
    Extracts YouTube video ID from various link formats.
    """
    parsed_url = urlparse(url)
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip('/')
    query = parse_qs(parsed_url.query)
    return query.get('v', [None])[0]

def generate_transcript(video_url: str):
    """
    Downloads metadata using yt-dlp and transcript (if available) for a YouTube video.
    Falls back gracefully if login or cookies are required.
    """
    video_id = extract_video_id(video_url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}

    # Make sure cookies.txt exists
    cookie_path = "cookies.txt"
    if not os.path.exists(cookie_path):
        return {"error": "cookies.txt file not found. Please add it to your project root."}

    # yt-dlp options with cookies
    ydl_opts = {
        'cookiefile': cookie_path,
        'quiet': True,
        'nocheckcertificate': True,
        'noplaylist': True,
        'geo_bypass': True,
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'retries': 5,
        'fragment_retries': 5,
    }

    info = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
    except yt_dlp.utils.DownloadError as e:
        error_message = str(e)
        if "Sign in to confirm you’re not a bot" in error_message:
            return {"error": "YouTube is asking for login verification. Try refreshing your cookies.txt."}
        else:
            return {"error": f"yt-dlp failed: {error_message}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

    # Get transcript if available
    transcript_text = ""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript_list])
    except (TranscriptsDisabled, NoTranscriptFound):
        transcript_text = "Transcript not available for this video."
    except Exception as e:
        transcript_text = f"Error fetching transcript: {str(e)}"

    return {
        "title": info.get("title", "Unknown Title"),
        "uploader": info.get("uploader", "Unknown Uploader"),
        "duration": info.get("duration", 0),
        "transcript": transcript_text
    }
