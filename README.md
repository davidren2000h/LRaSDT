# AutoLyric Sync

AI-powered tool that recognizes lyrics from MP3 files and displays them in sync during playback.

## Features

- Select a local MP3 file and automatically recognize lyrics using AI (Whisper / stable-ts)
- Optional vocal separation (Demucs) for better recognition accuracy
- Play songs with synchronized lyric display
- Export lyrics to LRC, SRT, or JSON formats
- Load existing LRC/JSON lyric files

## Requirements

- Python 3.10+
- ffmpeg (required for audio processing and vocal separation)

### Install ffmpeg

- **Windows**: Download from https://ffmpeg.org/download.html and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## Setup

```bash
cd LRaSDT
pip install -r requirements.txt
```

Dependencies installed:
- `openai-whisper` — speech recognition model
- `stable-ts` — improved timestamp accuracy for Whisper
- `demucs` — vocal separation from background music
- `pygame-ce` — audio playback
- `pydub` — audio duration detection

## Usage

```bash
cd src
python app.py
```

### Workflow

1. Click **Select MP3 File** and choose a song
2. (Optional) Check **Separate vocals** for better accuracy
3. Select a Whisper model size (tiny/base/small/medium)
4. Click **Generate Lyrics** — wait for AI processing
5. Click **Play** to hear the song with synced lyrics
6. Use **Export LRC/SRT/JSON** to save the lyrics

### Load Existing Lyrics

Click **Load LRC** to import a `.lrc` or `.json` lyric file instead of generating new ones.

## Project Structure

```
src/
  app.py              — Tkinter GUI (main entry point)
  audio_processor.py  — Vocal separation (Demucs)
  transcriber.py      — Lyric recognition (stable-ts / Whisper)
  lyric_exporter.py   — Export/import LRC, SRT, JSON
  lyric_sync.py       — Match playback time to lyric line
  player.py           — MP3 playback (pygame-ce)
```

## Notes

- First-time lyric generation downloads the Whisper model (~140MB for base)
- Processing a 3-5 minute song takes 1-5 minutes depending on hardware and model size
- Vocal separation is optional but improves accuracy for songs with heavy background music
- Larger models (small/medium) are more accurate but slower
