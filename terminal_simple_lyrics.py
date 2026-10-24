"""
=============================================================================
  SIENNA SPIRO — GREAT EXPECTATION
  TikTok Edit Edition: Chorus 1 langsung ke Bridge
  
  Urutan:
  1. Chorus 1 (00:37)
     - Selesai pada "All I need is the great expectation of you"
  2. Langsung ke Bridge: "Cry my tears and let 'em dry..."
  3. Chorus Climax
  4. Outro
=============================================================================
"""

import sys
import os
import time

# Pastikan ANSI color & UTF-8 aktif di Windows
os.system('')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# TrueColor ANSI Palette (Warm Amber & Luminous White)
def c(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

RESET        = "\033[0m"
BOLD         = "\033[1m"
DIM          = "\033[2m"
ITALIC       = "\033[3m"

WARM_AMBER   = c(255, 175, 80)
SOFT_GOLD    = c(255, 210, 120)
BRIGHT_WHITE = c(255, 255, 255)
WARM_GRAY    = c(140, 130, 120)

# Mulai langsung dari Chorus 1 (detik 00:37)
CHORUS_START_SEC = 37.0

# Daftar lirik: Chorus 1 langsung loncat ke Bridge
# Format: (timestamp_detik, teks_lirik, jeda_antar_bait)
LYRICS = [
    # ── [Chorus 1] (00:37) ──
    (37.80, "So I sing just to know I'm alive", False),
    (42.03, "And I cried all the tears I could cry", False),
    (45.51, "If happiness is just an illusion", False),
    (48.41, "You were the best I ever had", False),
    (51.68, "If you can't be what I want", False),
    (54.80, "And the things you say aren't true", False),
    (58.05, "All I need is the great expectation of you", True),

    # ── [Bridge] (Langsung dari baris di atas) ──
    (64.80, "Cry my tears and let 'em dry", False),
    (67.74, "Cry my tears and testify", False),
    (70.98, "You exist inside my mind", False),
    (74.42, "You, so...", True),

    # ── [Chorus Climax] ──
    (76.31, "So I sing just to know I'm alive", False),
    (80.60, "And I cried all the tears I could cry", False),
    (83.98, "If happiness is just an illusion", False),
    (86.80, "You were the best I ever had", False),
    (90.29, "If you can't be what I want", False),
    (92.95, "And the things you say aren't true", False),
    (96.62, "All I need is the great expectation of you", True),

    # ── [Outro] ──
    (103.42, "All I need is", False),
    (107.66, "All I need is you.", True),
    (114.66, "✦ (Piano echoes fade into silence) ✦", False),
    (120.00, "", False)
]

def main():
    # Sembunyikan kursor terminal untuk pengalaman bersih & sinematik
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n  {WARM_AMBER}{BOLD}✦ SIENNA SPIRO — GREAT EXPECTATION ✦{RESET}\n")

        # Sinkronisasi jam acuan mulai dari detik 37.0 (Chorus 1)
        t_start = time.perf_counter() - CHORUS_START_SEC

        for idx in range(len(LYRICS) - 1):
            target_ts, text, is_stanza_break = LYRICS[idx]
            next_ts = LYRICS[idx + 1][0]
            line_duration = next_ts - target_ts

            if not text:
                continue

            # Tunggu hingga pas dengan detik vokal lagu
            while True:
                elapsed = time.perf_counter() - t_start
                if elapsed >= target_ts:
                    break
                time.sleep(0.01)

            # Kecepatan ketikan santai & selaras dengan alunan vokal aslinya
            type_time = max(0.3, line_duration * 0.72)
            char_delay = type_time / max(len(text), 1)

            # Indentasi 2 spasi bersih
            print("  ", end="", flush=True)

            # Teks lirik utama bersinar putih terang
            sys.stdout.write(f"{BOLD}{BRIGHT_WHITE}")

            for char in text:
                # Huruf vokal diberi aksen emas lembut
                if char in "AEIOUaeiou":
                    sys.stdout.write(f"{SOFT_GOLD}{char}{BRIGHT_WHITE}")
                else:
                    sys.stdout.write(char)
                sys.stdout.flush()

                # Jeda ketikan alami
                if char in ",.!?":
                    time.sleep(char_delay * 1.5)
                elif char == " ":
                    time.sleep(char_delay * 1.1)
                else:
                    time.sleep(char_delay * 0.88)

            print(f"{RESET}")

            # Jeda baris kosong antar-bait
            if is_stanza_break:
                print()

        print(f"\n  {WARM_AMBER}✦ ✧ ✦  Selesai  ✦ ✧ ✦{RESET}\n")

    except KeyboardInterrupt:
        print(f"\n\n  {WARM_GRAY}Lirik dihentikan.{RESET}\n")
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
