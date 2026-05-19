Below is an English PRD version your son can directly use with AI coding tools like Cursor, Codex, Claude Code, or GitHub Copilot.

---

# PRD: AI-Powered Lyric Recognition and Synchronized Display Tool

## 1. Product Name

**AutoLyric Sync**

A Python-based application that takes a local MP3 song file, automatically recognizes the lyrics, generates timestamped lyrics, and displays them in sync while the song is playing.

---

## 2. Product Goal

The user selects a local MP3 file. The application automatically performs the following pipeline:

```text
Load MP3
→ Separate vocals from background music
→ Recognize lyrics using AI speech recognition
→ Generate timestamped lyrics
→ Play the song
→ Display lyrics in sync with playback
```

The MVP goal is to support **line-level lyric synchronization**, similar to subtitles or LRC lyrics.

A future version may support **word-level highlighting**, similar to karaoke lyrics.

---

## 3. Target Users

Primary users:

1. People who want to automatically generate lyrics from songs.
2. Students learning Python, AI, audio processing, and GUI development.
3. Music users who want to create timestamped lyric files from MP3 files.

---

## 4. Core Use Cases

### Use Case 1: Automatically Recognize Lyrics from a Song

The user selects an MP3 file and clicks “Generate Lyrics.”
The application extracts the vocals and uses an AI model to recognize the lyrics.

### Use Case 2: Play Music with Synchronized Lyrics

The user plays the MP3 file.
The application displays the current lyric line based on the playback time.

### Use Case 3: Export Lyrics

The user can export recognized lyrics into:

```text
.lrc
.srt
.json
```

`.lrc` can be used by music players.
`.srt` can be used as subtitles.
`.json` can be used for further processing inside the application.

---

## 5. MVP Scope

The first version should focus on the minimum working product.

### MVP Must Have

1. The user can select a local MP3 file.
2. The application can recognize lyrics using an AI model.
3. The application can generate timestamped lyrics.
4. The application can play the MP3 file.
5. The application can display the current lyric line during playback.
6. The application can export an LRC file.

### MVP Does Not Need

1. Word-level karaoke highlighting.
2. Perfect lyric recognition accuracy.
3. Batch processing.
4. Support for online music platforms.
5. Mobile app support.
6. Complex or highly polished UI.

---

## 6. Functional Requirements

## 6.1 File Import

### Description

The user can select a local MP3 file.

### Input

```text
Local .mp3 file
```

### Output

```text
File path
Song name
Audio duration
```

### Acceptance Criteria

* The user can select an MP3 file using a file picker.
* The application correctly displays the selected file name.
* If the selected file is not an MP3 file, the application shows an error message.

---

## 6.2 Vocal Separation

### Description

Songs contain background music, which can reduce speech recognition accuracy.
The application should separate the vocal track before running speech recognition.

Recommended tool:

```text
Demucs
```

### Input

```text
Original MP3 file
```

### Output

```text
vocals.wav
```

### Acceptance Criteria

* The application can call Demucs from Python.
* The application generates a separate vocal audio file.
* If vocal separation fails, the application shows a clear error message.

### Note

For the earliest prototype, this step may be skipped and the original MP3 can be sent directly to the speech recognition model.

However, the formal MVP should include vocal separation.

---

## 6.3 Lyric Recognition

### Description

The application uses an AI speech recognition model to transcribe the vocals.

Recommended options:

```text
Whisper
stable-ts
WhisperX
```

Recommended for the first version:

```text
stable-ts
```

Reason: stable-ts is easier to use than WhisperX and usually produces better timestamps than raw Whisper.

### Input

```text
vocals.wav
```

### Output

```json
[
  {
    "start": 12.3,
    "end": 16.8,
    "text": "When you were here before"
  },
  {
    "start": 17.1,
    "end": 21.5,
    "text": "Couldn't look you in the eye"
  }
]
```

### Acceptance Criteria

* The application can recognize lyric text.
* Each lyric line has a start time.
* Each lyric line has an end time.
* The result can be saved as JSON.

