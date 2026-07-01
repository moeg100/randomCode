import csv
import json
import os
import re
import requests
from keywords import SMART_HOME_PRODUCTS
from tqdm import tqdm

SMART_PATTERN = re.compile(
    "|".join(re.escape(p) for p in SMART_HOME_PRODUCTS),
    re.IGNORECASE,
)

CATEGORIES = [
    "raw/review_categories/Appliances.jsonl",
    "raw/review_categories/Home_and_Kitchen.jsonl",
    "raw/review_categories/Tools_and_Home_Improvement.jsonl",
    "raw/review_categories/Electronics.jsonl",
]

MAX_SCAN = 50000
MAX_PER_CAT = 200
OUTPUT = "output/amazon_reviews.csv"
TOTAL_MAX = 1000

LABELS = {
    "raw/review_categories/Appliances.jsonl": "Appliances",
    "raw/review_categories/Home_and_Kitchen.jsonl": "Home and Kitchen",
    "raw/review_categories/Tools_and_Home_Improvement.jsonl": "Tools & Home Imp.",
    "raw/review_categories/Electronics.jsonl": "Electronics",
}

def stream_category(repo_id: str, filepath: str) -> list[dict]:
    from huggingface_hub import hf_hub_url
    url = hf_hub_url(repo_id, filepath, repo_type="dataset")
    results = []
    label = LABELS.get(filepath, filepath)
    print(f"[amazon] Scanning {label} ...")
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"[amazon] Error fetching {label}: {e}")
        return results

    buffer = ""
    lines = 0
    for chunk in resp.iter_content(chunk_size=8192):
        if not chunk:
            break
        buffer += chunk.decode("utf-8", errors="replace")
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()
            if not line:
                continue
            try:
                review = json.loads(line)
            except json.JSONDecodeError:
                continue
            lines += 1
            text = (review.get("text") or "").strip()
            title = (review.get("title") or "").strip()
            rating = review.get("rating") or 0
            combined = text + " " + title
            if not SMART_PATTERN.search(combined):
                pass
            elif int(rating) <= 3:
                results.append({
                    "source": "amazon",
                    "problem_text": (text[:5000] if text else title[:5000]),
                    "category": "",
                    "rating": str(rating),
                    "timestamp": str(review.get("timestamp", "")),
                    "product_name": title[:200],
                    "device_type": label,
                })
            if len(results) >= MAX_PER_CAT or lines >= MAX_SCAN:
                break
        if len(results) >= MAX_PER_CAT or lines >= MAX_SCAN:
            break
    print(f"[amazon] {label}: {len(results)} reviews (scanned {lines} lines)")
    return results

def main():
    os.makedirs("output", exist_ok=True)
    repo_id = "McAuley-Lab/Amazon-Reviews-2023"
    keys = ["source", "problem_text", "category", "rating", "timestamp", "product_name", "device_type"]

    all_rows = []
    for filepath in CATEGORIES:
        if len(all_rows) >= TOTAL_MAX:
            break
        rows = stream_category(repo_id, filepath)
        all_rows.extend(rows)
        # write incrementally
        with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"[amazon] Saved {len(all_rows)} rows so far")

    print(f"[amazon] Done: {len(all_rows)} rows in {OUTPUT}")

if __name__ == "__main__":
    main()
