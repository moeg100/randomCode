import csv
import json
import os
import re
import requests
from keywords import SMART_HOME_PRODUCTS, PROBLEM_PHRASES

SMART_PATTERN = re.compile(
    "|".join(re.escape(p) for p in SMART_HOME_PRODUCTS),
    re.IGNORECASE,
)
PROBLEM_PATTERN = re.compile(
    "|".join(re.escape(p) for p in PROBLEM_PHRASES),
    re.IGNORECASE,
)

SUBREDDITS = ["smarthome", "homeautomation", "IoT"]
HEADERS = {"User-Agent": "IoTCollector/1.0 (Linux)"}
MAX_PER = 200
OUTPUT = "output/reddit_posts.csv"
TOTAL_MAX = 1000

def fetch_feed(sub: str, sort: str = "hot") -> list[dict]:
    results = []
    try:
        url = f"https://www.reddit.com/r/{sub}/{sort}.json?limit=100"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return results
        data = resp.json()
    except Exception:
        return results

    for child in data.get("data", {}).get("children", []):
        if child["kind"] != "t3":
            continue
        p = child["data"]
        title = (p.get("title") or "").strip()
        selftext = (p.get("selftext") or "").strip()
        combined = title + " " + selftext
        if not SMART_PATTERN.search(combined) or not PROBLEM_PATTERN.search(combined):
            continue
        body = selftext if selftext and len(selftext) > 20 else title
        results.append({
            "source": "reddit",
            "problem_text": body[:5000],
            "category": "",
            "rating": "",
            "timestamp": str(p.get("created_utc", "")),
            "product_name": title[:200],
            "device_type": f"r/{sub}",
        })
    return results

def main():
    os.makedirs("output", exist_ok=True)
    keys = ["source", "problem_text", "category", "rating", "timestamp", "product_name", "device_type"]

    all_rows = []
    for sub in SUBREDDITS:
        if len(all_rows) >= TOTAL_MAX:
            break
        for sort in ("hot", "new", "top"):
            if len(all_rows) >= MAX_PER:
                break
            rows = fetch_feed(sub, sort)
            for r in rows:
                if len(all_rows) >= MAX_PER:
                    break
                all_rows.append(r)
        print(f"[reddit] r/{sub}: {sum(1 for r in all_rows if r['device_type'] == f'r/{sub}')} posts")

    if all_rows:
        with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"[reddit] Saved {len(all_rows)} rows to {OUTPUT}")
    else:
        print("[reddit] No posts found")

if __name__ == "__main__":
    main()
