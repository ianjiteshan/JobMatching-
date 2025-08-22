#!/usr/bin/env python3
"""
Create Suryamitra database with real data structure based on the PDFs provided
"""

import pandas as pd
import json
import random
from datetime import datetime, timedelta

def create_suryamitra_sample_data():
    """Create sample data based on the real Suryamitra PDF structure"""
    
    # Based on the PDFs, here are the actual candidates I observed:
    real_candidates = [
        # 2020-21 Data (Tamil Nadu)
        {"name": "Ramya Nithya Sri S L", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Jayapriya C", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Kavitha M", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Krishna Moorthi D", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Krishnaveni B", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Manjula T", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "N"},
        {"name": "Mynavathi E", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Nishanth V", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Nithya M", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Renugadevi", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Santhiya S", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "N"},
        {"name": "Sowmiya S", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Sridhar M", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Surya B", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Vinitha V", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "N"},
        {"name": "Ranjith C", "category": "ST", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Balaji M", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "N"},
        {"name": "Haripriya V", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Dhivya Bharathi V", "category": "OBC", "gender": "Female", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Gokul R", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Pass", "placement": "Y"},
        {"name": "Elango C", "category": "OBC", "gender": "Male", "state": "TAMIL NADU", "city": "Coimbatore", "result": "Fail", "placement": "N"},
        
        # 2021-22 Data (Andhra Pradesh)
        {"name": "Veeranki Teja Gowd", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Panthagani Akhil", "category": "SC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Chinta Ravi Kiran", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Katta Ramakrishna", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Choppra Arvind Kumar", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Pamarthi Surya Venkata Purnacharyulu", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "KONA SAIBABU", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Mohammad Rasheed", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Mohammed Moheeddin", "category": "OBC", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Konduru Bhavana Varsha", "category": "OBC", "gender": "Female", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        {"name": "Cherukula Hemanth Reddy", "category": "Gen", "gender": "Male", "state": "ANDHRA PRADESH", "city": "Vijayawada", "result": "Pass", "placement": "-"},
        
        # 2022-23 Data (West Bengal)
        {"name": "Annapurna Bhowmick", "category": "Gen", "gender": "Female", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Abhijit Hansda", "category": "SC", "gender": "Male", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Arkadeep Das", "category": "SC", "gender": "Male", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Arpan Jana", "category": "Gen", "gender": "Male", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Avishek Sharma", "category": "Gen", "gender": "Male", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Debabrota Adhikary", "category": "Gen", "gender": "Male", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Debanna Datta", "category": "Gen", "gender": "Female", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Monisha Saha", "category": "Gen", "gender": "Female", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        {"name": "Nandini Mondal", "category": "Gen", "gender": "Female", "state": "WEST BENGAL", "city": "Kolkata", "result": "Pass", "placement": "-"},
        
        # 2022-23 Data (Uttar Pradesh)
        {"name": "Deepak Kumar", "category": "OBC", "gender": "Male", "state": "UTTAR PRADESH", "city": "Lucknow", "result": "Pass", "placement": "-"},
        {"name": "Nitin Sharma", "category": "Gen", "gender": "Male", "state": "UTTAR PRADESH", "city": "Lucknow", "result": "Pass", "placement": "-"},
        {"name": "Saurabh Purohit", "category": "Gen", "gender": "Male", "state": "UTTAR PRADESH", "city": "Lucknow", "result": "Pass", "placement": "-"},
        {"name": "Virendra Kumar", "category": "SC", "gender": "Male", "state": "UTTAR PRADESH", "city": "Lucknow", "result": "Pass", "placement": "-"},
        {"name": "Romesh Yadav", "category": "OBC", "gender": "Male", "state": "UTTAR PRADESH", "city": "Lucknow", "result": "Pass", "placement": "-"},
        {"name": "Vimlesh Kumar", "category": "OBC", "gender": "Male", "state": "UTTAR PRADESH", "city": "Lucknow", "result": "Pass", "placement": "-"},
    ]
    
    # Create structured database records
    job_seekers = []
    
    for i, candidate in enumerate(real_candidates, 1):
        # Generate realistic phone numbers
        phone = f"+91-{random.randint(70000, 99999)}{random.randint(10000, 99999)}"
        
        # Generate email
        email = f"{candidate['name'].lower().replace(' ', '.')}@gmail.com"
        
        # Assign diploma scores based on result and some variation
        if candidate['result'] == 'Pass':
            base_score = random.uniform(75, 95)
        else:
            base_score = random.uniform(45, 65)
        
        # Add some variation based on placement status
        if candidate['placement'] == 'Y':
            diploma_score = min(95, base_score + random.uniform(5, 15))
        elif candidate['placement'] == 'N':
            diploma_score = max(60, base_score - random.uniform(0, 10))
        else:  # placement == '-'
            diploma_score = base_score
        
        # Create skills based on solar technician training
        skills = [
            "Solar Panel Installation",
            "Solar System Maintenance", 
            "Electrical Wiring",
            "Power System Analysis",
            "Safety Protocols",
            "Technical Documentation"
        ]
        
        # Add some variation in skills
        candidate_skills = skills[:random.randint(4, 6)]
        if random.random() > 0.7:  # 30% chance of additional skills
            additional_skills = ["Project Management", "Customer Service", "Quality Control", "Troubleshooting"]
            candidate_skills.extend(random.sample(additional_skills, random.randint(1, 2)))
        
        job_seeker = {
            'id': i,
            'name': candidate['name'],
            'phone_number': phone,
            'email': email,
            'city': candidate['city'],
            'state': candidate['state'],
            'qualifications': 'Suryamitra Solar Technician Certification',
            'diploma_score': round(diploma_score, 2),
            'experience_years': 0,  # Fresh graduates
            'skills': json.dumps(candidate_skills),
            'category': candidate['category'],
            'gender': candidate['gender'],
            'training_result': candidate['result'],
            'placement_status': 'Placed' if candidate['placement'] == 'Y' else 'Not Placed' if candidate['placement'] == 'N' else 'Unknown',
            'preferred_salary_min': random.randint(15000, 25000),
            'preferred_salary_max': random.randint(25000, 40000),
            'availability_status': 'available'
        }
        
        job_seekers.append(job_seeker)
    
    return job_seekers

def create_sample_job_postings():
    """Create sample job postings that would match Suryamitra candidates"""
    
    job_postings = [
        {
            'id': 1,
            'title': 'Solar Panel Installation Technician',
            'description': 'Looking for certified solar technicians for residential and commercial solar panel installations.',
            'required_qualifications': 'Solar technician certification, Basic electrical knowledge',
            'required_skills': json.dumps(['Solar Panel Installation', 'Electrical Wiring', 'Safety Protocols']),
            'preferred_skills': json.dumps(['Project Management', 'Customer Service']),
            'city': 'Coimbatore',
            'state': 'TAMIL NADU',
            'salary_min': 18000,
            'salary_max': 30000,
            'experience_required': 0,
            'minimum_diploma_score': 70.0,
            'status': 'active'
        },
        {
            'id': 2,
            'title': 'Solar System Maintenance Engineer',
            'description': 'Seeking skilled professionals for solar system maintenance and troubleshooting.',
            'required_qualifications': 'Technical certification in solar energy systems',
            'required_skills': json.dumps(['Solar System Maintenance', 'Troubleshooting', 'Technical Documentation']),
            'preferred_skills': json.dumps(['Power System Analysis', 'Quality Control']),
            'city': 'Vijayawada',
            'state': 'ANDHRA PRADESH',
            'salary_min': 20000,
            'salary_max': 35000,
            'experience_required': 0,
            'minimum_diploma_score': 75.0,
            'status': 'active'
        },
        {
            'id': 3,
            'title': 'Junior Solar Engineer',
            'description': 'Entry-level position for solar energy system design and installation support.',
            'required_qualifications': 'Engineering degree or technical certification in renewable energy',
            'required_skills': json.dumps(['Solar Panel Installation', 'Power System Analysis', 'Technical Documentation']),
            'preferred_skills': json.dumps(['Project Management', 'Customer Service', 'Quality Control']),
            'city': 'Kolkata',
            'state': 'WEST BENGAL',
            'salary_min': 22000,
            'salary_max': 38000,
            'experience_required': 0,
            'minimum_diploma_score': 80.0,
            'status': 'active'
        },
        {
            'id': 4,
            'title': 'Solar Field Technician',
            'description': 'Field technician role for solar farm maintenance and operations.',
            'required_qualifications': 'Solar technician training, Physical fitness for field work',
            'required_skills': json.dumps(['Solar System Maintenance', 'Electrical Wiring', 'Safety Protocols']),
            'preferred_skills': json.dumps(['Troubleshooting', 'Technical Documentation']),
            'city': 'Lucknow',
            'state': 'UTTAR PRADESH',
            'salary_min': 16000,
            'salary_max': 28000,
            'experience_required': 0,
            'minimum_diploma_score': 65.0,
            'status': 'active'
        },
        {
            'id': 5,
            'title': 'Solar Installation Supervisor',
            'description': 'Supervisory role for solar installation projects, leading small teams.',
            'required_qualifications': 'Solar technician certification, Leadership experience preferred',
            'required_skills': json.dumps(['Solar Panel Installation', 'Project Management', 'Safety Protocols']),
            'preferred_skills': json.dumps(['Customer Service', 'Quality Control', 'Technical Documentation']),
            'city': 'Chennai',
            'state': 'TAMIL NADU',
            'salary_min': 25000,
            'salary_max': 45000,
            'experience_required': 1,
            'minimum_diploma_score': 85.0,
            'status': 'active'
        }
    ]
    
    return job_postings

def main():
    """Create the Suryamitra database with real data structure"""
    
    print("Creating Suryamitra Job Matching Database...")
    
    # Create job seekers data
    job_seekers = create_suryamitra_sample_data()
    job_seekers_df = pd.DataFrame(job_seekers)
    
    # Create job postings data
    job_postings = create_sample_job_postings()
    job_postings_df = pd.DataFrame(job_postings)
    
    # Save to CSV files
    job_seekers_df.to_csv('/home/ubuntu/job_matching_api/suryamitra_job_seekers.csv', index=False)
    job_postings_df.to_csv('/home/ubuntu/job_matching_api/sample_job_postings.csv', index=False)
    
    print(f"Created {len(job_seekers)} job seeker records")
    print(f"Created {len(job_postings)} job posting records")
    
    # Display summary statistics
    print("\n=== JOB SEEKERS SUMMARY ===")
    print(f"Total candidates: {len(job_seekers_df)}")
    print("\nBy State:")
    print(job_seekers_df['state'].value_counts())
    print("\nBy Gender:")
    print(job_seekers_df['gender'].value_counts())
    print("\nBy Category:")
    print(job_seekers_df['category'].value_counts())
    print("\nBy Training Result:")
    print(job_seekers_df['training_result'].value_counts())
    print("\nBy Placement Status:")
    print(job_seekers_df['placement_status'].value_counts())
    
    print(f"\nAverage Diploma Score: {job_seekers_df['diploma_score'].mean():.2f}")
    print(f"Score Range: {job_seekers_df['diploma_score'].min():.2f} - {job_seekers_df['diploma_score'].max():.2f}")
    
    print("\n=== JOB POSTINGS SUMMARY ===")
    print(f"Total job postings: {len(job_postings_df)}")
    print("\nBy State:")
    print(job_postings_df['state'].value_counts())
    print(f"\nSalary Range: ₹{job_postings_df['salary_min'].min():,} - ₹{job_postings_df['salary_max'].max():,}")
    
    print("\n=== SAMPLE RECORDS ===")
    print("\nSample Job Seekers:")
    print(job_seekers_df[['name', 'city', 'state', 'diploma_score', 'placement_status']].head())
    
    print("\nSample Job Postings:")
    print(job_postings_df[['title', 'city', 'state', 'salary_min', 'salary_max']].head())
    
    print("\nDatabase files created successfully!")
    print("- suryamitra_job_seekers.csv")
    print("- sample_job_postings.csv")

if __name__ == "__main__":
    main()

