from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from preprocess import prepare_train_test


# Where to save the trained model
ML_DIR = Path(__file__).resolve().parent
MODELS_DIR = ML_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODELS_DIR / "customer_value_model.joblib"


def train_and_save_model():
    X_train, X_test, y_train, y_test, feature_cols, full_df = prepare_train_test()

    # Simple numeric pipeline
    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(
                n_estimators=200,
                max_depth=None,
                random_state=42,
                n_jobs=-1,
            )),
        ]
    )

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n=== Classification report (high value vs not) ===")
    print(classification_report(y_test, y_pred))

    print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.3f}")

    # Bundle everything we need for inference
    bundle = {
        "model": model,
        "features": feature_cols,
        "target_name": "is_high_value",
    }
    joblib.dump(bundle, MODEL_PATH)
    print(f"\n✅ Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
