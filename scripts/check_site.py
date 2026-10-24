#!/usr/bin/env python3
"""Fail the CI build when a page or referenced photo is missing."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
PAGES=["index.html","apparel.html","jigs.html","gallery.html","about.html","contact.html","faq.html","privacy.html"]
for path in PAGES:
    text=(ROOT/path).read_text(encoding="utf-8")
    assert 'lang="en"' in text, path
    assert "assets/site.js" in text, path
js=(ROOT/"assets/site.js").read_text(encoding="utf-8")
asset_paths=set(re.findall(r'images/(?:logos|apparel|jigs|gallery)/[a-z0-9-]+\.webp',js))
assert len(asset_paths)>=11, "Expected all photographed items and both logos"
for asset in asset_paths:
    assert (ROOT/"assets"/asset).is_file(), f"Missing website asset: {asset}"
print(f"Verified {len(PAGES)} pages and {len(asset_paths)} generated image assets.")
