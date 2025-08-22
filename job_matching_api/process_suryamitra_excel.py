import pandas as pd
import os

def process_2018_2019_data(file_path):
    df = pd.read_excel(file_path, header=3) # Header is on 4th row (index 3)
    df = df.iloc[1:].copy() # Skip the extra header row
    df = df.rename(columns={
        'Training Partner': 'Training_Partner',
        'Batch Detail': 'Batch_Detail',
        'Count of Placement': 'Placement_Count',
        'Payment Record': 'Payment_Record'
    })
    # Select relevant columns and add placeholders for missing ones
    cols = ['Training_Partner', 'Batch_Detail', 'Placement_Count', 'Payment_Record']
    for col in ['Name', 'Father_Name', 'Gender', 'Category', 'Address', 'District', 'State', 'Mobile_No', 'Aadhar_No', 'Education_Qualification', 'Diploma_Marks', 'Training_Start_Date', 'Training_End_Date', 'Result', 'Placement_Status']:
        if col not in df.columns:
            df[col] = None
    return df[cols + [c for c in df.columns if c not in cols]]

def process_2020_2021_data(file_path):
    df = pd.read_excel(file_path, header=1) # Header is on 2nd row (index 1)
    df = df.iloc[1:].copy() # Skip the extra header row
    df = df.rename(columns={
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
    })
    # Select relevant columns and add placeholders for missing ones
    cols = ['S_No', 'Name', 'Father_Name', 'Gender', 'Category', 'Address', 'District', 'State', 'Mobile_No', 'Aadhar_No', 'Education_Qualification', 'Diploma_Marks', 'Training_Start_Date', 'Training_End_Date', 'Result', 'Placement_Status']
    for col in ['Training_Partner', 'Batch_Detail', 'Placement_Count', 'Payment_Record']:
        if col not in df.columns:
            df[col] = None
    return df[cols + [c for c in df.columns if c not in cols]]

def process_2021_2023_data(file_path):
    df = pd.read_excel(file_path, header=1) # Header is on 2nd row (index 1)
    df = df.iloc[1:].copy() # Skip the extra header row
    df = df.rename(columns={
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
        'Placed': 'Placement_Status' # Rename 'Placed' to 'Placement_Status'
    })
    # Select relevant columns and add placeholders for missing ones
    cols = ['S_No', 'Training_Partner', 'Batch_Detail', 'Name', 'Father_Name', 'Gender', 'Category', 'Address', 'District', 'State', 'Mobile_No', 'Aadhar_No', 'Education_Qualification', 'Diploma_Marks', 'Training_Start_Date', 'Training_End_Date', 'Result', 'Placement_Status']
    for col in ['Placement_Count', 'Payment_Record']:
        if col not in df.columns:
            df[col] = None
    return df[cols + [c for c in df.columns if c not in cols]]


excel_files = {
    'Suryamitra2018-2019.xlsx': process_2018_2019_data,
    'Suryamitra2019-2020.xlsx': process_2018_2019_data,
    'Suryamitra2020-2021.xlsx': process_2020_2021_data,
    'Suryamitra2021-2022.xlsx': process_2021_2023_data,
    'Suryamitra2022-2023.xlsx': process_2021_2023_data
}

all_consolidated_data = pd.DataFrame()

for file_path, process_func in excel_files.items():
    print(f"Processing {file_path}...")
    try:
        df_processed = process_func(file_path)
        all_consolidated_data = pd.concat([all_consolidated_data, df_processed], ignore_index=True)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

output_csv_path = 'suryamitra_consolidated_2018_2023.csv'
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
    # Convert 'Diploma_Marks' to numeric, coercing errors
    all_consolidated_data['Diploma_Marks'] = pd.to_numeric(all_consolidated_data['Diploma_Marks'], errors='coerce')

if 'Placement_Status' in all_consolidated_data.columns:
    # Fill missing 'Placement_Status' values with 'Unknown'
    all_consolidated_data['Placement_Status'] = all_consolidated_data['Placement_Status'].fillna('Unknown')

if 'Gender' in all_consolidated_data.columns:
    # Standardize 'Gender' column
    all_consolidated_data['Gender'] = all_consolidated_data['Gender'].replace({'M': 'Male', 'F': 'Female', 'm': 'Male', 'f': 'Female'})

if 'Category' in all_consolidated_data.columns:
    # Standardize 'Category' column
    all_consolidated_data['Category'] = all_consolidated_data['Category'].replace({'GEN': 'General', 'OBC': 'OBC', 'SC': 'SC', 'ST': 'ST'})

# Drop rows where 'Name' is NaN, as these are likely empty rows
if 'Name' in all_consolidated_data.columns:
    all_consolidated_data.dropna(subset=['Name'], inplace=True)

# Save the final cleaned data
final_output_csv_path = 'suryamitra_final_cleaned_2018_2023.csv'
all_consolidated_data.to_csv(final_output_csv_path, index=False)
print(f"Final cleaned data saved to {final_output_csv_path}")

print("\nFirst 5 rows of final cleaned data:")
print(all_consolidated_data.head())
print("\nColumns in final cleaned data:")
print(all_consolidated_data.columns.tolist())
print("\nTotal rows in final cleaned data:", len(all_consolidated_data))

