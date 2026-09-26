from fastapi import APIRouter,UploadFile,File
import pandas as pd
import io

router = APIRouter()

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    content = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))

    else:
        return{
            "error": "Only CSV and XLSX files are supported"
        }

    return{
        "filename": file.filename,
        "rows": df.shape[0],
        "columns": df.shape[1]
    }