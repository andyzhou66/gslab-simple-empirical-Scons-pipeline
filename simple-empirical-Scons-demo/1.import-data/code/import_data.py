"""
Step 1: Import raw data
Reads CSV files from raw-data/ and outputs combined dataset
Loads API key from .env file for authentication
"""
import pandas as pd
import os
import sys
from dotenv import load_dotenv

print(os.getcwd())

# Load .env from project root (one level up from step directory)
load_dotenv(dotenv_path='.env')
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise EnvironmentError("API_KEY not set. Copy .env.example to .env and fill in your API key.")

print(f"Using API key (first 4 chars): {API_KEY[:4]}...", file=sys.stderr)

# Create sample data (replace with actual import logic that uses API_KEY)
data = {
    'id': range(1, 101),
    'x': [i * 0.5 for i in range(100)],
    'y': [i * 1.2 + 10 for i in range(100)]
}

df = pd.DataFrame(data)

# Output as CSV (relative to step directory)
df.to_csv('1.import-data/raw-data/data.csv', index=False)
print("Imported 100 rows to output/data.csv", file=sys.stderr)
