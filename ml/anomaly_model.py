import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# ==========================================
# 1. Load engineered data
# ==========================================

DATA_PATH = "data/bronze/claims_ml_features.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ==========================================
# 2. Select anomaly features
# ==========================================

features = [
    "claim_amount",
    "premium",
    "coverage_amount",
    "income",
    "customer_age",
    "customer_tenure_days",
    "policy_age_days"
]

X = df[features].dropna()

print("Records used:", len(X))


# ==========================================
# 3. Build anomaly detection pipeline
# ==========================================

pipeline = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        (
            "model",
            IsolationForest(
                n_estimators=200,
                contamination=0.05,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


# ==========================================
# 4. Train
# ==========================================

print("\nTraining anomaly detection model...")

pipeline.fit(X)

print("Training completed!")


# ==========================================
# 5. Predict anomalies
# ==========================================

predictions = pipeline.predict(X)

df.loc[X.index, "anomaly_prediction"] = predictions

df["anomaly_status"] = df["anomaly_prediction"].map(
    {
        1: "Normal",
        -1: "Anomaly"
    }
)


# ==========================================
# 6. Results
# ==========================================

print("\n===================================")
print("ANOMALY DETECTION RESULTS")
print("===================================")

print(df["anomaly_status"].value_counts())

print("\nAnomaly percentage:")

anomaly_percentage = (
    (df["anomaly_status"] == "Anomaly").mean() * 100
)

print(f"{anomaly_percentage:.2f}%")


# ==========================================
# 7. Save model
# ==========================================

MODEL_PATH = "ml/anomaly_model.pkl"

joblib.dump(pipeline, MODEL_PATH)

print("\nModel saved:")
print(MODEL_PATH)


# ==========================================
# 8. Save predictions
# ==========================================

OUTPUT_PATH = "data/bronze/claims_anomaly_results.csv"

df.to_csv(OUTPUT_PATH, index=False)

print("\nResults saved:")
print(OUTPUT_PATH)