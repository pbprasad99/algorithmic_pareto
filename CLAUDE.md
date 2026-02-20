# Project: patb.fyi (algorithmic_pareto)

Personal website built with MkDocs Material, hosted on GitHub Pages.

## Stack

- **Framework**: MkDocs with Material theme
- **Font**: Fira Mono (text + code) — monospace throughout
- **Aesthetic**: Simple-blog inspired — monochrome palette, inverted inline code, gray underlined links, generous spacing
- **Hosting**: GitHub Pages via `pbprasad99/algorithmic_pareto`
- **Python env**: `.uv_venv/` (uv) or `venv/`

## Key Files

| File | Purpose |
|---|---|
| `mkdocs.yml` | Site config — theme, plugins, extensions, fonts |
| `docs/assets/stylesheets/extra.css` | All custom CSS (typography, links, code, tables, dark mode, homepage, about page) |
| `overrides/home.html` | Homepage template (Jinja2) — intro + recent posts list |
| `docs/About/README.md` | About page — terminal-style layout with `about-page` wrapper div |
| `docs/.nav.yml` | Navigation structure (used by awesome-nav plugin) |
| `scripts/mkdocs_hooks.py` | MkDocs build hooks |

## CSS Architecture (`extra.css`)

The stylesheet is organized in labeled sections:
1. **Homepage** — `.home-intro`, `.home-posts`, `.home-post` classes
2. **Typography** — `.md-typeset` line-height, letter-spacing, heading margins
3. **Links** — gray (`#808080`) with underline, hover darkens
4. **Inline code** — inverted look (dark bg, light text) scoped to `:not(pre) > code` to avoid overriding syntax highlighting
5. **Blockquotes / Tables** — minimal styling
6. **Dark mode** — `[data-md-color-scheme="slate"]` overrides
7. **About page** — terminal window with traffic light dots, title bar, no copy buttons
8. **Algorithm styles** — left-border blocks, complexity badges
9. **Responsive** — tablet (768px) and mobile (480px) breakpoints

## Design Conventions

- **Dark mode**: always test both modes. Use `[data-md-color-scheme="slate"]` selector for dark overrides
- **Inline code vs code blocks**: inline code uses `.md-typeset :not(pre) > code` to avoid clobbering syntax highlighting in fenced blocks
- **Homepage spacing**: kept tight — the user prefers minimal whitespace between header and content
- **About page**: uses `<div class="about-page" markdown>` wrapper to scope terminal styles; copy buttons hidden via `.about-page .md-clipboard { display: none }`
- **Frontmatter `hide`**: the about page hides navigation, toc, feedback, and title

## Useful Commands

```bash
# Serve locally with auto-reload
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Gotchas

- `docs/assets/css/extra.css` is a dead file (deleted) — all styles live in `docs/assets/stylesheets/extra.css`
- `mkdocs.yml` has duplicate `extra_javascript:` key — second one wins
- The `md_in_html` extension is required for markdown rendering inside HTML divs (e.g., the about page)
- Blog pages use the `blog` plugin with `post_excerpt: required` — posts need `<!-- more -->` excerpt markers
