from fastapi import FastAPI
from app.routes.predict import router as predict_router
from app.routes.alerts import router as alerts_router
from app.routes.stats import router as stats_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Intelligent Network Intrusion Detection System",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_router)
app.include_router(alerts_router)
app.include_router(stats_router)

@app.get("/")
def root():
    return {"status": "INIDS Backend Running"}