---

## 6.4 Lyric File Generation

### Description

The application converts recognized lyrics into LRC format.

### LRC Example

```text
[00:12.30]When you were here before
[00:17.10]Couldn't look you in the eye
[00:22.50]You're just like an angel
```

### Input

```json
Lyric JSON data
```

### Output

```text
lyrics.lrc
```

### Acceptance Criteria

* The application can generate a `.lrc` file.
* The timestamp format is correct.
* The lyric order is correct.
* The generated file can be loaded again by the application.

---

## 6.5 Music Playback

### Description

The application can play the selected MP3 file.

Recommended library:

```text
pygame
```

Alternative:

```text
python-vlc
```

### Basic Features

1. Play
2. Pause
3. Resume
4. Stop
5. Display current playback time

### Acceptance Criteria

* When the user clicks Play, the song starts playing.
* When the user clicks Pause, the song pauses.
* The application can get the current playback time.
* When playback ends, the application stops automatically.

---

## 6.6 Synchronized Lyric Display

### Description

The application displays the correct lyric line based on the current playback time.

### Sync Logic

If the current playback time is:

```python
current_time = 18.2
```

And the lyric data is:

```json
[
  {"start": 12.3, "end": 16.8, "text": "When you were here before"},
  {"start": 17.1, "end": 21.5, "text": "Couldn't look you in the eye"}
]
```

The application should display:

```text
Couldn't look you in the eye
```

### UI Display

The MVP can display:

```text
Previous line
Current line, highlighted
Next line
```

Example:

```text
When you were here before

> Couldn't look you in the eye

You're just like an angel
```

### Acceptance Criteria

* Lyrics automatically update during playback.
* The current lyric line is visually clear.
* When playback pauses, lyric updates pause as well.
* When playback resumes, lyric updates continue.

---

## 7. Non-Functional Requirements

## 7.1 Performance Requirements

The first version does not need real-time recognition.

The expected workflow is:

```text
Analyze the full song first
Generate lyrics
Then play the song with synchronized lyrics
```

Target performance:

```text
For a 3-5 minute song, processing should finish within 1-5 minutes.
```

Actual processing time depends on hardware and AI model size.

---

## 7.2 Recognition Accuracy Requirements

The MVP does not require perfect lyric accuracy.

Target expectations:

```text
Regular English pop songs: recognize most lyrics correctly
Regular Chinese songs: recognize main lyrics, with some errors allowed
Rap, metal, heavy reverb, or noisy songs: lower accuracy is acceptable
```

---

## 7.3 Usability Requirements

The user should not need to understand command-line tools to use the final MVP.

A simple GUI is preferred.

Recommended UI framework for the first version:

```text
Tkinter
```

For a more modern interface:

```text
Streamlit
```

Or:

```text
Flask + HTML/JavaScript
```

---

## 7.4 Local Runtime Requirements

The first version should run locally.

Recommended environment:

```text
Python 3.10+
ffmpeg
Demucs
stable-ts or Whisper
pygame
```

---

## 8. Technical Design

## 8.1 Recommended Tech Stack

### Main Programming Language

```text
Python
```

### Audio Conversion

```text
ffmpeg
```

### Vocal Separation

```text
Demucs
```

### Lyric Recognition

```text
stable-ts / Whisper
```

### Music Playback

```text
pygame
```

### UI

First version:

```text
Tkinter
```

More polished version:

```text
Streamlit
```

Or:

```text
Flask + Web UI
```

---

## 8.2 System Architecture

```text
User Interface
      |
      v
MP3 File Selector
      |
      v
Audio Processor
      |
      v
Vocal Separation
      |
      v
Speech Recognition
      |
      v
Lyric Timestamp Generator
      |
      v
LRC / JSON Exporter
      |
      v
Music Player + Lyric Sync Display
```

---

## 9. Data Structure Design

## 9.1 Lyric Segment Object

```python
{
    "start": 12.30,
    "end": 16.80,
    "text": "When you were here before"
}
```

