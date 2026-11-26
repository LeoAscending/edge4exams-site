# Edge 4 Exams hub site

Source for https://edge4exams.com

- `site/` is the live site. Merging to `main` deploys it automatically (GitHub Actions to Cloudflare Pages).
- `build_site.py` regenerates the original exam pages, Markdown copies and llms.txt into `site/`.
- Rules for contributors (including AI agents): see `CLAUDE.md`
