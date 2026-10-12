from fastapi import FastAPI

# =====================================================
# IMPORT ALL ROUTERS
# =====================================================

from backend.upload import router as upload_router
from backend.profile import router as profile_router
from backend.clean import router as clean_router
from backend.eda import router as eda_router
from backend.features import router as features_router
from backend.preprocessing import router as preprocessing_router
from backend.train import router as train_router
from backend.predict import router as predict_router
from backend.insights import router as insights_router
from backend.report import router as report_router


# =====================================================
# CREATE FASTAPI APPLICATION
# =====================================================

app = FastAPI(
    title="TAKSH AI",
    description="AI-Powered Data Analysis & AutoML Platform",
    version="1.0.0"
)


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Taksh AI",
        "status": "Backend is running",
        "version": "1.0.0"
    }


# =====================================================
# REGISTER ALL ROUTERS
# =====================================================

app.include_router(upload_router)

app.include_router(profile_router)

app.include_router(clean_router)

app.include_router(eda_router)

app.include_router(features_router)

app.include_router(preprocessing_router)

app.include_router(train_router)

app.include_router(predict_router)

app.include_router(insights_router)

app.include_router(report_router)