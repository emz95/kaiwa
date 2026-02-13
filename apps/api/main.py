import os
from pathlib import Path
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from routes.scenarios import router as scenarios_router
from routes.cards import router as cards_router
from routes.variants import router as variants_router

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI(title="Kaiwa API")

api_router = APIRouter(prefix="/api")

api_router.include_router(scenarios_router)
api_router.include_router(cards_router)
api_router.include_router(variants_router)

app.include_router(api_router)

@app.get("/health")
def health():
    return {"ok": True}