## 9.2 Full Lyric Object

```python
{
    "song_file": "song.mp3",
    "lyrics": [
        {
            "start": 12.30,
            "end": 16.80,
            "text": "When you were here before"
        },
        {
            "start": 17.10,
            "end": 21.50,
            "text": "Couldn't look you in the eye"
        }
    ]
}
```

---

## 10. UI Design

## 10.1 Main Window

The main window should include:

```text
[Select MP3 File]

File name: song.mp3

[Generate Lyrics]

Status: Separating vocals...
Status: Recognizing lyrics...
Status: Lyrics generated successfully

[Play] [Pause] [Stop]

Current Time: 00:18 / 03:45

Previous lyric line
Current lyric line
Next lyric line

[Export LRC]
[Export SRT]
[Export JSON]
```

---

## 11. User Flow

### Full Flow

```text
1. User opens the application
2. User clicks “Select MP3”
3. User selects a local song file
4. User clicks “Generate Lyrics”
5. Application separates vocals
6. Application recognizes lyrics
7. Application generates timestamped lyrics
8. User clicks “Play”
9. Application plays the song
10. Lyrics are displayed in sync with playback
11. User can export the LRC file
```

---

## 12. Error Handling

### 12.1 Invalid File Format

If the user selects a non-MP3 file:

```text
Error: Please select an MP3 file.
```

### 12.2 ffmpeg Not Installed

```text
Error: ffmpeg was not detected. Please install ffmpeg first.
```

### 12.3 Vocal Separation Failed

```text
Error: Vocal separation failed. You may try recognizing the original audio directly.
```

### 12.4 AI Recognition Failed

```text
Error: Lyric recognition failed. Please check whether the audio file is valid.
```

### 12.5 Playback Failed

```text
Error: Unable to play this MP3 file.
```

---

## 13. Development Milestones

## Phase 1: Command-Line Prototype

Goal: Validate the core pipeline without building a UI.

Tasks:

```text
1. Read an MP3 file path
2. Call Demucs to separate vocals
3. Call stable-ts to recognize lyrics
4. Generate JSON
5. Generate LRC
```

Completion Criteria:

```text
Input: song.mp3
Output: song.lrc
```

---

## Phase 2: Basic Player

Goal: Implement playback and lyric synchronization.

Tasks:

```text
1. Use pygame to play MP3
2. Get current playback time
3. Read an LRC file
4. Display the current lyric line based on playback time
```

Completion Criteria:

```text
When the song plays, the terminal or window displays the current lyric line in sync.
```

---

## Phase 3: Simple GUI

Goal: Build a demo-ready application.

Tasks:

```text
1. Add a file selection button
2. Add a generate lyrics button
3. Add play / pause / stop buttons
4. Add a lyric display area
5. Add export buttons
```

Completion Criteria:

```text
The user can complete the full workflow without using the command line.
```

---

## Phase 4: Experience Improvements

Goal: Improve usability and quality.

Optional tasks:

```text
1. Show processing progress
2. Support manual lyric editing
3. Support global time offset adjustment
4. Support word-level highlighting
5. Support language selection
6. Support saving project files
```

---

## 14. AI-Assisted Development Task Breakdown

This project is suitable for AI-assisted coding.
The developer can ask AI to implement each module separately.

---

### Prompt 1: Create Project Structure

```text
Please create a Python project structure for an MP3 lyric recognition and synchronized display application.

The project should include the following modules:

1. audio_processor.py: handles MP3 conversion and vocal separation
2. transcriber.py: calls Whisper or stable-ts to recognize lyrics
3. lyric_exporter.py: exports LRC, SRT, and JSON files
4. player.py: plays MP3 files and returns current playback time
5. lyric_sync.py: matches current playback time to the current lyric line
6. app.py: main application entry point

Please generate the project directory structure and starter code for each file.
```

---

### Prompt 2: Implement LRC Export

