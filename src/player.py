"""
player.py - Music playback using pygame.
"""

import pygame
import time
import threading


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self._file_path = None
        self._playing = False
        self._paused = False
        self._start_time = 0
        self._pause_offset = 0
        self._duration = 0
        self._lock = threading.Lock()

    def load(self, file_path):
        """Load an MP3 file for playback."""
        self._file_path = file_path
        pygame.mixer.music.load(file_path)
        self._playing = False
        self._paused = False
        self._start_time = 0
        self._pause_offset = 0

        # Try to get duration using pydub
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(file_path)
            self._duration = len(audio) / 1000.0
        except Exception:
            self._duration = 0

    def play(self):
        """Start playback from the beginning."""
        with self._lock:
            pygame.mixer.music.play()
            self._start_time = time.time()
            self._pause_offset = 0
            self._playing = True
            self._paused = False

    def pause(self):
        """Pause playback."""
        with self._lock:
            if self._playing and not self._paused:
                pygame.mixer.music.pause()
                self._pause_offset = time.time() - self._start_time
                self._paused = True

    def resume(self):
        """Resume playback after pause."""
        with self._lock:
            if self._paused:
                pygame.mixer.music.unpause()
                self._start_time = time.time() - self._pause_offset
                self._paused = False

    def stop(self):
        """Stop playback."""
        with self._lock:
            pygame.mixer.music.stop()
            self._playing = False
            self._paused = False
            self._start_time = 0
            self._pause_offset = 0

    def get_current_time(self):
        """Return current playback position in seconds."""
        with self._lock:
            if not self._playing:
                return 0.0
            if self._paused:
                return self._pause_offset
            return time.time() - self._start_time

    def is_playing(self):
        """Check if music is currently playing (not paused, not stopped)."""
        with self._lock:
            return self._playing and not self._paused and pygame.mixer.music.get_busy()

    def is_paused(self):
        """Check if playback is paused."""
        return self._paused

    def get_duration(self):
        """Return total duration in seconds."""
        return self._duration

    def get_file_path(self):
        """Return the loaded file path."""
        return self._file_path
