from pathlib import Path
import joblib
import pandas as pd

from preprocess import load_raw_data, build_customer_features


ML_DIR = Path(__file__).resolve().parent
MODELS_DIR = ML_DIR / "models"
MODEL_PATH = MODELS_DIR / "customer_value_model.joblib"
OUTPUT_PATH = ML_DIR / "customer_segments.csv"


def score_all_customers():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Trained model not found at {MODEL_PATH}. "
            f"Run train_model.py first."
        )

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    feature_cols = bundle["features"]

    # Rebuild the full customer feature table (same logic as training)
    data = load_raw_data()
    full_df, _, target_col = build_customer_features(data)

    X = full_df[feature_cols]

    scores = model.predict_proba(X)[:, 1]

    segments = pd.DataFrame({
        "customer_id": full_df["customer_id"],
        "high_value_score": scores,
    })

    # Simple segmentation into 3 buckets by score
    segments["segment"] = pd.qcut(
        segments["high_value_score"],
        q=3,
        labels=["Low", "Medium", "High"],
    )

    segments.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Saved customer segments to {OUTPUT_PATH}")


if __name__ == "__main__":
    score_all_customers()
