# ⚡ TAKSH AI

### AI-Powered Data Analysis & AutoML Platform

Taksh AI is an AI-powered data analysis and machine learning platform designed to simplify the complete data science workflow — from dataset upload and profiling to preprocessing, model training, prediction, insights, and report generation.

---

## 🚀 Features

### 📂 Dataset Upload
- Upload CSV and XLSX datasets
- Automatic dataset validation
- Display dataset size and basic information

### 🔍 Dataset Profiling
- Number of rows and columns
- Column names
- Data types
- Missing values
- Duplicate rows
- Numerical and categorical feature detection

### 🧹 Data Cleaning
- Duplicate row detection and removal
- Missing-value detection
- Numerical missing values handled using median
- Categorical missing values handled using mode

### 📊 Exploratory Data Analysis
- Statistical summaries
- Numerical feature analysis
- Categorical feature analysis
- Unique-value analysis
- Correlation analysis

### 🧩 Feature Analysis
- Automatic numerical feature detection
- Automatic categorical feature detection
- Feature preparation recommendations

### ⚙️ Data Preprocessing
- Feature scaling using StandardScaler
- Categorical encoding using OneHotEncoder
- Automatic preprocessing pipeline using ColumnTransformer

### 🤖 Automated Machine Learning
Taksh AI currently supports:

**Classification**
- Logistic Regression
- Random Forest Classifier

**Regression**
- Linear Regression
- Random Forest Regressor

### 📈 Model Evaluation

Classification:
- Accuracy

Regression:
- RMSE
- R² Score

### 🔮 Prediction
- Load trained models
- Provide new input data
- Generate predictions through the API

### 🧠 AI Insights
Automatically generates insights related to:
- Dataset structure
- Missing values
- Duplicate records
- Numerical features
- Categorical features
- Feature correlations

### 📄 Report Generation
- Automatically generate an HTML dataset report
- Download the generated report

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │      TAKSH AI       │
                    │   Streamlit UI      │
                    └──────────┬──────────┘
                               │
                               │ REST API
                               ↓
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ↓                 ↓                 ↓
        Data Processing      ML Engine       Insights
             │                 │                 │
             ↓                 ↓                 ↓
          Pandas          Scikit-learn        Analysis
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ↓
                        Reports / Models
