from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .downloader import download_audio
from .gemini_agent import process_with_gemini

app = FastAPI(
    title="Suno Prompt Generator API", 
    description="The Brain for processing YouTube audio into Suno prompts using Gemini"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    youtube_url: str
    language: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to Suno Prompt Generator API. The Gemini Brain is online."}

@app.post("/generate")
def generate_prompt(request: GenerateRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise HTTPException(status_code=500, detail="Gemini API Key is missing. Please add it to your .env file.")
        
    temp_audio_path = "temp_gemini_audio.mp3"
    
    try:
        # 1. Download audio
        audio_path = download_audio(request.youtube_url, output_path=temp_audio_path)
        
        # 2. Let Gemini do everything!
        raw_output = process_with_gemini(audio_path, api_key, request.language)
        
        style_tags = ""
        lyrics_prompt = raw_output
        
        if "---STYLE TAGS---" in raw_output and "---LYRICS PROMPT---" in raw_output:
            parts = raw_output.split("---LYRICS PROMPT---")
            style_tags = parts[0].replace("---STYLE TAGS---", "").strip()
            lyrics_prompt = parts[1].strip()
        
        return {
            "status": "success",
            "style_tags": style_tags,
            "suno_prompt": lyrics_prompt
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup temporary audio file
        if os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except:
                pass
