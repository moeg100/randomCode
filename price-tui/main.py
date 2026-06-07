#!/usr/bin/env python3
"""RAM & Gas Price Tracker - A Textual TUI"""

import asyncio
import os
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button, DataTable, Footer, Header, Input, Label, RichLog, Select, TabbedContent, TabPane, TextArea,
)

RAM_URL = "https://www.newegg.com/p/pl?d=ddr5+ddr4+ram&N=100007611"
GAS_URL = "https://gasprices.aaa.com/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
SAVE_DIR = os.path.expanduser("~/.local/share/price-tui")


def ensure_save_dir():
    os.makedirs(SAVE_DIR, exist_ok=True)


async def fetch_ram_prices():
    async with httpx.AsyncClient(follow_redirects=True, timeout=25) as client:
        resp = await client.get(RAM_URL, headers={"User-Agent": UA})
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for item in soup.select(".item-cell"):
        title_el = item.select_one(".item-title")
        price_el = item.select_one(".price-current")
        name = title_el.get_text(strip=True) if title_el else "-"
        price = re.sub(r"[^\d.$]", "", price_el.get_text(strip=True)) if price_el else "-"
        if name == "-" or not name:
            continue
        typ = "DDR5" if "DDR5" in name.upper() else ("DDR4" if "DDR4" in name.upper() else "")
        speed = ""
        mhz = re.search(r"(\d{4,5})\s*MHz", name, re.IGNORECASE)
        if mhz:
            speed = f"{mhz.group(1)} MHz"
        modules = ""
        m = re.search(r"(\d+)\s*x\s*(\d+\s*GB)", name, re.IGNORECASE)
        if m:
            modules = f"{m.group(1)} x {m.group(2)}"
        else:
            m2 = re.search(r"(\d+\s*GB)\s*\(.*?(\d+\s*x\s*\d+\s*GB)", name, re.IGNORECASE)
            if m2:
                modules = m2.group(1)
            else:
                cap = re.search(r"(\d+)\s*GB", name, re.IGNORECASE)
                if cap:
                    modules = cap.group(1) + " GB"
        results.append(dict(name=name[:80], type=typ, speed=speed, modules=modules, price=price))
    return results


async def fetch_ram_prices_bestbuy():
    url = "https://www.bestbuy.com/site/searchpage.jsp?st=ddr5+ddr4+ram&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&cp=1&nrp=24"
    async with httpx.AsyncClient(follow_redirects=True, timeout=25) as client:
        resp = await client.get(url, headers={"User-Agent": UA})
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for item in soup.select(".sku-item"):
        title_el = item.select_one(".sku-title a")
        price_el = item.select_one("[data-testid='customer-price'] span")
        name = title_el.get_text(strip=True) if title_el else "-"
        price = price_el.get_text(strip=True) if price_el else "-"
        if name == "-" or not name:
            continue
        typ = "DDR5" if "DDR5" in name.upper() else ("DDR4" if "DDR4" in name.upper() else "")
        speed = ""
        mhz = re.search(r"(\d{4,5})\s*MHz", name, re.IGNORECASE)
        if mhz:
            speed = f"{mhz.group(1)} MHz"
        modules = ""
        m = re.search(r"(\d+)\s*x\s*(\d+\s*GB)", name, re.IGNORECASE)
        if m:
            modules = f"{m.group(1)} x {m.group(2)}"
        else:
            cap = re.search(r"(\d+)\s*GB", name, re.IGNORECASE)
            if cap:
                modules = cap.group(1) + " GB"
        results.append(dict(name=name[:80], type=typ, speed=speed, modules=modules, price=price))
    return results


async def fetch_gas_prices(state: str):
    async with httpx.AsyncClient(follow_redirects=True, timeout=20) as client:
        resp = await client.get(f"{GAS_URL}?state={state}", headers={"User-Agent": UA})
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for heading in soup.find_all(["h2", "h3", "h4"]):
        area_name = heading.get_text(strip=True)
        if not area_name or len(area_name) < 2:
            continue
        wrap = heading.find_next("div", class_="tblwrap")
        if not wrap:
            continue
        nxt = heading.find_next(["h2", "h3", "h4"])
        if nxt and nxt.sourceline < wrap.sourceline:
            continue
        table = wrap.find("table", class_="table-mob")
        if not table:
            continue
        rows = table.find_all("tr")
        for r in rows:
            cells = r.find_all(["td", "th"])
            row_data = [c.get_text(strip=True) for c in cells]
            if len(row_data) >= 4 and "current" in row_data[0].lower():
                results.append(dict(
                    area=area_name,
                    regular=row_data[1] if len(row_data) > 1 else "-",
                    mid=row_data[2] if len(row_data) > 2 else "-",
                    premium=row_data[3] if len(row_data) > 3 else "-",
                    diesel=row_data[4] if len(row_data) > 4 else "-",
                ))
                break
    return results


