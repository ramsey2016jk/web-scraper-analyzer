#!/usr/bin/env python3
"""analyze.py

Read a CSV produced by scraper.py, perform basic cleaning and summarize.
Saves a summary CSV and a bar chart of counts for a selected column.
Usage:
    python analyze.py --csv examples/sample_output.csv --out-dir results
"""

import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

def load_csv(path):
    if not os.path.exists(path):
        print(f"[ERROR] CSV not found: {path}")
        return None
    try:
        df = pd.read_csv(path)
        print(f"[INFO] Loaded CSV with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return None

def clean_data(df):
    # Trim whitespace from string columns
    for c in df.select_dtypes(include=['object']).columns:
        df[c] = df[c].astype(str).str.strip()
    # Attempt numeric conversion for columns that look numeric
    for c in df.columns:
        try:
            df[c + '_num'] = pd.to_numeric(df[c], errors='coerce')
        except Exception:
            pass
    return df

def summarize(df, count_col=None):
    summary = {}
    summary['n_rows'] = len(df)
    summary['n_columns'] = len(df.columns)
    if count_col and count_col in df.columns:
        counts = df[count_col].value_counts(dropna=False)
        summary['counts'] = counts.to_dict()
    return summary

def save_summary_csv(summary, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for k, v in summary.items():
        if k == 'counts':
            for key, val in v.items():
                rows.append({'metric': 'count:'+str(key), 'value': val})
        else:
            rows.append({'metric': k, 'value': v})
    out_path = os.path.join(out_dir, 'summary.csv')
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"[OK] Saved summary to {out_path}")
    return out_path

def plot_bar(df, column, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    counts = df[column].value_counts().sort_values(ascending=False)
    if counts.empty:
        print(f"[WARN] No data to plot for column {column}")
        return None
    plt.figure(figsize=(8,6))
    counts.plot(kind='bar')
    plt.title(f'Counts by {column}')
    plt.ylabel('Count')
    plt.xlabel(column)
    out_path = os.path.join(out_dir, 'bar_chart.png')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[OK] Saved bar chart to {out_path}")
    return out_path

def main():
    parser = argparse.ArgumentParser(description='Analyze CSV output from scraper')
    parser.add_argument('--csv', help='Input CSV path', default='examples/sample_output.csv')
    parser.add_argument('--out-dir', help='Directory to save results', default='results')
    parser.add_argument('--plot-col', help='Column name to plot (defaults to first column)', default=None)
    args = parser.parse_args()

    df = load_csv(args.csv)
    if df is None:
        sys.exit(1)
    df = clean_data(df)
    plot_col = args.plot_col or (df.columns[0] if len(df.columns) > 0 else None)
    summary = summarize(df, count_col=plot_col)
    save_summary_csv(summary, args.out_dir)
    if plot_col:
        plot_bar(df, plot_col, args.out_dir)
    print('[DONE] Analysis complete.')

if __name__ == '__main__':
    main()
