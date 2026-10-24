"""
Generate Apple Music iPad style warm amber backdrop matching the TikTok video
"""
import math
from PIL import Image, ImageDraw, ImageFilter

def generate_tiktok_style_bg(out_path="E:/JIRO_PROJECT/lyrics-sienna-spiro/background.png", width=1920, height=1080):
    # Base dark warm brown/amber
    base = Image.new("RGB", (width, height), (18, 12, 10))
    draw = ImageDraw.Draw(base)

    # Gradient: Deep warm noir to soft mahogany
    for y in range(height):
        ratio = y / height
        r = int(22 * (1 - ratio) + 38 * ratio * (1 - ratio) * 2 + 16 * ratio)
        g = int(14 * (1 - ratio) + 20 * ratio * (1 - ratio) * 2 + 10 * ratio)
        b = int(10 * (1 - ratio) + 16 * ratio * (1 - ratio) * 2 + 8 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    # Warm amber / orange glowing orbs as seen in Apple Music lyrics backdrop
    orbs = [
        (int(width * 0.25), int(height * 0.40), 550, (225, 120, 50, 75)),  # Apple Music Warm Orange
        (int(width * 0.75), int(height * 0.45), 650, (200, 95, 35, 65)),   # Amber glow
        (int(width * 0.50), int(height * 0.70), 500, (160, 60, 25, 60)),   # Deep terracotta
        (int(width * 0.15), int(height * 0.85), 350, (190, 80, 30, 45)),   # Bottom glow
    ]
    for cx, cy, rad, color in orbs:
        ov_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=color)

    overlay = overlay.filter(ImageFilter.GaussianBlur(140))
    base = Image.alpha_composite(base.convert("RGBA"), overlay)

    # Subtle radial vignette
    vig_img = Image.radial_gradient("L").resize((width, height))
    vig_mask = Image.eval(vig_img, lambda p: int((255 - p) * 0.80))
    black_layer = Image.new("RGBA", (width, height), (8, 6, 5, 255))
    base.paste(black_layer, (0, 0), vig_mask)

    base.convert("RGB").save(out_path, quality=95)
    print("TikTok/Apple Music style background generated at:", out_path)

if __name__ == "__main__":
    generate_tiktok_style_bg()
