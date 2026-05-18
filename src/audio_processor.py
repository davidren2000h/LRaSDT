"""
audio_processor.py - MP3 conversion and vocal separation using Demucs.
"""

import os
import subprocess
import shutil


def check_ffmpeg():
    """Check if ffmpeg is installed and accessible."""
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError(
            "ffmpeg was not detected. Please install ffmpeg first.\n"
            "Download from: https://ffmpeg.org/download.html"
        )
    return True


def separate_vocals(mp3_path, output_dir=None):
    """
    Separate vocals from an MP3 file using Demucs.

    Args:
        mp3_path: path to the input MP3 file
        output_dir: directory to store separated tracks (default: same dir as input)

    Returns:
        str: path to the separated vocals.wav file
    """
    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"MP3 file not found: {mp3_path}")

    check_ffmpeg()

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(mp3_path), "separated")

    os.makedirs(output_dir, exist_ok=True)

    try:
        # Run demucs with the htdemucs model (default, good quality)
        result = subprocess.run(
            [
                "python", "-m", "demucs",
                "--two-stems", "vocals",
                "-o", output_dir,
                mp3_path
            ],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Vocal separation failed.\n"
                f"stderr: {result.stderr}\n"
                f"You may try recognizing the original audio directly."
            )
    except FileNotFoundError:
        raise ImportError(
            "Demucs is not installed. Install it with: pip install demucs"
        )

    # Demucs outputs to: output_dir/htdemucs/<song_name>/vocals.wav
    song_name = os.path.splitext(os.path.basename(mp3_path))[0]

    # Try common model output directories
    for model_name in ["htdemucs", "htdemucs_ft", "mdx_extra"]:
        vocals_path = os.path.join(output_dir, model_name, song_name, "vocals.wav")
        if os.path.exists(vocals_path):
            return vocals_path

    # Fallback: search for vocals.wav
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            if f == "vocals.wav":
                return os.path.join(root, f)

    raise FileNotFoundError(
        "Vocal separation completed but vocals.wav was not found. "
        "Check the output directory."
    )


def get_audio_duration(file_path):
    """Get duration of an audio file in seconds using pydub."""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(file_path)
        return len(audio) / 1000.0
    except Exception:
        return 0.0
