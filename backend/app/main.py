from fastapi import FastAPI
from app.routes import api

app = FastAPI(
    title="Intelligent Network Intrusion Detection System",
    version="1.0"
)

# Include routes
app.include_router(api.router)

@app.get("/")
def root():
    return {"message": "INIDS Backend is running"}