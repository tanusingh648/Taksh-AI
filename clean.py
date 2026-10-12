from fastapi import APIRouter, File, UploadFile
import pandas as pd
import io

router = APIRouter()
@router.post("/clean")
async def clean_dataset(file: UploadFile= File(...)):
    contents = await file.read()
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))

    else:
        return{
            "Only CSV and XLSX files are supported"
        }
    original_rows = len(df)
    missing_before = int(df.isnull().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    df = df.drop_duplicates()
    for column in df.columns:
        if df[column].isnull().sum()>0:
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = df[column].fillna(
                    df[column].median()

                )
            else :
                df[column] = df[column].fillna(
                    df[column].mode()[0]
                )

    missing_after = int(df.isnull().sum().sum())
    duplicates_after = int(df.duplicated().sum())

    return{
        "filename": file.filename,
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "missing_values_before": missing_before,
        "missing_values_after": missing_after,
        "duplicates_before": duplicates_before,
        "duplicates_after": duplicates_after,
        "status" : "Dataset Cleaned Sucessfully"
         

    }
    
    
    

     