
import pandas as pd

excel_files = [
    '/home/ubuntu/upload/Suryamitra2018-2019.xlsx',
    '/home/ubuntu/upload/Suryamitra2019-2020.xlsx',
    '/home/ubuntu/upload/Suryamitra2020-2021.xlsx',
    '/home/ubuntu/upload/Suryamitra2021-2022.xlsx',
    '/home/ubuntu/upload/Suryamitra2022-2023.xlsx'
]

for file in excel_files:
    print(f"\n--- Inspecting {file} ---")
    try:
        # Try reading with no header, then infer header
        df_no_header = pd.read_excel(file, header=None)
        print("First 5 rows (no header):")
        print(df_no_header.head())
        print("Shape (no header):", df_no_header.shape)

        # Try reading with default header inference
        df_default_header = pd.read_excel(file)
        print("\nFirst 5 rows (default header):")
        print(df_default_header.head())
        print("Shape (default header):", df_default_header.shape)
        print("Columns (default header):", df_default_header.columns.tolist())

    except Exception as e:
        print(f"Error reading {file}: {e}")


