# from fastapi import FastAPI
# from pydantic import BaseModel
# import asyncio
# from src.pipelines.orchestrator import run_pipeline

# app = FastAPI(title="Multi-Health Agent API", version="1.0")

# class RunRequest(BaseModel):
#     max_items: int = 5

# @app.post("/predict")
# async def predict(req: RunRequest):
#     results = await run_pipeline(max_items=req.max_items)
#     return {"count": len(results), "results": results}

# @app.get("/health")
# async def health():
#     return {"status": "ok"}
from fastapi import FastAPI
from pydantic import BaseModel
import os
os.environ["CREWAI_STORAGE_PATH"] = "/tmp/crewai_data"
from src.pipelines.orchestrator import kickoff_crew




app = FastAPI()

class RunRequest(BaseModel):
    max_items: int = 5

import json

@app.post("/predict")
async def predict(req: RunRequest):
    crew_output = await kickoff_crew()

    # Convert CrewOutput string representation to actual Python list
    try:
        results = json.loads(str(crew_output))
    except Exception:
        results = []

    return {"count": len(results), "results": results}


@app.get("/health")
async def health():
    return {"status": "ok"}
