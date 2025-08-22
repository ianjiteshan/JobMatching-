#!/usr/bin/env python3
"""
Machine Learning Engine for Job Matching System
Uses KNN and other ML techniques to match candidates with job postings
"""

import pandas as pd
import numpy as np
import json
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from datetime import datetime

class JobMatchingEngine:
    """
    Machine Learning engine for matching job seekers with job postings
    """
    
    def __init__(self):
        self.knn_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.rf_classifier = None
        self.feature_columns = []
        self.is_trained = False
        
    def prepare_features(self, job_seekers_df, job_postings_df=None):
        """
        Prepare features for machine learning from job seekers and job postings data
        """
        features_list = []
        
        for _, seeker in job_seekers_df.iterrows():
            # Parse skills from JSON string
            try:
                skills = json.loads(seeker['skills']) if isinstance(seeker['skills'], str) else seeker['skills']
            except:
                skills = []
            
            # Create feature vector
            features = {
                # Numerical features
                'diploma_score': seeker['diploma_score'],
                'experience_years': seeker['experience_years'],
                'preferred_salary_min': seeker.get('preferred_salary_min', 20000),
                'preferred_salary_max': seeker.get('preferred_salary_max', 35000),
                'skills_count': len(skills),
                
                # Categorical features (will be encoded)
                'state': seeker['state'],
                'city': seeker['city'],
                'category': seeker['category'],
                'gender': seeker['gender'],
                'training_result': seeker['training_result'],
                'placement_status': seeker.get('placement_status', 'Unknown'),
                
                # Skills features (binary encoding for common skills)
                'has_solar_installation': 1 if any('Solar Panel Installation' in skill for skill in skills) else 0,
                'has_maintenance': 1 if any('Maintenance' in skill for skill in skills) else 0,
                'has_electrical': 1 if any('Electrical' in skill for skill in skills) else 0,
                'has_safety': 1 if any('Safety' in skill for skill in skills) else 0,
                'has_technical_doc': 1 if any('Technical Documentation' in skill for skill in skills) else 0,
                'has_project_mgmt': 1 if any('Project Management' in skill for skill in skills) else 0,
                
                # Derived features
                'salary_range': seeker.get('preferred_salary_max', 35000) - seeker.get('preferred_salary_min', 20000),
                'is_placed': 1 if seeker.get('placement_status') == 'Placed' else 0,
                'passed_training': 1 if seeker['training_result'] == 'Pass' else 0,
                
                # ID for reference
                'seeker_id': seeker['id']
            }
            
            features_list.append(features)
        
        return pd.DataFrame(features_list)
    
    def encode_categorical_features(self, df, fit=True):
        """
        Encode categorical features using label encoding
        """
        categorical_columns = ['state', 'city', 'category', 'gender', 'training_result', 'placement_status']
        
        for col in categorical_columns:
            if col in df.columns:
                if fit:
                    if col not in self.label_encoders:
                        self.label_encoders[col] = LabelEncoder()
                    df[col + '_encoded'] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    if col in self.label_encoders:
                        # Handle unseen categories
                        unique_values = set(self.label_encoders[col].classes_)
                        df[col] = df[col].astype(str).apply(lambda x: x if x in unique_values else 'Unknown')
                        df[col + '_encoded'] = self.label_encoders[col].transform(df[col])
                    else:
                        df[col + '_encoded'] = 0  # Default encoding for unseen categories
        
        return df
    
    def train_models(self, job_seekers_df):
        """
        Train the machine learning models using job seekers data
        """
        print("Training ML models...")
        
        # Prepare features
        features_df = self.prepare_features(job_seekers_df)
        
        # Encode categorical features
        features_df = self.encode_categorical_features(features_df, fit=True)
        
        # Select numerical features for ML
        numerical_features = [
            'diploma_score', 'experience_years', 'preferred_salary_min', 'preferred_salary_max',
            'skills_count', 'has_solar_installation', 'has_maintenance', 'has_electrical',
            'has_safety', 'has_technical_doc', 'has_project_mgmt', 'salary_range',
            'is_placed', 'passed_training'
        ]
        
        # Add encoded categorical features
        encoded_features = [col for col in features_df.columns if col.endswith('_encoded')]
        self.feature_columns = numerical_features + encoded_features
        
        # Prepare training data
        X = features_df[self.feature_columns].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train KNN model for similarity matching
        self.knn_model = NearestNeighbors(n_neighbors=10, metric='cosine')
        self.knn_model.fit(X_scaled)
        
        # Train Random Forest for placement prediction
        y_placement = features_df['is_placed']
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.rf_classifier.fit(X_scaled, y_placement)
        
        self.is_trained = True
        print(f"Models trained successfully with {len(features_df)} candidates")
        print(f"Feature columns: {len(self.feature_columns)}")
        
        return True
    
    def calculate_skill_similarity(self, candidate_skills, job_required_skills, job_preferred_skills=None):
        """
        Calculate skill similarity between candidate and job requirements
        """
        if not candidate_skills:
            return 0.0
        
        if not job_required_skills:
            job_required_skills = []
        
        if job_preferred_skills is None:
            job_preferred_skills = []
        
        # Convert to lowercase for comparison
        candidate_skills_lower = [skill.lower() for skill in candidate_skills]
        required_skills_lower = [skill.lower() for skill in job_required_skills]
        preferred_skills_lower = [skill.lower() for skill in job_preferred_skills]
        
        # Calculate required skills match
        required_matches = 0
        for req_skill in required_skills_lower:
            for cand_skill in candidate_skills_lower:
                if req_skill in cand_skill or cand_skill in req_skill:
                    required_matches += 1
                    break
        
        required_score = required_matches / len(required_skills_lower) if required_skills_lower else 0
        
        # Calculate preferred skills match
        preferred_matches = 0
        if preferred_skills_lower:
            for pref_skill in preferred_skills_lower:
                for cand_skill in candidate_skills_lower:
                    if pref_skill in cand_skill or cand_skill in pref_skill:
                        preferred_matches += 1
                        break
            preferred_score = preferred_matches / len(preferred_skills_lower)
        else:
            preferred_score = 0
        
        # Weighted combination (required skills are more important)
        total_score = (required_score * 0.7) + (preferred_score * 0.3)
        return min(total_score, 1.0)
    
    def calculate_location_score(self, candidate_city, candidate_state, job_city, job_state):
        """
        Calculate location compatibility score
        """
        if candidate_city.lower() == job_city.lower():
            return 1.0  # Same city
        elif candidate_state.lower() == job_state.lower():
            return 0.7  # Same state, different city
        else:
            return 0.3  # Different state
    
    def calculate_salary_compatibility(self, candidate_min, candidate_max, job_min, job_max):
        """
        Calculate salary compatibility score
        """
        if not all([candidate_min, candidate_max, job_min, job_max]):
            return 0.5  # Default score if salary info is missing
        
        # Check for overlap
        overlap_start = max(candidate_min, job_min)
        overlap_end = min(candidate_max, job_max)
        
        if overlap_start <= overlap_end:
            # There's an overlap
            overlap_size = overlap_end - overlap_start
            candidate_range = candidate_max - candidate_min
            job_range = job_max - job_min
            avg_range = (candidate_range + job_range) / 2
            
            if avg_range > 0:
                return min(overlap_size / avg_range, 1.0)
            else:
                return 1.0
        else:
            # No overlap - calculate how far apart they are
            gap = overlap_start - overlap_end
            max_salary = max(candidate_max, job_max)
            if max_salary > 0:
                return max(0, 1 - (gap / max_salary))
            else:
                return 0
    
    def match_candidates_to_job(self, job_posting, job_seekers_df, top_k=10):
        """
        Find the best matching candidates for a specific job posting
        """
        if not self.is_trained:
            print("Models not trained yet. Training with current data...")
            self.train_models(job_seekers_df)
        
        matches = []
        
        # Parse job requirements
        try:
            job_required_skills = json.loads(job_posting.get('required_skills', '[]'))
        except:
            job_required_skills = []
        
        try:
            job_preferred_skills = json.loads(job_posting.get('preferred_skills', '[]'))
        except:
            job_preferred_skills = []
        
        for _, candidate in job_seekers_df.iterrows():
            # Skip unavailable candidates
            if candidate.get('availability_status') != 'available':
                continue
            
            # Parse candidate skills
            try:
                candidate_skills = json.loads(candidate['skills']) if isinstance(candidate['skills'], str) else candidate['skills']
            except:
                candidate_skills = []
            
            # Calculate individual scores
            skill_score = self.calculate_skill_similarity(
                candidate_skills, job_required_skills, job_preferred_skills
            )
            
            location_score = self.calculate_location_score(
                candidate['city'], candidate['state'],
                job_posting['city'], job_posting['state']
            )
            
            salary_score = self.calculate_salary_compatibility(
                candidate.get('preferred_salary_min', 20000),
                candidate.get('preferred_salary_max', 35000),
                job_posting.get('salary_min', 15000),
                job_posting.get('salary_max', 40000)
            )
            
            # Experience score
            required_exp = job_posting.get('experience_required', 0)
            candidate_exp = candidate.get('experience_years', 0)
            if required_exp == 0:
                experience_score = 1.0  # No experience required
            elif candidate_exp >= required_exp:
                experience_score = 1.0  # Meets requirement
            else:
                experience_score = max(0.3, candidate_exp / required_exp)  # Partial credit
            
            # Diploma score
            min_diploma_score = job_posting.get('minimum_diploma_score', 60.0)
            candidate_diploma = candidate.get('diploma_score', 70.0)
            if candidate_diploma >= min_diploma_score:
                diploma_score = min(candidate_diploma / 100.0, 1.0)
            else:
                diploma_score = max(0.2, candidate_diploma / min_diploma_score)
            
            # Training result bonus
            training_bonus = 0.1 if candidate.get('training_result') == 'Pass' else 0
            
            # Calculate weighted overall score
            weights = {
                'skills': 0.35,
                'location': 0.20,
                'salary': 0.15,
                'experience': 0.15,
                'diploma': 0.15
            }
            
            overall_score = (
                skill_score * weights['skills'] +
                location_score * weights['location'] +
                salary_score * weights['salary'] +
                experience_score * weights['experience'] +
                diploma_score * weights['diploma'] +
                training_bonus
            )
            
            # Create match reasons
            reasons = []
            if skill_score > 0.7:
                reasons.append(f"Strong skills match ({skill_score:.1%})")
            if location_score == 1.0:
                reasons.append("Same city location")
            elif location_score > 0.5:
                reasons.append("Same state location")
            if salary_score > 0.8:
                reasons.append("Excellent salary compatibility")
            if candidate_diploma >= 85:
                reasons.append("High diploma score")
            if candidate.get('placement_status') == 'Placed':
                reasons.append("Previously placed successfully")
            
            match_data = {
                'job_seeker_id': candidate['id'],
                'match_score': min(overall_score, 1.0),
                'skill_score': skill_score,
                'location_score': location_score,
                'salary_score': salary_score,
                'experience_score': experience_score,
                'diploma_score': diploma_score,
                'reasons': reasons,
                'candidate_data': candidate.to_dict() if hasattr(candidate, 'to_dict') else candidate.to_dict()
            }
            
            matches.append(match_data)
        
        # Sort by match score and return top k
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches[:top_k]
    
    def save_models(self, model_dir):
        """
        Save trained models to disk
        """
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        if self.is_trained:
            joblib.dump(self.knn_model, os.path.join(model_dir, 'knn_model.pkl'))
            joblib.dump(self.scaler, os.path.join(model_dir, 'scaler.pkl'))
            joblib.dump(self.label_encoders, os.path.join(model_dir, 'label_encoders.pkl'))
            joblib.dump(self.rf_classifier, os.path.join(model_dir, 'rf_classifier.pkl'))
            
            # Save metadata
            metadata = {
                'feature_columns': self.feature_columns,
                'is_trained': self.is_trained,
                'training_date': datetime.now().isoformat()
            }
            
            with open(os.path.join(model_dir, 'metadata.json'), 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"Models saved to {model_dir}")
        else:
            print("No trained models to save")
    
    def load_models(self, model_dir):
        """
        Load trained models from disk
        """
        try:
            self.knn_model = joblib.load(os.path.join(model_dir, 'knn_model.pkl'))
            self.scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
            self.label_encoders = joblib.load(os.path.join(model_dir, 'label_encoders.pkl'))
            self.rf_classifier = joblib.load(os.path.join(model_dir, 'rf_classifier.pkl'))
            
            # Load metadata
            with open(os.path.join(model_dir, 'metadata.json'), 'r') as f:
                metadata = json.load(f)
            
            self.feature_columns = metadata['feature_columns']
            self.is_trained = metadata['is_trained']
            
            print(f"Models loaded from {model_dir}")
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False

# Global ML engine instance
ml_engine = JobMatchingEngine()

def initialize_ml_engine(job_seekers_data):
    """
    Initialize and train the ML engine with job seekers data
    """
    global ml_engine
    
    if isinstance(job_seekers_data, list):
        df = pd.DataFrame(job_seekers_data)
    else:
        df = job_seekers_data
    
    success = ml_engine.train_models(df)
    return success

def get_job_matches(job_posting_dict, job_seekers_data, top_k=10):
    """
    Get top matching candidates for a job posting
    """
    global ml_engine
    
    if isinstance(job_seekers_data, list):
        df = pd.DataFrame(job_seekers_data)
    else:
        df = job_seekers_data
    
    matches = ml_engine.match_candidates_to_job(job_posting_dict, df, top_k)
    return matches

