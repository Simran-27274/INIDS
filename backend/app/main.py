from fastapi import FastAPI

app = FastAPI(
    title="Intelligent Network Intrusion Detection System",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "INIDS Backend is running"}