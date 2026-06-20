import json
import os
from graph.state import JobState
from tools.fetcher import fetch_listings
from tools.scorer import score_jobs


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
    print(">> Node 3: Scoring jobs with ModernBERT...")
    try:
        analyzed = score_jobs(state["jobs"])
        print(f"   Scored {len(analyzed)} jobs")
        return {"analyzed": analyzed, "errors": []}
    except Exception as e:
        print(f"   Scoring failed: {e}")
        return {"analyzed": [], "errors": [str(e)]}


def store_results_node(state: JobState) -> dict:
    print(">> Node 4: Saving results...")
    path = "data/results.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(state["analyzed"], f, indent=2)
    print(f"   Saved {len(state['analyzed'])} results to {path}")
    return {}