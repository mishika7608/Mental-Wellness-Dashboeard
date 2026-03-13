"""
Model Training Script
Trains Random Forest classifier on Student Depression Dataset
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler, OrdinalEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, recall_score
import joblib
import os

def load_and_preprocess_data(filepath):
    """Load and preprocess the dataset"""
    print("Loading dataset...")
    df = pd.read_csv(filepath)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Drop unnecessary columns
    columns_to_drop = ['id', 'City']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    
    # Handle missing values
    print(f"Missing values before: {df.isnull().sum().sum()}")
    df = df.dropna()
    print(f"Missing values after: {df.isnull().sum().sum()}")
    
    # Clean string columns - remove extra quotes from values
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.strip("'")
    
    return df

def encode_features(df):
    """Encode categorical and ordinal features"""
    print("Encoding features...")
    
    encoders = {}
    
    # Target variable: Depression
    le_target = LabelEncoder()
    df['Depression'] = le_target.fit_transform(df['Depression'])
    encoders['target'] = le_target
    
    # Gender encoding
    if 'Gender' in df.columns:
        le_gender = LabelEncoder()
        df['Gender'] = le_gender.fit_transform(df['Gender'])
        encoders['gender'] = le_gender
    
    # Ordinal encoding for Sleep Duration
    if 'Sleep Duration' in df.columns:
        # Map 'Others' to a known category (middle value)
        df['Sleep Duration'] = df['Sleep Duration'].replace('Others', '5-6 hours')
        sleep_order = ['Less than 5 hours', '5-6 hours', '7-8 hours', 'More than 8 hours']
        sleep_encoder = OrdinalEncoder(categories=[sleep_order], handle_unknown='use_encoded_value', unknown_value=-1)
        df['Sleep Duration'] = sleep_encoder.fit_transform(df[['Sleep Duration']])
        encoders['sleep'] = sleep_encoder
    
    # Ordinal encoding for Dietary Habits
    if 'Dietary Habits' in df.columns:
        # Map 'Others' to a known category (middle value)
        df['Dietary Habits'] = df['Dietary Habits'].replace('Others', 'Moderate')
        diet_order = ['Unhealthy', 'Moderate', 'Healthy']
        diet_encoder = OrdinalEncoder(categories=[diet_order], handle_unknown='use_encoded_value', unknown_value=-1)
        df['Dietary Habits'] = diet_encoder.fit_transform(df[['Dietary Habits']])
        encoders['diet'] = diet_encoder
    
    # Encode other categorical variables if present
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col != 'Depression':
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            encoders[col] = le
    
    return df, encoders

def scale_features(X_train, X_test):
    """Scale numerical features"""
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, scaler

def train_random_forest(X_train, y_train, X_test, y_test):
    """Train Random Forest classifier"""
    print("Training Random Forest model...")
    
    # Initialize model with optimized hyperparameters
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight='balanced',  # Handle class imbalance
        random_state=42,
        n_jobs=-1  # Use all CPU cores
    )
    
    # Train model
    rf_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test)
    y_pred_proba = rf_model.predict_proba(X_test)
    
    # Evaluate model
    print("\n" + "="*50)
    print("MODEL PERFORMANCE")
    print("="*50)
    
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    print(f"\nAccuracy: {accuracy*100:.2f}%")
    print(f"Recall (Sensitivity): {recall*100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=['No Depression', 'Depression']))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Cross-validation
    print("\n5-Fold Cross-Validation Scores:")
    cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='recall')
    print(f"Recall scores: {cv_scores}")
    print(f"Mean Recall: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*200:.2f}%)")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns if hasattr(X_train, 'columns') else range(X_train.shape[1]),
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Feature Importances:")
    print(feature_importance.head(10))
    
    return rf_model, feature_importance

def save_models(model, scaler, encoders, feature_importance):
    """Save trained model and preprocessing objects"""
    print("\nSaving models...")
    
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model, 'models/random_forest_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(encoders, 'models/encoders.pkl')
    feature_importance.to_csv('models/feature_importance.csv', index=False)
    
    print("✓ Model saved to models/random_forest_model.pkl")
    print("✓ Scaler saved to models/scaler.pkl")
    print("✓ Encoders saved to models/encoders.pkl")
    print("✓ Feature importance saved to models/feature_importance.csv")

def main():
    """Main training pipeline"""
    
    # Load data
    df = load_and_preprocess_data('data/Student_Depression_Dataset.csv')
    
    # Encode features
    df, encoders = encode_features(df)
    
    # Separate features and target
    X = df.drop('Depression', axis=1)
    y = df['Depression']
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    
    # Convert back to DataFrame for feature names
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    # Train model
    model, feature_importance = train_random_forest(
        X_train_scaled, y_train, X_test_scaled, y_test
    )
    
    # Save everything
    save_models(model, scaler, encoders, feature_importance)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    print("\nYou can now run the dashboard with: streamlit run app.py")

if __name__ == "__main__":
    main()