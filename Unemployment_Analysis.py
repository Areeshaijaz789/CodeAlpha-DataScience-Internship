# ...existing code...
import os
import sys
from pathlib import Path

# Step 1: Import Libraries
import numpy as np
import pandas as pd
import warnings
import logging
logging.getLogger().setLevel(logging.ERROR)

import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Ignore Warnings
warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

def find_csv(filename="GenderBasedEmploymentInPakistan2023.csv"):
    candidates = [
        Path(__file__).parent / filename,
        Path.cwd() / filename
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def safe_read_csv(path):
    try:
        return pd.read_csv(path, encoding="utf-8", on_bad_lines="warn")
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)

def main():
    csv_path = find_csv()
    if csv_path is None:
        print("❌ CSV file not found in script directory or current working directory.")
        print("📁 Current working dir:", Path.cwd())
        sys.exit(1)

    data = safe_read_csv(csv_path)

    # sanitize column names
    data.columns = data.columns.str.strip()

    # Basic info
    print("✅ Dataset Loaded Successfully!\n")
    print("📊 First 5 Rows of the Dataset:\n")
    print(data.head())
    print("\n🔢 Dataset Shape (Rows, Columns):", data.shape)
    print("\n📁 Column Names:\n", list(data.columns))

    # Missing values and stats
    print("\n🕳️ Missing Values in Each Column:\n")
    print(data.isnull().sum())

    print("\n📈 Basic Statistical Summary (numeric columns):\n")
    print(data.describe(include=[np.number]))

    # Correlation heatmap for numeric columns only
    numeric = data.select_dtypes(include=[np.number])
    if numeric.shape[1] >= 2:
        corr = numeric.corr()
        try:
            plt.figure(figsize=(10,6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title("Correlation Heatmap of Employment Data", fontsize=14)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print("⚠️ Could not plot heatmap:", e)
    else:
        print("\n⚠️ Not enough numeric columns to compute correlation heatmap.")

    # Example bar chart: verify exact column names
    col_region = next((c for c in data.columns if c.lower() == 'region'), None)
    col_unemp = next((c for c in data.columns if 'unemploy' in c.lower()), None)

    if col_region and col_unemp:
        try:
            plt.figure(figsize=(12,6))
            sns.barplot(x=col_region, y=col_unemp, data=data)
            plt.title("Unemployment Rate by Region", fontsize=14)
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print("⚠️ Could not plot bar chart:", e)
    else:
        print("\n⚠️ Columns for bar plot not found. Available columns:")
        print(list(data.columns))

if __name__ == "__main__":
    main()
# ...existing code...