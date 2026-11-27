# Editing the site's text

Every page's prose lives here, one `.md` file per page, mirroring the site
structure (`content/zero-one/game11.md` → `/zero-one/game11.html`).

Each file is a list of named blocks:

    <!-- block: eyebrow -->
    Chapter 17 · Example 17.3

Edit the text under a block header, then either:

- **push to GitHub** (or edit right on github.com) — the `build content`
  Action rebuilds the pages automatically, or
- run `python3 build.py` locally and refresh your browser.

Formatting inside blocks:

| write | get |
|---|---|
| `**bold**` | bold |
| `*italic*` | italic |
| `` `x = 2μ/σ²` `` | the site's mono/math style |
| `[text](url)` | a link |
| blank line | new paragraph |
| `\*` | a literal asterisk (math like S\*) |
| `# ` at line start | comment — stripped from output |

Raw HTML (`<span class="m">`, `<sub>`, `<sup>`, …) passes through untouched.

Don't edit the generated `.html` pages at the repo root — they carry a
GENERATED banner and are overwritten by every build. Page *structure*
(panels, sliders, charts) lives in `templates/`.