async def fetch_gas_prices_eia():
    url = "https://www.eia.gov/petroleum/gasdiesel/"
    async with httpx.AsyncClient(follow_redirects=True, timeout=20) as client:
        resp = await client.get(url, headers={"User-Agent": UA})
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for table in soup.select("table"):
        rows = table.select("tr")
        for row in rows:
            cells = row.select("td, th")
            text = [c.get_text(strip=True) for c in cells]
            if len(text) >= 5 and any(x in text[0].lower() for x in ("regular", "area", "region", "us", "east", "west", "gulf", "midwest", "rocky")):
                results.append(dict(
                    area=text[0],
                    regular=text[1] if len(text) > 1 else "-",
                    mid=text[2] if len(text) > 2 else "-",
                    premium=text[3] if len(text) > 3 else "-",
                    diesel=text[4] if len(text) > 4 else "-",
                ))
        if results:
            break
    return results


RAM_SOURCES = {
    "newegg": ("Newegg", fetch_ram_prices),
    "bestbuy": ("Best Buy", fetch_ram_prices_bestbuy),
}

GAS_SOURCES = {
    "aaa": ("AAA", fetch_gas_prices),
    "eia": ("EIA (US Avg)", fetch_gas_prices_eia),
}

CS_SKILLS = [
    "python", "java", "javascript", "typescript", "react", "angular",
    "vue", "node.js", "nodejs", "rust", "go", "golang", "c++", "c#",
    "ruby", "php", "swift", "kotlin", "scala", "perl", "bash",
    "powershell", "aws", "azure", "gcp", "docker", "kubernetes",
    "terraform", "ansible", "jenkins", "git", "linux", "sql", "nosql",
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "kafka", "rabbitmq", "spark", "hadoop", "airflow",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas",
    "numpy", "django", "flask", "fastapi", "spring", "rails",
    "graphql", "rest", "grpc", "machine learning", "deep learning",
    "nlp", "computer vision", "data science", "data engineering",
    "agile", "scrum", "ci/cd", "microservices", "serverless",
]

CS_TITLES = [
    r"software engineer", r"software developer", r"data scientist",
    r"data engineer", r"ml engineer", r"machine learning engineer",
    r"backend engineer", r"backend developer", r"frontend engineer",
    r"frontend developer", r"full.?stack", r"devops engineer",
    r"devops", r"sre", r"site reliability", r"cloud architect",
    r"cloud engineer", r"systems engineer", r"security engineer",
    r"qa engineer", r"ai engineer", r"ai researcher",
    r"research scientist", r"research engineer",
    r"infrastructure engineer", r"platform engineer",
    r"data analyst", r"solutions architect",
    r"python developer", r"java developer", r"react developer",
    r"net developer", r"embedded engineer", r"firmware engineer",
    r"network engineer", r"database administrator", r"dba",
    r"technical lead", r"tech lead", r"engineering manager",
    r"staff engineer", r"principal engineer", r"devsecops",
    r"software architect", r"systems architect",
]


def parse_resume(text: str) -> dict:
    lines = text.lower().split("\n")
    found_skills = set()
    found_titles = set()
    for line in lines:
        for skill in CS_SKILLS:
            if skill in line:
                found_skills.add(skill.title() if skill.islower() and len(skill) > 2 else skill)
        for pattern in CS_TITLES:
            if re.search(pattern, line):
                found_titles.add(re.search(pattern, line).group().strip().title())
    queries = []
    skills_list = sorted(found_skills)
    titles_list = sorted(found_titles)
    if titles_list:
        for t in titles_list[:3]:
            if skills_list:
                queries.append(f"{t} {' '.join(skills_list[:3])}")
            else:
                queries.append(t)
    else:
        if skills_list:
            queries.append(" ".join(skills_list[:5]))
        else:
            queries.append("software engineer")
    return {"skills": skills_list, "titles": titles_list, "queries": queries}


def load_resume_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


