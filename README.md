# Robert Schwab — Apparel & Fishing Jigs

Responsive website built with the original logos and photographs from the Robert Google Drive folder.

## Website sections
Homepage (two fish facing one another), Apparel, Fishing Jigs, Photo Gallery, About, FAQ, Contact and draft Privacy Notice.

**Demonstration catalog.** No prices, specifications, availability or biography have been invented. One supplied photograph displaying Pyle Drilling branding is retained in the source assets but excluded from Schwab galleries pending owner approval.

## Images
The two original PNG logos are in the assets directory. Five original JPG photographs and five original HEIC photographs are preserved under assets/originals. The build script (scripts/build_images.py) converts HEIC images and all approved photos and logos into lightweight, browser-friendly WebP files under assets/images. The GitHub Action commits generated images to main, then deploys a clean build to GitHub Pages.

## Deployment
The automated workflow is at .github/workflows/deploy.yml. The owner may need to enable GitHub Pages in Settings > Pages > Build and deployment > Source: GitHub Actions. The expected project site URL is https://wellsmm.github.io/RobertSchwab/ after a successful deployment.

## Contact form: not yet active
Form submissions are intentionally disabled until Robert selects an inbox and a secure backend such as Formspree. Edit the endpoint constant in assets/site.js, update the privacy notice, and test delivery before enabling live submissions. The UI already includes validation, a honeypot, a required consent acknowledgment and accessible status messaging.

## Validation
The workflow runs Node JavaScript syntax validation and checks site pages/image references before deployment. Complete an automated WCAG 2.2 AA and manual mobile review, confirm permission to use assets, and verify business terms before a commercial launch. There is no shopping cart, online payment or analytics.

## Local build
Install Pillow and pillow-heif, run python scripts/build_images.py, then python scripts/check_site.py. Serve this directory using a static web server and open index.html.
