from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from .downloader import download_audio
from .analyzer import analyze_audio
from .transcriber import transcribe_audio
from .prompt_generator import generate_suno_prompt

app = FastAPI(
    title="Suno Prompt Generator API", 
    description="The Brain for processing YouTube audio into Suno prompts"
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
    genre: Optional[str] = "pop"

@app.get("/")
def read_root():
    return {"message": "Welcome to Suno Prompt Generator API. The Brain is online."}

@app.post("/generate")
def generate_prompt(request: GenerateRequest):
    temp_audio_path = "temp_audio.mp3"
    
    try:
        # 1. Download audio
        audio_path = download_audio(request.youtube_url, output_path=temp_audio_path)
        
        # 2. Analyze audio (BPM, Key, Chords)
        analysis_result = analyze_audio(audio_path)
        
        # 3. Transcribe audio (Lyrics)
        transcription_result = transcribe_audio(audio_path)
        
        # Combine lyrics for the prompt generator
        full_lyrics = "\n".join([seg["text"] for seg in transcription_result])
        
        # 4. Generate Prompt
        prompt = generate_suno_prompt(
            bpm=analysis_result.get("bpm", 120.0),
            key=analysis_result.get("key", "Unknown"),
            chords=analysis_result.get("segments", []),
            raw_chords=analysis_result.get("raw_chords", []),
            lyrics=transcription_result
        )
        
        return {
            "status": "success",
            "analysis": analysis_result,
            "transcription": transcription_result,
            "transcription_preview": full_lyrics[:100] + "...",
            "suno_prompt": prompt
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup temporary audio file if it exists
        if os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except:
                pass
