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
def generate(request: Request, url: str, query: str = None):
    """
    Generate transcript and optionally process a query.
    """
    try:
        result = generate_transcript(url)

        # Handle both dict and string types
        if isinstance(result, dict):
            if "error" in result:
                return {"status": "error", "message": result["error"]}
            else:
                transcript_text = result.get("transcript", "")
        else:
            transcript_text = str(result)

        # Build chain or process query if provided
        if query:
            try:
                if url not in cache:
                    cache[url] = build_chain(transcript_text)
                answer = cache[url].invoke(query)
                return {"status": "success", "answer": answer}
            except Exception as e:
                return {"status": "error", "message": f"Query failed: {str(e)}"}

        return {"status": "success", "data": transcript_text}

    except Exception as e:
        return {"status": "error", "message": f"Internal error: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
