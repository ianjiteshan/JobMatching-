from flask import Blueprint, request, jsonify
from src.models.user import db, User
from src.models.job_seeker import JobSeeker
from src.models.job_posting import JobPosting
from src.models.job_match import JobMatch
from src.ml_engine import get_job_matches
import json

employer_bp = Blueprint('employer', __name__)

@employer_bp.route('/jobs', methods=['GET'])
def get_employer_jobs():
    """Get all job postings for the current employer"""
    try:
        # In a real app, you'd get employer_id from JWT token
        # For now, we'll use a query parameter or get all jobs
        employer_id = request.args.get('employer_id', type=int)
        
        if employer_id:
            jobs = JobPosting.query.filter_by(employer_id=employer_id).all()
        else:
            jobs = JobPosting.query.all()
        
        return jsonify({
            'jobs': [job.to_dict() for job in jobs]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/jobs', methods=['POST'])
def create_job_posting():
    """Create a new job posting"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'required_qualifications', 'city', 'state']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new job posting
        job_posting = JobPosting(
            employer_id=data.get('employer_id', 1),  # Default employer for demo
            title=data['title'],
            description=data['description'],
            required_qualifications=data['required_qualifications'],
            city=data['city'],
            state=data['state'],
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            experience_required=data.get('experience_required', 0),
            minimum_diploma_score=data.get('minimum_diploma_score'),
            status=data.get('status', 'active')
        )
        
        # Set skills if provided
        if 'required_skills' in data:
            job_posting.set_required_skills_list(data['required_skills'])
        
        if 'preferred_skills' in data:
            job_posting.set_preferred_skills_list(data['preferred_skills'])
        
        db.session.add(job_posting)
        db.session.commit()
        
        return jsonify({
            'message': 'Job posting created successfully',
            'job_posting': job_posting.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job_posting(job_id):
    """Get a specific job posting by ID"""
    try:
        job_posting = JobPosting.query.get_or_404(job_id)
        return jsonify(job_posting.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job_posting(job_id):
    """Update a job posting"""
    try:
        job_posting = JobPosting.query.get_or_404(job_id)
        data = request.get_json()
        
        # Update fields
        updatable_fields = [
            'title', 'description', 'required_qualifications', 'city', 'state',
            'salary_min', 'salary_max', 'experience_required', 'minimum_diploma_score', 'status'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(job_posting, field, data[field])
        
        # Update skills if provided
        if 'required_skills' in data:
            job_posting.set_required_skills_list(data['required_skills'])
        
        if 'preferred_skills' in data:
            job_posting.set_preferred_skills_list(data['preferred_skills'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Job posting updated successfully',
            'job_posting': job_posting.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job_posting(job_id):
    """Delete a job posting"""
    try:
        job_posting = JobPosting.query.get_or_404(job_id)
        db.session.delete(job_posting)
        db.session.commit()
        
        return jsonify({'message': 'Job posting deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/jobs/<int:job_id>/matches', methods=['GET'])
def get_job_matches(job_id):
    """Get ranked candidate matches for a specific job posting"""
    try:
        job_posting = JobPosting.query.get_or_404(job_id)
        
        # Get query parameters
        top_k = request.args.get('top_k', 10, type=int)
        min_score = request.args.get('min_score', 0.0, type=float)
        
        # Get all available job seekers
        job_seekers = JobSeeker.query.filter_by(availability_status='available').all()
        
        if not job_seekers:
            return jsonify({
                'matches': [],
                'message': 'No available job seekers found'
            })
        
        # Convert to list of dictionaries for ML engine
        seekers_data = [seeker.to_dict() for seeker in job_seekers]
        job_posting_dict = job_posting.to_dict()
        
        # Get matches from ML engine
        from src.ml_engine import get_job_matches
        matches = get_job_matches(job_posting_dict, seekers_data, top_k)
        
        # Filter by minimum score
        filtered_matches = [match for match in matches if match['match_score'] >= min_score]
        
        # Save matches to database
        for match in filtered_matches:
            # Check if match already exists
            existing_match = JobMatch.query.filter_by(
                job_posting_id=job_id,
                job_seeker_id=match['job_seeker_id']
            ).first()
            
            if not existing_match:
                job_match = JobMatch(
                    job_posting_id=job_id,
                    job_seeker_id=match['job_seeker_id'],
                    match_score=match['match_score']
                )
                job_match.set_match_reasons_list(match['reasons'])
                db.session.add(job_match)
        
        db.session.commit()
        
        # Format response
        formatted_matches = []
        for match in filtered_matches:
            formatted_match = {
                'job_seeker_id': match['job_seeker_id'],
                'match_score': match['match_score'],
                'match_percentage': round(match['match_score'] * 100, 1),
                'reasons': match['reasons'],
                'candidate': match['candidate_data'],
                'score_breakdown': {
                    'skills': round(match['skill_score'] * 100, 1),
                    'location': round(match['location_score'] * 100, 1),
                    'salary': round(match['salary_score'] * 100, 1),
                    'experience': round(match['experience_score'] * 100, 1),
                    'diploma': round(match['diploma_score'] * 100, 1)
                }
            }
            formatted_matches.append(formatted_match)
        
        return jsonify({
            'job_posting': job_posting.to_dict_summary(),
            'matches': formatted_matches,
            'total_matches': len(formatted_matches),
            'total_candidates_evaluated': len(seekers_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/jobs/<int:job_id>/matches/refresh', methods=['POST'])
def refresh_job_matches(job_id):
    """Refresh matches for a job posting (recalculate with latest data)"""
    try:
        job_posting = JobPosting.query.get_or_404(job_id)
        
        # Delete existing matches
        JobMatch.query.filter_by(job_posting_id=job_id).delete()
        db.session.commit()
        
        # Redirect to get new matches
        return get_job_matches(job_id)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate_details(candidate_id):
    """Get detailed information about a specific candidate"""
    try:
        candidate = JobSeeker.query.get_or_404(candidate_id)
        
        # Get candidate's match history
        matches = JobMatch.query.filter_by(job_seeker_id=candidate_id).all()
        match_history = []
        
        for match in matches:
            match_data = {
                'job_posting_id': match.job_posting_id,
                'job_title': match.job_posting.title if match.job_posting else 'Unknown',
                'match_score': match.match_score,
                'match_percentage': round(match.match_score * 100, 1),
                'reasons': match.get_match_reasons_list(),
                'created_at': match.created_at.isoformat() if match.created_at else None
            }
            match_history.append(match_data)
        
        return jsonify({
            'candidate': candidate.to_dict(),
            'match_history': match_history,
            'total_matches': len(match_history)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@employer_bp.route('/dashboard/stats', methods=['GET'])
def get_employer_dashboard_stats():
    """Get employer dashboard statistics"""
    try:
        # For demo purposes, we'll show stats for all employers
        # In a real app, filter by employer_id from JWT token
        
        # Job postings stats
        total_jobs = JobPosting.query.count()
        active_jobs = JobPosting.query.filter_by(status='active').count()
        
        # Matches stats
        total_matches = JobMatch.query.count()
        
        # Top matched candidates (highest average match scores)
        top_candidates = db.session.query(
            JobSeeker.id,
            JobSeeker.name,
            JobSeeker.city,
            JobSeeker.state,
            db.func.avg(JobMatch.match_score).label('avg_score'),
            db.func.count(JobMatch.id).label('match_count')
        ).join(JobMatch).group_by(JobSeeker.id).order_by(
            db.func.avg(JobMatch.match_score).desc()
        ).limit(10).all()
        
        # Recent matches
        recent_matches = db.session.query(JobMatch).join(JobSeeker).join(JobPosting).order_by(
            JobMatch.created_at.desc()
        ).limit(10).all()
        
        recent_matches_data = []
        for match in recent_matches:
            match_data = {
                'id': match.id,
                'candidate_name': match.job_seeker.name,
                'job_title': match.job_posting.title,
                'match_score': match.match_score,
                'match_percentage': round(match.match_score * 100, 1),
                'created_at': match.created_at.isoformat() if match.created_at else None
            }
            recent_matches_data.append(match_data)
        
        return jsonify({
            'job_postings': {
                'total': total_jobs,
                'active': active_jobs
            },
            'matches': {
                'total': total_matches
            },
            'top_candidates': [
                {
                    'id': candidate.id,
                    'name': candidate.name,
                    'city': candidate.city,
                    'state': candidate.state,
                    'avg_match_score': round(candidate.avg_score * 100, 1),
                    'total_matches': candidate.match_count
                }
                for candidate in top_candidates
            ],
            'recent_matches': recent_matches_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

