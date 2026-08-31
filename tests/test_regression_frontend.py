import os
import pytest

def test_frontend_index_exists():
    path = os.path.join("frontend", "index.html")
    assert os.path.exists(path), "frontend/index.html must exist"

def test_frontend_contains_header_and_dashboard():
    path = os.path.join("frontend", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<header" in content or "header" in content.lower()
    assert "dashboard" in content.lower()
    assert "id=\"theme-toggle\"" in content or "class=\"theme-toggle\"" in content or "theme" in content.lower()
