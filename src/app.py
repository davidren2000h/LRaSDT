"""
app.py - Main application entry point with Tkinter GUI.
AutoLyric Sync: AI-Powered Lyric Recognition and Synchronized Display Tool
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import json

from player import MusicPlayer
from lyric_sync import get_display_lines
from lyric_exporter import export_lrc, export_srt, export_json, load_lrc, load_json
from transcriber import transcribe, align_lyrics
from audio_processor import separate_vocals, check_ffmpeg, get_audio_duration


class AutoLyricSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoLyric Sync")
        self.root.geometry("700x650")
        self.root.resizable(True, True)

        self.player = MusicPlayer()
        self.lyrics = []
        self.mp3_path = None
        self.update_job = None
        self.is_processing = False

        self._build_ui()

    def _build_ui(self):
        # --- File Selection ---
        file_frame = tk.LabelFrame(self.root, text="File", padx=10, pady=5)
        file_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.btn_select = tk.Button(file_frame, text="Select MP3 File", command=self._select_file)
        self.btn_select.pack(side="left")

        self.lbl_filename = tk.Label(file_frame, text="No file selected", anchor="w")
        self.lbl_filename.pack(side="left", padx=10, fill="x", expand=True)

        # --- Processing Options ---
        proc_frame = tk.LabelFrame(self.root, text="Lyric Generation", padx=10, pady=5)
        proc_frame.pack(fill="x", padx=10, pady=5)

        options_row = tk.Frame(proc_frame)
        options_row.pack(fill="x", pady=(0, 5))

        tk.Label(options_row, text="Model:").pack(side="left")
        self.model_var = tk.StringVar(value="base")
        model_menu = tk.OptionMenu(options_row, self.model_var, "tiny", "base", "small", "medium")
        model_menu.pack(side="left", padx=5)

        tk.Label(options_row, text="Language:").pack(side="left", padx=(10, 0))
        self.lang_var = tk.StringVar(value="en")
        lang_menu = tk.OptionMenu(options_row, self.lang_var, "en", "zh", "ja", "ko", "es", "fr", "de")
        lang_menu.pack(side="left", padx=5)

        self.vocal_sep_var = tk.BooleanVar(value=False)
        tk.Checkbutton(options_row, text="Separate vocals (Demucs)", variable=self.vocal_sep_var).pack(side="left", padx=10)

        btn_row = tk.Frame(proc_frame)
        btn_row.pack(fill="x")

        self.btn_generate = tk.Button(btn_row, text="Generate Lyrics", command=self._generate_lyrics)
        self.btn_generate.pack(side="left")

        self.btn_load_lrc = tk.Button(btn_row, text="Load LRC", command=self._load_lrc_file)
        self.btn_load_lrc.pack(side="left", padx=5)

        self.btn_align = tk.Button(btn_row, text="Load TXT & Align", command=self._align_lyrics)
        self.btn_align.pack(side="left", padx=5)

        self.lbl_status = tk.Label(proc_frame, text="Status: Ready", anchor="w", fg="gray")
        self.lbl_status.pack(fill="x", pady=(5, 0))

        # --- Playback Controls ---
        play_frame = tk.LabelFrame(self.root, text="Playback", padx=10, pady=5)
        play_frame.pack(fill="x", padx=10, pady=5)

        btn_bar = tk.Frame(play_frame)
        btn_bar.pack(fill="x")

        self.btn_play = tk.Button(btn_bar, text="▶ Play", command=self._play, width=8)
        self.btn_play.pack(side="left", padx=2)

        self.btn_pause = tk.Button(btn_bar, text="⏸ Pause", command=self._pause, width=8)
        self.btn_pause.pack(side="left", padx=2)

        self.btn_stop = tk.Button(btn_bar, text="⏹ Stop", command=self._stop, width=8)
        self.btn_stop.pack(side="left", padx=2)

        self.lbl_time = tk.Label(play_frame, text="00:00 / 00:00", font=("Consolas", 11))
        self.lbl_time.pack(pady=(5, 0))

        # --- Lyric Display ---
        lyric_frame = tk.LabelFrame(self.root, text="Lyrics", padx=10, pady=10)
        lyric_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.lbl_prev = tk.Label(lyric_frame, text="", font=("Arial", 12), fg="gray", wraplength=600)
        self.lbl_prev.pack(pady=(10, 5))

        self.lbl_current = tk.Label(lyric_frame, text="♪", font=("Arial", 18, "bold"), fg="#1a73e8", wraplength=600)
        self.lbl_current.pack(pady=5)

        self.lbl_next = tk.Label(lyric_frame, text="", font=("Arial", 12), fg="gray", wraplength=600)
        self.lbl_next.pack(pady=(5, 10))

        # --- Export ---
        export_frame = tk.LabelFrame(self.root, text="Export", padx=10, pady=5)
        export_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.btn_export_lrc = tk.Button(export_frame, text="Export LRC", command=lambda: self._export("lrc"))
        self.btn_export_lrc.pack(side="left", padx=2)

        self.btn_export_srt = tk.Button(export_frame, text="Export SRT", command=lambda: self._export("srt"))
        self.btn_export_srt.pack(side="left", padx=2)

        self.btn_export_json = tk.Button(export_frame, text="Export JSON", command=lambda: self._export("json"))
        self.btn_export_json.pack(side="left", padx=2)

    # --- File Selection ---
    def _select_file(self):
        path = filedialog.askopenfilename(
            title="Select MP3 File",
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if path:
            if not path.lower().endswith(".mp3"):
                messagebox.showerror("Error", "Please select an MP3 file.")
                return
            self.mp3_path = path
            self.lbl_filename.config(text=os.path.basename(path))
            self.player.load(path)
            duration = self.player.get_duration()
            self.lbl_time.config(text=f"00:00 / {self._format_time(duration)}")
            self._set_status("File loaded successfully.")

    # --- Lyric Generation ---
    def _generate_lyrics(self):
        if not self.mp3_path:
            messagebox.showwarning("Warning", "Please select an MP3 file first.")
            return
        if self.is_processing:
            return

        self.is_processing = True
        self.btn_generate.config(state="disabled")
        thread = threading.Thread(target=self._run_pipeline, daemon=True)
        thread.start()

    def _run_pipeline(self):
        try:
            audio_path = self.mp3_path

            # Step 1: Vocal separation (optional)
            if self.vocal_sep_var.get():
                self._set_status("Status: Separating vocals...")
                try:
                    audio_path = separate_vocals(self.mp3_path)
                    self._set_status("Status: Vocals separated successfully.")
                except Exception as e:
                    self._set_status(f"Vocal separation failed: {e}\nUsing original audio.")
                    audio_path = self.mp3_path

            # Step 2: Transcribe
            self._set_status("Status: Recognizing lyrics... (this may take a while)")
            model_size = self.model_var.get()
            self.lyrics = transcribe(audio_path, model_size=model_size)

            if not self.lyrics:
                self._set_status("Status: No lyrics recognized.")
            else:
                self._set_status(f"Status: Lyrics generated successfully ({len(self.lyrics)} lines)")

        except Exception as e:
            self._set_status(f"Error: {e}")
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.btn_generate.config(state="normal"))

    # --- Load LRC ---
    def _load_lrc_file(self):
        path = filedialog.askopenfilename(
            title="Load LRC File",
            filetypes=[("LRC files", "*.lrc"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            if path.lower().endswith(".json"):
                self.lyrics = load_json(path)
            else:
                self.lyrics = load_lrc(path)
            self._set_status(f"Loaded {len(self.lyrics)} lyric lines from file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load lyrics: {e}")

    # --- Align Lyrics from TXT ---
    def _align_lyrics(self):
        if not self.mp3_path:
            messagebox.showwarning("Warning", "Please select an MP3 file first.")
            return
        if self.is_processing:
            return

        txt_path = filedialog.askopenfilename(
            title="Select Lyrics TXT File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not txt_path:
            return

        self.is_processing = True
        self.btn_align.config(state="disabled")
        self.btn_generate.config(state="disabled")
        thread = threading.Thread(target=self._run_alignment, args=(txt_path,), daemon=True)
        thread.start()

    def _run_alignment(self, txt_path):
        try:
            audio_path = self.mp3_path

            # Optional vocal separation
            if self.vocal_sep_var.get():
                self._set_status("Status: Separating vocals...")
                try:
                    audio_path = separate_vocals(self.mp3_path)
                    self._set_status("Status: Vocals separated successfully.")
                except Exception as e:
                    self._set_status(f"Vocal separation failed: {e}\nUsing original audio.")
                    audio_path = self.mp3_path

            self._set_status("Status: Aligning lyrics with audio... (this may take a while)")
            model_size = self.model_var.get()
            language = self.lang_var.get()
            self.lyrics = align_lyrics(audio_path, txt_path, model_size=model_size, language=language)

            if not self.lyrics:
                self._set_status("Status: Alignment produced no results.")
            else:
                self._set_status(f"Status: Lyrics aligned successfully ({len(self.lyrics)} lines)")

        except Exception as e:
            self._set_status(f"Error: {e}")
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.btn_align.config(state="normal"))
            self.root.after(0, lambda: self.btn_generate.config(state="normal"))

    # --- Playback ---
    def _play(self):
        if not self.mp3_path:
            messagebox.showwarning("Warning", "Please select an MP3 file first.")
            return
        self.player.load(self.mp3_path)
        self.player.play()
        self._start_lyric_update()

    def _pause(self):
        if self.player.is_paused():
            self.player.resume()
            self.btn_pause.config(text="⏸ Pause")
            self._start_lyric_update()
        else:
            self.player.pause()
            self.btn_pause.config(text="▶ Resume")
            self._stop_lyric_update()

    def _stop(self):
        self.player.stop()
        self._stop_lyric_update()
        self.lbl_prev.config(text="")
        self.lbl_current.config(text="♪")
        self.lbl_next.config(text="")
        self.lbl_time.config(text=f"00:00 / {self._format_time(self.player.get_duration())}")
        self.btn_pause.config(text="⏸ Pause")

    # --- Lyric Update Loop ---
    def _start_lyric_update(self):
        self._stop_lyric_update()
        self._update_display()

    def _stop_lyric_update(self):
        if self.update_job:
            self.root.after_cancel(self.update_job)
            self.update_job = None

    def _update_display(self):
        current_time = self.player.get_current_time()
        duration = self.player.get_duration()

        # Update time display
        self.lbl_time.config(text=f"{self._format_time(current_time)} / {self._format_time(duration)}")

        # Update lyric display
        if self.lyrics:
            display = get_display_lines(current_time, self.lyrics)
            self.lbl_prev.config(text=display["previous"])
            self.lbl_current.config(text=display["current"] if display["current"] else "♪")
            self.lbl_next.config(text=display["next"])

        # Check if playback ended
        if not self.player.is_playing() and not self.player.is_paused():
            if current_time > 0 and duration > 0 and current_time >= duration - 0.5:
                self._stop()
                return

        # Schedule next update (100ms = 10 updates/sec)
        self.update_job = self.root.after(100, self._update_display)

    # --- Export ---
    def _export(self, fmt):
        if not self.lyrics:
            messagebox.showwarning("Warning", "No lyrics to export. Generate or load lyrics first.")
            return

        filetypes = {
            "lrc": ("LRC files", "*.lrc"),
            "srt": ("SRT files", "*.srt"),
            "json": ("JSON files", "*.json"),
        }

        default_name = ""
        if self.mp3_path:
            default_name = os.path.splitext(os.path.basename(self.mp3_path))[0]

        path = filedialog.asksaveasfilename(
            title=f"Export {fmt.upper()}",
            defaultextension=f".{fmt}",
            initialfile=f"{default_name}.{fmt}" if default_name else "",
            filetypes=[filetypes[fmt], ("All files", "*.*")]
        )
        if not path:
            return

        try:
            if fmt == "lrc":
                export_lrc(self.lyrics, path)
            elif fmt == "srt":
                export_srt(self.lyrics, path)
            elif fmt == "json":
                export_json(self.lyrics, self.mp3_path or "unknown.mp3", path)
            self._set_status(f"Exported to {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    # --- Helpers ---
    def _set_status(self, text):
        self.root.after(0, lambda: self.lbl_status.config(text=text))

    @staticmethod
    def _format_time(seconds):
        if seconds <= 0:
            return "00:00"
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m:02d}:{s:02d}"


def main():
    root = tk.Tk()
    app = AutoLyricSyncApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
