#!/usr/bin/env python3
"""scraper.py

Simple scraper that extracts rows from an HTML table and writes them to CSV.
Usage:
    python scraper.py --source data/sample_site.html --out examples/sample_output.csv
    python scraper.py --source https://example.com/page.html --out examples/output.csv
"""

import argparse
import csv
import os
import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def is_url(path):
    try:
        parsed = urlparse(path)
        return parsed.scheme in ('http', 'https')
    except Exception:
        return False

def load_html(source):
    if is_url(source):
        print(f"[INFO] Fetching URL: {source}")
        try:
            r = requests.get(source, timeout=10)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            print(f"[ERROR] Network error while fetching {source}: {e}")
            return None
    else:
        # local file
        if not os.path.exists(source):
            print(f"[ERROR] File not found: {source}")
            return None
        print(f"[INFO] Reading local file: {source}")
        with open(source, 'r', encoding='utf-8') as f:
            return f.read()

def extract_table_rows(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Heuristic: find the first <table> with a header (th)
    table = soup.find('table')
    if not table:
        print('[WARN] No <table> element found in HTML.')
        return [], []
    # header
    headers = []
    thead = table.find('thead')
    if thead:
        headers = [th.get_text(strip=True) for th in thead.find_all('th')]
    if not headers:
        # try first row as header
        first_row = table.find('tr')
        if first_row:
            headers = [cell.get_text(strip=True) for cell in first_row.find_all(['th','td'])]
            # remove this row later when collecting rows
    # collect rows
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td','th'])]
        if not cells:
            continue
        # Skip header row if it matches headers
        if headers and [c for c in cells] == headers:
            continue
        # If row length is less than headers, pad with empty strings
        if headers and len(cells) < len(headers):
            cells += [''] * (len(headers) - len(cells))
        rows.append(cells)
    return headers, rows

def write_csv(headers, rows, out_path):
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for r in rows:
            writer.writerow(r)
    print(f"[OK] Wrote {len(rows)} rows to {out_path}")

def main():
    parser = argparse.ArgumentParser(description='Mini web scraper: extract HTML table -> CSV')
    parser.add_argument('--source', help='URL or local HTML file', default='data/sample_site.html')
    parser.add_argument('--out', help='Output CSV path', default='examples/sample_output.csv')
    args = parser.parse_args()

    html = load_html(args.source)
    if html is None:
        print('[ERROR] Failed to load source; exiting.')
        sys.exit(1)
    print('[INFO] Parsing HTML and extracting table...')
    headers, rows = extract_table_rows(html)
    if not headers and not rows:
        print('[ERROR] No table data extracted.')
        sys.exit(1)
    write_csv(headers, rows, args.out)
    print('[DONE] Scraping complete.')

if __name__ == '__main__':
    main()
