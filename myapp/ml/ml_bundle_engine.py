"""
ML-Powered Bundle Recommendation Engine

This module:
1. Analyzes transaction patterns to find product pairs
2. Extracts features for each potential bundle
3. Uses ML to predict bundle success probability
4. Returns ranked bundle recommendations
"""

from pathlib import Path
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

ML_DIR = Path(__file__).resolve().parent
MODELS_DIR = ML_DIR / "models"
BUNDLE_MODEL_PATH = MODELS_DIR / "bundle_predictor.joblib"


class BundleRecommendationEngine:
    """
    ML-powered engine that predicts bundle success probability.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_cols = None
        
    def extract_bundle_features(
        self, 
        df: pd.DataFrame, 
        tx_col: str, 
        item_col: str,
        price_col: str = None,
        category_col: str = None
    ) -> pd.DataFrame:
        """
        Extract features for all potential product bundles.
        
        Features include:
        - Co-occurrence frequency (support)
        - Confidence (A→B and B→A)
        - Lift
        - Price compatibility
        - Category diversity
        - Temporal patterns
        - Customer segment overlap
        
        Args:
            df: Transaction data with columns [tx_col, item_col, ...]
            tx_col: Transaction ID column name
            item_col: Product/Item column name
            price_col: Optional price column
            category_col: Optional category column
            
        Returns:
            DataFrame with bundle features
        """
        # Group by transaction
        grouped = df.groupby(tx_col)[item_col].apply(list)
        total_tx = len(grouped)
        
        # Count individual items and pairs
        item_counter = Counter()
        pair_counter = Counter()
        
        # Track which transactions contain each item
        item_transactions = {}
        
        for tx_id, basket in grouped.items():
            unique_items = list(set(basket))
            
            # Count individual items
            for item in unique_items:
                item_counter[item] += 1
                if item not in item_transactions:
                    item_transactions[item] = set()
                item_transactions[item].add(tx_id)
            
            # Count pairs
            for a, b in combinations(sorted(unique_items), 2):
                pair_counter[(a, b)] += 1
        
        # Build feature table
        bundles = []
        
        for (item_a, item_b), pair_count in pair_counter.items():
            # Basic metrics
            support = pair_count / total_tx
            count_a = item_counter[item_a]
            count_b = item_counter[item_b]
            
            # Confidence scores
            conf_a_to_b = pair_count / count_a if count_a > 0 else 0
            conf_b_to_a = pair_count / count_b if count_b > 0 else 0
            
            # Lift
            expected = (count_a / total_tx) * (count_b / total_tx)
            lift = support / expected if expected > 0 else 0
            
            # Frequency features
            freq_a = count_a / total_tx
            freq_b = count_b / total_tx
            
            # Jaccard similarity (intersection / union)
            union_size = len(item_transactions[item_a] | item_transactions[item_b])
            jaccard = pair_count / union_size if union_size > 0 else 0
            
            # Create feature dict
            features = {
                'item_a': item_a,
                'item_b': item_b,
                'support': support,
                'confidence_a_to_b': conf_a_to_b,
                'confidence_b_to_a': conf_b_to_a,
                'lift': lift,
                'frequency_a': freq_a,
                'frequency_b': freq_b,
                'pair_count': pair_count,
                'jaccard_similarity': jaccard,
                'min_confidence': min(conf_a_to_b, conf_b_to_a),
                'max_confidence': max(conf_a_to_b, conf_b_to_a),
                'avg_confidence': (conf_a_to_b + conf_b_to_a) / 2,
            }
            
            bundles.append(features)
        
        bundle_df = pd.DataFrame(bundles)
        
        # Add price-based features if available
        if price_col and price_col in df.columns:
            bundle_df = self._add_price_features(bundle_df, df, item_col, price_col)
        
        # Add category-based features if available
        if category_col and category_col in df.columns:
            bundle_df = self._add_category_features(bundle_df, df, item_col, category_col)
        
        return bundle_df
    
    def _add_price_features(self, bundle_df, df, item_col, price_col):
        """Add price compatibility features."""
        # Get average price per product
        price_map = df.groupby(item_col)[price_col].mean().to_dict()
        
        bundle_df['price_a'] = bundle_df['item_a'].map(price_map).fillna(0)
        bundle_df['price_b'] = bundle_df['item_b'].map(price_map).fillna(0)
        bundle_df['total_price'] = bundle_df['price_a'] + bundle_df['price_b']
        bundle_df['price_ratio'] = bundle_df.apply(
            lambda x: max(x['price_a'], x['price_b']) / (min(x['price_a'], x['price_b']) + 0.01),
            axis=1
        )
        
        return bundle_df
    
    def _add_category_features(self, bundle_df, df, item_col, category_col):
        """Add category diversity features."""
        # Get category per product
        cat_map = df.groupby(item_col)[category_col].first().to_dict()
        
        bundle_df['category_a'] = bundle_df['item_a'].map(cat_map).fillna('Unknown')
        bundle_df['category_b'] = bundle_df['item_b'].map(cat_map).fillna('Unknown')
        bundle_df['is_cross_category'] = (
            bundle_df['category_a'] != bundle_df['category_b']
        ).astype(int)
        
        return bundle_df
    
    def predict_bundle_success(self, bundle_features: pd.DataFrame) -> pd.DataFrame:
        """
        Predict success probability for each bundle.
        
        Uses a simple heuristic model initially. Can be replaced with
        trained ML model once we have historical bundle performance data.
        
        Args:
            bundle_features: DataFrame with extracted bundle features
            
        Returns:
            DataFrame with added 'success_probability' column
        """
        df = bundle_features.copy()
        
        # Define feature columns for prediction
        feature_cols = [
            'support', 'lift', 'min_confidence', 'avg_confidence',
            'jaccard_similarity', 'frequency_a', 'frequency_b'
        ]
        
        # Add optional features if they exist
        if 'price_ratio' in df.columns:
            feature_cols.append('price_ratio')
        if 'is_cross_category' in df.columns:
            feature_cols.append('is_cross_category')
        
        # Ensure all features exist
        feature_cols = [col for col in feature_cols if col in df.columns]
        
        # Check if we have a trained model
        if BUNDLE_MODEL_PATH.exists():
            try:
                model_bundle = joblib.load(BUNDLE_MODEL_PATH)
                model = model_bundle['model']
                
                X = df[feature_cols].fillna(0)
                success_prob = model.predict_proba(X)[:, 1]
                df['success_probability'] = success_prob
                df['ml_model_used'] = True
                
                return df
            except Exception as e:
                print(f"Warning: Could not load ML model: {e}")
                print("Falling back to heuristic scoring...")
        
        # Heuristic scoring (weighted combination of metrics)
        # This works well even without historical training data
        weights = {
            'lift': 0.25,
            'min_confidence': 0.25,
            'support': 0.20,
            'jaccard_similarity': 0.15,
            'avg_confidence': 0.15,
        }
        
        # Normalize features to 0-1 range
        normalized = df[list(weights.keys())].copy()
        for col in normalized.columns:
            max_val = normalized[col].max()
            if max_val > 0:
                normalized[col] = normalized[col] / max_val
        
        # Calculate weighted score
        score = sum(normalized[col] * weight for col, weight in weights.items())
        
        # Apply sigmoid to get probability-like values
        df['success_probability'] = 1 / (1 + np.exp(-5 * (score - 0.5)))
        df['ml_model_used'] = False
        
        return df
    
    def get_top_bundles(
        self,
        df: pd.DataFrame,
        tx_col: str,
        item_col: str,
        top_n: int = 20,
        min_support: float = 0.001,
        min_confidence: float = 0.1,
        price_col: str = None,
        category_col: str = None
    ) -> List[Dict]:
        """
        Main method to get ML-powered bundle recommendations.
        
        Args:
            df: Transaction data
            tx_col: Transaction ID column
            item_col: Product/Item column
            top_n: Number of top bundles to return
            min_support: Minimum support threshold (very low default)
            min_confidence: Minimum confidence threshold
            price_col: Optional price column
            category_col: Optional category column
            
        Returns:
            List of bundle dictionaries with predictions
        """
        # Extract features
        bundle_features = self.extract_bundle_features(
            df, tx_col, item_col, price_col, category_col
        )
        
        # Filter by minimum thresholds
        filtered = bundle_features[
            (bundle_features['support'] >= min_support) &
            (bundle_features['min_confidence'] >= min_confidence)
        ].copy()
        
        if len(filtered) == 0:
            return []
        
        # Predict success probability
        with_predictions = self.predict_bundle_success(filtered)
        
        # Sort by success probability
        top_bundles = with_predictions.nlargest(top_n, 'success_probability')
        
        # Format output
        results = []
        for _, row in top_bundles.iterrows():
            bundle = {
                'products': f"{row['item_a']} + {row['item_b']}",
                'item_a': row['item_a'],
                'item_b': row['item_b'],
                'success_probability': float(row['success_probability']),
                'support': float(row['support']),
                'confidence_a_to_b': float(row['confidence_a_to_b']),
                'confidence_b_to_a': float(row['confidence_b_to_a']),
                'lift': float(row['lift']),
                'pair_count': int(row['pair_count']),
                'recommendation_score': float(row['success_probability'] * 100),
                'ml_model_used': row.get('ml_model_used', False),
            }
            
            # Add optional fields if available
            if 'total_price' in row:
                bundle['total_price'] = float(row['total_price'])
            if 'is_cross_category' in row:
                bundle['is_cross_category'] = bool(row['is_cross_category'])
            
            results.append(bundle)
        
        return results


def train_bundle_success_model(
    historical_bundles: pd.DataFrame,
    success_col: str = 'was_successful'
):
    """
    Train an ML model to predict bundle success from historical data.
    
    Args:
        historical_bundles: DataFrame with bundle features and success labels
        success_col: Column indicating if bundle was successful (0/1)
    """
    feature_cols = [
        'support', 'lift', 'min_confidence', 'avg_confidence',
        'jaccard_similarity', 'frequency_a', 'frequency_b',
        'price_ratio', 'is_cross_category'
    ]
    
    # Filter to available features
    feature_cols = [col for col in feature_cols if col in historical_bundles.columns]
    
    X = historical_bundles[feature_cols].fillna(0)
    y = historical_bundles[success_col]
    
    # Train model
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        ))
    ])
    
    model.fit(X, y)
    
    # Save model
    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump({
        'model': model,
        'feature_cols': feature_cols,
    }, BUNDLE_MODEL_PATH)
    
    print(f"✅ Bundle prediction model saved to {BUNDLE_MODEL_PATH}")
    
    return model