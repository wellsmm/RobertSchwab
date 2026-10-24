#!/usr/bin/env python3
"""Validate pages, routes, local links and generated assets before publishing."""
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "apparel.html", "jigs.html", "gallery.html", "about.html", "contact.html", "faq.html", "privacy.html")

class LocalReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.lang = False
        self.page = None

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.lang = attrs.get("lang") == "en"
        if tag == "body":
            self.page = attrs.get("data-page")
        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value and not value.startswith(("http:", "https:", "mailto:", "tel:", "#", "data:")):
                self.links.append(value.split("?", 1)[0].split("#", 1)[0])

assert (ROOT / ".nojekyll").is_file(), "Missing GitHub Pages .nojekyll marker"
for filename in PAGES:
    page_text = (ROOT / filename).read_text(encoding="utf-8")
    parser = LocalReferences()
    parser.feed(page_text)
    assert parser.lang, f"Missing HTML language: {filename}"
    expected = "home" if filename == "index.html" else filename[:-5]
    assert parser.page == expected, f"Incorrect data-page in {filename}: {parser.page!r}"
    assert 'assets/site.js' in page_text and 'assets/site.css' in page_text, filename
    assert "<title>" in page_text, f"Missing page title: {filename}"
    for link in parser.links:
        assert (ROOT / link).is_file(), f"Broken local reference in {filename}: {link}"

js = (ROOT / "assets/site.js").read_text(encoding="utf-8")
css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
asset_paths = set(re.findall(r'images/(?:logos|apparel|jigs|gallery)/[a-z0-9-]+\.webp', js))
assert len(asset_paths) >= 11, f"Expected 11 approved images, found {len(asset_paths)}"
for asset in asset_paths:
    file = ROOT / "assets" / asset
    assert file.is_file() and file.stat().st_size > 0, f"Missing or empty image: {asset}"
# Logo optimization must retain real alpha transparency, not flatten on ivory.
for logo in ("schwab.webp", "schwab-jigs.webp"):
    file = ROOT / "assets" / "images" / "logos" / logo
    with Image.open(file) as logo_image:
        assert "A" in logo_image.getbands(), f"Logo must retain transparency: {logo}"
        assert logo_image.getpixel((0, 0))[3] == 0, f"Logo background not removed: {logo}"
        assert logo_image.getpixel((logo_image.width // 2, logo_image.height // 2))[3] > 200, f"Logo interior unexpectedly transparent: {logo}"
for filename in PAGES:
    assert filename in js or filename == "privacy.html", f"Navigation lacks {filename}"
assert "skip" in js and "focus-visible" in css and "prefers-reduced-motion" in css, "Accessibility basics missing"
assert 'const endpoint=""' in js, "Confirm approved contact endpoint and privacy policy before activation"
assert all(token in js for token in ('data-filter="all"', 'data-filter="apparel"', 'data-filter="jigs"', 'data-filter="workshop"')), "Gallery filter missing"
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for filename in PAGES[1:]:
    assert "/" + filename in sitemap, f"Sitemap missing {filename}"
print(f"PASS: {len(PAGES)} HTML pages, {len(asset_paths)} images, navigation, sitemap, accessibility hooks and gallery filters.")
