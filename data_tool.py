#!/usr/bin/env python3
"""Command-Line Data Analysis Tool (Pandas + argparse).

Examples:
    python data_tool.py data.csv summary
    python data_tool.py data.csv filter --column age --op gt --value 25
    python data_tool.py data.csv group --by city --column salary --agg mean
    python data_tool.py data.csv stats --column salary
    python data_tool.py data.csv summary --output report.csv
"""
import argparse
import os
import sys

import pandas as pd

OPS = {
    "eq": lambda s, v: s == v,
    "ne": lambda s, v: s != v,
    "gt": lambda s, v: s > v,
    "lt": lambda s, v: s < v,
    "ge": lambda s, v: s >= v,
    "le": lambda s, v: s <= v,
    "contains": lambda s, v: s.astype(str).str.contains(str(v), case=False, na=False),
}
AGGS = ["mean", "sum", "min", "max", "count", "median"]


# ---------- helpers ----------
def load_csv(path):
    if not os.path.isfile(path):
        sys.exit(f"Error: file '{path}' not found.")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        sys.exit(f"Error: could not read CSV -> {e}")
    if df.empty:
        sys.exit("Error: CSV file is empty.")
    return df


def check_column(df, col):
    if col not in df.columns:
        sys.exit(f"Error: column '{col}' not found. Available: {', '.join(df.columns)}")


def convert_value(series, value):
    """Convert the CLI string to the column's type (numeric columns)."""
    if pd.api.types.is_numeric_dtype(series):
        try:
            return float(value)
        except ValueError:
            sys.exit(f"Error: '{value}' is not a number but the column is numeric.")
    return value


def output(result, args):
    print(result.to_string() if hasattr(result, "to_string") else result)
    if args.output:
        result.to_csv(args.output)
        print(f"\nSaved to {args.output}")


# ---------- commands ----------
def cmd_summary(df, args):
    print(f"Rows: {len(df)}  |  Columns: {len(df.columns)}\n")
    print("Column types:")
    print(df.dtypes.to_string(), "\n")
    print("Missing values:")
    print(df.isnull().sum().to_string(), "\n")
    print("Describe:")
    output(df.describe(include="all").T, args)


def cmd_head(df, args):
    output(df.head(args.n), args)


def cmd_filter(df, args):
    check_column(df, args.column)
    value = convert_value(df[args.column], args.value)
    result = df[OPS[args.op](df[args.column], value)]
    print(f"{len(result)} row(s) matched.\n")
    output(result, args)


def cmd_group(df, args):
    check_column(df, args.by)
    check_column(df, args.column)
    result = df.groupby(args.by)[args.column].agg(args.agg)
    output(result, args)


def cmd_stats(df, args):
    check_column(df, args.column)
    s = df[args.column]
    if not pd.api.types.is_numeric_dtype(s):
        sys.exit(f"Error: column '{args.column}' is not numeric.")
    result = pd.Series({
        "count": s.count(),
        "mean": s.mean(),
        "median": s.median(),
        "std": s.std(),
        "min": s.min(),
        "max": s.max(),
        "variance": s.var(),
    }, name=args.column)
    output(result, args)


def cmd_sort(df, args):
    check_column(df, args.column)
    output(df.sort_values(args.column, ascending=not args.desc), args)


# ---------- parser ----------
def build_parser():
    p = argparse.ArgumentParser(
        description="CLI tool for analysing CSV files with Pandas.")
    p.add_argument("csv", help="path to the CSV file")
    sub = p.add_subparsers(dest="command", required=True, metavar="command")

    def add(name, help_, func):
        sp = sub.add_parser(name, help=help_, description=help_)
        sp.add_argument("-o", "--output", help="save result to this CSV file")
        sp.set_defaults(func=func)
        return sp

    add("summary", "shape, dtypes, missing values, describe", cmd_summary)

    sp = add("head", "show first N rows", cmd_head)
    sp.add_argument("-n", type=int, default=5, help="number of rows (default 5)")

    sp = add("filter", "filter rows by a condition", cmd_filter)
    sp.add_argument("--column", required=True)
    sp.add_argument("--op", choices=OPS.keys(), required=True)
    sp.add_argument("--value", required=True)

    sp = add("group", "group by a column and aggregate another", cmd_group)
    sp.add_argument("--by", required=True, help="column to group by")
    sp.add_argument("--column", required=True, help="column to aggregate")
    sp.add_argument("--agg", choices=AGGS, default="mean")

    sp = add("stats", "statistical report for a numeric column", cmd_stats)
    sp.add_argument("--column", required=True)

    sp = add("sort", "sort rows by a column", cmd_sort)
    sp.add_argument("--column", required=True)
    sp.add_argument("--desc", action="store_true", help="descending order")

    return p


def main():
    args = build_parser().parse_args()
    df = load_csv(args.csv)
    args.func(df, args)


if __name__ == "__main__":
    main()