REMOTEOK_CS_TAGS = {
    "dev", "engineer", "data science", "data", "backend", "frontend",
    "full stack", "devops", "sys admin", "cloud", "design", "product",
    "management", "security", "embedded", "mobile", "blockchain",
    "architecture", "qa", "testing", "ui/ux", "react", "node",
    "python", "javascript", "typescript", "go", "rust", "java",
    "machine learning", "ai", "deep learning", "nlp", "computer vision",
    "database", "dba", "analytics", "support",
}

JOBICY_CS_INDUSTRIES = {
    "programming", "software engineering", "data science & analytics",
    "information technology", "web development", "it & software",
    "engineering", "technology", "design & ux", "product management",
}


async def search_remoteok(query: str, location: str) -> list:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get("https://remoteok.com/api")
            resp.raise_for_status()
            data = resp.json()
    except Exception:
        return []
    if not isinstance(data, list) or len(data) < 2:
        return []
    jobs = data[1:] if isinstance(data[0], dict) and 'legal' in data[0] else data
    results = []
    query_lower = query.lower()
    for job in jobs:
        position = job.get("position", "") or ""
        tags = [t.lower() for t in job.get("tags", [])]
        title_lower = position.lower()
        is_cs = any(t in REMOTEOK_CS_TAGS for t in tags)
        if not is_cs:
            is_cs = any(re.search(p, title_lower) for p in CS_TITLES)
        if not is_cs:
            continue
        if query_lower and query_lower not in title_lower and not any(query_lower in t for t in tags):
            if not any(w in title_lower for w in query_lower.split()):
                continue
        salary = ""
        if job.get("salary_min") or job.get("salary_max"):
            s_min = job.get("salary_min") or ""
            s_max = job.get("salary_max") or ""
            salary = f"${s_min}-${s_max}" if s_min and s_max else f"${s_min or s_max}"
        posted = job.get("date", "")[:10] if job.get("date") else ""
        results.append(dict(
            title=position,
            company=job.get("company", "-"),
            location=job.get("location", "Remote") or "Remote",
            salary=salary,
            posted=posted,
            source="RemoteOK",
            url=job.get("url", "") or job.get("apply_url", ""),
        ))
    return results


async def search_jobicy(query: str, location: str) -> list:
    query_lower = query.lower()
    words = query_lower.split()
    tag_hits = set()
    for tag in JOBICY_CS_INDUSTRIES:
        for w in words:
            if w in tag or tag.startswith(w):
                tag_hits.add(tag)
    if not tag_hits:
        tag_hits = {"programming", "software engineering"}
    results = []
    for tag in list(tag_hits)[:3]:
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
                resp = await client.get("https://jobicy.com/api/v2/remote-jobs", params={"tag": tag.split()[0]})
                if resp.status_code != 200:
                    continue
                data = resp.json()
                for job in data.get("jobs", []):
                    title = job.get("jobTitle", "")
                    title_lower = title.lower()
                    is_cs = any(re.search(p, title_lower) for p in CS_TITLES)
                    if not is_cs:
                        industries = [ind.lower() for ind in job.get("jobIndustry", [])]
                        is_cs = any("program" in ind or "software" in ind or "data" in ind or "engineer" in ind or "tech" in ind for ind in industries)
                    if not is_cs:
                        continue
                    posted = job.get("pubDate", "")[:10] if job.get("pubDate") else ""
                    results.append(dict(
                        title=title,
                        company=job.get("companyName", "-"),
                        location=job.get("jobGeo", "Remote") or "Remote",
                        salary="",
                        posted=posted,
                        source="Jobicy",
                        url=job.get("url", ""),
                    ))
        except Exception:
            continue
    return results


async def search_all_jobs(queries: list, location: str) -> list:
    seen = set()
    all_results = []
    tasks = []
    for query in queries[:3]:
        tasks.append(search_remoteok(query, location))
        tasks.append(search_jobicy(query, location))
    if not tasks:
        tasks.append(search_remoteok("software engineer", location))
        tasks.append(search_jobicy("software engineer", location))
    gathered = await asyncio.gather(*tasks, return_exceptions=True)
    for chunk in gathered:
        if isinstance(chunk, Exception):
            continue
        for job in chunk:
            key = (re.sub(r"[^a-z0-9]", "", job["title"].lower()),
                   re.sub(r"[^a-z0-9]", "", job["company"].lower()))
            if key not in seen:
                seen.add(key)
                all_results.append(job)
    all_results.sort(key=lambda j: j.get("posted", ""), reverse=True)
    return all_results[:100]


