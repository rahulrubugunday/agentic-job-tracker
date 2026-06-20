import requests

LISTINGS_URL = "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/.github/scripts/listings.json"

def fetch_listings(limit: int = 10) -> list[dict]:
    response = requests.get(LISTINGS_URL, timeout=10)
    response.raise_for_status()
    jobs = response.json()

    active_jobs = [
        {
            "id": job.get("id", ""),
            "company": job.get("company_name", "Unknown"),
            "role": job.get("title", "Unknown"),
            "location": ", ".join(job.get("locations", ["Remote"])),
            "url": job.get("url", ""),
            "active": job.get("active", False),
            "date_updated": job.get("date_updated", 0),
        }
        for job in jobs
        if job.get("active", False)
    ]

    return active_jobs[:limit]


if __name__ == "__main__":
    jobs = fetch_listings(limit=5)
    for job in jobs:
        print(f"{job['company']} — {job['role']} — {job['location']}")