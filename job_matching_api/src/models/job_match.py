from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class JobMatch(db.Model):
    __tablename__ = 'job_matches'
    
    id = db.Column(db.Integer, primary_key=True)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('job_seekers.id'), nullable=False)
    match_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    match_reasons = db.Column(db.Text)  # JSON array explaining match factors
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate matches
    __table_args__ = (db.UniqueConstraint('job_posting_id', 'job_seeker_id', name='unique_job_match'),)

    def __repr__(self):
        return f'<JobMatch {self.job_posting_id}-{self.job_seeker_id}: {self.match_score}>'

    def get_match_reasons_list(self):
        """Parse match reasons JSON string to list"""
        try:
            return json.loads(self.match_reasons) if self.match_reasons else []
        except:
            return []

    def set_match_reasons_list(self, reasons_list):
        """Set match reasons from list to JSON string"""
        self.match_reasons = json.dumps(reasons_list)

    def to_dict(self):
        return {
            'id': self.id,
            'job_posting_id': self.job_posting_id,
            'job_seeker_id': self.job_seeker_id,
            'match_score': self.match_score,
            'match_reasons': self.get_match_reasons_list(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def to_dict_summary(self):
        """Return summary dict for listing purposes"""
        return {
            'id': self.id,
            'job_posting_id': self.job_posting_id,
            'job_seeker_id': self.job_seeker_id,
            'match_score': self.match_score,
            'match_score_percentage': round(self.match_score * 100, 1),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

