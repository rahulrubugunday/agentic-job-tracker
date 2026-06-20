import os
import json
from graph.state import JobState
from tools.fetcher import fetch_listings


def fetch_jobs_node(state: JobState) -> dict:
    print(">> Node 1: Fetching jobs from Simplify...")
    jobs = fetch_listings(limit=10)
    print(f"   Fetched {len(jobs)} active jobs")
    return {"jobs": jobs}


def filter_jobs_node(state: JobState) -> dict:
    print(">> Node 2: Filtering jobs...")
    filtered = [
        job for job in state["jobs"]
        if job["active"] and job["role"] and job["company"]
    ]
    print(f"   {len(filtered)} jobs passed filter")
    return {"jobs": filtered}


def analyze_fit_node(state: JobState) -> dict:
    print(">> Node 3: Reading Colab results...")
    path = "data/results.json"
    if not os.path.exists(path):
        print("   No results.json found. Run the Colab notebook first.")
        return {"analyzed": [], "errors": ["Run Colab notebook first"]}
    with open(path) as f:
        analyzed = json.load(f)
    print(f"   Loaded {len(analyzed)} analyzed jobs from Colab output")
    return {"analyzed": analyzed, "errors": []}


def store_results_node(state: JobState) -> dict:
    print(">> Node 4: Results already stored by Colab.")
    return {}