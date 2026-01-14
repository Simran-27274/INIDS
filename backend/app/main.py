from fastapi import FastAPI
from app.routes.predict import router as predict_router

app = FastAPI(
    title="Intelligent Network Intrusion Detection System",
    version="1.0"
)

# Include routes
app.include_router(predict_router)

@app.get("/")
def root():
    return {"message": "INIDS Backend is running"}