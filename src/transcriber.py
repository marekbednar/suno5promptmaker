import whisper

def transcribe_audio(file_path: str, model_name: str = "base"):
    """
    Logic for OpenAI Whisper to get lyrics and timestamps.
    """
    # Load the model (this will download it if it's not already cached)
    model = whisper.load_model(model_name)
    
    # Transcribe the audio file
    result = model.transcribe(file_path, word_timestamps=True, verbose=False)
    
    # Extract segments and align keys with analyzer (start_time, end_time)
    lyrics_segments = []
    for segment in result["segments"]:
        lyrics_segments.append({
            "start_time": round(segment["start"], 2),
            "end_time": round(segment["end"], 2),
            "text": segment["text"].strip()
        })
        
    return lyrics_segments
