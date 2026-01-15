from fastapi import FastAPI
from app.routes.predict import router as predict_router
from app.routes.alerts import router as alerts_router
from app.routes.stats import router as stats_router

app = FastAPI(
    title="Intelligent Network Intrusion Detection System",
    version="1.0"
)

app.include_router(predict_router)
app.include_router(alerts_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return {"status": "INIDS Backend Running"}