from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import run_pipeline
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Eklavya AI Pipeline", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    grade: int
    topic: str

@app.get("/")
def root():
    return {"status": "running", "message": "Eklavya AI Pipeline API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate(req: GenerateRequest):
    print(f"[API] Received request: grade={req.grade}, topic={req.topic}")
    if not (1 <= req.grade <= 12):
        raise HTTPException(status_code=400, detail="Grade must be between 1 and 12")
    if not req.topic.strip() or len(req.topic.strip()) < 2:
        raise HTTPException(status_code=400, detail="Topic too short")
    try:
        result = run_pipeline(grade=req.grade, topic=req.topic.strip())
        data = result.model_dump()
        print(f"[API] Returning result, keys: {list(data.keys())}")
        return data
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[API] Error: {e}\n{tb}")
        raise HTTPException(status_code=500, detail=str(e))