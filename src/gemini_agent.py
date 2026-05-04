from google import genai
from google.genai import types
import time

def process_with_gemini(audio_path: str, api_key: str, language: str = None) -> str:
    """
    Uploads the audio to Gemini and asks it to generate a complete Suno prompt.
    """
    client = genai.Client(api_key=api_key)
    
    print("Uploading audio to Gemini...")
    # Upload the file to Gemini's File API
    audio_file = client.files.upload(file=audio_path)
    
    # Wait for the file to be processed (audio usually needs a few seconds)
    while True:
        file_info = client.files.get(name=audio_file.name)
        if file_info.state.name == "ACTIVE":
            break
        elif file_info.state.name == "FAILED":
            raise Exception("Gemini failed to process the audio file.")
        print("Waiting for Gemini to process audio...")
        time.sleep(2)
        
    print("Audio ready. Generating prompt...")
    
    lang_instruction = f"The song's language is likely {language}. Please transcribe any lyrics in {language}." if language else "Auto-detect the language of the lyrics."
    
    prompt = f"""
You are an expert music theorist, transcriber, audio engineer, and prompt engineer for Suno AI v5.
I have uploaded an audio file of a song. I need you to listen to the ENTIRE track from beginning to end before generating the output. Then, generate a highly optimized Suno AI v5 prompt with extreme musical precision.

Please analyze the audio deeply and provide the output in EXACTLY this format with the exact delimiters:

---STYLE TAGS---
Provide a highly detailed, comma-separated list of genres, sub-genres, moods, vocal timbres, production styles, and key instruments. 
CRITICAL FOR STYLE: You must perform a deep sonic audit of the ENTIRE song from start to finish. Progressive and complex songs evolve, so do not base this only on the beginning. Capture the full range of genres, dynamic shifts, and instruments used throughout the whole track. Do not just say "guitar" or "drums". Specify the exact tones and types of instruments you hear (e.g., "fuzz-pedal electric guitar", "Hammond B3 organ", "slap bass", "analog synth arpeggiator", "double-kick acoustic drums", "808 sub-bass"). Identify the specific era/vibe (e.g., "70s progressive rock", "modern djent"). You have up to 1000 characters. Do not wrap this text in any brackets or symbols. Example: Slovak 70s progressive rock, evolving dynamics, 5/4 meter, heavy fuzz-pedal rhythm guitar, gritty male tenor vocals, virtuosic Moog synth solos, Hammond B3 organ, double-kick acoustic drums, complex jazz-fusion harmony

---LYRICS PROMPT---
[Tempo: estimated BPM]
[Key: estimated musical key]
[Time signature: estimated time signature, e.g., 4/4, 3/4, 5/4, 7/8]
(Arrangement: 1 sentence describing the overall mood/arrangement)

<Then, map out the structure of the song using tags like [Intro], [Verse], [Chorus], etc. 
CRITICAL INSTRUCTION FOR META-TAGS: All non-lyric text (like tempo, key, time signature, arrangement, and section headers) MUST be enclosed in brackets [] or parentheses (). Never leave instruction text bare, or Suno will try to sing it.

CRITICAL INSTRUCTION FOR KEY CHANGES (MODULATIONS): Suno often ignores inline chords. If the song changes key (modulates) at any point, you MUST explicitly declare the new key by adding a `[Key: new key]` tag immediately before the section header where the key change occurs. Example:
[Key: F Major]
[Chorus: Sweeping orchestral strings, operatic female soprano]

CRITICAL INSTRUCTION FOR INSTRUMENTATION & VOCALS:
For every section header, you must include a brief description of the specific instruments playing and the vocal style/timbre. Use the deep sonic audit you performed earlier.
Place this inside the bracket next to the section name.
Example: `[Verse: Gritty male tenor, fuzz electric guitar, Hammond B3 organ, driving slap bass]`

CRITICAL INSTRUCTION FOR CHORDS: You must inline the musical chords exactly where they occur within the lyrics. 
- You MUST analyze the harmony with extreme precision. Do not just use basic triads. You must identify the exact voicings, extensions, suspensions, and inversions.
- Place the chord in brackets right before the word where the chord change happens.
- If a chord change happens IN THE MIDDLE of a word, place the chord exactly between the syllables with NO spaces. Example: `Začí[Fm7]na`.

If a section is purely instrumental, just list the progression.
CRITICAL INSTRUCTION FOR INSTRUMENTALS: Do NOT write repeating chords over and over like `[Fm] [Fm]`. Instead, use a multiplier format like `[Fm - 4x]`.

{lang_instruction}
Make sure to accurately capture the structural flow, the deep instrumentation, the time signature, modulations, and transcribe the lyrics perfectly. Do not include conversational text, just the requested format.
"""

    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=[audio_file, prompt],
        config=types.GenerateContentConfig(temperature=0.0)
    )
    
    # Cleanup the file from Gemini's servers
    try:
        client.files.delete(name=audio_file.name)
    except:
        pass
        
    return response.text
