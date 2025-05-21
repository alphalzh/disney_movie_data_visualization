#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import re

# ─── CONFIG ───────────────────────────────────────────────────────────────────
csv_path    = '/home/v-zhifeng/HPE/disney_movie_data_visualization/disney_movies_total_gross_chinese.csv'
txt_path    = '/home/v-zhifeng/HPE/disney_movie_data_visualization/chinese_with_annotation.txt'
output_path = '/home/v-zhifeng/HPE/disney_movie_data_visualization/disney_movies_total_gross_chinese_annotated.csv'
# ────────────────────────────────────────────────────────────────────────────────

# 1. Load the CSV
df = pd.read_csv(csv_path, encoding='utf-8')

# 2. Parse your TXT file into a dict: { index → annotation }
annotations = {}
pattern = re.compile(r'^(\d+)[，,\s]+[^：:]+[：:](.+)$')
with open(txt_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = pattern.match(line)
        if m:
            idx = int(m.group(1))
            annotations[idx] = m.group(2).strip()

# 3. Map annotations into a new column
df['annotation'] = df['index'].map(annotations)

# 4. Write out the merged CSV
df.to_csv(output_path, index=False, encoding='utf-8')
print(f'✅ Saved annotated CSV as: {output_path}')
