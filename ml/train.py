from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


# Load customer churn dataset
data = fetch_openml(
    name="telco-customer-churn",
    version=1,
    as_frame=True
)

df = data.frame

# Convert target to numeric
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Remove customer ID
df = df.drop(columns=["customerID"], errors="ignore")

# Convert categorical columns to numbers
df = df.dropna()

X = df.drop(columns=["Churn"])
y = df["Churn"]

X = X.select_dtypes(include=["number"])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create ML pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)

print("Model accuracy:", accuracy)

# Save model
joblib.dump(model, "ml/churn_model.pkl")

print("Model saved successfully!")