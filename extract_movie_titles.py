#!/usr/bin/env python3
import csv
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Extract movie titles with numeric labels"
    )
    parser.add_argument(
        "csv_file",
        help="Path to the CSV file containing movie data"
    )
    args = parser.parse_args()

    with open(args.csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            title = row.get("movie_title", "")
            print(f"{idx}, {title}")

if __name__ == "__main__":
    main()
