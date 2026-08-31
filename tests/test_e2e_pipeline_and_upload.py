import os
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
from main import app

client = TestClient(app)

@patch("tools.scorer._get_embedding")
@patch("tools.scorer.cosine_similarity")
@patch("graph.nodes.fetch_listings")
def test_e2e_analyze_with_custom_resume_pdf(mock_fetch_listings, mock_cosine, mock_get_embedding):
    """End-to-end test exercising the upload resume endpoint, PDF parsing, graph execution, and job scoring pipeline."""
    mock_fetch_listings.return_value = [
        {"company": "Global AI", "role": "Senior ML Engineer", "location": "San Francisco", "active": True}
    ]
    mock_get_embedding.return_value = np.array([[0.5, 0.5, 0.5]])
    mock_cosine.return_value = np.array([[0.92]])

    # Create dummy bytes simulating a PDF file or use a small mock PDF content
    dummy_pdf_content = b"%PDF-1.4 mock pdf resume content for testing multi-user dynamic upload"
    
    response = client.post(
        "/analyze",
        files={
            "resume": ("test_resume.pdf", dummy_pdf_content, "application/pdf")
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "analyzed" in data
    assert "errors" in data
    assert data["total"] == 1
    assert data["analyzed"][0]["company"] == "Global AI"
    assert data["analyzed"][0]["score"] == 92