```text
Please implement lyric_exporter.py.

Input data format:

[
    {"start": 12.3, "end": 16.8, "text": "When you were here before"},
    {"start": 17.1, "end": 21.5, "text": "Couldn't look you in the eye"}
]

Expected LRC output:

[00:12.30]When you were here before
[00:17.10]Couldn't look you in the eye

Requirements:
1. Correctly format minutes, seconds, and centiseconds
2. Support exporting to a specified file path
3. Include basic error handling
4. Provide simple test code
```

---

### Prompt 3: Implement Lyric Sync Logic

```text
Please implement lyric_sync.py.

Function:
Given current_time and a list of lyric segments, return the lyric line that should currently be displayed.

Lyric format:

[
    {"start": 12.3, "end": 16.8, "text": "line 1"},
    {"start": 17.1, "end": 21.5, "text": "line 2"}
]

Requirements:
1. If current_time is between a lyric's start and end time, return that lyric
2. If current_time is before the first lyric, return an empty string
3. If current_time is after the last lyric, return the last lyric
4. The code should be simple, clear, and testable
```

---

### Prompt 4: Implement Whisper Transcription Module

```text
Please implement transcriber.py.

Function:
Use stable-ts or openai-whisper to transcribe an audio file and return timestamped lyric lines.

Return format:

[
    {"start": 12.3, "end": 16.8, "text": "lyrics line"}
]

Requirements:
1. Support passing in an audio file path
2. Support selecting model size, such as base, small, or medium
3. Raise a clear error if transcription fails
4. Do not hardcode file paths inside the module
```

---

### Prompt 5: Implement Music Player

```text
Please implement player.py.

Function:
Use pygame to play MP3 files.

Requirements:
1. Support load(file_path)
2. Support play()
3. Support pause()
4. Support resume()
5. Support stop()
6. Support get_current_time()
7. Return current playback time in seconds
8. The code should be callable from a GUI
```

---

### Prompt 6: Implement Simple GUI

```text
Please implement app.py using Tkinter.

Features:
1. Select MP3 file
2. Generate lyrics
3. Play music
4. Pause music
5. Stop music
6. Display current lyric line
7. Export LRC file

Requirements:
1. Keep the UI simple and clear
2. Do not block the main UI thread
3. Show status text during processing
4. Keep the code structure clean for future expansion
```

---

## 15. Risks and Challenges

## 15.1 Lyric Recognition May Be Inaccurate

Songs are harder to transcribe than normal speech because of:

```text
Background music
Reverb
Harmony vocals
Unclear pronunciation
Fast rap sections
Repeated lyrics
Mixed languages
```

Possible solutions:

```text
Separate vocals first
Allow users to manually edit lyrics
Support importing official lyrics and only aligning timestamps
```

---

## 15.2 Timestamps May Be Inaccurate

Raw speech recognition timestamps may drift or be imprecise.

Possible solutions:

```text
Use stable-ts or WhisperX
Support manual global time offset adjustment
Support per-line timestamp editing
```

---

## 15.3 Local Environment Setup May Be Difficult

The project may require several dependencies:

```text
Python
ffmpeg
Demucs
Whisper
PyTorch
```

This may be challenging for beginners.

Possible solutions:

```text
Start with a command-line prototype
Write a clear setup guide
Consider packaging the app into an executable later
```

---

## 16. Future Enhancements

### 16.1 Word-Level Highlighting

Recognize timestamps for each word and implement karaoke-style highlighting.

Example display:

```text
I [love] this song
```

The currently sung word is highlighted.

---

### 16.2 Manual Lyric Editing

The user can correct recognition errors.

Features:

```text
Edit lyric text
Adjust start time
Adjust end time
Save changes
```

---

### 16.3 Import Official Lyrics and Auto-Align

The user provides correct lyrics manually.
The application only performs timestamp alignment.

This may be more useful than fully automatic lyric recognition.

Flow:

```text
Import official lyric text
→ Analyze audio
→ Align lyrics with audio
→ Generate accurate LRC
```

---

### 16.4 Batch Processing

