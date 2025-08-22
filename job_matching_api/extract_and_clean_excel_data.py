
import pandas as pd
import os

excel_files_info = {
    '/home/ubuntu/upload/Suryamitra2018-2019.xlsx': {
        'header_row': 3,  # 0-indexed, row 4 in Excel
        'data_start_row': 4, # 0-indexed, data starts from row 5
        'columns': {
            'Training Partner': 'Training_Partner',
            'Batch Detail': 'Batch_Detail',
            'Count of Placement': 'Placement_Count',
            'Payment Record': 'Payment_Record'
        },
        'relevant_columns': ['Training_Partner', 'Batch_Detail', 'Placement_Count', 'Payment_Record']
    },
    '/home/ubuntu/upload/Suryamitra2019-2020.xlsx': {
        'header_row': 3,  # 0-indexed, row 4 in Excel
        'data_start_row': 4, # 0-indexed, data starts from row 5
        'columns': {
            'Training Partner': 'Training_Partner',
            'Batch Detail': 'Batch_Detail',
            'Count of Placement': 'Placement_Count',
            'Payment Record': 'Payment_Record'
        },
        'relevant_columns': ['Training_Partner', 'Batch_Detail', 'Placement_Count', 'Payment_Record']
    },
    '/home/ubuntu/upload/Suryamitra2020-2021.xlsx': {
        'header_row': 1,  # 0-indexed, row 2 in Excel
        'data_start_row': 2, # 0-indexed, data starts from row 3
        'columns': {
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
            'Placement Status': 'Placement_Status'
        },
        'relevant_columns': [
            'S_No', 'Name', 'Father_Name', 'Gender', 'Category', 'Address', 'District', 'State',
            'Mobile_No', 'Aadhar_No', 'Education_Qualification', 'Diploma_Marks',
            'Training_Start_Date', 'Training_End_Date', 'Result', 'Placement_Status'
        ]
    },
    '/home/ubuntu/upload/Suryamitra2021-2022.xlsx': {
        'header_row': 1,  # 0-indexed, row 2 in Excel
        'data_start_row': 2, # 0-indexed, data starts from row 3
        'columns': {
            'S.No': 'S_No',
            'Training Partner': 'Training_Partner',
            'Batch Detail': 'Batch_Detail',
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
            'Placed': 'Placement_Status' # Renaming 'Placed' to 'Placement_Status'
        },
        'relevant_columns': [
            'S_No', 'Training_Partner', 'Batch_Detail', 'Name', 'Father_Name', 'Gender', 'Category',
            'Address', 'District', 'State', 'Mobile_No', 'Aadhar_No', 'Education_Qualification',
            'Diploma_Marks', 'Training_Start_Date', 'Training_End_Date', 'Result', 'Placement_Status'
        ]
    },
    '/home/ubuntu/upload/Suryamitra2022-2023.xlsx': {
        'header_row': 1,  # 0-indexed, row 2 in Excel
        'data_start_row': 2, # 0-indexed, data starts from row 3
        'columns': {
            'S.No': 'S_No',
            'Training Partner': 'Training_Partner',
            'Batch Detail': 'Batch_Detail',
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
            'Placed': 'Placement_Status' # Renaming 'Placed' to 'Placement_Status'
        },
        'relevant_columns': [
            'S_No', 'Training_Partner', 'Batch_Detail', 'Name', 'Father_Name', 'Gender', 'Category',
            'Address', 'District', 'State', 'Mobile_No', 'Aadhar_No', 'Education_Qualification',
            'Diploma_Marks', 'Training_Start_Date', 'Training_End_Date', 'Result', 'Placement_Status'
        ]
    }
}

all_consolidated_data = pd.DataFrame()

for file_path, info in excel_files_info.items():
    print(f"Processing {file_path}...")
    try:
        # Read the Excel file, skipping rows before the header
        df = pd.read_excel(file_path, header=info['header_row'], skiprows=range(info['header_row']))
        
        # Filter out rows that are entirely NaN (often blank rows after the header)
        df = df.dropna(how='all')

        # Rename columns for consistency
        df = df.rename(columns=info['columns'])
        
        # Select only the relevant columns that are present in the dataframe
        cols_to_select = [col for col in info['relevant_columns'] if col in df.columns]
        df_selected = df[cols_to_select]
        
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


