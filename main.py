import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
def analyze():
    graph = build_graph()
    initial_state = {
        "jobs": [],
        "analyzed": [],
        "errors": []
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