import os
import pytest
from fastapi.testclient import TestClient
from main import app
from tools.scorer import score_jobs

client = TestClient(app)

def test_regression_score_jobs_default_profile(monkeypatch):
    """Confirm that score_jobs successfully reads data/profile.txt when no profile_text is explicitly passed."""
    # Mock _get_embedding so it doesn't load real ML weights in unit tests
    import numpy as np
    monkeypatch.setattr("tools.scorer._get_embedding", lambda text: np.array([[0.1, 0.2, 0.3]])) 
    monkeypatch.setattr("tools.scorer.cosine_similarity", lambda a, b: np.array([[0.8]])) 
    
    sample_jobs = [
        {"company": "TechCorp", "role": "Software Engineer", "location": "Remote", "active": True},
        {"company": "AI Startup", "role": "Machine Learning Engineer", "location": "New York", "active": True}
    ]
    
    scored = score_jobs(sample_jobs)
    assert len(scored) == 2
    assert scored[0]["company"] == "TechCorp"
    assert "score" in scored[0]
    assert "resume" in scored[0]
    assert "reasoning" in scored[0]


def test_regression_main_endpoints():
    """Confirm basic main endpoints work correctly and return expected structures."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    response_results = client.get("/results")
    assert response_results.status_code == 200
    assert "analyzed" in response_results.json()
