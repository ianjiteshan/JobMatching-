#!/usr/bin/env python3
"""
Script to extract Suryamitra training data from PDFs and create structured database
"""

import pandas as pd
import pdfplumber
import re
import json
from pathlib import Path

def extract_candidate_data(pdf_path, year):
    """Extract candidate data from Suryamitra PDF"""
    candidates = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            for line in lines:
                # Skip header lines and empty lines
                if (any(header in line for header in ['S.No', 'Batch Detail', 'Suryamitra Skill Development', 'Training Partner']) or
                    line.strip() == '' or len(line.strip()) < 20):
                    continue
                
                # Try to parse candidate data from each line
                try:
                    # Split by multiple spaces to separate fields
                    parts = re.split(r'\s{2,}', line.strip())
                    
                    if len(parts) < 8:  # Not enough data fields
                        continue
                    
                    # Extract serial number (first field should be a number)
                    sno_match = re.match(r'^(\d+)', parts[0])
                    if not sno_match:
                        continue
                    
                    sno = int(sno_match.group(1))
                    
                    # Parse the line to extract candidate information
                    # The format varies slightly between years, so we'll be flexible
                    
                    candidate_data = {
                        'serial_no': sno,
                        'year': year,
                        'raw_line': line.strip()
                    }
                    
                    # Try to extract key fields based on common patterns
                    # Look for name (usually after state name)
                    name_pattern = r'(TAMIL NADU|ANDHRA PRADESH|WEST BENGAL|UTTAR PRADESH)\s+([A-Za-z\s]+?)\s+(OBC|SC|ST|Gen)\s+(Male|Female)'
                    name_match = re.search(name_pattern, line)
                    
                    if name_match:
                        candidate_data['state'] = name_match.group(1)
                        candidate_data['name'] = name_match.group(2).strip()
                        candidate_data['category'] = name_match.group(3)
                        candidate_data['gender'] = name_match.group(4)
                    
                    # Extract result (Pass/Fail)
                    result_match = re.search(r'\b(Pass|Fail)\b', line)
                    if result_match:
                        candidate_data['result'] = result_match.group(1)
                    
                    # Extract placement status (Y/N or -)
                    placement_match = re.search(r'\b(Pass|Fail)\s+([YN-])\s*$', line)
                    if placement_match:
                        placement_status = placement_match.group(2)
                        candidate_data['placement_status'] = 'Yes' if placement_status == 'Y' else 'No' if placement_status == 'N' else 'Unknown'
                    
                    # Extract batch information
                    batch_match = re.search(r'BCH/(\d{4}-\d{4})/(\d+)', line)
                    if batch_match:
                        candidate_data['batch_year'] = batch_match.group(1)
                        candidate_data['batch_id'] = batch_match.group(2)
                    
                    # Extract training dates
                    date_pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{4}-\d{2}-\d{2})'
                    date_match = re.search(date_pattern, line)
                    if date_match:
                        candidate_data['training_start'] = date_match.group(1)
                        candidate_data['training_end'] = date_match.group(2)
                    
                    # Extract city information
                    city_pattern = r'(Vadavalli|Vijayawada|Visakhapatnam|Kolkata|lucknow)'
                    city_match = re.search(city_pattern, line)
                    if city_match:
                        candidate_data['training_city'] = city_match.group(1)
                    
                    # Only add if we have essential information
                    if 'name' in candidate_data and 'result' in candidate_data:
                        candidates.append(candidate_data)
                        
                except Exception as e:
                    # Skip problematic lines
                    continue
    
    return candidates

def main():
    """Main function to process all PDFs and create structured data"""
    
    # PDF file paths
    pdf_files = [
        ('/home/ubuntu/upload/Suryamitra2020-21.pdf', '2020-21'),
        ('/home/ubuntu/upload/SuryamitraData2021-22.pdf', '2021-22'),
        ('/home/ubuntu/upload/SuryamitraData2022-23.pdf', '2022-23')
    ]
    
    all_candidates = []
    
    print("Extracting Suryamitra candidate data...")
    
    for pdf_path, year in pdf_files:
        print(f"\nProcessing {pdf_path} ({year})...")
        candidates = extract_candidate_data(pdf_path, year)
        all_candidates.extend(candidates)
        print(f"Extracted {len(candidates)} candidates from {year}")
    
    print(f"\nTotal candidates extracted: {len(all_candidates)}")
    
    # Create DataFrame
    df = pd.DataFrame(all_candidates)
    
    # Save to CSV
    csv_path = '/home/ubuntu/job_matching_api/suryamitra_candidates.csv'
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
    # Display summary statistics
    print("\n=== DATA SUMMARY ===")
    print(f"Total records: {len(df)}")
    
    if 'year' in df.columns:
        print("\nRecords by year:")
        print(df['year'].value_counts().sort_index())
    
    if 'result' in df.columns:
        print("\nResults distribution:")
        print(df['result'].value_counts())
    
    if 'gender' in df.columns:
        print("\nGender distribution:")
        print(df['gender'].value_counts())
    
    if 'category' in df.columns:
        print("\nCategory distribution:")
        print(df['category'].value_counts())
    
    if 'placement_status' in df.columns:
        print("\nPlacement status:")
        print(df['placement_status'].value_counts())
    
    # Show sample records
    print("\n=== SAMPLE RECORDS ===")
    print(df.head(3).to_string())
    
    # Create a clean dataset for the job matching system
    clean_data = []
    for _, row in df.iterrows():
        if pd.notna(row.get('name')) and pd.notna(row.get('result')):
            # Create a clean record with standardized fields
            clean_record = {
                'name': row.get('name', '').strip(),
                'gender': row.get('gender', 'Unknown'),
                'category': row.get('category', 'Unknown'),
                'state': row.get('state', 'Unknown'),
                'training_city': row.get('training_city', 'Unknown'),
                'result': row.get('result', 'Unknown'),
                'placement_status': row.get('placement_status', 'Unknown'),
                'year': row.get('year', 'Unknown'),
                'batch_year': row.get('batch_year', 'Unknown'),
                'training_start': row.get('training_start', ''),
                'training_end': row.get('training_end', ''),
                # Add derived fields for ML
                'passed_training': 1 if row.get('result') == 'Pass' else 0,
                'got_placement': 1 if row.get('placement_status') == 'Yes' else 0,
                'qualification': 'Suryamitra Solar Technician Training',  # Standard qualification
                'skills': json.dumps(['Solar Panel Installation', 'Solar System Maintenance', 'Electrical Work', 'Technical Skills']),
                'experience_years': 0,  # Fresh graduates
                'diploma_score': 85.0 if row.get('result') == 'Pass' else 60.0,  # Estimated scores
            }
            clean_data.append(clean_record)
    
    # Save clean dataset
    clean_df = pd.DataFrame(clean_data)
    clean_csv_path = '/home/ubuntu/job_matching_api/suryamitra_clean_data.csv'
    clean_df.to_csv(clean_csv_path, index=False)
    print(f"\nClean dataset saved to {clean_csv_path}")
    print(f"Clean records: {len(clean_df)}")
    
    return clean_df

if __name__ == "__main__":
    main()

