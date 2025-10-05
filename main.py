from fastapi import FastAPI
from get_transcript import generate_transcript
from cookies_helper import ensure_cookies_file
from index import build_chain
import logging

app = FastAPI()
logger = logging.getLogger("main")

cache = {}

@app.on_event("startup")
def on_startup():
    cookies_path = ensure_cookies_file()
    if cookies_path:
        logger.info(f"Using cookies from {cookies_path}")
    else:
        logger.warning("No valid cookies found. Some YouTube videos may fail.")

@app.get("/generate")
def generate(url: str, query: str = None):
    if url not in cache:
        transcript = generate_transcript(url)
        if not transcript:
            return {"error": "Transcript unavailable"}
        cache[url] = build_chain(transcript)

    if query:
        try:
            return {"answer": cache[url].invoke(query)}
        except Exception as e:
            return {"error": str(e)}

    return {"message": "Transcript ready. Add &query=your+question"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
