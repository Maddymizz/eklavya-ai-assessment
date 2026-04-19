from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import run_pipeline, fallback_data   # <-- import fallback_data
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Eklavya AI Content Pipeline", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    grade: int
    topic: str

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}

@app.post("/generate")
def generate(req: GenerateRequest):
    if not (1 <= req.grade <= 12):
        raise HTTPException(status_code=400, detail="Grade must be between 1 and 12")
    if not req.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    if len(req.topic.strip()) < 3:
        raise HTTPException(status_code=400, detail="Topic too short")
    try:
        # TEMPORARY FALLBACK MODE
        return fallback_data(req.topic.strip())
        
        # If you want to revert later, just comment the above line
        # and uncomment the pipeline call below:
        # result = run_pipeline(grade=req.grade, topic=req.topic.strip())
        # return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
