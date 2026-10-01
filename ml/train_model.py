import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. Load engineered features
# ==========================================

DATA_PATH = "data/bronze/claims_ml_features.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ==========================================
# 2. Features and target
# ==========================================

target = "claim_status"

features = [
    "claim_amount",
    "claim_type",
    "claim_location",

    "policy_type",
    "policy_status",
    "premium",
    "coverage_amount",
    "payment_frequency",

    "gender",
    "city",
    "state",
    "customer_segment",
    "income",
    "occupation",

    "customer_age",
    "customer_tenure_days",
    "policy_age_days",
    "claim_year",
    "claim_month"
]

# Keep only required columns
df = df[features + [target]].dropna()

X = df[features]
y = df[target]

print("\nUsable records:", len(df))

print("\nTarget distribution:")
print(y.value_counts())


# ==========================================
# 3. Identify categorical/numeric features
# ==========================================

categorical_features = [
    "claim_type",
    "claim_location",
    "policy_type",
    "policy_status",
    "payment_frequency",
    "gender",
    "city",
    "state",
    "customer_segment",
    "occupation"
]

numeric_features = [
    "claim_amount",
    "premium",
    "coverage_amount",
    "income",
    "customer_age",
    "customer_tenure_days",
    "policy_age_days",
    "claim_year",
    "claim_month"
]


# ==========================================
# 4. Train/test split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 5. Preprocessing
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ==========================================
# 6. Random Forest
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)


# ==========================================
# 7. Pipeline
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# 8. Train
# ==========================================

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 9. Evaluate
# ==========================================

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n===================================")
print("MODEL RESULTS")
print("===================================")

print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ==========================================
# 10. Save model
# ==========================================

MODEL_PATH = "ml/claim_status_model.pkl"

joblib.dump(pipeline, MODEL_PATH)

print("\nModel saved successfully:")
print(MODEL_PATH)