from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class JobSeeker(db.Model):
    __tablename__ = 'job_seekers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    diploma_score = db.Column(db.Float, nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    skills = db.Column(db.Text)  # JSON string of skills array
    category = db.Column(db.String(10))  # OBC, SC, ST, Gen
    gender = db.Column(db.String(10))  # Male, Female
    training_result = db.Column(db.String(10))  # Pass, Fail
    placement_status = db.Column(db.String(20))  # Placed, Not Placed, Unknown
    preferred_salary_min = db.Column(db.Integer)
    preferred_salary_max = db.Column(db.Integer)
    availability_status = db.Column(db.String(20), default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<JobSeeker {self.name}>'

    def get_skills_list(self):
        """Parse skills JSON string to list"""
        try:
            return json.loads(self.skills) if self.skills else []
        except:
            return []

    def set_skills_list(self, skills_list):
        """Set skills from list to JSON string"""
        self.skills = json.dumps(skills_list)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'email': self.email,
            'city': self.city,
            'state': self.state,
            'qualifications': self.qualifications,
            'diploma_score': self.diploma_score,
            'experience_years': self.experience_years,
            'skills': self.get_skills_list(),
            'category': self.category,
            'gender': self.gender,
            'training_result': self.training_result,
            'placement_status': self.placement_status,
            'preferred_salary_min': self.preferred_salary_min,
            'preferred_salary_max': self.preferred_salary_max,
            'availability_status': self.availability_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def to_dict_summary(self):
        """Return summary dict for listing purposes"""
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'qualifications': self.qualifications,
            'diploma_score': self.diploma_score,
            'experience_years': self.experience_years,
            'skills_count': len(self.get_skills_list()),
            'category': self.category,
            'gender': self.gender,
            'training_result': self.training_result,
            'placement_status': self.placement_status,
            'availability_status': self.availability_status
        }

