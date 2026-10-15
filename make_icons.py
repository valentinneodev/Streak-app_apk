"""Erzeugt alle Android-App-Symbole aus icon.png und icon-foreground.png.
Wird vom GitHub-Workflow nach 'npx cap add android' ausgefuehrt."""
import os
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
LAUNCHER = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
FOREGROUND = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}

full = Image.open("icon.png").convert("RGBA")
fg = Image.open("icon-foreground.png").convert("RGBA")

def round_icon(img, size):
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size * 4 - 1, size * 4 - 1], fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out

for dpi, px in LAUNCHER.items():
    d = os.path.join(RES, "mipmap-" + dpi)
    os.makedirs(d, exist_ok=True)
    full.resize((px, px), Image.LANCZOS).save(os.path.join(d, "ic_launcher.png"))
    round_icon(full, px).save(os.path.join(d, "ic_launcher_round.png"))
    fpx = FOREGROUND[dpi]
    fg.resize((fpx, fpx), Image.LANCZOS).save(os.path.join(d, "ic_launcher_foreground.png"))

with open(os.path.join(RES, "values", "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FF7A1A</color>\n</resources>\n')
print("Symbole erzeugt.")
