#!/usr/bin/env python3
"""Build optimized, browser-compatible WebP files from approved original photos."""
from pathlib import Path
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()
ROOT = Path(__file__).resolve().parents[1]
SOURCE_TO_TARGET = {
    "assets/schwab-logo.png": "assets/images/logos/schwab.webp",
    "assets/schwab-jigs-logo.png": "assets/images/logos/schwab-jigs.webp",
    "assets/originals/schwab-cap.jpg": "assets/images/apparel/schwab-cap.webp",
    "assets/originals/schwab-grey-shirt.jpg": "assets/images/apparel/schwab-grey-shirt.webp",
    "assets/originals/schwab-hoodie-front.jpg": "assets/images/apparel/schwab-hoodie-front.webp",
    "assets/originals/schwab-hoodie-back.jpg": "assets/images/apparel/schwab-hoodie-back.webp",
    "assets/originals/fish-on-front.heic": "assets/images/apparel/fish-on-front.webp",
    "assets/originals/fish-on-back-1.heic": "assets/images/apparel/fish-on-back-1.webp",
    "assets/originals/fish-on-back-2.heic": "assets/images/apparel/fish-on-back-2.webp",
    "assets/originals/jig-lures.heic": "assets/images/jigs/jig-lures.webp",
    "assets/originals/wood-items.heic": "assets/images/gallery/wood-items.webp",
}

def build() -> None:
    for source, target in SOURCE_TO_TARGET.items():
        src, dst = ROOT / source, ROOT / target
        if not src.is_file():
            raise FileNotFoundError(f"Missing original photo: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as file_image:
            img = ImageOps.exif_transpose(file_image)
            if img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, "#fffaf0")
                background.paste(img, mask=img.getchannel("A"))
                img = background
            else:
                img = img.convert("RGB")
            limit = (1000, 1000) if "logos/" in target else (1600, 1600)
            img.thumbnail(limit, Image.Resampling.LANCZOS)
            img.save(dst, "WEBP", quality=85, method=6)
        print(f"{source} -> {target}: {dst.stat().st_size:,} bytes", flush=True)

if __name__ == "__main__":
    build()
