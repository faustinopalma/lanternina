"""Generate the first 800x480 monochrome screen used to prove the Wi-Fi path."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def make_screen(path: Path) -> None:
    image = Image.new("1", (800, 480), 1)
    draw = ImageDraw.Draw(image)
    draw.rectangle((18, 18, 781, 461), outline=0, width=6)
    draw.text((400, 150), "LANTERNINA", font=font(72), fill=0, anchor="mm")
    draw.text((400, 260), "COLLEGAMENTO WIFI", font=font(40), fill=0, anchor="mm")
    draw.text((400, 330), "RIUSCITO", font=font(48), fill=0, anchor="mm")
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="BMP")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    make_screen(args.output)


if __name__ == "__main__":
    main()