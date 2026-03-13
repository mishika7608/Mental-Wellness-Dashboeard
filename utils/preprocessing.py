"""
Data Preprocessing Utilities
Contains functions for cleaning, encoding, and transforming data
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, OrdinalEncoder
import joblib

class DataPreprocessor:
    """
    Handles all data preprocessing tasks including:
    - Missing value handling
    - Feature encoding
    - Scaling
    - Feature engineering
    """
    
    def __init__(self):
        self.encoders = {}
        self.scaler = None
        
    def clean_data(self, df):
        """
        Clean the dataset by handling missing values and outliers
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Create a copy to avoid modifying original
        df_clean = df.copy()
        
        # Drop unnecessary columns
        columns_to_drop = ['id', 'City', 'Unnamed: 0']
        df_clean = df_clean.drop(columns=[col for col in columns_to_drop if col in df_clean.columns])
        
        # Handle missing values
        print(f"Missing values before cleaning: {df_clean.isnull().sum().sum()}")
        
        # For numerical columns, fill with median
        numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
        
        # For categorical columns, fill with mode
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Handle outliers in age (reasonable range: 17-35)
        if 'Age' in df_clean.columns:
            df_clean = df_clean[(df_clean['Age'] >= 17) & (df_clean['Age'] <= 35)]
        
        # Handle outliers in CGPA (reasonable range: 0-10)
        if 'CGPA' in df_clean.columns:
            df_clean = df_clean[(df_clean['CGPA'] >= 0) & (df_clean['CGPA'] <= 10)]
        
        print(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
        print(f"Rows after cleaning: {len(df_clean)}")
        
        return df_clean
    
    def encode_target(self, y, target_name='Depression'):
        """
        Encode target variable
        
        Args:
            y: Target series
            target_name: Name of target variable
            
        Returns:
            Encoded target
        """
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        self.encoders[target_name] = le
        
        print(f"Target classes: {le.classes_}")
        return y_encoded
    
    def encode_categorical_features(self, df):
        """
        Encode categorical features with appropriate encoding
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with encoded features
        """
        df_encoded = df.copy()
        
        # Ordinal encoding for Sleep Duration (has natural order)
        if 'Sleep Duration' in df_encoded.columns:
            sleep_order = ['Less than 5 hours', '5-6 hours', '7-8 hours', 'More than 8 hours']
            sleep_encoder = OrdinalEncoder(categories=[sleep_order])
            df_encoded['Sleep Duration'] = sleep_encoder.fit_transform(df_encoded[['Sleep Duration']])
            self.encoders['Sleep Duration'] = sleep_encoder
            print("Sleep Duration encoded (ordinal)")
        
        # Ordinal encoding for Dietary Habits
        if 'Dietary Habits' in df_encoded.columns:
            diet_order = ['Unhealthy', 'Moderate', 'Healthy']
            diet_encoder = OrdinalEncoder(categories=[diet_order])
            df_encoded['Dietary Habits'] = diet_encoder.fit_transform(df_encoded[['Dietary Habits']])
            self.encoders['Dietary Habits'] = diet_encoder
            print("Dietary Habits encoded (ordinal)")
        
        # Label encoding for binary/nominal categorical features
        categorical_cols = df_encoded.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col])
            self.encoders[col] = le
            print(f"{col} encoded (label) - classes: {le.classes_}")
        
        return df_encoded
    
    def scale_features(self, X_train, X_test=None):
        """
        Scale numerical features using StandardScaler
        
        Args:
            X_train: Training features
            X_test: Test features (optional)
            
        Returns:
            Scaled features
        """
        self.scaler = StandardScaler()
        
        # Preserve column names if DataFrame
        columns = X_train.columns if hasattr(X_train, 'columns') else None
        index_train = X_train.index if hasattr(X_train, 'index') else None
        
        # Fit and transform training data
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Convert back to DataFrame if it was originally
        if columns is not None:
            X_train_scaled = pd.DataFrame(X_train_scaled, columns=columns, index=index_train)
        
        if X_test is not None:
            index_test = X_test.index if hasattr(X_test, 'index') else None
            X_test_scaled = self.scaler.transform(X_test)
            
            if columns is not None:
                X_test_scaled = pd.DataFrame(X_test_scaled, columns=columns, index=index_test)
            
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def create_features(self, df):
        """
        Create additional engineered features
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional features
        """
        df_featured = df.copy()
        
        # Sleep quality score (higher is better)
        if 'Sleep Duration' in df_featured.columns:
            sleep_mapping = {
                0: 1,  # Less than 5 hours - poor
                1: 2,  # 5-6 hours - moderate
                2: 4,  # 7-8 hours - good
                3: 3   # More than 8 hours - slightly excessive
            }
            df_featured['Sleep_Quality_Score'] = df_featured['Sleep Duration'].map(sleep_mapping)
        
        # Academic stress index (combination of pressure and hours)
        if 'Academic Pressure' in df_featured.columns and 'Study Hours' in df_featured.columns:
            df_featured['Academic_Stress_Index'] = (
                df_featured['Academic Pressure'] * df_featured['Study Hours'] / 10
            )
        
        # Overall wellbeing score
        if all(col in df_featured.columns for col in ['CGPA', 'Study Satisfaction']):
            df_featured['Wellbeing_Score'] = (
                (df_featured['CGPA'] / 2) + df_featured['Study Satisfaction']
            )
        
        # Risk factor count
        risk_features = []
        
        if 'Sleep Duration' in df_featured.columns:
            risk_features.append(df_featured['Sleep Duration'] <= 1)  # Poor sleep
        
        if 'Academic Pressure' in df_featured.columns:
            risk_features.append(df_featured['Academic Pressure'] >= 4)  # High pressure
        
        if 'Financial Stress' in df_featured.columns:
            risk_features.append(df_featured['Financial Stress'] >= 4)  # High stress
        
        if 'Study Satisfaction' in df_featured.columns:
            risk_features.append(df_featured['Study Satisfaction'] <= 2)  # Low satisfaction
        
        if risk_features:
            df_featured['Risk_Factor_Count'] = sum(risk_features)
        
        return df_featured
    
    def save_preprocessor(self, filepath='models/preprocessor.pkl'):
        """
        Save the preprocessor with all encoders and scaler
        
        Args:
            filepath: Path to save the preprocessor
        """
        preprocessor_data = {
            'encoders': self.encoders,
            'scaler': self.scaler
        }
        joblib.dump(preprocessor_data, filepath)
        print(f"Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.pkl'):
        """
        Load a saved preprocessor
        
        Args:
            filepath: Path to the saved preprocessor
        """
        preprocessor_data = joblib.load(filepath)
        self.encoders = preprocessor_data['encoders']
        self.scaler = preprocessor_data['scaler']
        print(f"Preprocessor loaded from {filepath}")
    
    def transform_new_data(self, df):
        """
        Transform new data using fitted encoders and scaler
        
        Args:
            df: New data to transform
            
        Returns:
            Transformed data
        """
        df_transformed = df.copy()
        
        # Apply encoders
        for col, encoder in self.encoders.items():
            if col in df_transformed.columns and col != 'Depression':
                if isinstance(encoder, OrdinalEncoder):
                    df_transformed[col] = encoder.transform(df_transformed[[col]])
                elif isinstance(encoder, LabelEncoder):
                    df_transformed[col] = encoder.transform(df_transformed[col])
        
        # Apply scaler
        if self.scaler is not None:
            columns = df_transformed.columns
            df_transformed = pd.DataFrame(
                self.scaler.transform(df_transformed),
                columns=columns
            )
        
        return df_transformed


def validate_data_quality(df):
    """
    Validate data quality and print summary statistics
    
    Args:
        df: Input DataFrame
    """
    print("\n" + "="*60)
    print("DATA QUALITY REPORT")
    print("="*60)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}")
    
    print("\nColumn Types:")
    print(df.dtypes.value_counts())
    
    print("\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values found ✓")
    
    print("\nDuplicate Rows:")
    duplicates = df.duplicated().sum()
    print(f"{duplicates} duplicate rows found")
    
    print("\nNumerical Features Summary:")
    print(df.describe())
    
    print("\nCategorical Features:")
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        print(f"\n{col}:")
        print(df[col].value_counts())
    
    print("\n" + "="*60)


def split_features_target(df, target_col='Depression'):
    """
    Split DataFrame into features (X) and target (y)
    
    Args:
        df: Input DataFrame
        target_col: Name of target column
        
    Returns:
        X, y tuple
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame")
    
    X = df.drop(target_col, axis=1)
    y = df[target_col]
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    
    return X, y


def get_feature_info(df):
    """
    Get detailed information about features
    
    Args:
        df: Input DataFrame
        
    Returns:
        Dictionary with feature information
    """
    feature_info = {
        'numerical': list(df.select_dtypes(include=[np.number]).columns),
        'categorical': list(df.select_dtypes(include=['object']).columns),
        'total_features': df.shape[1],
        'feature_names': list(df.columns)
    }
    
    return feature_info


if __name__ == "__main__":
    # Example usage
    print("Data Preprocessing Utilities Module")
    print("Import this module to use preprocessing functions")