#!/usr/bin/env python3
"""
Fix database initialization and load sample data
"""
import os
import sys
import pandas as pd
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'suryamitra_job_matching_secret_key_2025'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define models directly here to avoid import issues
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class JobSeeker(db.Model):
    __tablename__ = 'job_seekers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    qualifications = db.Column(db.Text)
    diploma_score = db.Column(db.Float)
    experience_years = db.Column(db.Integer, default=0)
    category = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    training_result = db.Column(db.String(20))
    placement_status = db.Column(db.String(20))
    availability_status = db.Column(db.String(20), default='available')
    skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    required_qualifications = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    experience_required = db.Column(db.Integer, default=0)
    minimum_diploma_score = db.Column(db.Float)
    required_skills = db.Column(db.Text)
    preferred_skills = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def load_job_seekers():
    """Load job seekers from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), 'suryamitra_job_seekers.csv')
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return 0
    
    df = pd.read_csv(csv_path)
    count = 0
    
    for _, row in df.iterrows():
        # Check if job seeker already exists
        existing = JobSeeker.query.filter_by(name=row['name']).first()
        if existing:
            continue
            
        job_seeker = JobSeeker(
            name=row['name'],
            phone_number=row.get('phone_number', ''),
            email=row.get('email', ''),
            city=row['city'],
            state=row['state'],
            qualifications=row.get('qualifications', ''),
            diploma_score=float(row['diploma_score']) if pd.notna(row['diploma_score']) else 0.0,
            experience_years=int(row.get('experience_years', 0)),
            category=row.get('category', 'Gen'),
            gender=row.get('gender', 'Male'),
            training_result=row.get('training_result', 'Pass'),
            placement_status=row.get('placement_status', 'Available'),
            availability_status='available',
            skills=row.get('skills', '')
        )
        
        db.session.add(job_seeker)
        count += 1
    
    db.session.commit()
    return count

def load_job_postings():
    """Load job postings from CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), 'sample_job_postings.csv')
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return 0
    
    df = pd.read_csv(csv_path)
    count = 0
    
    for _, row in df.iterrows():
        # Check if job posting already exists
        existing = JobPosting.query.filter_by(title=row['title'], city=row['city']).first()
        if existing:
            continue
            
        job_posting = JobPosting(
            title=row['title'],
            description=row.get('description', ''),
            required_qualifications=row.get('required_qualifications', ''),
            city=row['city'],
            state=row['state'],
            salary_min=int(row['salary_min']),
            salary_max=int(row['salary_max']),
            experience_required=int(row.get('experience_required', 0)),
            minimum_diploma_score=float(row.get('minimum_diploma_score', 0.0)),
            required_skills=row.get('required_skills', ''),
            preferred_skills=row.get('preferred_skills', ''),
            status='active'
        )
        
        db.session.add(job_posting)
        count += 1
    
    db.session.commit()
    return count

def create_default_users():
    """Create default admin and employer users"""
    # Create admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create employer user
    employer = User.query.filter_by(username='employer').first()
    if not employer:
        employer = User(username='employer', role='employer')
        employer.set_password('employer123')
        db.session.add(employer)
    
    db.session.commit()

def main():
    """Main function to initialize database and load data"""
    with app.app_context():
        print("Initializing database...")
        
        # Create database directory if it doesn't exist
        db_dir = os.path.join(os.path.dirname(__file__), 'src', 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Create default users
        create_default_users()
        print("Default users created!")
        
        # Load job seekers
        job_seekers_count = load_job_seekers()
        print(f"Loaded {job_seekers_count} job seekers")
        
        # Load job postings
        job_postings_count = load_job_postings()
        print(f"Loaded {job_postings_count} job postings")
        
        # Print summary
        total_seekers = JobSeeker.query.count()
        total_postings = JobPosting.query.count()
        total_users = User.query.count()
        
        print(f"\n=== DATABASE SUMMARY ===")
        print(f"Total job seekers: {total_seekers}")
        print(f"Total job postings: {total_postings}")
        print(f"Total users: {total_users}")
        print("Database initialization complete!")

if __name__ == '__main__':
    main()

