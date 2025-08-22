from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_qualifications = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text)  # JSON array of required skills
    preferred_skills = db.Column(db.Text)  # JSON array of preferred skills
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    experience_required = db.Column(db.Integer, default=0)
    minimum_diploma_score = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, inactive, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<JobPosting {self.title}>'

    def get_required_skills_list(self):
        """Parse required skills JSON string to list"""
        try:
            return json.loads(self.required_skills) if self.required_skills else []
        except:
            return []

    def set_required_skills_list(self, skills_list):
        """Set required skills from list to JSON string"""
        self.required_skills = json.dumps(skills_list)

    def get_preferred_skills_list(self):
        """Parse preferred skills JSON string to list"""
        try:
            return json.loads(self.preferred_skills) if self.preferred_skills else []
        except:
            return []

    def set_preferred_skills_list(self, skills_list):
        """Set preferred skills from list to JSON string"""
        self.preferred_skills = json.dumps(skills_list)

    def to_dict(self):
        return {
            'id': self.id,
            'employer_id': self.employer_id,
            'title': self.title,
            'description': self.description,
            'required_qualifications': self.required_qualifications,
            'required_skills': self.get_required_skills_list(),
            'preferred_skills': self.get_preferred_skills_list(),
            'city': self.city,
            'state': self.state,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'experience_required': self.experience_required,
            'minimum_diploma_score': self.minimum_diploma_score,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def to_dict_summary(self):
        """Return summary dict for listing purposes"""
        return {
            'id': self.id,
            'title': self.title,
            'city': self.city,
            'state': self.state,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'experience_required': self.experience_required,
            'minimum_diploma_score': self.minimum_diploma_score,
            'status': self.status,
            'required_skills_count': len(self.get_required_skills_list()),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

