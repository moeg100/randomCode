import time
import re
import requests
from bs4 import BeautifulSoup
from collections import defaultdict, deque
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser


HEADERS = {
    "User-Agent": "MiniCrawler/1.0 (educational)"
}



def normalize(url):
    parsed = urlparse(url)

    # remove fragment (#something)
    parsed = parsed._replace(fragment="")

    # fix empty path
    path = parsed.path or "/"

    return urlunparse(parsed._replace(path=path))



robots_cache = {}

def allowed(url):
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    if base not in robots_cache:
        rp = RobotFileParser()
        try:
            rp.set_url(urljoin(base, "/robots.txt"))
            rp.read()
        except:
            rp = None
        robots_cache[base] = rp

    rp = robots_cache[base]
    if rp is None:
        return True

    return rp.can_fetch(HEADERS["User-Agent"], url)


# -------------------------
# PARSER / TEXT EXTRACTION
# -------------------------
def extract(html, parser="lxml"):
    soup = BeautifulSoup(html, parser)

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    words = re.findall(r"[a-zA-Z]+", text.lower())

    links = set()
    for a in soup.find_all("a", href=True):
        links.add(a["href"])

    return words, links



def crawl(seed, max_depth=2, delay=0.5, parser="lxml"):
    queue = deque([(seed, 0)])
    visited = set()

    index = defaultdict(set)
    pages = {}

    while queue:
        url, depth = queue.popleft()
        url = normalize(url)

        if url in visited:
            continue
        visited.add(url)

        if depth > max_depth:
            continue

        if not allowed(url):
            print("Blocked by robots:", url)
            continue

        try:
            r = requests.get(url, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                continue

            words, links = extract(r.text, parser=parser)
            pages[url] = r.text

            # build inverted index
            for w in words:
                index[w].add(url)

            print(f"Crawled [{depth}]: {url} ({len(words)} words)")

            # follow links
            if depth < max_depth:
                for link in links:
                    full = normalize(urljoin(url, link))
                    if full.startswith("http"):
                        queue.append((full, depth + 1))

            time.sleep(delay)

        except Exception as e:
            print("Error:", url, e)

    return pages, index


def search(query, index):
    words = query.lower().split()

    results = None

    for w in words:
        if w in index:
            if results is None:
                results = index[w]
            else:
                results = results & index[w]
        else:
            return set()

    return results or set()

if __name__ == "__main__":
    seed_url = input("Enter the URL : ")

    pages, index = crawl(
        seed=seed_url,
        max_depth=2,
        delay=0.5,
        parser="lxml"   # change to "html.parser" if needed
    )

    print("\nSearch results:")
    results = search("example domain", index)

    for r in results:
        print(r)
