# Command-Line Data Analysis Tool

A Python CLI tool that loads a CSV file and lets you generate summaries, filter rows, group data, sort, and get statistical reports directly from the terminal. Built with **Pandas** and **argparse**.

## Features

- `summary`: shape, column types, missing values and descriptive statistics
- `head`: preview the first N rows
- `filter`: filter rows using a condition (`eq`, `ne`, `gt`, `lt`, `ge`, `le`, `contains`)
- `group`: group by a column and aggregate another (`mean`, `sum`, `min`, `max`, `count`, `median`)
- `stats`: mean, median, std, min, max and variance of a numeric column
- `sort`: sort rows by a column (ascending or descending)
- Save any result to a CSV file with `-o`
- Input validation and clear error messages (missing file, wrong column, non-numeric data)
- Built-in help for every command

## Requirements

- Python 3.8+
- Pandas

```bash
pip install pandas
```

## Usage

```bash
python data_tool.py <csv_file> <command> [options]
```

### Examples

```bash
# Overall summary
python data_tool.py data.csv summary

# First 10 rows
python data_tool.py data.csv head -n 10

# Rows where age > 25
python data_tool.py data.csv filter --column age --op gt --value 25

# Average salary per city
python data_tool.py data.csv group --by city --column salary --agg mean

# Statistical report of a column
python data_tool.py data.csv stats --column salary

# Sort by salary (descending)
python data_tool.py data.csv sort --column salary --desc

# Save output to a file
python data_tool.py data.csv summary -o report.csv
```

### Help

```bash
python data_tool.py -h
python data_tool.py data.csv filter -h
```

## Commands

| Command   | Description                              | Main options                          |
|-----------|------------------------------------------|---------------------------------------|
| `summary` | Dataset overview and describe            | `-o`                                  |
| `head`    | Show first N rows                        | `-n`, `-o`                            |
| `filter`  | Filter rows by condition                 | `--column`, `--op`, `--value`, `-o`   |
| `group`   | Group and aggregate                      | `--by`, `--column`, `--agg`, `-o`     |
| `stats`   | Statistics for a numeric column          | `--column`, `-o`                      |
| `sort`    | Sort by a column                         | `--column`, `--desc`, `-o`            |

## Project Structure

```
.
├── data_tool.py
└── README.md
```

## Concepts Covered

- Command-line interfaces with `argparse` (subcommands, choices, flags)
- Data analysis with Pandas
- Input validation and error handling
- Reusable, function-based application design

## Author

**Praval**: Python Programming Track, Veda Technology Internship (Task 30)
