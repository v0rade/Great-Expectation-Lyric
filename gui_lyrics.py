"""
=============================================================================
  SIENNA SPIRO — GREAT EXPECTATION
  Apple Music iPad Style GUI Lyrics Player (Chorus 1 langsung ke Bridge)
=============================================================================
"""

import tkinter as tk
import time
import math
import random
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageTk

LYRICS_DATA = [
    # ── [Chorus 1] (00:37) ──
    (37.80, "So I sing just to know I'm alive", "CHORUS", 5),
    (42.03, "And I cried all the tears I could cry", "CHORUS", 5),
    (45.51, "If happiness is just an illusion", "CHORUS", 4),
    (48.41, "You were the best I ever had", "CHORUS", 4),
    (51.68, "If you can't be what I want", "CHORUS", 5),
    (54.80, "And the things you say aren't true", "CHORUS", 5),
    (58.05, "All I need is the great expectation of you", "CHORUS", 5),

    # ── [Bridge] (Langsung dari baris di atas) ──
    (64.80, "Cry my tears and let 'em dry", "BRIDGE", 3),
    (67.74, "Cry my tears and testify", "BRIDGE", 4),
    (70.98, "You exist inside my mind", "BRIDGE", 4),
    (74.42, "You, so...", "BRIDGE", 3),

    # ── [Chorus Climax] ──
    (76.31, "So I sing just to know I'm alive", "CHORUS", 5),
    (80.60, "And I cried all the tears I could cry", "CHORUS", 5),
    (83.98, "If happiness is just an illusion", "CHORUS", 4),
    (86.80, "You were the best I ever had", "CHORUS", 4),
    (90.29, "If you can't be what I want", "CHORUS", 5),
    (92.95, "And the things you say aren't true", "CHORUS", 5),
    (96.62, "All I need is the great expectation of you", "CHORUS", 5),

    # ── [Outro] ──
    (103.42, "All I need is", "OUTRO", 3),
    (107.66, "All I need is you.", "OUTRO", 2),
    (114.66, "✦ (Piano echoes fade into silence) ✦", "OUTRO", 1),
    (120.00, "[Track Completed]", "OUTRO", 0)
]

TOTAL_DURATION = 120.0
START_TIME = 37.0  # 00:37 (Chorus 1)

class GreatExpectationPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sienna Spiro — Great Expectation ♫ (Apple Music Live Lyrics Style)")
        self.width = 1120
        self.height = 720
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.minsize(980, 640)
        self.root.configure(bg="#120c0a")

        self.is_playing = False
        self.current_time = START_TIME
        self.speed = 1.0
        self.last_update_perf = 0.0
        self.active_index = 0
        self.tick = 0

        self.particles = []
        for _ in range(40):
            self.particles.append({
                "x": random.uniform(0, self.width),
                "y": random.uniform(0, self.height),
                "speed": random.uniform(2.0, 5.0),
                "length": random.uniform(6.0, 16.0),
            })

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, 
                                bg="#120c0a", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bg_photo = None
        self.build_background()
        self.build_album_art_card()

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind("<space>", lambda e: self.toggle_play())
        self.root.bind("<Left>", lambda e: self.seek_relative(-5))
        self.root.bind("<Right>", lambda e: self.seek_relative(5))
        self.root.bind("<Configure>", self.on_resize)

        self.root.after(400, self.start_playback)
        self.animate()

    def build_background(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        custom_bg = os.path.join(script_dir, "background.png")
        if os.path.exists(custom_bg):
            try:
                base = Image.open(custom_bg).convert("RGB")
                base = base.resize((self.width, self.height), Image.Resampling.LANCZOS)
            except Exception:
                base = Image.new("RGB", (self.width, self.height), (20, 14, 12))
        else:
            base = Image.new("RGB", (self.width, self.height), (20, 14, 12))

        self.bg_photo = ImageTk.PhotoImage(base)

    def build_album_art_card(self):
        size = 260
        img = Image.new("RGB", (size, size), (225, 125, 55))
        draw = ImageDraw.Draw(img)

        for y in range(size):
            r = int(240 - y * 0.25)
            g = int(140 - y * 0.35)
            b = int(60 - y * 0.15)
            draw.line([(0, y), (size, y)], fill=(r, g, b))

        draw.text((size // 2, size - 45), "SIENNA SPIRO", fill=(255, 245, 235), anchor="ms")
        draw.text((size // 2, size - 22), "GREAT EXPECTATION", fill=(255, 220, 180), anchor="ms")
        
        self.album_art_photo = ImageTk.PhotoImage(img)

    def on_resize(self, event):
        if event.widget == self.root:
            if abs(event.width - self.width) > 30 or abs(event.height - self.height) > 30:
                self.width = max(event.width, 900)
                self.height = max(event.height, 600)
                self.build_background()

    def start_playback(self):
        self.is_playing = True
        self.last_update_perf = time.perf_counter()

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.last_update_perf = time.perf_counter()

    def seek_to(self, target_seconds):
        self.current_time = max(0.0, min(target_seconds, TOTAL_DURATION))
        self.last_update_perf = time.perf_counter()

    def seek_relative(self, delta_seconds):
        self.seek_to(self.current_time + delta_seconds)

    def get_current_section_info(self):
        active_idx = 0
        for i, (ts, text, sec, inten) in enumerate(LYRICS_DATA):
            if self.current_time >= ts:
                active_idx = i
            else:
                break
        return active_idx

    def animate(self):
        now = time.perf_counter()
        if self.is_playing:
            dt = now - self.last_update_perf
            self.current_time += dt * self.speed
            if self.current_time >= TOTAL_DURATION:
                self.current_time = TOTAL_DURATION
                self.is_playing = False
        self.last_update_perf = now
        self.tick += 1

        self.render_frame()
        self.root.after(33, self.animate)

    def render_frame(self):
        self.canvas.delete("all")
        w, h = self.width, self.height

        if self.bg_photo:
            self.canvas.create_image(w // 2, h // 2, image=self.bg_photo)

        for p in self.particles:
            p["y"] += p["speed"]
            if p["y"] > h:
                p["y"] = random.uniform(-20, 0)
                p["x"] = random.uniform(0, w)
            col = "#5a3a2a" if p["speed"] > 3.5 else "#3d271c"
            self.canvas.create_line(p["x"], p["y"], p["x"], p["y"] + p["length"],
                                    fill=col, width=1)

        active_idx = self.get_current_section_info()
        self.active_index = active_idx

        self.render_music_card(50, 60, 320, h - 140)
        self.render_lyrics_panel(430, 60, w - 480, h - 140, active_idx)

    def render_music_card(self, x, y, width, height):
        center_x = x + width // 2
        art_y = y + 150
        if hasattr(self, 'album_art_photo'):
            self.canvas.create_image(center_x, art_y, image=self.album_art_photo)
            self.canvas.create_rectangle(center_x - 130, art_y - 130, center_x + 130, art_y + 130,
                                         outline="#ffb270", width=1)

        meta_y = art_y + 165
        self.canvas.create_text(center_x, meta_y, 
                                text="Great Expectation", 
                                font=("Segoe UI", 16, "bold"), fill="#ffffff")
        self.canvas.create_text(center_x, meta_y + 26, 
                                text="Sienna Spiro", 
                                font=("Segoe UI", 13), fill="#f0ad78")

        ctrl_y = meta_y + 70
        rem_sec = max(0, TOTAL_DURATION - self.current_time)
        rem_str = f"-{self.format_time(rem_sec)}"
        cur_str = self.format_time(self.current_time)

        scrub_w = width - 40
        scrub_x = x + 20
        progress = min(max(self.current_time / TOTAL_DURATION, 0.0), 1.0)
        fill_w = scrub_w * progress

        self.canvas.create_text(scrub_x, ctrl_y - 14, anchor="w",
                                text=cur_str, font=("Segoe UI", 9), fill="#cf9f80")
        self.canvas.create_text(scrub_x + scrub_w, ctrl_y - 14, anchor="e",
                                text=rem_str, font=("Segoe UI", 9), fill="#cf9f80")

        self.canvas.create_line(scrub_x, ctrl_y, scrub_x + scrub_w, ctrl_y, 
                                fill="#4a2e22", width=4)
        self.canvas.create_line(scrub_x, ctrl_y, scrub_x + fill_w, ctrl_y, 
                                fill="#ffffff", width=4)
        self.canvas.create_oval(scrub_x + fill_w - 5, ctrl_y - 5, scrub_x + fill_w + 5, ctrl_y + 5, 
                                fill="#ffffff")

        self.scrub_bounds = (scrub_x, ctrl_y - 10, scrub_x + scrub_w, ctrl_y + 10)

        btn_y = ctrl_y + 40
        self.canvas.create_text(center_x - 70, btn_y, text="⏮", font=("Segoe UI", 16), fill="#e0bfad")
        
        play_icon = "⏸" if self.is_playing else "▶"
        self.canvas.create_text(center_x, btn_y, text=play_icon, font=("Segoe UI", 20, "bold"), fill="#ffffff")
        self.btn_play_bounds = (center_x - 20, btn_y - 20, center_x + 20, btn_y + 20)

        self.canvas.create_text(center_x + 70, btn_y, text="⏭", font=("Segoe UI", 16), fill="#e0bfad")

    def render_lyrics_panel(self, x, y, width, height, active_idx):
        center_y = y + height // 2
        display_offsets = [-2, -1, 0, 1, 2]

        for offset in display_offsets:
            target_i = active_idx + offset
            if 0 <= target_i < len(LYRICS_DATA):
                ts, text, sec, inten = LYRICS_DATA[target_i]

                if offset == 0:
                    line_y = center_y
                    self.canvas.create_text(x + 20, line_y, anchor="w",
                                            text=text, 
                                            font=("Segoe UI", 21, "bold"), fill="#ffffff")

                elif offset < 0:
                    line_y = center_y + (offset * 64) - 10
                    color = "#b5876d" if offset == -1 else "#6b4a3a"
                    self.canvas.create_text(x + 20, line_y, anchor="w",
                                            text=text, 
                                            font=("Segoe UI", 17, "bold"), fill=color)

                elif offset > 0:
                    line_y = center_y + (offset * 64) + 12
                    color = "#b5876d" if offset == 1 else "#6b4a3a"
                    self.canvas.create_text(x + 20, line_y, anchor="w",
                                            text=text, 
                                            font=("Segoe UI", 17, "bold"), fill=color)

    def on_canvas_click(self, event):
        cx, cy = event.x, event.y

        if hasattr(self, 'btn_play_bounds'):
            x1, y1, x2, y2 = self.btn_play_bounds
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                self.toggle_play()
                return

        if hasattr(self, 'scrub_bounds'):
            x1, y1, x2, y2 = self.scrub_bounds
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                ratio = (cx - x1) / max((x2 - x1), 1)
                self.seek_to(ratio * TOTAL_DURATION)
                return

    @staticmethod
    def format_time(seconds: float) -> str:
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins:02d}:{secs:02d}"

def main():
    root = tk.Tk()
    app = GreatExpectationPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
