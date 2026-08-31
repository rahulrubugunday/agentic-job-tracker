import os
import pytest

def test_theme_toggle_end_to_end_structure():
    path = os.path.join("frontend", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify acceptance criteria elements are present in the full single-file frontend
    assert "top" in html or "right" in html
    assert "light" in html.lower()
    assert "dark" in html.lower()
    assert "onclick" in html.lower() or "addEventListener" in html
