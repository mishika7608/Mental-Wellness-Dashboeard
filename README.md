# Mental Health Prediction Dashboard

AI-Powered Student Wellness Assessment Tool

## Overview

This dashboard uses Machine Learning (Random Forest) to predict depression risk in college students based on academic, lifestyle, and demographic factors.

## Features

- **87% Recall Rate**: Catches 87 out of 100 at-risk students
- **Privacy-First**: No data storage, local processing
- **Real-time Predictions**: <200ms response time
- **Interpretable Results**: Feature importance and personalized recommendations

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download dataset to `data/` folder
4. Train model: `python train_model.py`
5. Run dashboard: `streamlit run app.py`

## Usage

1. Fill in the assessment form
2. Click "Predict Depression Risk"
3. View results and recommendations
4. Access crisis resources if needed

## Model Performance

- Accuracy: 84.1%
- Recall: 87%
- Precision: 83%
- ROC-AUC: 0.91

## Authors

- Divyanshi Sahu
- Deeksha Singh
- Chhavi Agrahari
- Mishika Kulshrestha

GL Bajaj Institute of Technology & Management

## License

This project is for educational and research purposes.