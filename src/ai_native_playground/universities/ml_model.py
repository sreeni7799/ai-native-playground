"""
University Recommendation ML Model

This module implements a content-based recommendation system for universities.
The model learns from university features and can recommend similar universities
or match universities to student preferences.
"""

import json
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity


class UniversityRecommendationModel:
    """
    Content-based recommendation model for universities.

    Features used:
    - Student population (numerical)
    - World ranking (numerical)
    - University type (categorical)
    - Country (categorical)
    - Founding year (numerical)
    """

    def __init__(self, n_neighbors: int = 5):
        """
        Initialize the recommendation model.

        Args:
            n_neighbors: Number of similar universities to recommend
        """
        self.n_neighbors = n_neighbors
        self.scaler = StandardScaler()
        self.country_encoder = LabelEncoder()
        self.type_encoder = LabelEncoder()
        self.knn_model = NearestNeighbors(n_neighbors=n_neighbors + 1, metric='cosine')
        self.pca = PCA(n_components=10)

        self.universities = []
        self.feature_matrix = None
        self.is_trained = False

    def prepare_features(self, universities: List[Dict[str, Any]]) -> np.ndarray:
        """
        Extract and engineer features from university data.

        Args:
            universities: List of university dictionaries

        Returns:
            Feature matrix (numpy array)
        """
        features = []

        for uni in universities:
            feature_vec = []

            # Numerical features
            feature_vec.append(uni.get('students', 0))
            feature_vec.append(uni.get('ranking', 500))  # Default mid-range ranking
            feature_vec.append(uni.get('founded', 1900))

            # Calculate age of university
            age = 2024 - uni.get('founded', 1900)
            feature_vec.append(age)

            # Categorical features (encoded later)
            uni_type = uni.get('type', 'Public')

            # Extract country from location fields
            country = ''
            if 'state' in uni:
                country = 'US'
            elif 'province' in uni:
                country = 'Canada'
            elif 'region' in uni and 'England' in str(uni.get('region', '')):
                country = 'UK'
            else:
                # Try to infer from context
                location = str(uni.get('location', ''))
                if 'Germany' in location or 'Bavaria' in location:
                    country = 'Germany'
                elif 'Australia' in location:
                    country = 'Australia'
                elif 'France' in location:
                    country = 'France'
                else:
                    country = 'Unknown'

            features.append({
                'numerical': feature_vec,
                'type': uni_type,
                'country': country
            })

        # Separate numerical and categorical
        numerical_features = np.array([f['numerical'] for f in features])
        type_categories = [f['type'] for f in features]
        country_categories = [f['country'] for f in features]

        # Encode categorical features
        type_encoded = self.type_encoder.fit_transform(type_categories).reshape(-1, 1)
        country_encoded = self.country_encoder.fit_transform(country_categories).reshape(-1, 1)

        # Combine all features
        combined_features = np.hstack([
            numerical_features,
            type_encoded,
            country_encoded
        ])

        return combined_features

    def train(self, universities: List[Dict[str, Any]]):
        """
        Train the recommendation model.

        Args:
            universities: List of university dictionaries with features
        """
        print(f"Training model with {len(universities)} universities...")

        self.universities = universities

        # Prepare features
        features = self.prepare_features(universities)

        # Normalize features
        features_scaled = self.scaler.fit_transform(features)

        # Apply PCA for dimensionality reduction
        if features_scaled.shape[1] > 10:
            features_reduced = self.pca.fit_transform(features_scaled)
        else:
            features_reduced = features_scaled

        self.feature_matrix = features_reduced

        # Train KNN model for similarity search
        self.knn_model.fit(features_reduced)

        self.is_trained = True
        print("✓ Model training completed!")

    def recommend_similar(
        self,
        university_name: str,
        n_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Recommend universities similar to a given university.

        Args:
            university_name: Name of the reference university
            n_recommendations: Number of recommendations to return

        Returns:
            List of recommended universities with similarity scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        # Find the university
        uni_idx = None
        for idx, uni in enumerate(self.universities):
            if university_name.lower() in uni['name'].lower():
                uni_idx = idx
                break

        if uni_idx is None:
            return []

        # Find similar universities
        distances, indices = self.knn_model.kneighbors(
            self.feature_matrix[uni_idx].reshape(1, -1),
            n_neighbors=n_recommendations + 1
        )

        recommendations = []
        for i, (dist, idx) in enumerate(zip(distances[0][1:], indices[0][1:])):
            uni = self.universities[idx].copy()
            uni['similarity_score'] = float(1 - dist)  # Convert distance to similarity
            uni['rank'] = i + 1
            recommendations.append(uni)

        return recommendations

    def recommend_by_preferences(
        self,
        preferences: Dict[str, Any],
        n_recommendations: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recommend universities based on student preferences.

        Args:
            preferences: Dictionary with keys like:
                - country: str (optional)
                - min_ranking: int (optional)
                - max_ranking: int (optional)
                - min_students: int (optional)
                - max_students: int (optional)
                - university_type: str (optional, 'Public' or 'Private')

        Returns:
            List of recommended universities
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        # Filter universities based on preferences
        filtered = self.universities.copy()

        if 'country' in preferences and preferences['country']:
            country_pref = preferences['country'].lower()
            filtered = [
                uni for uni in filtered
                if self._match_country(uni, country_pref)
            ]

        if 'min_ranking' in preferences:
            filtered = [
                uni for uni in filtered
                if uni.get('ranking', 1000) >= preferences['min_ranking']
            ]

        if 'max_ranking' in preferences:
            filtered = [
                uni for uni in filtered
                if uni.get('ranking', 0) <= preferences['max_ranking']
            ]

        if 'min_students' in preferences:
            filtered = [
                uni for uni in filtered
                if uni.get('students', 0) >= preferences['min_students']
            ]

        if 'max_students' in preferences:
            filtered = [
                uni for uni in filtered
                if uni.get('students', 999999) <= preferences['max_students']
            ]

        if 'university_type' in preferences and preferences['university_type']:
            filtered = [
                uni for uni in filtered
                if uni.get('type', '').lower() == preferences['university_type'].lower()
            ]

        # Sort by ranking (lower is better)
        filtered.sort(key=lambda x: x.get('ranking', 1000))

        # Return top N
        return filtered[:n_recommendations]

    def _match_country(self, uni: Dict[str, Any], country_pref: str) -> bool:
        """Check if university matches country preference."""
        if 'state' in uni and 'us' in country_pref:
            return True
        if 'province' in uni and 'canada' in country_pref:
            return True
        if 'region' in uni and 'uk' in country_pref:
            return True

        location_str = str(uni.get('location', '')).lower()
        return country_pref in location_str

    def get_university_embedding(self, university_name: str) -> Optional[np.ndarray]:
        """
        Get the feature embedding for a specific university.

        Args:
            university_name: Name of the university

        Returns:
            Feature embedding vector or None if not found
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        for idx, uni in enumerate(self.universities):
            if university_name.lower() in uni['name'].lower():
                return self.feature_matrix[idx]

        return None

    def save_model(self, filepath: str):
        """
        Save the trained model to disk.

        Args:
            filepath: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Cannot save untrained model.")

        model_data = {
            'scaler': self.scaler,
            'country_encoder': self.country_encoder,
            'type_encoder': self.type_encoder,
            'knn_model': self.knn_model,
            'pca': self.pca,
            'feature_matrix': self.feature_matrix,
            'universities': self.universities,
            'n_neighbors': self.n_neighbors
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✓ Model saved to: {filepath}")

    def load_model(self, filepath: str):
        """
        Load a trained model from disk.

        Args:
            filepath: Path to the saved model
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.scaler = model_data['scaler']
        self.country_encoder = model_data['country_encoder']
        self.type_encoder = model_data['type_encoder']
        self.knn_model = model_data['knn_model']
        self.pca = model_data['pca']
        self.feature_matrix = model_data['feature_matrix']
        self.universities = model_data['universities']
        self.n_neighbors = model_data['n_neighbors']
        self.is_trained = True

        print(f"✓ Model loaded from: {filepath}")


def train_model_from_dataset(dataset_path: str, output_path: str):
    """
    Train the model using the university dataset.

    Args:
        dataset_path: Path to the university dataset JSON file
        output_path: Path to save the trained model
    """
    # Load dataset
    print(f"Loading dataset from: {dataset_path}")
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Combine all universities
    all_universities = []
    for country, unis in data.items():
        for uni in unis:
            uni['source_country'] = country
            all_universities.append(uni)

    print(f"Total universities: {len(all_universities)}")

    # Create and train model
    model = UniversityRecommendationModel(n_neighbors=10)
    model.train(all_universities)

    # Save model
    model.save_model(output_path)

    return model


if __name__ == "__main__":
    # Train the model
    dataset_path = Path(__file__).parent / "data" / "universities_1000_dataset.json"
    model_path = Path(__file__).parent / "data" / "university_recommendation_model.pkl"

    if dataset_path.exists():
        model = train_model_from_dataset(str(dataset_path), str(model_path))

        # Test the model
        print("\n" + "="*80)
        print("TESTING MODEL")
        print("="*80 + "\n")

        # Test 1: Find similar universities to MIT
        print("Test 1: Universities similar to MIT")
        similar = model.recommend_similar("MIT", n_recommendations=5)
        for i, uni in enumerate(similar, 1):
            print(f"{i}. {uni['name']} (Similarity: {uni['similarity_score']:.3f})")

        # Test 2: Recommend based on preferences
        print("\nTest 2: Recommendations for: Top-ranked, Large public universities")
        prefs = {
            'max_ranking': 100,
            'min_students': 30000,
            'university_type': 'Public'
        }
        recommendations = model.recommend_by_preferences(prefs, n_recommendations=5)
        for i, uni in enumerate(recommendations, 1):
            print(f"{i}. {uni['name']} - {uni['students']:,} students, Rank #{uni['ranking']}")

        print("\n✓ Model training and testing completed!")
    else:
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please run: python -m ai_native_playground.universities.generate_data")
