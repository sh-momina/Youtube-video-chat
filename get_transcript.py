import yt_dlp
import os
from pydub import AudioSegment
import openai
from dotenv import load_dotenv

load_dotenv()

def split_audio(file_path, max_chunk_size=25 * 1024 * 1024): 
    audio = AudioSegment.from_mp3(file_path)
    chunk_length_ms = 5 * 60 * 1000  
    chunks = []
    i = 0

    while len(audio[i * chunk_length_ms:]) > 0:
        chunk = audio[i * chunk_length_ms:(i + 1) * chunk_length_ms]
        chunk_path = f"chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        if os.path.getsize(chunk_path) > max_chunk_size:
            raise Exception(f"Chunk {i} is still too large. Reduce chunk length.")
        chunks.append(chunk_path)
        i += 1

    return chunks

def generate_transcript(video_url: str):
    output_dir = os.getcwd()
    output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        downloaded_file = ydl.prepare_filename(info).replace('.webm', '.mp3')
        audio_file = "audio.mp3"
        os.rename(downloaded_file, audio_file)

    file_size = os.path.getsize(audio_file)
    print("Transcribing audio...")

    transcript_text = ""

    if file_size > 25 * 1024 * 1024:
        print("splitting into chunks...")
        chunks = split_audio(audio_file)
    else:
        chunks = [audio_file]

    for i, chunk in enumerate(chunks):
        with open(chunk, "rb") as f:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="en"
            )
            transcript_text += f"\n--- Chunk {i + 1} ---\n" + response.text

    os.remove(audio_file)
    for chunk_file in chunks:
        if chunk_file != audio_file:
            os.remove(chunk_file)

    return transcript_text
