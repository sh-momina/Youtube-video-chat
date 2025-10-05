# get_transcript.py
import os
import yt_dlp
import openai
from dotenv import load_dotenv
from cookies_helper import ensure_cookies_file

load_dotenv()  

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
    # ensure cookies.txt exists if env var (writes file from env)
    cookies_path = ensure_cookies_file()

    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "audio.%(ext)s",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "cookiefile": cookies_path if cookies_path else None,
    "quiet": True,
}
    
    if cookies_path:
        # Python yt-dlp option for cookie file
        ydl_opts["cookiefile"] = cookies_path

    audio_file = "audio.mp3"
    transcript = ""

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)

        # Ensure only one audio.mp3 exists
        if os.path.exists(audio_file):
            os.remove(audio_file)
        os.rename(filename, audio_file)

    # Split & transcribe
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
        # cleanup
        for chunk in chunks:
            if os.path.exists(chunk):
                os.remove(chunk)
        if os.path.exists(audio_file):
            os.remove(audio_file)

    with open("transcript.txt", "w", encoding="utf-8") as out:
        out.write(transcript)

    return transcript
