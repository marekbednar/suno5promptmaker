import yt_dlp
import os

def download_audio(url: str, output_path: str = "downloaded_audio.wav") -> str:
    """
    Downloads audio from a YouTube URL and saves it as a 16000Hz .wav file.
    
    Args:
        url (str): The YouTube URL to download from.
        output_path (str, optional): The desired output file path. Defaults to "downloaded_audio.wav".
        
    Returns:
        str: The absolute path to the downloaded .wav file.
    """
    # Ensure the output path ends with .wav
    if not output_path.endswith('.wav'):
        output_path += '.wav'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }
        ],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'outtmpl': output_path.rsplit('.wav', 1)[0],
        'quiet': True,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    return os.path.abspath(output_path)
