import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load CSV
df = pd.read_csv("student_data.csv")

# Select features for performance prediction
features = [
    "Attendance Percentage", "Daily Study Hours", "Internet Usage (Hours/Day)",
    "Internal Exam1 Marks", "Internal Exam2 Marks", "Assignment Average", "Lab Marks",
    "Mini Project Marks", "Major Project Marks", "CGPA",
    "Communication Skills", "Programming Skills", "Logical Thinking", "Leadership Quality",
    "Aptitude Score", "Technical Score", "HR Score"
]

X = df[features]

# Encode target variable
y = df["Performance_Prediction"]
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Save model and label encoder
joblib.dump(model, "trained_model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Model saved as trained_model.pkl and label_encoder.pkl")