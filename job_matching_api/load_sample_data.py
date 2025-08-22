#!/usr/bin/env python3
"""
Load Suryamitra sample data into the database
"""

import pandas as pd
import json
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app
from src.models.user import User
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.models.user import db

def load_job_seekers():
    """Load job seekers from CSV file"""
    try:
        df = pd.read_csv('/home/ubuntu/job_matching_api/suryamitra_job_seekers.csv')
        
        loaded_count = 0
        
        for _, row in df.iterrows():
            # Check if job seeker already exists
            existing = JobSeeker.query.filter_by(name=row['name']).first()
            if existing:
                continue
            
            # Create new job seeker
            job_seeker = JobSeeker(
                name=row['name'],
                phone_number=row['phone_number'],
                email=row['email'],
                city=row['city'],
                state=row['state'],
                qualifications=row['qualifications'],
                diploma_score=row['diploma_score'],
                experience_years=row['experience_years'],
                category=row['category'],
                gender=row['gender'],
                training_result=row['training_result'],
                placement_status=row['placement_status'],
                preferred_salary_min=row['preferred_salary_min'],
                preferred_salary_max=row['preferred_salary_max'],
                availability_status=row['availability_status']
            )
            
            # Set skills
            try:
                skills = json.loads(row['skills'])
                job_seeker.set_skills_list(skills)
            except:
                pass
            
            db.session.add(job_seeker)
            loaded_count += 1
        
        db.session.commit()
        print(f"Loaded {loaded_count} job seekers")
        return loaded_count
        
    except Exception as e:
        print(f"Error loading job seekers: {e}")
        db.session.rollback()
        return 0

def load_job_postings():
    """Load job postings from CSV file"""
    try:
        df = pd.read_csv('/home/ubuntu/job_matching_api/sample_job_postings.csv')
        
        loaded_count = 0
        
        for _, row in df.iterrows():
            # Check if job posting already exists
            existing = JobPosting.query.filter_by(title=row['title'], city=row['city']).first()
            if existing:
                continue
            
            # Create new job posting
            job_posting = JobPosting(
                employer_id=1,  # Default employer
                title=row['title'],
                description=row['description'],
                required_qualifications=row['required_qualifications'],
                city=row['city'],
                state=row['state'],
                salary_min=row['salary_min'],
                salary_max=row['salary_max'],
                experience_required=row['experience_required'],
                minimum_diploma_score=row['minimum_diploma_score'],
                status=row['status']
            )
            
            # Set skills
            try:
                required_skills = json.loads(row['required_skills'])
                job_posting.set_required_skills_list(required_skills)
            except:
                pass
            
            try:
                preferred_skills = json.loads(row['preferred_skills'])
                job_posting.set_preferred_skills_list(preferred_skills)
            except:
                pass
            
            db.session.add(job_posting)
            loaded_count += 1
        
        db.session.commit()
        print(f"Loaded {loaded_count} job postings")
        return loaded_count
        
    except Exception as e:
        print(f"Error loading job postings: {e}")
        db.session.rollback()
        return 0

def create_default_users():
    """Create default admin and employer users"""
    try:
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@suryamitra.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        # Create employer user
        employer = User.query.filter_by(username='employer').first()
        if not employer:
            employer = User(
                username='employer',
                email='employer@company.com',
                role='employer'
            )
            employer.set_password('employer123')
            db.session.add(employer)
        
        db.session.commit()
        print("Created default users (admin/admin123, employer/employer123)")
        
    except Exception as e:
        print(f"Error creating users: {e}")
        db.session.rollback()

def main():
    """Main function to load all sample data"""
    with app.app_context():
        print("Loading Suryamitra sample data...")
        
        # Create default users
        create_default_users()
        
        # Load job seekers
        seekers_count = load_job_seekers()
        
        # Load job postings
        postings_count = load_job_postings()
        
        print(f"\nData loading complete!")
        print(f"- Job seekers: {seekers_count}")
        print(f"- Job postings: {postings_count}")
        print(f"- Default users created")
        
        # Display summary
        total_seekers = JobSeeker.query.count()
        total_postings = JobPosting.query.count()
        total_users = User.query.count()
        
        print(f"\nDatabase summary:")
        print(f"- Total job seekers: {total_seekers}")
        print(f"- Total job postings: {total_postings}")
        print(f"- Total users: {total_users}")

if __name__ == "__main__":
    main()

