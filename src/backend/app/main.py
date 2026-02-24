from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.scan_routes import router as scan_router

app = FastAPI(
    title="Project Neev API - Term 1",
    description="Term 1: Scan + Compliance + Cost Estimation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan_router, prefix="/api/v1", tags=["Term 1 Analysis"])


@app.get("/")
def root():
    return {
        "message": "Project Neev Term 1 Backend is Live",
        "version": "1.0.0",
        "features": [
            "Computer Vision Plot Scanning",
            "Regulatory Compliance Checking",
            "Cost Estimation",
        ],
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
