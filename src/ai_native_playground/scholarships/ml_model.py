"""
Scholarship Recommendation ML Model

Content-based recommendation system for scholarships using student preferences.
"""

import json
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder, MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity


class ScholarshipRecommendationModel:
    """
    Content-based recommendation model for scholarships.

    Features:
    - Amount (numerical)
    - Type (categorical)
    - Field of study (categorical)
    - Degree level (categorical)
    - Country (categorical)
    - Renewable (binary)
    """

    def __init__(self, n_neighbors: int = 10):
        """Initialize the model."""
        self.n_neighbors = n_neighbors
        self.scaler = StandardScaler()
        self.country_encoder = LabelEncoder()
        self.type_encoder = LabelEncoder()
        self.field_encoder = LabelEncoder()
        self.level_encoder = LabelEncoder()
        self.knn_model = NearestNeighbors(n_neighbors=n_neighbors + 1, metric='cosine')
        self.pca = PCA(n_components=10)

        self.scholarships = []
        self.feature_matrix = None
        self.is_trained = False

    def prepare_features(self, scholarships: List[Dict[str, Any]]) -> np.ndarray:
        """Extract and engineer features from scholarship data."""
        features = []

        for scholarship in scholarships:
            feature_vec = []

            # Numerical features
            feature_vec.append(scholarship.get('amount', 0))
            feature_vec.append(1 if scholarship.get('renewable', False) else 0)
            feature_vec.append(scholarship.get('application_fee', 0))

            # Categorical features (encoded later)
            features.append({
                'numerical': feature_vec,
                'type': scholarship.get('type', 'Merit-based'),
                'field': scholarship.get('field', 'All Fields'),
                'level': scholarship.get('level', 'Undergraduate'),
                'country': scholarship.get('country', 'United States')
            })

        # Separate numerical and categorical
        numerical_features = np.array([f['numerical'] for f in features])
        type_categories = [f['type'] for f in features]
        field_categories = [f['field'] for f in features]
        level_categories = [f['level'] for f in features]
        country_categories = [f['country'] for f in features]

        # Encode categorical features
        type_encoded = self.type_encoder.fit_transform(type_categories).reshape(-1, 1)
        field_encoded = self.field_encoder.fit_transform(field_categories).reshape(-1, 1)
        level_encoded = self.level_encoder.fit_transform(level_categories).reshape(-1, 1)
        country_encoded = self.country_encoder.fit_transform(country_categories).reshape(-1, 1)

        # Combine all features
        combined_features = np.hstack([
            numerical_features,
            type_encoded,
            field_encoded,
            level_encoded,
            country_encoded
        ])

        return combined_features

    def train(self, scholarships: List[Dict[str, Any]]):
        """Train the recommendation model."""
        print(f"Training scholarship model with {len(scholarships)} scholarships...")

        self.scholarships = scholarships

        # Prepare features
        features = self.prepare_features(scholarships)

        # Normalize features
        features_scaled = self.scaler.fit_transform(features)

        # Apply PCA for dimensionality reduction
        if features_scaled.shape[1] > 10:
            features_reduced = self.pca.fit_transform(features_scaled)
        else:
            features_reduced = features_scaled

        self.feature_matrix = features_reduced

        # Train KNN model
        self.knn_model.fit(features_reduced)

        self.is_trained = True
        print("✓ Scholarship model training completed!")

    def recommend_by_preferences(
        self,
        preferences: Dict[str, Any],
        n_recommendations: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recommend scholarships based on student preferences.

        Args:
            preferences: Dictionary with keys like:
                - country: str (optional)
                - min_amount: int (optional)
                - max_amount: int (optional)
                - field: str (optional)
                - level: str (optional)
                - type: str (optional)
                - renewable: bool (optional)

        Returns:
            List of recommended scholarships
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        # Filter scholarships based on preferences
        filtered = self.scholarships.copy()

        if 'country' in preferences and preferences['country']:
            country_pref = preferences['country']
            filtered = [
                s for s in filtered
                if country_pref.lower() in s.get('country', '').lower()
            ]

        if 'min_amount' in preferences:
            filtered = [
                s for s in filtered
                if s.get('amount', 0) >= preferences['min_amount']
            ]

        if 'max_amount' in preferences:
            filtered = [
                s for s in filtered
                if s.get('amount', 999999) <= preferences['max_amount']
            ]

        if 'field' in preferences and preferences['field']:
            field_pref = preferences['field'].lower()
            filtered = [
                s for s in filtered
                if field_pref in s.get('field', '').lower() or s.get('field', '').lower() == 'all fields'
            ]

        if 'level' in preferences and preferences['level']:
            level_pref = preferences['level'].lower()
            filtered = [
                s for s in filtered
                if level_pref in s.get('level', '').lower()
            ]

        if 'type' in preferences and preferences['type']:
            type_pref = preferences['type'].lower()
            filtered = [
                s for s in filtered
                if type_pref in s.get('type', '').lower()
            ]

        if 'renewable' in preferences:
            filtered = [
                s for s in filtered
                if s.get('renewable') == preferences['renewable']
            ]

        # Sort by amount (descending)
        filtered.sort(key=lambda x: x.get('amount', 0), reverse=True)

        # Return top N
        return filtered[:n_recommendations]

    def find_similar(self, scholarship_name: str, n_recommendations: int = 5) -> List[Dict[str, Any]]:
        """Find scholarships similar to a given scholarship."""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        # Find the scholarship
        scholarship_idx = None
        for idx, s in enumerate(self.scholarships):
            if scholarship_name.lower() in s['name'].lower():
                scholarship_idx = idx
                break

        if scholarship_idx is None:
            return []

        # Find similar scholarships
        distances, indices = self.knn_model.kneighbors(
            self.feature_matrix[scholarship_idx].reshape(1, -1),
            n_neighbors=n_recommendations + 1
        )

        recommendations = []
        for i, (dist, idx) in enumerate(zip(distances[0][1:], indices[0][1:])):
            scholarship = self.scholarships[idx].copy()
            scholarship['similarity_score'] = float(1 - dist)
            scholarship['rank'] = i + 1
            recommendations.append(scholarship)

        return recommendations

    def save_model(self, filepath: str):
        """Save the trained model."""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model.")

        model_data = {
            'scaler': self.scaler,
            'country_encoder': self.country_encoder,
            'type_encoder': self.type_encoder,
            'field_encoder': self.field_encoder,
            'level_encoder': self.level_encoder,
            'knn_model': self.knn_model,
            'pca': self.pca,
            'feature_matrix': self.feature_matrix,
            'scholarships': self.scholarships,
            'n_neighbors': self.n_neighbors
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✓ Scholarship model saved to: {filepath}")

    def load_model(self, filepath: str):
        """Load a trained model."""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.scaler = model_data['scaler']
        self.country_encoder = model_data['country_encoder']
        self.type_encoder = model_data['type_encoder']
        self.field_encoder = model_data['field_encoder']
        self.level_encoder = model_data['level_encoder']
        self.knn_model = model_data['knn_model']
        self.pca = model_data['pca']
        self.feature_matrix = model_data['feature_matrix']
        self.scholarships = model_data['scholarships']
        self.n_neighbors = model_data['n_neighbors']
        self.is_trained = True

        print(f"✓ Scholarship model loaded from: {filepath}")


def train_model_from_dataset(dataset_path: str, output_path: str):
    """Train the scholarship model."""
    print(f"Loading dataset from: {dataset_path}")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    scholarships = data['scholarships']
    print(f"Total scholarships: {len(scholarships)}")

    # Create and train model
    model = ScholarshipRecommendationModel(n_neighbors=15)
    model.train(scholarships)

    # Save model
    model.save_model(output_path)

    return model


if __name__ == "__main__":
    # Train the model
    dataset_path = Path(__file__).parent / "data" / "scholarships_4000_dataset.json"
    model_path = Path(__file__).parent / "data" / "scholarship_recommendation_model.pkl"

    if dataset_path.exists():
        model = train_model_from_dataset(str(dataset_path), str(model_path))

        # Test the model
        print("\n" + "="*80)
        print("TESTING SCHOLARSHIP MODEL")
        print("="*80 + "\n")

        # Test 1: Engineering scholarships in US
        print("Test 1: Engineering scholarships in the United States")
        prefs = {
            'country': 'United States',
            'field': 'Engineering',
            'level': 'Graduate'
        }
        recommendations = model.recommend_by_preferences(prefs, n_recommendations=5)
        for i, s in enumerate(recommendations, 1):
            print(f"{i}. {s['name']} - ${s['amount']:,} ({s['provider']})")

        # Test 2: High-value scholarships
        print("\nTest 2: High-value scholarships (>$40,000)")
        prefs = {
            'min_amount': 40000
        }
        recommendations = model.recommend_by_preferences(prefs, n_recommendations=5)
        for i, s in enumerate(recommendations, 1):
            print(f"{i}. {s['name']} - ${s['amount']:,} in {s['country']}")

        print("\n✓ Scholarship model training and testing completed!")
    else:
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please run: python -m ai_native_playground.scholarships.generate_scholarships")
