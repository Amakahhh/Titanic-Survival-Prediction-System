import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

print("=" * 80)
print("TITANIC SURVIVAL PREDICTION - MODEL TRAINING")
print("=" * 80)

# Step 1: Load Dataset
print("\n[1/9] Loading Titanic Dataset...")
df = pd.read_csv('Titanic-Dataset.csv')
print(f"✓ Dataset loaded: {df.shape}")

# Step 2: Select required columns
print("\n[2/9] Selecting features...")
required_features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Fare', 'Survived']
df_clean = df[required_features].copy()
print(f"✓ Features selected: {list(df_clean.columns)}")

# Step 3: Handle missing values
print("\n[3/9] Handling missing values...")
df_clean = df_clean.dropna(subset=['Survived'])
df_clean['Age'].fillna(df_clean['Age'].median(), inplace=True)
df_clean['Fare'].fillna(df_clean['Fare'].median(), inplace=True)
print(f"✓ Missing values handled. Shape: {df_clean.shape}")

# Step 4: Encode categorical variables
print("\n[4/9] Encoding categorical variables...")
df_clean['Sex'] = (df_clean['Sex'] == 'male').astype(int)
print("✓ Sex encoded (male=1, female=0)")

# Step 5: Prepare features and target
print("\n[5/9] Preparing features and target...")
X = df_clean[['Pclass', 'Sex', 'Age', 'SibSp', 'Fare']]
y = df_clean['Survived']
selected_features = X.columns.tolist()
print(f"✓ Features: {selected_features}")
print(f"✓ Target: Survived (0/1)")

# Step 6: Train-test split BEFORE scaling (prevent data leakage)
print("\n[6/9] Splitting data (BEFORE scaling)...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)
print(f"✓ Train set: {X_train.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

# Step 7: Scale features (fit ONLY on training data)
print("\n[7/9] Scaling features (fit on X_train only)...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("✓ Scaler fitted on X_train")
print("✓ Scaler applied to both X_train and X_test")

# Step 8: Train Random Forest
print("\n[8/9] Training Random Forest Classifier...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_scaled, y_train)
print("✓ Model trained successfully!")

# Step 9: Evaluate Model
print("\n[9/9] Evaluating model...")
y_pred_train = model.predict(X_train_scaled)
y_pred_test = model.predict(X_test_scaled)

train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\n✓ Training Accuracy: {train_accuracy:.4f}")
print(f"✓ Test Accuracy: {test_accuracy:.4f}")

print("\n" + "=" * 80)
print("CLASSIFICATION REPORT (Test Set)")
print("=" * 80)
print(classification_report(y_test, y_pred_test, 
                          target_names=['Did Not Survive', 'Survived']))

print("\n" + "=" * 80)
print("CONFUSION MATRIX (Test Set)")
print("=" * 80)
print(confusion_matrix(y_test, y_pred_test))

# Feature Importance
print("\n" + "=" * 80)
print("FEATURE IMPORTANCE")
print("=" * 80)
feature_importance = pd.DataFrame({
    'Feature': selected_features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance.to_string(index=False))

# Save model artifacts
print("\n" + "=" * 80)
print("SAVING MODEL ARTIFACTS")
print("=" * 80)

# Create model directory if needed
os.makedirs('model', exist_ok=True)

# Save model
model_path = 'model/titanic_survival_model.pkl'
joblib.dump(model, model_path)
print(f"✓ Model saved to: {model_path}")

# Save scaler
scaler_path = 'model/titanic_scaler.pkl'
joblib.dump(scaler, scaler_path)
print(f"✓ Scaler saved to: {scaler_path}")

# Save features
features_path = 'model/selected_features.pkl'
joblib.dump(selected_features, features_path)
print(f"✓ Features saved to: {features_path}")

# Verify reload
print("\n" + "=" * 80)
print("VERIFYING MODEL RELOAD")
print("=" * 80)
loaded_model = joblib.load(model_path)
loaded_scaler = joblib.load(scaler_path)
loaded_features = joblib.load(features_path)

test_sample = X_test.iloc[0:1]
test_sample_scaled = loaded_scaler.transform(test_sample)
predicted_class = loaded_model.predict(test_sample_scaled)[0]
probabilities = loaded_model.predict_proba(test_sample_scaled)[0]
confidence = float(np.max(probabilities)) * 100

print(f"✓ Model reloaded successfully!")
print(f"✓ Test prediction: {predicted_class} (Survived)" if predicted_class == 1 else f"✓ Test prediction: {predicted_class} (Did Not Survive)")
print(f"✓ Confidence: {confidence:.2f}%")
print(f"✓ Actual value: {y_test.iloc[0]}")

print("\n" + "=" * 80)
print("✅ MODEL TRAINING COMPLETE!")
print("=" * 80)
print(f"\nAll artifacts ready for deployment:")
print(f"  • {model_path}")
print(f"  • {scaler_path}")
print(f"  • {features_path}")
print("\n")
