import os
import pytest

def test_e2e_ui_header_rendering_and_positioning():
    path = os.path.join("frontend", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Verify flexbox alignment and header placement
    assert "display: flex" in html or "display:flex" in html.replace(" ", "")
    assert "justify-content: space-between" in html or "justify-content:space-between" in html.replace(" ", "")
    
    # Verify title is positioned within the header element on the left (first child or before actions)
    header_start = html.find("<header>")
    header_end = html.find("</header>")
    assert header_start != -1 and header_end != -1
    
    header_content = html[header_start:header_end]
    title_pos = header_content.find("Agentic Job Tracker")
    actions_pos = header_content.find("header-actions")
    
    assert title_pos != -1
    assert actions_pos != -1
    assert title_pos < actions_pos, "Project title must be positioned on the left side before header actions"
