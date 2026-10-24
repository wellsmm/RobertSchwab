# Robert Schwab — Apparel & Fishing Jigs

A responsive, rustic-themed demonstration catalog using authentic Schwab logos and product photos from the Robert folder on Google Drive.

## Website sections
- Home: both original fish-logo designs side-by-side
- Apparel: seven approved sample photographs
- Fishing Jigs: one verified jig/lure assortment photograph
- Photo Gallery: nine approved photos with interactive category filters and an enlarged-photo viewer
- About: factual introduction without an invented biography
- FAQs, Contact, and draft Privacy Notice

The two logo images are preserved exactly as supplied in PNG format, with optimized display copies in WebP. **Fish facing directions still require visual owner approval.**

## Photo processing
Five original JPEGs and five original HEICs are preserved in `assets/originals/`. `scripts/build_images.py` converts the approved photos and original PNG logos to eleven optimized WebP browser assets in `assets/images/`.

A Pyle Drilling-branded image is deliberately **excluded** from the Schwab gallery until its relevance and display rights are confirmed. A workshop photograph is labeled as a workshop image, not as a jig or item for sale.

To rebuild locally:

```bash
python -m pip install "Pillow>=11,<13" "pillow-heif>=1,<2"
python scripts/build_images.py
python scripts/check_site.py
node --check assets/site.js
```

## GitHub Pages — one-time setup required

The workflow in `.github/workflows/deploy.yml` converts images, validates all pages and assets, creates a Pages artifact, and deploys. It runs on pushes to `main` and via manual dispatch.

**The repository owner must first enable GitHub Pages:**
1. Open `wellsmm/RobertSchwab` on GitHub and choose **Settings > Pages**.
2. Under **Build and deployment**, change **Source** to **GitHub Actions** and save.
3. Open **Actions > Build and deploy Robert Schwab website**, and rerun or dispatch the workflow.
4. After the deploy job succeeds, open `https://wellsmm.github.io/RobertSchwab/` and confirm page rendering.

The prior workflow failed because `actions/configure-pages` attempted to create the Pages site using a token without the required repository administration privileges. This is a one-time account-side setting, not an error in HEIC conversion or page validation. The website must **not** be reported as live before a successful Pages deployment and browser smoke test.

## Contact delivery and launch checklist

The contact form is intentionally disabled: `assets/site.js` contains `const endpoint=""`. To activate it, Robert must choose the destination inbox and a Formspree or equivalent form endpoint. Update the contact form setup notice and draft privacy notice with the approved processor and real handling practices, then test successful and failed submissions. Do not put account passwords or tokens into browser JavaScript.

Product names, available sizes, jig weights and colors, inventory, prices, ordering/shipping/returns, business details, and the About biography need Robert's approval. There is no cart, checkout or analytics.

Accessibility measures include semantic headings, skip navigation, visible keyboard focus, reduced-motion rules, responsive layouts, a native dialog lightbox and announced gallery-filter results. **Automated and manual WCAG 2.2 AA testing is still outstanding**, including real-device mobile, keyboard and screen-reader testing.
