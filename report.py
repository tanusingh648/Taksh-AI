from fastapi import APIRouter, UploadFile, File
from fastapi.responses import HTMLResponse
import pandas as pd
import io
import os

router = APIRouter()

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


@router.post("/report")
async def generate_report(file: UploadFile = File(...)):

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))

    else:
        return {
            "error": "Only CSV and XLSX files are supported"
        }

    rows = int(df.shape[0])
    columns = int(df.shape[1])

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicates = int(
        df.duplicated().sum()
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Taksh AI Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #0b1020;
                color: white;
                padding: 40px;
            }}

            h1 {{
                color: #00e5ff;
            }}

            .card {{
                background: #151b2e;
                padding: 20px;
                margin: 15px 0;
                border-radius: 12px;
                border: 1px solid #303b63;
            }}

            .value {{
                font-size: 28px;
                font-weight: bold;
            }}
        </style>
    </head>

    <body>

        <h1>TAKSH AI — Dataset Report</h1>

        <div class="card">
            <h2>Dataset</h2>
            <p>Filename: {file.filename}</p>
            <p>Rows: <span class="value">{rows}</span></p>
            <p>Columns: <span class="value">{columns}</span></p>
        </div>

        <div class="card">
            <h2>Data Quality</h2>
            <p>Missing Values: <span class="value">{missing_values}</span></p>
            <p>Duplicate Rows: <span class="value">{duplicates}</span></p>
        </div>

        <div class="card">
            <h2>Features</h2>
            <p>Numerical Features: {len(numerical_columns)}</p>
            <p>Categorical Features: {len(categorical_columns)}</p>
        </div>

        <div class="card">
            <h2>Numerical Columns</h2>
            <p>{", ".join(numerical_columns) if numerical_columns else "None"}</p>
        </div>

        <div class="card">
            <h2>Categorical Columns</h2>
            <p>{", ".join(categorical_columns) if categorical_columns else "None"}</p>
        </div>

    </body>
    </html>
    """

    report_path = os.path.join(
        REPORT_DIR,
        "taksh_ai_report.html"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    return HTMLResponse(
        content=html,
        status_code=200
    )
