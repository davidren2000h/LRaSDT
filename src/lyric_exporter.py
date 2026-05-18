"""
lyric_exporter.py - Export recognized lyrics to LRC, SRT, and JSON formats.
"""

import json
import os


def format_lrc_time(seconds):
    """Convert seconds to LRC timestamp format [MM:SS.CC]."""
    if seconds < 0:
        seconds = 0
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"[{minutes:02d}:{secs:05.2f}]"


def format_srt_time(seconds):
    """Convert seconds to SRT timestamp format HH:MM:SS,mmm."""
    if seconds < 0:
        seconds = 0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    millis = int(round((secs - int(secs)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{int(secs):02d},{millis:03d}"


def export_lrc(lyrics, output_path):
    """
    Export lyrics to LRC format.

    Args:
        lyrics: list of dicts with 'start', 'end', 'text' keys
        output_path: path to save the .lrc file
    """
    if not lyrics:
        raise ValueError("Lyrics list is empty.")

    lines = []
    for seg in lyrics:
        timestamp = format_lrc_time(seg["start"])
        lines.append(f"{timestamp}{seg['text']}")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return output_path


def export_srt(lyrics, output_path):
    """
    Export lyrics to SRT subtitle format.

    Args:
        lyrics: list of dicts with 'start', 'end', 'text' keys
        output_path: path to save the .srt file
    """
    if not lyrics:
        raise ValueError("Lyrics list is empty.")

    lines = []
    for i, seg in enumerate(lyrics, 1):
        start_ts = format_srt_time(seg["start"])
        end_ts = format_srt_time(seg["end"])
        lines.append(f"{i}")
        lines.append(f"{start_ts} --> {end_ts}")
        lines.append(seg["text"])
        lines.append("")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return output_path


def export_json(lyrics, song_file, output_path):
    """
    Export lyrics to JSON format.

    Args:
        lyrics: list of dicts with 'start', 'end', 'text' keys
        song_file: original song file name
        output_path: path to save the .json file
    """
    if not lyrics:
        raise ValueError("Lyrics list is empty.")

    data = {
        "song_file": os.path.basename(song_file),
        "lyrics": lyrics
    }

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return output_path


def load_lrc(lrc_path):
    """
    Load lyrics from an LRC file.

    Returns:
        list of dicts with 'start', 'text' keys
    """
    lyrics = []
    with open(lrc_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parse [MM:SS.CC]text
            if line.startswith("["):
                bracket_end = line.index("]")
                timestamp_str = line[1:bracket_end]
                text = line[bracket_end + 1:]
                parts = timestamp_str.split(":")
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = float(parts[1])
                    start = minutes * 60 + seconds
                    lyrics.append({"start": start, "text": text})

    # Compute end times from next segment's start
    for i in range(len(lyrics) - 1):
        lyrics[i]["end"] = lyrics[i + 1]["start"]
    if lyrics:
        lyrics[-1]["end"] = lyrics[-1]["start"] + 5.0  # default duration for last line

    return lyrics


def load_json(json_path):
    """
    Load lyrics from a JSON file.

    Returns:
        list of dicts with 'start', 'end', 'text' keys
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("lyrics", [])
