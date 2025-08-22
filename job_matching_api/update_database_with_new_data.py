import pandas as pd
import sqlite3
from datetime import datetime
import os

# Read the consolidated data
csv_file_path = '/home/ubuntu/job_matching_api/suryamitra_final_cleaned_2018_2023.csv'
df = pd.read_csv(csv_file_path)

print(f"Loading {len(df)} records from consolidated data...")

# Database connection - use the correct path
db_path = '/home/ubuntu/job_matching_api/src/database/app.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clear existing job_seekers data to replace with new data
cursor.execute("DELETE FROM job_seekers")
print("Cleared existing job seeker data...")

# Prepare data for insertion
job_seekers_data = []
for index, row in df.iterrows():
    # Handle missing values and data type conversions
    name = str(row['Name']) if pd.notna(row['Name']) else f"Candidate_{index+1}"
    phone_number = str(row['Mobile_No']) if pd.notna(row['Mobile_No']) else ""
    email = ""  # Not available in the Excel data
    city = str(row['District']) if pd.notna(row['District']) else ""
    state = str(row['State']) if pd.notna(row['State']) else ""
    qualifications = str(row['Education_Qualification']) if pd.notna(row['Education_Qualification']) else ""
    
    # Handle diploma marks - convert to float, default to 75.0 if missing
    try:
        diploma_score = float(row['Diploma_Marks']) if pd.notna(row['Diploma_Marks']) else 75.0
    except (ValueError, TypeError):
        diploma_score = 75.0
    
    # Experience years - default to 0 for entry level
    experience_years = 0
    
    category = str(row['Category']) if pd.notna(row['Category']) else "General"
    gender = str(row['Gender']) if pd.notna(row['Gender']) else "Unknown"
    
    # Handle result and placement status
    training_result = str(row['Result']) if pd.notna(row['Result']) else "Pass"
    placement_status = str(row['Placement_Status']) if pd.notna(row['Placement_Status']) else "Unknown"
    
    # Standardize placement status
    if placement_status.lower() in ['yes', 'y', 'placed', 'true']:
        placement_status = "Placed"
        availability_status = "Unavailable"
    elif placement_status.lower() in ['no', 'n', 'not placed', 'false']:
        placement_status = "Not Placed"
        availability_status = "Available"
    else:
        placement_status = "Unknown"
        availability_status = "Available"
    
    # Generate skills based on education qualification and result
    skills = []
    if "solar" in qualifications.lower() or "renewable" in qualifications.lower():
        skills.extend(["Solar Panel Installation", "Solar System Maintenance", "Renewable Energy"])
    else:
        skills.extend(["Solar Panel Installation", "Electrical Work", "Technical Skills"])
    
    if training_result.lower() == "pass":
        skills.append("Certified Technician")
    
    skills_str = ", ".join(skills)
    
    job_seekers_data.append((
        name, phone_number, email, city, state, qualifications, diploma_score,
        experience_years, category, gender, training_result, placement_status,
        availability_status, skills_str, datetime.now().isoformat()
    ))

# Insert data into job_seekers table
insert_query = """
INSERT INTO job_seekers (
    name, phone_number, email, city, state, qualifications, diploma_score,
    experience_years, category, gender, training_result, placement_status,
    availability_status, skills, created_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(insert_query, job_seekers_data)
conn.commit()

print(f"Successfully inserted {len(job_seekers_data)} job seekers into the database.")

# Verify the insertion
cursor.execute("SELECT COUNT(*) FROM job_seekers")
count = cursor.fetchone()[0]
print(f"Total job seekers in database: {count}")

# Display some sample records
cursor.execute("SELECT name, state, diploma_score, placement_status FROM job_seekers LIMIT 10")
sample_records = cursor.fetchall()
print("\nSample records:")
for record in sample_records:
    print(f"Name: {record[0]}, State: {record[1]}, Score: {record[2]}, Status: {record[3]}")

# Display statistics
cursor.execute("SELECT state, COUNT(*) FROM job_seekers GROUP BY state ORDER BY COUNT(*) DESC LIMIT 10")
state_stats = cursor.fetchall()
print("\nTop 10 states by candidate count:")
for state, count in state_stats:
    print(f"{state}: {count} candidates")

cursor.execute("SELECT placement_status, COUNT(*) FROM job_seekers GROUP BY placement_status")
placement_stats = cursor.fetchall()
print("\nPlacement status distribution:")
for status, count in placement_stats:
    print(f"{status}: {count} candidates")

conn.close()
print("Database update completed successfully!")

