#!/usr/bin/env python3
import csv

# --- CONFIGURE PATHS HERE ---
chinese_txt_path = "/home/v-zhifeng/HPE/disney_movie_data_visualization/chinese.txt"
input_csv_path  = "/home/v-zhifeng/HPE/disney_movie_data_visualization/disney_movies_total_gross.csv"
output_csv_path = "/home/v-zhifeng/HPE/disney_movie_data_visualization/disney_movies_total_gross_chinese.csv"

# 1) Load your Chinese titles into a dict[index] = title
chinese_map = {}
with open(chinese_txt_path, encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        idx_str, title = line.strip().split(",", 1)
        chinese_map[int(idx_str)] = title.strip()

# 2) Read the original CSV, replace titles, collect rows
with open(input_csv_path, newline="", encoding="utf-8") as fin:
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames
    rows = []
    for row in reader:
        idx = int(row["index"])
        if idx in chinese_map:
            row["movie_title"] = chinese_map[idx]
        rows.append(row)

# 3) Write out the new CSV
with open(output_csv_path, "w", newline="", encoding="utf-8") as fout:
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Written translated CSV to {output_csv_path}")
