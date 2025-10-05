import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import os

def generate_transcript(video_url):
    cookie_path = "cookies.txt"
    if not os.path.exists(cookie_path):
        return {"status": "error", "message": f"Cookie file not found at {cookie_path}"}

    ydl_opts = {
        "quiet": True,
        "cookiefile": cookie_path,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "noplaylist": True,
        "retries": 3,
        "fragment_retries": 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_id = info.get("id")
            title = info.get("title")

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([x["text"] for x in transcript])
            return {
                "status": "success",
                "video_title": title,
                "video_id": video_id,
                "transcript": text
            }
        except TranscriptsDisabled:
            return {"status": "error", "message": "Transcripts are disabled for this video."}
        except NoTranscriptFound:
            return {"status": "error", "message": "No transcript available for this video."}
        except Exception as e:
            return {"status": "error", "message": f"Transcript fetch failed: {str(e)}"}

    except Exception as e:
        return {"status": "error", "message": f"yt-dlp failed: {str(e)}"}
