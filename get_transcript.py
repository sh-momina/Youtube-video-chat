import yt_dlp
import os
import openai
from dotenv import load_dotenv

load_dotenv()


def split_file(file_path, max_chunk_size=25 * 1024 * 1024):
    """Split a file into smaller chunks (25 MB default)."""
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
    """Download YouTube audio, transcribe, and clean up temporary files."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
    }

    audio_file = "audio.mp3"

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        filename = ydl.prepare_filename(info)

        # Ensure only one audio.mp3 exists
        if os.path.exists(audio_file):
            os.remove(audio_file)

        os.rename(filename, audio_file)

    transcript = ""
    chunks = split_file(audio_file)

    try:
        # Transcribe chunks
        for i, chunk in enumerate(chunks):
            with open(chunk, "rb") as f:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language="en"
                )
                transcript += f"\n--- Chunk {i+1} ---\n" + response.text

    finally:
        # Clean up temp files (chunks + main audio)
        for chunk in chunks:
            if os.path.exists(chunk):
                os.remove(chunk)
        if os.path.exists(audio_file):
            os.remove(audio_file)

    return transcript
