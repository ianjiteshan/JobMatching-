from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.models.job_match import JobMatch
from src.ml_engine import initialize_ml_engine, get_job_matches
import json
import pandas as pd

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/job-seekers', methods=['GET'])
def get_job_seekers():
    """Get all job seekers with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        city = request.args.get('city', '')
        state = request.args.get('state', '')
        category = request.args.get('category', '')
        
        # Build query
        query = JobSeeker.query
        
        if search:
            query = query.filter(JobSeeker.name.contains(search))
        if city:
            query = query.filter(JobSeeker.city == city)
        if state:
            query = query.filter(JobSeeker.state == state)
        if category:
            query = query.filter(JobSeeker.category == category)
        
        # Paginate
        paginated = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        job_seekers = [seeker.to_dict() for seeker in paginated.items]
        
        return jsonify({
            'job_seekers': job_seekers,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/job-seekers', methods=['POST'])
def create_job_seeker():
    """Create a new job seeker"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone_number', 'city', 'state', 'qualifications', 'diploma_score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new job seeker
        job_seeker = JobSeeker(
            name=data['name'],
            phone_number=data['phone_number'],
            email=data.get('email', ''),
            city=data['city'],
            state=data['state'],
            qualifications=data['qualifications'],
            diploma_score=float(data['diploma_score']),
            experience_years=data.get('experience_years', 0),
            category=data.get('category', 'Gen'),
            gender=data.get('gender', 'Male'),
            training_result=data.get('training_result', 'Pass'),
            placement_status=data.get('placement_status', 'Unknown'),
            preferred_salary_min=data.get('preferred_salary_min', 20000),
            preferred_salary_max=data.get('preferred_salary_max', 35000),
            availability_status=data.get('availability_status', 'available')
        )
        
        # Set skills if provided
        if 'skills' in data:
            job_seeker.set_skills_list(data['skills'])
        
        db.session.add(job_seeker)
        db.session.commit()
        
        return jsonify({
            'message': 'Job seeker created successfully',
            'job_seeker': job_seeker.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/job-seekers/<int:seeker_id>', methods=['GET'])
def get_job_seeker(seeker_id):
    """Get a specific job seeker by ID"""
    try:
        job_seeker = JobSeeker.query.get_or_404(seeker_id)
        return jsonify(job_seeker.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/job-seekers/<int:seeker_id>', methods=['PUT'])
def update_job_seeker(seeker_id):
    """Update a job seeker"""
    try:
        job_seeker = JobSeeker.query.get_or_404(seeker_id)
        data = request.get_json()
        
        # Update fields
        updatable_fields = [
            'name', 'phone_number', 'email', 'city', 'state', 'qualifications',
            'diploma_score', 'experience_years', 'category', 'gender',
            'training_result', 'placement_status', 'preferred_salary_min',
            'preferred_salary_max', 'availability_status'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(job_seeker, field, data[field])
        
        # Update skills if provided
        if 'skills' in data:
            job_seeker.set_skills_list(data['skills'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Job seeker updated successfully',
            'job_seeker': job_seeker.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/job-seekers/<int:seeker_id>', methods=['DELETE'])
def delete_job_seeker(seeker_id):
    """Delete a job seeker"""
    try:
        job_seeker = JobSeeker.query.get_or_404(seeker_id)
        db.session.delete(job_seeker)
        db.session.commit()
        
        return jsonify({'message': 'Job seeker deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/job-seekers/bulk-import', methods=['POST'])
def bulk_import_job_seekers():
    """Bulk import job seekers from CSV data"""
    try:
        data = request.get_json()
        
        if 'csv_data' not in data:
            return jsonify({'error': 'CSV data is required'}), 400
        
        # Parse CSV data
        import io
        csv_string = data['csv_data']
        df = pd.read_csv(io.StringIO(csv_string))
        
        imported_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Check if job seeker already exists
                existing = JobSeeker.query.filter_by(
                    name=row['name'],
                    phone_number=row.get('phone_number', '')
                ).first()
                
                if existing:
                    continue  # Skip duplicates
                
                # Create new job seeker
                job_seeker = JobSeeker(
                    name=row['name'],
                    phone_number=row.get('phone_number', ''),
                    email=row.get('email', ''),
                    city=row['city'],
                    state=row['state'],
                    qualifications=row['qualifications'],
                    diploma_score=float(row['diploma_score']),
                    experience_years=int(row.get('experience_years', 0)),
                    category=row.get('category', 'Gen'),
                    gender=row.get('gender', 'Male'),
                    training_result=row.get('training_result', 'Pass'),
                    placement_status=row.get('placement_status', 'Unknown'),
                    preferred_salary_min=int(row.get('preferred_salary_min', 20000)),
                    preferred_salary_max=int(row.get('preferred_salary_max', 35000)),
                    availability_status=row.get('availability_status', 'available')
                )
                
                # Set skills if provided
                if 'skills' in row and pd.notna(row['skills']):
                    try:
                        skills = json.loads(row['skills'])
                        job_seeker.set_skills_list(skills)
                    except:
                        pass  # Skip invalid skills data
                
                db.session.add(job_seeker)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully imported {imported_count} job seekers',
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get admin dashboard statistics"""
    try:
        # Job seekers statistics
        total_seekers = JobSeeker.query.count()
        placed_seekers = JobSeeker.query.filter_by(placement_status='Placed').count()
        available_seekers = JobSeeker.query.filter_by(availability_status='available').count()
        
        # Group by state
        state_stats = db.session.query(
            JobSeeker.state,
            db.func.count(JobSeeker.id).label('count')
        ).group_by(JobSeeker.state).all()
        
        # Group by category
        category_stats = db.session.query(
            JobSeeker.category,
            db.func.count(JobSeeker.id).label('count')
        ).group_by(JobSeeker.category).all()
        
        # Group by gender
        gender_stats = db.session.query(
            JobSeeker.gender,
            db.func.count(JobSeeker.id).label('count')
        ).group_by(JobSeeker.gender).all()
        
        # Average diploma score
        avg_diploma_score = db.session.query(
            db.func.avg(JobSeeker.diploma_score)
        ).scalar()
        
        # Job postings statistics
        total_jobs = JobPosting.query.count()
        active_jobs = JobPosting.query.filter_by(status='active').count()
        
        # Job matches statistics
        total_matches = JobMatch.query.count()
        
        return jsonify({
            'job_seekers': {
                'total': total_seekers,
                'placed': placed_seekers,
                'available': available_seekers,
                'placement_rate': round((placed_seekers / total_seekers * 100), 2) if total_seekers > 0 else 0,
                'avg_diploma_score': round(avg_diploma_score, 2) if avg_diploma_score else 0,
                'by_state': [{'state': state, 'count': count} for state, count in state_stats],
                'by_category': [{'category': category, 'count': count} for category, count in category_stats],
                'by_gender': [{'gender': gender, 'count': count} for gender, count in gender_stats]
            },
            'job_postings': {
                'total': total_jobs,
                'active': active_jobs
            },
            'matches': {
                'total': total_matches
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/train-ml-model', methods=['POST'])
def train_ml_model():
    """Train the machine learning model with current job seekers data"""
    try:
        # Get all job seekers
        job_seekers = JobSeeker.query.all()
        
        if not job_seekers:
            return jsonify({'error': 'No job seekers data available for training'}), 400
        
        # Convert to list of dictionaries
        seekers_data = [seeker.to_dict() for seeker in job_seekers]
        
        # Initialize ML engine
        success = initialize_ml_engine(seekers_data)
        
        if success:
            return jsonify({
                'message': 'ML model trained successfully',
                'training_data_count': len(seekers_data)
            })
        else:
            return jsonify({'error': 'Failed to train ML model'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

