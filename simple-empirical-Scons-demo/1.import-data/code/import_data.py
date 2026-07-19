"""
Step 1: Import raw data
Reads CSV files from raw-data/ and outputs combined dataset
Loads API key from .env file for authentication
"""
import pandas as pd
import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path
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

# ── Fix: resolve .env relative to THIS script file, not the SCons working dir ──
# SCons runs from repo root, so plain load_dotenv() would look there instead of
# next to this script. Using __file__ makes it portable regardless of cwd.
# print(__file__)
# script_dir = Path(__file__).resolve().parent          # .../1.import-data/code/
# env_path   = script_dir.parent.parent / ".env"        # .../simple-empirical-Scons-demo/.env
# print(script_dir,env_path)
# load_dotenv(dotenv_path=env_path)

# # ── Load API key ────────────────────────────────────────────────────────────────
# API_KEY = os.getenv("API_KEY")
# print(API_KEY)
# if not API_KEY:
#     raise EnvironmentError(
#         f"API_KEY not found. Make sure a .env file exists at:\n  {env_path}\n"
#         "Copy .env.example → .env and fill in your key."
#     )

# # ── Generate sample data ────────────────────────────────────────────────────────
# data = {
#     'id': range(1, 101),
#     'x': [i * 0.5 for i in range(100)],
#     'y': [i * 1.2 + 10 for i in range(100)]
# }

# df = pd.DataFrame(data)

# # ── Save output ─────────────────────────────────────────────────────────────────
# output_dir = script_dir.parent / "raw-data"
# output_dir.mkdir(parents=True, exist_ok=True)

# df.to_csv(output_dir / "data.csv", index=False)
# print(f"Generated 100 rows to {output_dir / 'data.csv'}", file=sys.stderr)
