"""
Step 1: Import raw data
Reads CSV files from raw-data/ and outputs combined dataset
"""
import pandas as pd
import os
import sys

# Create sample data (replace with actual import logic)
data = {
    'id': range(1, 101),
    'x': [i * 0.5 for i in range(100)],
    'y': [i * 1.2 + 10 for i in range(100)]
}

df = pd.DataFrame(data)

# Output as CSV (relative to code/ → ../output/)
df.to_csv('../output/data.csv', index=False)
print("Imported 100 rows to ../output/data.csv", file=sys.stderr)