def save_to_txt(data, prefix):
    ensure_save_dir()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(SAVE_DIR, f"{prefix}_{now}.txt")
    with open(path, "w") as f:
        f.write(f"{prefix.upper()} Prices - {now}\n")
        f.write("=" * 60 + "\n\n")
        if isinstance(data, list) and data:
            headers = list(data[0].keys())
            f.write("\t".join(h.upper() for h in headers) + "\n")
            f.write("-" * 60 + "\n")
            for row in data:
                f.write("\t".join(str(row.get(h, "")) for h in headers) + "\n")
        else:
            f.write(str(data) + "\n")
    return path


class SaveDialog(Screen):
    def __init__(self, path: str, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def compose(self):
        with Vertical(id="dialog"):
            yield Label(f"Saved: {self.path}")
            yield Button("OK", variant="primary", id="ok")

    def on_button_pressed(self, event: Button.Pressed):
        self.app.pop_screen()


class PriceTUI(App):
    CSS = """
    Screen {
        background: $surface;
    }
    #header {
        text-align: center;
        text-style: bold;
        padding: 1;
    }
    .section-title {
        text-style: bold;
        padding: 0 1;
    }
    .actions {
        padding: 1;
    }
    DataTable {
        height: 1fr;
        margin: 0 1;
    }
    .status {
        padding: 1 2;
        background: $accent;
        color: $text;
    }
    #ram-tab .actions {
        layout: horizontal;
        align: center middle;
        height: 3;
    }
    .source-select {
        layout: horizontal;
        align: center middle;
        height: 3;
    }
    Select {
        width: 30;
    }
    Button {
        margin: 0 1;
    }
    #gas-inputs {
        layout: horizontal;
        height: 5;
        align: center middle;
    }
    #gas-inputs Input {
        width: 20;
        margin: 0 1;
    }
    #dialog {
        align: center middle;
        width: 60;
        height: 8;
        border: thick $primary;
        background: $surface;
    }
    #dialog Label {
        text-align: center;
        padding: 1;
    }
    #dialog Button {
        align: center middle;
    }
    RichLog {
        height: 3;
        margin: 1 1;
    }
    #resume-text {
        height: 10;
        border: solid $primary;
        margin: 0 1;
    }
    #keywords-display {
        height: 3;
        margin: 0 1;
        padding: 0 1;
    }
    #job-tab .source-select {
        layout: horizontal;
        align: center middle;
        height: 3;
    }
    #job-tab .actions {
        layout: horizontal;
        align: center middle;
        height: 3;
    }
    """

    def compose(self):
        yield Header(show_clock=True)
        with TabbedContent():
            with TabPane("RAM Prices", id="ram-tab"):
                yield Label("DDR4 / DDR5 Market Prices", classes="section-title")
                with Horizontal(classes="source-select"):
                    yield Select(
                        [(label, key) for key, (label, _) in RAM_SOURCES.items()],
                        id="ram-source", value="newegg", prompt="Source",
                    )
                with Horizontal(classes="actions"):
                    yield Button("Fetch RAM Prices", id="fetch-ram", variant="primary")
                    yield Button("Save", id="save-ram", variant="default")
                yield DataTable(id="ram-table")
                yield RichLog(id="ram-status", markup=True, max_lines=3)
            with TabPane("Gas Prices", id="gas-tab"):
                yield Label("Gas Prices by Location", classes="section-title")
                with Horizontal(classes="source-select"):
                    yield Select(
                        [(label, key) for key, (label, _) in GAS_SOURCES.items()],
                        id="gas-source", value="aaa", prompt="Source",
                    )
                with Horizontal(id="gas-inputs"):
                    yield Input(placeholder="State (e.g. CA)", id="state-input")
                    yield Input(placeholder="City (e.g. Los Angeles)", id="city-input")
                    yield Button("Search", id="search-gas", variant="primary")
                with Horizontal(classes="actions"):
                    yield Button("Save", id="save-gas", variant="default")
                yield DataTable(id="gas-table")
                yield RichLog(id="gas-status", markup=True, max_lines=3)
            with TabPane("Job Search", id="job-tab"):
                yield Label("CS Job Search from Resume", classes="section-title")
                yield TextArea(id="resume-text", text="Paste your resume here...")
                with Horizontal(classes="source-select"):
                    yield Input(placeholder="File path (.txt)", id="file-path")
                    yield Button("Load File", id="load-file", variant="default")
                    yield Button("Parse Resume", id="parse-resume", variant="primary")
                yield Label(id="keywords-display")
                with Horizontal(id="gas-inputs"):
                    yield Input(placeholder="City, State (optional)", id="job-location")
                    yield Input(placeholder="Extra keywords (optional)", id="job-keywords")
                    yield Button("Search Jobs", id="search-jobs", variant="primary")
                    yield Button("Save Jobs", id="save-jobs", variant="default")
                yield DataTable(id="job-table")
                yield RichLog(id="job-status", markup=True, max_lines=3)
        yield Footer()

    def on_mount(self):
        ram_table = self.query_one("#ram-table", DataTable)
        ram_table.add_columns("Name", "Type", "Speed", "Modules", "Price")
        gas_table = self.query_one("#gas-table", DataTable)
        gas_table.add_columns("Area", "Regular", "Mid", "Premium", "Diesel")
        job_table = self.query_one("#job-table", DataTable)
        job_table.add_columns("Title", "Company", "Location", "Salary", "Posted", "Source")
        self.query_one("#ram-status", RichLog).write("[green]Ready. Select source and click 'Fetch RAM Prices'.")
        self.query_one("#gas-status", RichLog).write("[green]Ready. Select source, enter state, click 'Search'.")
        self.query_one("#job-status", RichLog).write("[green]Ready. Paste resume, click 'Parse Resume', then 'Search 6 Sites'.")

    def on_button_pressed(self, event: Button.Pressed):
        btn_id = event.button.id
        if btn_id == "fetch-ram":
            self.run_worker(self.do_fetch_ram(), exclusive=True)
        elif btn_id == "save-ram":
            self.run_worker(self.do_save_ram(), exclusive=True)
        elif btn_id == "search-gas":
            self.run_worker(self.do_search_gas(), exclusive=True)
        elif btn_id == "save-gas":
            self.run_worker(self.do_save_gas(), exclusive=True)
        elif btn_id == "load-file":
            self.run_worker(self.do_load_file(), exclusive=True)
        elif btn_id == "parse-resume":
            self.run_worker(self.do_parse_resume(), exclusive=True)
        elif btn_id == "search-jobs":
            self.run_worker(self.do_search_jobs(), exclusive=True)
        elif btn_id == "save-jobs":
            self.run_worker(self.do_save_jobs(), exclusive=True)

    async def do_fetch_ram(self):
        status = self.query_one("#ram-status", RichLog)
        table = self.query_one("#ram-table", DataTable)
        source_id = self.query_one("#ram-source", Select).value
        source_label = RAM_SOURCES.get(source_id, ("Unknown",))[0]
        status.write(f"[yellow]Fetching RAM prices from {source_label}...")
        try:
            fetch_fn = RAM_SOURCES[source_id][1]
            data = await fetch_fn()
        except Exception as e:
            status.write(f"[red]Error: {e}")
            return
        table.clear()
        if not data:
            status.write("[red]No RAM data found.")
            return
        for item in data:
            table.add_row(
                item["name"][:60],
                item["type"],
                item["speed"],
                item["modules"],
                item["price"],
            )
        status.write(f"[green]Loaded {len(data)} RAM products from {source_label}.")
        self._ram_data = data

    async def do_search_gas(self):
        state = self.query_one("#state-input", Input).value.strip()
        city = self.query_one("#city-input", Input).value.strip().lower()
        source_id = self.query_one("#gas-source", Select).value
        source_label = GAS_SOURCES.get(source_id, ("Unknown",))[0]
        status = self.query_one("#gas-status", RichLog)
        table = self.query_one("#gas-table", DataTable)
        if source_id == "eia":
            status.write(f"[yellow]Fetching national gas prices from EIA...")
        else:
            if not state:
                status.write("[red]Please enter a state (e.g. CA).")
                return
            status.write(f"[yellow]Fetching gas prices for {state} from {source_label}...")
        try:
            if source_id == "aaa":
                data = await fetch_gas_prices(state.upper())
            else:
                data = await fetch_gas_prices_eia()
        except Exception as e:
            status.write(f"[red]Error: {e}")
            return
        table.clear()
        if not data:
            status.write("[red]No gas price data found.")
            return
        if source_id == "aaa" and city:
            filtered = [r for r in data if city in r["area"].lower()]
        else:
            filtered = data
        if source_id == "aaa" and city and not filtered:
            status.write(f"[yellow]No results for '{city}' in {state}. Showing all.")
            filtered = data
        for item in filtered:
            table.add_row(
                item["area"], item["regular"], item["mid"],
                item["premium"], item["diesel"],
            )
        status.write(f"[green]Loaded {len(filtered)} areas from {source_label}.")
        self._gas_data = filtered
        self._all_gas = data

    async def do_save_ram(self):
        data = getattr(self, "_ram_data", None)
        if not data:
            self.query_one("#ram-status", RichLog).write("[red]No RAM data to save. Fetch first.")
            return
        path = save_to_txt(data, "ram")
        self.push_screen(SaveDialog(path))
        self.query_one("#ram-status", RichLog).write(f"[green]Saved RAM prices to {path}")

    async def do_save_gas(self):
        data = getattr(self, "_gas_data", None)
        if not data and hasattr(self, "_all_gas"):
            data = self._all_gas
        if not data:
            self.query_one("#gas-status", RichLog).write("[red]No gas data to save. Search first.")
            return
        path = save_to_txt(data, "gas")
        self.push_screen(SaveDialog(path))
        self.query_one("#gas-status", RichLog).write(f"[green]Saved gas prices to {path}")

    async def do_load_file(self):
        path = self.query_one("#file-path", Input).value.strip()
        if not path:
            self.query_one("#job-status", RichLog).write("[red]Enter a file path first.")
            return
        try:
            content = load_resume_file(path)
            self.query_one("#resume-text", TextArea).text = content
            self.query_one("#job-status", RichLog).write(f"[green]Loaded resume from {path}")
        except Exception as e:
            self.query_one("#job-status", RichLog).write(f"[red]Error loading file: {e}")

    async def do_parse_resume(self):
        text = self.query_one("#resume-text", TextArea).text
        if not text.strip() or text.strip() == "Paste your resume here...":
            self.query_one("#job-status", RichLog).write("[red]No resume text entered.")
            return
        parsed = parse_resume(text)
        label = self.query_one("#keywords-display", Label)
        parts = []
        if parsed["titles"]:
            parts.append(f"[bold]Titles:[/] {', '.join(parsed['titles'][:5])}")
        if parsed["skills"]:
            parts.append(f"[bold]Skills:[/] {', '.join(parsed['skills'][:10])}")
        parts.append(f"[bold]Queries:[/] {' | '.join(parsed['queries'])}")
        label.update("  ".join(parts))
        self._parsed_resume = parsed
        self.query_one("#job-status", RichLog).write(f"[green]Parsed resume: {len(parsed['skills'])} skills, {len(parsed['titles'])} titles.")

    async def do_search_jobs(self):
        parsed = getattr(self, "_parsed_resume", None)
        extra_keywords = self.query_one("#job-keywords", Input).value.strip()
        location = self.query_one("#job-location", Input).value.strip()
        if not parsed:
            self.query_one("#job-status", RichLog).write("[yellow]No resume parsed. Searching with CS default.")
            queries = ["software engineer"]
        else:
            queries = list(parsed["queries"])
        if extra_keywords:
            queries = [f"{q} {extra_keywords}" for q in queries]
        status = self.query_one("#job-status", RichLog)
        table = self.query_one("#job-table", DataTable)
        status.write("[yellow]Searching RemoteOK + Jobicy for CS roles...")
        try:
            results = await search_all_jobs(queries, location)
        except Exception as e:
            status.write(f"[red]Error: {e}")
            return
        table.clear()
        if not results:
            status.write("[yellow]No CS job listings found.")
            return
        for job in results:
            table.add_row(
                job["title"][:55], job["company"][:30], job["location"][:25],
                job["salary"][:20], job["posted"][:15], job["source"],
            )
        by_source = {}
        for j in results:
            by_source.setdefault(j["source"], 0)
            by_source[j["source"]] += 1
        src_summary = " | ".join(f"{s}: {c}" for s, c in sorted(by_source.items()))
        status.write(f"[green]Loaded {len(results)} CS jobs. {src_summary}")
        self._job_data = results

    async def do_save_jobs(self):
        data = getattr(self, "_job_data", None)
        if not data:
            self.query_one("#job-status", RichLog).write("[red]No job data to save. Search first.")
            return
        path = save_to_txt(data, "jobs")
        self.push_screen(SaveDialog(path))
        self.query_one("#job-status", RichLog).write(f"[green]Saved jobs to {path}")


def main():
    app = PriceTUI()
    app.run()


if __name__ == "__main__":
    main()
