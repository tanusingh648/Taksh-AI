from fastapi import APIRouter, UploadFile, File, Form
import pandas as pd
import io
import os
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.metrics import accuracy_score, mean_squared_error, r2_score


router = APIRouter()

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)


@router.post("/train")
async def train_model(
    file: UploadFile = File(...),
    target_column: str = Form(...)
):

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))

    else:
        return {
            "error": "Only CSV and XLSX files are supported"
        }

    if target_column not in df.columns:
        return {
            "error": f"Target column '{target_column}' not found",
            "available_columns": df.columns.tolist()
        }

    df = df.dropna(subset=[target_column])

    X = df.drop(columns=[target_column])
    y = df[target_column]

    numerical_columns = X.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = X.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    transformers = []

    if numerical_columns:
        transformers.append(
            (
                "numerical",
                StandardScaler(),
                numerical_columns
            )
        )

    if categorical_columns:
        transformers.append(
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_columns
            )
        )

    preprocessor = ColumnTransformer(
        transformers=transformers
    )

    # Classification
    if (
        y.dtype == "object"
        or str(y.dtype) == "category"
        or y.nunique() <= 10
    ):

        problem_type = "classification"

        models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
        }

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42,
                stratify=y
            )
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

        results = {}

        for name, model in models.items():

            pipeline = Pipeline(
                steps=[
                    ("preprocessing", preprocessor),
                    ("model", model)
                ]
            )

            pipeline.fit(X_train, y_train)

            predictions = pipeline.predict(X_test)

            accuracy = accuracy_score(
                y_test,
                predictions
            )

            model_filename = (
                name.replace(" ", "_").lower()
            )

            model_path = os.path.join(
                MODEL_DIR,
                f"{model_filename}.joblib"
            )

            joblib.dump(
                pipeline,
                model_path
            )

            metadata = {
                "model_name": name,
                "target_column": target_column,
                "feature_columns": X.columns.tolist(),
                "numerical_features": numerical_columns,
                "categorical_features": categorical_columns,
                "problem_type": problem_type
            }

            metadata_path = os.path.join(
                MODEL_DIR,
                f"{model_filename}_metadata.json"
            )

            with open(metadata_path, "w") as f:
                json.dump(
                    metadata,
                    f,
                    indent=4
                )

            results[name] = {
                "accuracy": round(
                    float(accuracy),
                    4
                ),
                "model_path": model_path,
                "metadata_path": metadata_path
            }

    # Regression
    else:

        problem_type = "regression"

        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
        }

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        results = {}

        for name, model in models.items():

            pipeline = Pipeline(
                steps=[
                    ("preprocessing", preprocessor),
                    ("model", model)
                ]
            )

            pipeline.fit(X_train, y_train)

            predictions = pipeline.predict(X_test)

            mse = mean_squared_error(
                y_test,
                predictions
            )

            rmse = mse ** 0.5

            r2 = r2_score(
                y_test,
                predictions
            )

            model_filename = (
                name.replace(" ", "_").lower()
            )

            model_path = os.path.join(
                MODEL_DIR,
                f"{model_filename}.joblib"
            )

            joblib.dump(
                pipeline,
                model_path
            )

            metadata = {
                "model_name": name,
                "target_column": target_column,
                "feature_columns": X.columns.tolist(),
                "numerical_features": numerical_columns,
                "categorical_features": categorical_columns,
                "problem_type": problem_type
            }

            metadata_path = os.path.join(
                MODEL_DIR,
                f"{model_filename}_metadata.json"
            )

            with open(metadata_path, "w") as f:
                json.dump(
                    metadata,
                    f,
                    indent=4
                )

            results[name] = {
                "RMSE": round(
                    float(rmse),
                    4
                ),
                "R2": round(
                    float(r2),
                    4
                ),
                "model_path": model_path,
                "metadata_path": metadata_path
            }

    return {
        "filename": file.filename,
        "target_column": target_column,
        "problem_type": problem_type,
        "numerical_features": numerical_columns,
        "categorical_features": categorical_columns,
        "results": results,
        "status": "Models trained and saved successfully"
    }
