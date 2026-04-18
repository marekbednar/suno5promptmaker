# Suno Prompt Generator v5

The **Suno Prompt Generator** acts as a brilliant AI "music brain" to process a YouTube URL, natively analyze its audio properties (BPM, Key, Time Signatures, Chords, Voicings, Instrumentals), perfectly transcribe its lyrics, and intelligently format everything into a highly-optimized prompt tailored specifically for **Suno AI v5**.

It completely bypasses heavy local machine learning models by sending the raw audio directly to the **Gemini 3.1 Pro API**, which uses its massive multimodal reasoning to perform expert-level music theory analysis and lyric alignment.

## Prerequisites

1. **Python 3.10** (Highly recommended for maximum compatibility).
2. **FFmpeg**: Required by `yt-dlp` to download and process the YouTube audio.
   - **Windows:** Install via winget: `winget install ffmpeg` (Restart your terminal/VS Code afterwards!)
   - **macOS:** `brew install ffmpeg`
   - **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg`
3. **Gemini API Key**: You must have a Google Gemini API Key with access to the 3.1 Pro model. You can get one from Google AI Studio.

## Installation

1. Clone or download the repository.
2. Open your terminal in the project directory.
3. Create a clean virtual environment and activate it:
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. Install the lightweight dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration (API Key)

For security, your Gemini API Key is stored in a hidden `.env` file.

1. In the root directory of the project, create a new file named `.env`
2. Add your API key to the file like this:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   *(Note: Do not put quotes around the key, just paste the raw string).*

## Running the Application

This project consists of a FastAPI backend and a simple static HTML frontend.

### 1. Start the Backend Server

Make sure your virtual environment is activated `(venv)`, then run:

```bash
uvicorn src.main:app --reload
```

You should see an output indicating the server is running on `http://127.0.0.1:8000`.

### 2. Launch the Frontend

Since the frontend is a standalone static HTML file and the backend has CORS enabled, you can simply **double-click the `index.html` file** to open it in your web browser. 

*(Alternatively, if you are using VS Code, you can use the **Live Server** extension to serve the `index.html` file).*

### 3. Generate a Prompt

1. Paste a valid YouTube URL into the input field on the web page.
2. (Optional) Select a target language from the dropdown to force Gemini to listen for specific lyrics.
3. Click **Process**.
4. The backend will download the audio and send it to Gemini. Please wait about 30-60 seconds for the deep musical analysis to complete.
5. You will be given two distinct outputs:
   - **Style of Music Box:** Up to 1000 characters of highly detailed genre, instrument, and production tags to paste into Suno's "Style" box.
   - **Lyrics / Structure Prompt:** The massive, perfectly formatted lyrics box featuring exact time signatures, extreme chord precision (inversions, extensions) mapped perfectly to the exact syllables of the transcribed lyrics. 
6. Click **Copy** on both boxes and paste them directly into Suno!

## Project Structure

- `src/main.py`: FastAPI server definitions and route handlers.
- `src/downloader.py`: Logic for downloading audio using `yt-dlp`.
- `src/gemini_agent.py`: The core intelligence. Uploads audio to Gemini, enforces strict musical theory prompts, and parses the output.
- `index.html`: The web-based User Interface.
- `requirements.txt`: Python dependencies (`fastapi`, `uvicorn`, `yt-dlp`, `google-genai`, `python-dotenv`, `pydantic`).
- `.env`: (You create this) Stores your secret API key.
