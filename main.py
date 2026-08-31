import json
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pypdf import PdfReader
from graph.graph import build_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


@app.post("/analyze")
async def analyze(resume: UploadFile = File(None)):
    profile_text = None
    if resume:
        contents = await resume.read()
        import io
        reader = PdfReader(io.BytesIO(contents))
        extracted_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
        if extracted_text:
            profile_text = "\n".join(extracted_text)

    graph = build_graph()
    initial_state = {
        "jobs": [],
        "analyzed": [],
        "errors": [],
        "profile_text": profile_text
    }
    result = graph.invoke(initial_state)
    return {
        "analyzed": result["analyzed"],
        "errors": result["errors"],
        "total": len(result["analyzed"])
    }


@app.get("/results")
def get_results():
    path = "data/results.json"
    if not os.path.exists(path):
        return {"analyzed": [], "message": "No results yet. Run /analyze first."}
    with open(path) as f:
        data = json.load(f)
    return {"analyzed": data, "total": len(data)}
