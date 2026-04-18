# Suno Prompt Generator

The **Suno Prompt Generator** acts as a "brain" to process a YouTube URL, analyze its audio properties (BPM, Key, Chords/Segments), transcribe its lyrics using OpenAI Whisper, and intelligently stitch them together to generate an optimized prompt for Suno AI.

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg**: Required by `librosa` and `openai-whisper` for audio processing.
   - **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via winget: `winget install ffmpeg` / choco: `choco install ffmpeg`
   - **macOS:** `brew install ffmpeg`
   - **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install ffmpeg`

## Installation

1. Clone or download the repository.
2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   > *Note:* If you intend to use GPU acceleration for Whisper, ensure you install the correct PyTorch version with CUDA support before running the script.

## Running the Application

This project consists of a FastAPI backend and a simple static HTML frontend.

### 1. Start the Backend (FastAPI)

Run the backend development server from the root of the project:

```bash
uvicorn src.main:app --reload
```

You should see an output indicating the server is running on `http://127.0.0.1:8000`. You can also visit `http://127.0.0.1:8000/docs` to view the interactive Swagger API documentation.

### 2. Launch the Frontend

Since the frontend is a standalone static HTML file and the backend has CORS enabled, you can simply double-click the `index.html` file to open it in your default web browser.

Alternatively, if you are using VS Code, you can use the **Live Server** extension to serve the `index.html`.

### 3. Generate a Prompt

1. Paste a valid YouTube URL into the input field on the `index.html` page.
2. Click **Process**.
3. Wait for the audio to be downloaded, analyzed, and transcribed. (This may take a minute depending on the length of the video and your computer's processing power).
4. Click **Copy to Clipboard** to copy the final generated prompt and paste it directly into Suno!

## Project Structure

- `src/main.py`: FastAPI server definitions and route handlers.
- `src/downloader.py`: Logic for downloading audio using `yt-dlp`.
- `src/analyzer.py`: Audio analysis logic (BPM, Key, Chords, Structure) using `allin1`.
- `src/transcriber.py`: Lyric transcription logic using `openai-whisper`.
- `src/prompt_generator.py`: Formatting logic to stitch audio segments and lyrics into the final Suno Prompt.
- `index.html`: The web-based User Interface.
- `requirements.txt`: Python dependencies.