from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

router = APIRouter()


@router.post("/processing")
async def process_dataset(file: UploadFile = File(...)):

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))

    else:
        return {
            "error": "Only CSV and XLSX files are supported"
        }

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
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
                    handle_unknown="ignore",
                    sparse_output=False
                ),
                categorical_columns
            )
        )

    if not transformers:
        return {
            "error": "No numerical or categorical columns found"
        }

    preprocessor = ColumnTransformer(
        transformers=transformers
    )

    processed_data = preprocessor.fit_transform(df)

    feature_names = preprocessor.get_feature_names_out()

    return {
        "filename": file.filename,
        "original_rows": int(df.shape[0]),
        "original_columns": int(df.shape[1]),
        "processed_columns": int(len(feature_names)),
        "numerical_features": numerical_columns,
        "categorical_features": categorical_columns,
        "processed_feature_names": feature_names.tolist(),
        "status": "Dataset preprocessing completed successfully"
    }
