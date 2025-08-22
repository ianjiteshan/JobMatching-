import pandas as pd
import sqlite3
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

print("Starting ML model retraining with comprehensive dataset...")

# Database connection
db_path = '/home/ubuntu/job_matching_api/src/database/app.db'
conn = sqlite3.connect(db_path)

# Load job seekers data
query = """
SELECT id, name, city, state, qualifications, diploma_score, experience_years, 
       category, gender, training_result, placement_status, availability_status, skills
FROM job_seekers
"""
df = pd.read_sql_query(query, conn)
conn.close()

print(f"Loaded {len(df)} job seekers for ML training")

# Data preprocessing
print("Preprocessing data for ML training...")

# Handle missing values
df['city'] = df['city'].fillna('Unknown')
df['state'] = df['state'].fillna('Unknown')
df['qualifications'] = df['qualifications'].fillna('General')
df['diploma_score'] = df['diploma_score'].fillna(75.0)
df['skills'] = df['skills'].fillna('General Skills')

# Create label encoders
label_encoders = {}
categorical_columns = ['city', 'state', 'qualifications', 'category', 'gender', 'training_result']

for col in categorical_columns:
    le = LabelEncoder()
    df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Create features for ML model
feature_columns = [
    'diploma_score', 'experience_years',
    'city_encoded', 'state_encoded', 'qualifications_encoded',
    'category_encoded', 'gender_encoded', 'training_result_encoded'
]

X = df[feature_columns].copy()
y_placement = (df['placement_status'] == 'Placed').astype(int)

print(f"Feature matrix shape: {X.shape}")
print(f"Target distribution: {y_placement.value_counts()}")

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y_placement, test_size=0.2, random_state=42, stratify=y_placement)

print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train Random Forest for placement prediction
print("Training Random Forest model for placement prediction...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)

# Train KNN model for candidate similarity
print("\nTraining KNN model for candidate similarity...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

knn_model = NearestNeighbors(n_neighbors=10, metric='euclidean')
knn_model.fit(X_scaled)

# Create skills similarity matrix
print("Creating skills similarity matrix...")
unique_skills = set()
for skills_str in df['skills']:
    if pd.notna(skills_str):
        skills_list = [skill.strip() for skill in str(skills_str).split(',')]
        unique_skills.update(skills_list)

unique_skills = list(unique_skills)
print(f"Found {len(unique_skills)} unique skills")

# Create skills vectors for each candidate
skills_matrix = np.zeros((len(df), len(unique_skills)))
for i, skills_str in enumerate(df['skills']):
    if pd.notna(skills_str):
        skills_list = [skill.strip() for skill in str(skills_str).split(',')]
        for skill in skills_list:
            if skill in unique_skills:
                skill_idx = unique_skills.index(skill)
                skills_matrix[i, skill_idx] = 1

# Save all models and encoders
models_dir = '/home/ubuntu/job_matching_api/models'
os.makedirs(models_dir, exist_ok=True)

print("Saving trained models and encoders...")

# Save Random Forest model
with open(f'{models_dir}/placement_predictor.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

# Save KNN model
with open(f'{models_dir}/similarity_model.pkl', 'wb') as f:
    pickle.dump(knn_model, f)

# Save scaler
with open(f'{models_dir}/feature_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save label encoders
with open(f'{models_dir}/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

# Save skills data
with open(f'{models_dir}/skills_data.pkl', 'wb') as f:
    pickle.dump({
        'unique_skills': unique_skills,
        'skills_matrix': skills_matrix
    }, f)

# Save feature columns
with open(f'{models_dir}/feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

# Create model metadata
model_metadata = {
    'training_date': pd.Timestamp.now().isoformat(),
    'total_candidates': len(df),
    'training_accuracy': accuracy,
    'feature_columns': feature_columns,
    'unique_skills_count': len(unique_skills),
    'placement_distribution': {
        'placed': int(y_placement.sum()),
        'not_placed': int(len(y_placement) - y_placement.sum())
    }
}

with open(f'{models_dir}/model_metadata.pkl', 'wb') as f:
    pickle.dump(model_metadata, f)

print(f"\nModel training completed successfully!")
print(f"Models saved to: {models_dir}")
print(f"Training accuracy: {accuracy:.4f}")
print(f"Total candidates used for training: {len(df)}")
print(f"Unique skills identified: {len(unique_skills)}")

# Test the model with a sample prediction
print("\nTesting model with sample predictions...")
sample_indices = np.random.choice(len(X), 5, replace=False)
for idx in sample_indices:
    sample_features = X.iloc[idx:idx+1]
    prediction = rf_model.predict(sample_features)[0]
    probability = rf_model.predict_proba(sample_features)[0]
    actual = y_placement.iloc[idx]
    
    print(f"Candidate: {df.iloc[idx]['name']}")
    print(f"  Predicted placement: {'Yes' if prediction else 'No'} (confidence: {max(probability):.3f})")
    print(f"  Actual placement: {'Yes' if actual else 'No'}")
    print(f"  Diploma score: {df.iloc[idx]['diploma_score']}")
    print()

print("ML model retraining completed successfully!")

