
import pandas as pd
import os

excel_files = [
    '/home/ubuntu/upload/Suryamitra2018-2019.xlsx',
    '/home/ubuntu/upload/Suryamitra2019-2020.xlsx',
    '/home/ubuntu/upload/Suryamitra2020-2021.xlsx',
    '/home/ubuntu/upload/Suryamitra2021-2022.xlsx',
    '/home/ubuntu/upload/Suryamitra2022-2023.xlsx'
]

# Define a mapping for common column names to a standardized format
column_mapping = {
    'S.No': 'S_No',
    'Name of the Candidate': 'Name',
    'Father\'s Name': 'Father_Name',
    'Gender': 'Gender',
    'Category': 'Category',
    'Address': 'Address',
    'District': 'District',
    'State': 'State',
    'Mobile No.': 'Mobile_No',
    'Aadhar No.': 'Aadhar_No',
    'Education Qualification': 'Education_Qualification',
    'Marks in Diploma/ITI/Graduation': 'Diploma_Marks',
    'Training Start Date': 'Training_Start_Date',
    'Training End Date': 'Training_End_Date',
    'Result': 'Result',
    'Placement Status': 'Placement_Status',
    'Placed': 'Placement_Status', # Handle variation
    'Training Partner': 'Training_Partner',
    'Batch Detail': 'Batch_Detail',
    'Count of Placement': 'Placement_Count',
    'Payment Record': 'Payment_Record'
}

# Define keywords to identify the header row
header_keywords = ['Name', 'S.No', 'Training Partner', 'Result', 'Placement Status', 'Placed']

all_consolidated_data = pd.DataFrame()

for file_path in excel_files:
    print(f"Processing {file_path}...")
    try:
        # Read the first few rows to find the header dynamically
        df_temp = pd.read_excel(file_path, header=None, nrows=10) # Read first 10 rows
        header_row_index = -1

        for i, row in df_temp.iterrows():
            # Check if any of the header keywords are present in the row
            if any(keyword in str(cell) for cell in row.values for keyword in header_keywords):
                header_row_index = i
                break
        
        if header_row_index == -1:
            print(f"Could not find a suitable header row in {file_path}. Skipping.")
            continue

        # Read the actual data using the identified header row
        df = pd.read_excel(file_path, header=header_row_index)
        
        # Drop rows where all values are NaN (often blank rows after the header)
        df = df.dropna(how='all')

        # Rename columns to a standardized format
        df = df.rename(columns=column_mapping)
        
        # Select only the columns that are in our standardized mapping and present in the dataframe
        # Also ensure all expected columns are present, filling with NaN if not
        standardized_cols = list(column_mapping.values())
        for col in standardized_cols:
            if col not in df.columns:
                df[col] = None
        
        df_selected = df[standardized_cols]
        
        all_consolidated_data = pd.concat([all_consolidated_data, df_selected], ignore_index=True)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

output_csv_path = '/home/ubuntu/job_matching_api/suryamitra_consolidated_2018_2023.csv'
all_consolidated_data.to_csv(output_csv_path, index=False)
print(f"Consolidated and cleaned data saved to {output_csv_path}")

# Display first few rows and columns to verify
print("\nFirst 5 rows of consolidated and cleaned data:")
print(all_consolidated_data.head())
print("\nColumns in consolidated and cleaned data:")
print(all_consolidated_data.columns.tolist())
print("\nTotal rows in consolidated data:", len(all_consolidated_data))

# Further cleaning and standardization
if 'Diploma_Marks' in all_consolidated_data.columns:
    all_consolidated_data['Diploma_Marks'] = pd.to_numeric(all_consolidated_data['Diploma_Marks'], errors='coerce')

if 'Placement_Status' in all_consolidated_data.columns:
    all_consolidated_data['Placement_Status'] = all_consolidated_data['Placement_Status'].fillna('Unknown')

if 'Gender' in all_consolidated_data.columns:
    all_consolidated_data['Gender'] = all_consolidated_data['Gender'].replace({'M': 'Male', 'F': 'Female', 'm': 'Male', 'f': 'Female'})

if 'Category' in all_consolidated_data.columns:
    all_consolidated_data['Category'] = all_consolidated_data['Category'].replace({'GEN': 'General', 'OBC': 'OBC', 'SC': 'SC', 'ST': 'ST'})

if 'Name' in all_consolidated_data.columns:
    all_consolidated_data.dropna(subset=['Name'], inplace=True)

final_output_csv_path = '/home/ubuntu/job_matching_api/suryamitra_final_cleaned_2018_2023.csv'
all_consolidated_data.to_csv(final_output_csv_path, index=False)
print(f"Final cleaned data saved to {final_output_csv_path}")

print("\nFirst 5 rows of final cleaned data:")
print(all_consolidated_data.head())
print("\nColumns in final cleaned data:")
print(all_consolidated_data.columns.tolist())
print("\nTotal rows in final cleaned data:", len(all_consolidated_data))


