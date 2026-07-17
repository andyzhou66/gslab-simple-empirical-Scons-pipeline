"""
Step 2: Clean imported data
Reads from input-data/data.csv and outputs cleaned dataset
"""
import pandas as pd
import sys

# Read data from input (relative to code/ → ../input-data/)
df = pd.read_csv('../input-data/data.csv')

# Simple cleaning: remove any rows with NaN, check data types
df = df.dropna()
df['x'] = pd.to_numeric(df['x'], errors='coerce')
df['y'] = pd.to_numeric(df['y'], errors='coerce')
df = df.dropna()

# Output cleaned data (relative to code/ → ../output/)
df.to_csv('../output/clean_data.csv', index=False)
print(f"Cleaned data: {len(df)} rows, columns: {list(df.columns)}", file=sys.stderr)
