# get_transcript.py
import os
import yt_dlp
import openai
import base64
import tempfile
from dotenv import load_dotenv

load_dotenv()  # load .env file

def split_file(file_path, max_chunk_size=25 * 1024 * 1024):
    chunks = []
    with open(file_path, "rb") as f:
        i = 0
        while True:
            data = f.read(max_chunk_size)
            if not data:
                break
            chunk_path = f"chunk_{i}.mp3"
            with open(chunk_path, "wb") as c:
                c.write(data)
            chunks.append(chunk_path)
            i += 1
    return chunks

def generate_transcript(video_url: str):
    # 🔹 Get encoded cookies from .env
    encoded_cookies = os.getenv("YOUTUBE_COOKIES_B64")

    cookies_path = None
    if encoded_cookies:
        decoded = base64.b64decode(encoded_cookies)
        # Write decoded cookies into a temporary file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        tmp.write(decoded)
        tmp.close()
        cookies_path = tmp.name
        print("Using cookies from:", cookies_path)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "quiet": True,
    }
    if cookies_path:
        # yt-dlp option for passing cookies file
        ydl_opts["cookiefile"] = cookies_path

    audio_file = "audio.mp3"
    transcript = ""

    # 🔹 Download audio using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)

        # Ensure only one audio.mp3 exists
        if os.path.exists(audio_file):
            os.remove(audio_file)
        os.rename(filename, audio_file)

    # 🔹 Split & transcribe audio
    chunks = split_file(audio_file)
    try:
        for i, chunk in enumerate(chunks):
            with open(chunk, "rb") as f:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language="en"
                )
                transcript += f"\n--- Chunk {i+1} ---\n" + response.text
    finally:
        # Cleanup temporary files
        for chunk in chunks:
            if os.path.exists(chunk):
                os.remove(chunk)
        if os.path.exists(audio_file):
            os.remove(audio_file)
        if cookies_path and os.path.exists(cookies_path):
            os.remove(cookies_path)

    # 🔹 Save transcript to file
    with open("transcript.txt", "w", encoding="utf-8") as out:
        out.write(transcript)

    return transcript

# For quick testing
# if __name__ == "__main__":
#     url = "https://youtu.be/8SdR5i3ZoqE?si=WNK6Sas1pJADS5DX"
#     transcript = generate_transcript(url)
#     print("Transcript length:", len(transcript))
#     print("First 500 chars:\n", transcript[:500])
