import os
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "profile.txt")

MLE_KEYWORDS = [
    "machine learning", "deep learning", "ml", "ai", "nlp", "computer vision",
    "neural", "model", "research", "data science", "pytorch", "tensorflow",
    "embedding", "transformer", "llm", "scientist"
]

_tokenizer = None
_model = None
_device = None


def _load_model():
    global _tokenizer, _model, _device
    if _model is not None:
        return _tokenizer, _model, _device
    from transformers import AutoTokenizer, AutoModel
    print("   Loading ModernBERT (first run takes ~1 min)...")
    _device = "cuda" if torch.cuda.is_available() else "cpu"
    _tokenizer = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
    _model = AutoModel.from_pretrained("answerdotai/ModernBERT-base").to(_device)
    _model.eval()
    print(f"   ModernBERT loaded on {_device.upper()}")
    return _tokenizer, _model, _device


def _get_embedding(text: str) -> np.ndarray:
    tokenizer, model, device = _load_model()
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy()


def _recommend_resume(role: str) -> str:
    role_lower = role.lower()
    if any(kw in role_lower for kw in MLE_KEYWORDS):
        return "MLE"
    return "SWE"


def _build_reasoning(score: int, resume: str, company: str, role: str) -> str:
    if score >= 75:
        fit = "strong fit"
    elif score >= 50:
        fit = "moderate fit"
    else:
        fit = "weak fit"
    return f"{company} — {role} is a {fit} at {score}% similarity. Recommend {resume} resume."


def score_jobs(jobs: list) -> list:
    with open(PROFILE_PATH) as f:
        profile_text = f.read()

    profile_embedding = _get_embedding(profile_text)

    results = []
    for job in jobs:
        job_text = f"{job['company']} {job['role']} {job.get('location', '')}"
        job_embedding = _get_embedding(job_text)
        similarity = cosine_similarity(profile_embedding, job_embedding)[0][0]
        score = max(0, min(100, round(float(similarity) * 100)))
        resume = _recommend_resume(job["role"])
        reasoning = _build_reasoning(score, resume, job["company"], job["role"])
        results.append({**job, "score": score, "resume": resume, "reasoning": reasoning})
        print(f"   {job['company']} — {job['role']} — {score}% — {resume}")

    return results