The user selects a folder and the application processes all MP3 files inside it.

---

### 16.5 Web Version

Convert the application into a web app:

```text
Flask / FastAPI backend
HTML / JavaScript frontend
Browser-based music playback
Browser-based lyric display
```

---

## 17. Success Criteria

MVP success criteria:

```text
Given a regular English MP3 song, the application can automatically generate a lyric file and display the current lyric line while playing the song.
```

Strong version success criteria:

```text
1. Vocal separation works
2. Lyric recognition is reasonably accurate
3. Timestamp error is within about 0.5-1 second
4. Lyrics switch naturally during playback
5. The application can export an LRC file
6. The user can manually correct lyrics
```

---

## 18. Recommended Implementation Order

Recommended development order:

```text
1. Implement LRC generation
2. Implement lyric synchronization logic
3. Implement the music player
4. Add Whisper / stable-ts transcription
5. Add Demucs vocal separation
6. Build the GUI last
```

Do not start with the full UI.

First, make the core pipeline work:

```text
mp3 → lyrics.json → lyrics.lrc
```

Then add playback and synchronized lyric display.

---

## 19. Minimum Demo Example

The first demo can work like this:

```text
User selects song.mp3
User clicks Generate Lyrics
The application processes the file
The application generates song.lrc
User clicks Play
The song starts playing

The application displays:

Previous:
When you were here before

Current:
Couldn't look you in the eye

Next:
You're just like an angel
```

This is already a complete and demo-worthy AI project.

---

## 20. Summary

This project is not just a music player.
It is a complete AI pipeline involving:

```text
Audio processing
Speech recognition
Timestamp generation
File format conversion
Music playback
Synchronized UI display
```

It is a strong student AI project because it demonstrates several useful technical skills:

```text
Python programming
AI model integration
Audio processing
File format conversion
GUI development
Data structure design
```

The first version should stay focused:

**Do not aim for perfect lyric recognition. Do not aim for word-level karaoke highlighting yet. First build an MVP that can generate LRC lyrics and display them in sync during playback.**

---

## 21. Feature: Import Lyrics TXT and Auto-Align with Audio

### Description

The user provides a plain text file (.txt) containing the correct lyrics (one line per lyric segment). The application aligns the lyrics with the audio using the AI model and generates accurate timestamps for each line.

This is useful when automatic lyric recognition is inaccurate but the user already has the correct lyrics. Instead of recognizing lyrics from scratch, the AI only needs to determine when each line is sung.

### User Flow

```text
1. User selects an MP3 file
2. User clicks "Load TXT & Align"
3. User selects a .txt file containing lyrics
4. Application uses stable-ts to align the text with the audio
5. Application generates timestamped lyrics
6. User can play the song with synchronized lyrics
7. User can export the aligned lyrics as LRC/SRT/JSON
```

### Input

```text
lyrics.txt — plain text file, one lyric line per line
```

Example:

```text
When you were here before
Couldn't look you in the eye
You're just like an angel
Your skin makes me cry
```

### Output

```json
[
  {"start": 12.30, "end": 16.80, "text": "When you were here before"},
  {"start": 17.10, "end": 21.50, "text": "Couldn't look you in the eye"},
  {"start": 22.00, "end": 26.30, "text": "You're just like an angel"},
  {"start": 26.80, "end": 31.20, "text": "Your skin makes me cry"}
]
```

### Technical Implementation

Uses `stable_whisper.load_model().align(audio_path, lyric_text)` to force-align user-provided lyrics with the audio. This produces more accurate timestamps than full transcription because the text content is already known.

### Acceptance Criteria

* The user can select a .txt file containing lyrics.
* The application aligns the lyrics with the audio and generates timestamps.
* The aligned lyrics can be played back with synchronized display.
* The aligned lyrics can be exported to LRC, SRT, or JSON.
* Empty lines in the .txt file are ignored.
* If the .txt file is empty, the application shows an error message.
* If alignment fails, the application shows a clear error message.
