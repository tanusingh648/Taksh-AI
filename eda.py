from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter()


@router.post("/eda")
async def perform_eda(file: UploadFile = File(...)):

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

    if numerical_columns:
        statistics = (
            df[numerical_columns]
            .describe()
            .to_dict()
        )
    else:
        statistics = {}

    unique_values = {
        column: int(df[column].nunique())
        for column in df.columns
    }

    categorical_summary = {}

    for column in categorical_columns:
        categorical_summary[column] = (
            df[column]
            .value_counts()
            .head(10)
            .to_dict()
        )

    correlation = {}

    if len(numerical_columns) > 1:
        correlation = (
            df[numerical_columns]
            .corr()
            .round(3)
            .to_dict()
        )

    return {
        "filename": file.filename,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "statistics": statistics,
        "unique_values": unique_values,
        "categorical_summary": categorical_summary,
        "correlation": correlation,
        "status": "EDA completed successfully"
    }
