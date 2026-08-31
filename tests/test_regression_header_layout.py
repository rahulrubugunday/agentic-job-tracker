import os
import pytest

def test_header_left_title_regression():
    path = os.path.join("frontend", "index.html")
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Assert structure and header elements exist and title is present
    assert "<header>" in content
    assert "Agentic Job Tracker" in content
    assert "header-title" in content
