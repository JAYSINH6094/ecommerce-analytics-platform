from pathlib import Path
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"


def inspect_dataset():
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    print("=" * 80)
    print("OLIST RAW DATASET INSPECTION")
    print("=" * 80)

    for file_path in csv_files:
        print(f"\n{'=' * 80}")
        print(f"FILE: {file_path.name}")
        print("=" * 80)

        df = pd.read_csv(file_path)

        print(f"Rows       : {len(df):,}")
        print(f"Columns    : {len(df.columns)}")
        print(f"Memory     : {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        print("\nColumns:")
        print(list(df.columns))

        print("\nData Types:")
        print(df.dtypes.to_string())

        print("\nMissing Values:")
        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if missing.empty:
            print("No missing values.")
        else:
            print(missing.to_string())

        print("\nDuplicate Rows:")
        print(f"{df.duplicated().sum():,}")

        print("\nSample Records:")
        print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    inspect_dataset()