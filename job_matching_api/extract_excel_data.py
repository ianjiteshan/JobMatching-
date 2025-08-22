
import pandas as pd
import os

excel_files = [
    'Suryamitra2018-2019.xlsx',
    'Suryamitra2019-2020.xlsx',
    'Suryamitra2020-2021.xlsx',
    'Suryamitra2021-2022.xlsx',
    'Suryamitra2022-2023.xlsx'

]

all_data = pd.DataFrame()

for file in excel_files:
    print(f"Processing {file}...")
    try:
        df = pd.read_excel(file)
        all_data = pd.concat([all_data, df], ignore_index=True)
    except Exception as e:
        print(f"Error processing {file}: {e}")

output_csv_path = '/home/ubuntu/job_matching_api/suryamitra_all_years.csv'
all_data.to_csv(output_csv_path, index=False)
print(f"Consolidated data saved to {output_csv_path}")

# Display first few rows and columns to verify
print("\nFirst 5 rows of consolidated data:")
print(all_data.head())
print("\nColumns in consolidated data:")
print(all_data.columns.tolist())


