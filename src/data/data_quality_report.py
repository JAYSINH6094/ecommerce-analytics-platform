from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "olist"
REPORT_DIR = PROJECT_ROOT / "reports"


def generate_quality_report():
    REPORT_DIR.mkdir(exist_ok=True)

    records = []

    for file_path in sorted(RAW_DATA_DIR.glob("*.csv")):
        df = pd.read_csv(file_path)

        total_rows = len(df)
        total_columns = len(df.columns)
        duplicate_rows = int(df.duplicated().sum())
        missing_cells = int(df.isnull().sum().sum())

        missing_percentage = (
            (missing_cells / (total_rows * total_columns)) * 100
            if total_rows > 0
            else 0
        )

        records.append(
            {
                "table_name": file_path.stem,
                "rows": total_rows,
                "columns": total_columns,
                "duplicate_rows": duplicate_rows,
                "missing_cells": missing_cells,
                "missing_percentage": round(missing_percentage, 2),
            }
        )

    report_df = pd.DataFrame(records)

    output_file = REPORT_DIR / "data_quality_report.csv"
    report_df.to_csv(output_file, index=False)

    print("=" * 80)
    print("DATA QUALITY REPORT")
    print("=" * 80)
    print(report_df.to_string(index=False))
    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    generate_quality_report()