from fastapi import APIRouter,UploadFile,File
import pandas as pd
import io

router = APIRouter()
@router.post("/upload")
async def profile_dataset(file:UploadFile = File(...)):
    contents = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))
    else:
        return{
            "error": "Only CSV and XLSX files are supported"
        }
    numerical_columns = df.select_dtypes(
        include = ["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include = ["object","category"]
    ).columns.tolist()


    missing_values  = df.isnull().sum().to_dict()

    return{
        "filename": file.filename,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "data_types": df.dtype.astype(str).todict(),
        "missing_values" : missing_values,
        "duplicate_rows":int(df.duplicated().sum()),
        "numerical_columns": numerical_columns,
    }