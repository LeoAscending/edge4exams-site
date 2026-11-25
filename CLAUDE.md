# Edge 4 Exams hub site (edge4exams.pages.dev)

Read this before changing anything. More than one Claude agent works in this repo.

## How it works
- `build_site.py` generates the whole site into `site/` (standard library only: `python3 build_site.py`).
- `site/` is generated and git-ignored. **Never hand-edit HTML.** Change `build_site.py` instead, or the next build wipes your edit.
- Images or other files that should be served as-is go in `static/` (create it if missing). It is copied into the site root before the build writes its own files.
- Deploy: `.github/workflows/deploy.yml` builds on every pull request (check only) and on every push to `main` builds and deploys to the existing Cloudflare Pages project `edge4exams` (a Direct Upload project, so it is deployed with Wrangler, not Cloudflare's Git integration). Secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` are set by the owner in GitHub.

## Working rules
- Work on a branch and open a pull request. The owner reviews and merges. Merging to `main` = live within about a minute.
- Run `python3 build_site.py` before pushing and make sure it succeeds.
- This repo is **public**. Never commit secrets, API keys, customer data, or paid study material (PDFs, mock exams). Only public page content belongs here.
- Do not put the owner's real name anywhere. The public brand is "Edge 4 Exams Singapore" (also "Edge4Exams").

## Files the build must keep producing (never remove)
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
- Every exam page gets a plain Markdown copy and an entry in `llms.txt` (the build does this automatically for each page in `PAGES`).
- Getting mentioned on pages AI already cites (forums, Lemon8, blogs) matters more than adding more pages here.
