"""
transcriber.py - Lyric recognition using stable-ts / Whisper.
"""

import os


def transcribe(audio_path, model_size="base", use_stable_ts=True):
    """
    Transcribe an audio file and return timestamped lyric segments.

    Args:
        audio_path: path to the audio file (wav or mp3)
        model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        use_stable_ts: if True, use stable-ts; otherwise use raw whisper

    Returns:
        list of dicts: [{"start": float, "end": float, "text": str}, ...]
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    lyrics = []

    if use_stable_ts:
        lyrics = _transcribe_stable_ts(audio_path, model_size)
    else:
        lyrics = _transcribe_whisper(audio_path, model_size)

    return lyrics


def _transcribe_stable_ts(audio_path, model_size):
    """Transcribe using stable-ts for better timestamps."""
    try:
        import stable_whisper
    except ImportError:
        raise ImportError(
            "stable-ts is not installed. Install it with: pip install stable-ts"
        )

    model = stable_whisper.load_model(model_size)
    result = model.transcribe(audio_path)

    lyrics = []
    for segment in result.segments:
        lyrics.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })

    return lyrics


def _transcribe_whisper(audio_path, model_size):
    """Transcribe using raw openai-whisper."""
    try:
        import whisper
    except ImportError:
        raise ImportError(
            "openai-whisper is not installed. Install it with: pip install openai-whisper"
        )

    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)

    lyrics = []
    for segment in result["segments"]:
        lyrics.append({
            "start": round(segment["start"], 2),
            "end": round(segment["end"], 2),
            "text": segment["text"].strip()
        })

    return lyrics


def align_lyrics(audio_path, text_path, model_size="base"):
    """
    Align user-provided lyrics (TXT) with audio to generate timestamps.

    Args:
        audio_path: path to the audio file (mp3 or wav)
        text_path: path to a .txt file with lyrics (one line per lyric segment)
        model_size: Whisper model size

    Returns:
        list of dicts: [{"start": float, "end": float, "text": str}, ...]
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not os.path.exists(text_path):
        raise FileNotFoundError(f"Lyrics text file not found: {text_path}")

    with open(text_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    # Filter out empty lines
    lyric_lines = [line.strip() for line in raw_lines if line.strip()]
    if not lyric_lines:
        raise ValueError("The lyrics text file is empty.")

    lyric_text = "\n".join(lyric_lines)

    try:
        import stable_whisper
    except ImportError:
        raise ImportError(
            "stable-ts is not installed. Install it with: pip install stable-ts"
        )

    model = stable_whisper.load_model(model_size)
    result = model.align(audio_path, lyric_text)

    lyrics = []
    for segment in result.segments:
        lyrics.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })

    return lyrics
