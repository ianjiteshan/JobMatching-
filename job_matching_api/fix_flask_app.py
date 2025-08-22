import os
import sys
sys.path.append('./src')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Import models to register them with SQLAlchemy
from models.user import User
from models.job_seeker import JobSeeker
from models.job_posting import JobPosting
from models.job_match import JobMatch

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    print("Database tables created/verified successfully!")

# Import and register routes
from routes.admin import admin_bp
from routes.employer import employer_bp

app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(employer_bp, url_prefix='/api/employer')

@app.route('/')
def index():
    return {'message': 'Suryamitra Job Matching API', 'status': 'running'}

@app.route('/health')
def health():
    return {'status': 'healthy', 'database': 'connected'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

