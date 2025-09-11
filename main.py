from fastapi import FastAPI
from get_transcript import generate_transcript
from index import build_chain

app = FastAPI()

cache = {}

@app.get("/")
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