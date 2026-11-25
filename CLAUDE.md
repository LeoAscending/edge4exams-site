# Edge 4 Exams hub site (edge4exams.pages.dev)

Read this before changing anything. More than one Claude agent works in this repo.

## How it works
- **`site/` is the live site.** Whatever is committed in `site/` is deployed exactly as-is. Put finished HTML, CSS, images and other files there.
- Deploy: `.github/workflows/deploy.yml`. On a pull request it only checks that `index.html`, `robots.txt`, `sitemap.xml`, `llms.txt`, the Google verification file and at least one `.md` copy exist in `site/`. On every push to `main` it runs the same check, then deploys `site/` to the existing Cloudflare Pages project `edge4exams` with Wrangler (a Direct Upload project, so Cloudflare's Git integration is not used). If the check fails, nothing is deployed. Secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set by the owner in GitHub.
- `build_site.py` is the generator that produced the original exam pages, the Markdown copies, `llms.txt`, `llms-full.txt` and `_headers` (`python3 build_site.py` writes into `site/`, standard library only, and copies `static/` in first if it exists). If you redesign pages by hand instead, make sure the files below still exist and that each `.md` copy and `llms.txt` match the new page content and prices. Do not run `build_site.py` over a hand-built `site/` without checking the diff, because it rewrites every page it knows about.

## Site structure
- **The home page is for both audiences** (owner's decision, 25 Nov 2026): a neutral hero, then two doors, PSLE Math (parents) and Licensing exams (professionals). Below the doors the home page lists the licensing exams. The professional nav links to PSLE Math.
- **PSLE pages stay a separate section** (owner's rule). PSLE pages (`PSLE_PATHS` in `build_site.py`) get their own header nav, cream hero, footer and About text, and never mention the former financial adviser. Keep PSLE out of the licensing exam picker and licensing popular packs.
- Images are in `static/img/`: product thumbnails are the real Gumroad thumbnails as WebP (`<name>-thumb.webp`), share images are `og-*.jpg` (1200 wide), plus the logo, favicon and the public teaser images. Every `<img>` needs `alt`, `width` and `height`.

## Working rules
- Work on a branch and open a pull request. The owner reviews and merges. Merging to `main` = live within about a minute.
- Before pushing, check that the required files below are still in `site/`.
- This repo is **public**. Never commit secrets, API keys, customer data, or paid study material (PDFs, mock exams). Only public page content belongs here.
- Do not put the owner's real name anywhere. The public brand is "Edge 4 Exams Singapore" (also "Edge4Exams").

## Files that must always be in `site/` (never remove)
- `google9b9b5686a32dca00.html`: Google Search Console verification. Deleting it breaks verification.
- `robots.txt`, `sitemap.xml`
- `llms.txt`, `llms-full.txt`, one `<page>.md` Markdown copy per exam page, and `_headers` (marks the HTML page as canonical for each `.md` copy)

## Brand
- Teal `#0f6e6e`: logo and all Gumroad product thumbnails
- Green `#0b6e4f` (darker `#14532d`): site buttons, links, tiles
- Gold `#f5c542`: accents
- Keep these. New images (listing images, banners) should use teal and gold, not navy or other palettes.
- Prices on the site are written `S$34`. Store: https://edge4examsg.gumroad.com (product links `/l/<slug>`).

## Content rules
- Every question is original. Never use leaked or real exam questions, or copied textbook content.
- Only state facts about a pack that are true of the live Gumroad listing.
- Independent study aids: not affiliated with SCI, IBF, MAS, CEA or ACAMS.

## AI visibility (owner's standing rule)
- Humans and bots see the same content. Never cloak or hide content that only crawlers can see.
- Every exam page gets a plain Markdown copy (`site/<page>.md`) and an entry in `llms.txt`. `build_site.py` does this automatically for pages in `PAGES`; hand-built pages need them added too.
- Getting mentioned on pages AI already cites (forums, Lemon8, blogs) matters more than adding more pages here.
