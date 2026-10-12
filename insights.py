from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter()


@router.post("/insights")
async def generate_insights(file: UploadFile = File(...)):

    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))

    else:
        return {
            "error": "Only CSV and XLSX files are supported"
        }

    rows = df.shape[0]
    columns = df.shape[1]

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    insights = []

    insights.append(
        f"The dataset contains {rows} rows and {columns} columns."
    )

    missing_values = df.isnull().sum()
    missing_columns = (
        missing_values[missing_values > 0].to_dict()
    )

    if missing_columns:
        insights.append(
            f"Missing values were found in {len(missing_columns)} column(s)."
        )
    else:
        insights.append(
            "No missing values were found."
        )

    duplicates = int(df.duplicated().sum())

    if duplicates > 0:
        insights.append(
            f"The dataset contains {duplicates} duplicate row(s)."
        )
    else:
        insights.append(
            "No duplicate rows were detected."
        )

    numerical_insights = []

    for column in numerical_columns:

        numerical_insights.append({
            "column": column,
            "mean": round(float(df[column].mean()), 2),
            "minimum": round(float(df[column].min()), 2),
            "maximum": round(float(df[column].max()), 2)
        })

    categorical_insights = []

    for column in categorical_columns:

        unique_count = int(
            df[column].nunique()
        )

        most_common = (
            df[column]
            .value_counts()
            .head(1)
        )

        if not most_common.empty:

            common_value = str(
                most_common.index[0]
            )

            common_count = int(
                most_common.iloc[0]
            )

        else:

            common_value = None
            common_count = 0

        categorical_insights.append({
            "column": column,
            "unique_values": unique_count,
            "most_common_value": common_value,
            "frequency": common_count
        })

    correlations = []

    if len(numerical_columns) >= 2:

        correlation_matrix = (
            df[numerical_columns]
            .corr()
        )

        for i in range(len(numerical_columns)):

            for j in range(
                i + 1,
                len(numerical_columns)
            ):

                column1 = numerical_columns[i]
                column2 = numerical_columns[j]

                correlation = (
                    correlation_matrix
                    .loc[column1, column2]
                )

                if pd.notna(correlation):

                    correlations.append({
                        "feature_1": column1,
                        "feature_2": column2,
                        "correlation": round(
                            float(correlation),
                            3
                        )
                    })

    return {
        "filename": file.filename,

        "dataset": {
            "rows": rows,
            "columns": columns,
            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns
        },

        "insights": insights,

        "missing_values": missing_columns,

        "duplicates": duplicates,

        "numerical_analysis": numerical_insights,

        "categorical_analysis": categorical_insights,

        "correlations": correlations,

        "status": "Insights generated successfully"
    }
