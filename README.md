# Mini Web Scraper + Data Analyzer

A small, self-contained project that demonstrates scraping a simple HTML page (local or remote),
exporting extracted data to CSV, and performing basic data cleaning and analysis with plots.

## Contents
- `scraper.py` — scrape a URL or local HTML file (defaults to `data/sample_site.html`) and export results to CSV.
- `analyze.py` — read the CSV, clean data, generate summary statistics and a bar chart.
- `data/sample_site.html` — a local example HTML file (optional).
- `examples/sample_output.csv` — example scraper output.
- `requirements.txt` — Python dependencies.

## Installation

Recommended: use a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## Usage

### Scrape a local sample file (default)
```bash
python scraper.py
# or explicitly:
python scraper.py --source data/sample_site.html --out examples/sample_output.csv
```

### Scrape a remote URL
```bash
python scraper.py --source https://example.com/page-with-table.html --out examples/output.csv
```

The scraper:
- handles network errors,
- prints progress messages,
- skips missing cells, and
- writes a clean CSV with headers.

### Analyze the CSV
```bash
python analyze.py --csv examples/sample_output.csv --out-dir results
```

The analyzer:
- reads the CSV with pandas,
- cleans numeric fields,
- shows summary statistics,
- saves a CSV summary and a bar chart (`results/summary.csv`, `results/bar_chart.png`).

## Example
`examples/sample_output.csv` contains sample data extracted from `data/sample_site.html`. Run:

```bash
python analyze.py --csv examples/sample_output.csv --out-dir results
```

Then open `results/bar_chart.png`.

## Notes
- This project is meant for learning/demonstration. Respect robots.txt and site terms when scraping real websites.
- The sample HTML is included to make the project self-contained.

## License
MIT
