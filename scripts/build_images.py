#!/usr/bin/env python3
"""Build optimized WebP photos and transparent, artwork-preserving logo assets."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageChops, ImageFilter
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


def remove_logo_background(image: Image.Image) -> Image.Image:
    """Clear only the near-white canvas connected to an image edge.

    Keep the cream and white details enclosed by the logo artwork. An edge
    flood-fill is safer for these distressed logos than removing every white
    pixel, which would erase highlights, lettering and mountain snow.
    """
    rgb = image.convert("RGB")
    marked = rgb.copy()
    marker = (255, 0, 255)
    width, height = marked.size
    for corner in ((0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)):
        if marked.getpixel(corner) != marker:
            ImageDraw.floodfill(marked, corner, marker, thresh=50)

    red, green, blue = marked.split()
    red_key = red.point(lambda v: 255 if v == 255 else 0)
    green_key = green.point(lambda v: 255 if v == 0 else 0)
    blue_key = blue.point(lambda v: 255 if v == 255 else 0)
    exterior = ImageChops.multiply(ImageChops.multiply(red_key, green_key), blue_key)

    # Feather just the silhouette boundary for smooth display on dark themes.
    alpha = ImageChops.invert(exterior).filter(ImageFilter.GaussianBlur(0.7))
    result = rgb.convert("RGBA")
    result.putalpha(alpha)
    return result

def build() -> None:
    for source, target in SOURCE_TO_TARGET.items():
        src, dst = ROOT / source, ROOT / target
        if not src.is_file():
            raise FileNotFoundError(f"Missing original photo: {src}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as file_image:
            img = ImageOps.exif_transpose(file_image)
            is_logo = "logos/" in target
            if is_logo:
                img = remove_logo_background(img)
            elif img.mode in ("RGBA", "LA"):
                background = Image.new("RGB", img.size, "#fffaf0")
                background.paste(img, mask=img.getchannel("A"))
                img = background
            else:
                img = img.convert("RGB")
            limit = (1000, 1000) if is_logo else (1600, 1600)
            img.thumbnail(limit, Image.Resampling.LANCZOS)
            if is_logo:
                img.save(dst, "WEBP", lossless=True, method=6)
            else:
                img.save(dst, "WEBP", quality=85, method=6)
        print(f"{source} -> {target}: {dst.stat().st_size:,} bytes", flush=True)

if __name__ == "__main__":
    build()
