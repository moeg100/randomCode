#!/usr/bin/env python3
"""RAM & Gas Price Tracker - A Textual TUI"""

import os
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button, DataTable, Footer, Header, Input, Label, RichLog, TabbedContent, TabPane,
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
    """

    def compose(self):
        yield Header(show_clock=True)
        with TabbedContent():
            with TabPane("RAM Prices", id="ram-tab"):
                yield Label("DDR4 / DDR5 Market Prices", classes="section-title")
                with Horizontal(classes="actions"):
                    yield Button("🔄 Fetch RAM Prices", id="fetch-ram", variant="primary")
                    yield Button("💾 Save", id="save-ram", variant="default")
                yield DataTable(id="ram-table")
                yield RichLog(id="ram-status", markup=True, max_lines=3)
            with TabPane("Gas Prices", id="gas-tab"):
                yield Label("Gas Prices by Location", classes="section-title")
                with Horizontal(id="gas-inputs"):
                    yield Input(placeholder="State (e.g. CA)", id="state-input")
                    yield Input(placeholder="City (e.g. Los Angeles)", id="city-input")
                    yield Button("🔍 Search", id="search-gas", variant="primary")
                with Horizontal(classes="actions"):
                    yield Button("💾 Save", id="save-gas", variant="default")
                yield DataTable(id="gas-table")
                yield RichLog(id="gas-status", markup=True, max_lines=3)
        yield Footer()

    def on_mount(self):
        ram_table = self.query_one("#ram-table", DataTable)
        ram_table.add_columns("Name", "Type", "Speed", "Modules", "Price")
        gas_table = self.query_one("#gas-table", DataTable)
        gas_table.add_columns("Area", "Regular", "Mid", "Premium", "Diesel")
        self.query_one("#ram-status", RichLog).write("[green]Ready. Click 'Fetch RAM Prices'.")
        self.query_one("#gas-status", RichLog).write("[green]Ready. Enter state and click 'Search'.")

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

    async def do_fetch_ram(self):
        status = self.query_one("#ram-status", RichLog)
        table = self.query_one("#ram-table", DataTable)
        status.write("[yellow]Fetching RAM prices...")
        try:
            data = await fetch_ram_prices()
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
        status.write(f"[green]Loaded {len(data)} RAM products.")
        self._ram_data = data

    async def do_search_gas(self):
        state = self.query_one("#state-input", Input).value.strip()
        city = self.query_one("#city-input", Input).value.strip().lower()
        if not state:
            self.query_one("#gas-status", RichLog).write("[red]Please enter a state (e.g. CA).")
            return
        status = self.query_one("#gas-status", RichLog)
        table = self.query_one("#gas-table", DataTable)
        status.write(f"[yellow]Fetching gas prices for {state}...")
        try:
            data = await fetch_gas_prices(state.upper())
        except Exception as e:
            status.write(f"[red]Error: {e}")
            return
        table.clear()
        if not data:
            status.write("[red]No gas price data found for that state.")
            return
        if city:
            filtered = [r for r in data if city in r["area"].lower()]
        else:
            filtered = data
        if not filtered:
            status.write(f"[yellow]No results for '{city}' in {state}. Showing all.")
            filtered = data
        for item in filtered:
            table.add_row(
                item["area"], item["regular"], item["mid"],
                item["premium"], item["diesel"],
            )
        status.write(f"[green]Loaded {len(filtered)} areas.")
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


def main():
    app = PriceTUI()
    app.run()


if __name__ == "__main__":
    main()
