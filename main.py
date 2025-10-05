from fastapi import FastAPI, Request
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
def generate(request: Request, url: str, query: str):
    result = generate_transcript(url)
    if "error" in result:
        return {"status": "error", "message": result["error"]}
    return {"status": "success", "data": result}

    if query:
        try:
            return {"answer": cache[url].invoke(query)}
        except Exception as e:
            return {"error": str(e)}

    return {"message": "Transcript ready. Add &query=your+question"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
