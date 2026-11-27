#!/usr/bin/env python3
"""Build site pages from templates/ + content/.

    templates/risk/index.html   page structure, with {{block-name}} slots
    content/risk/index.md       the prose, in named blocks:

        <!-- block: lede -->
        Chapters 22-25 of Chen & Ankenman's *The Mathematics of Poker* ...

    python3 build.py            regenerates risk/index.html (and every other
                                templated page). Run it after editing content.

Markdown supported in blocks: **bold**, *italic*, `math/code` (renders in the
site's mono style), [link](url), and blank lines for paragraph breaks.
Raw HTML (e.g. <span class="m">, <sub>, <sup>) passes through untouched —
use whichever is comfortable.

A GitHub Action runs this automatically on push, so editing a .md on
github.com deploys without any local tooling.
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
TPL = ROOT / "templates"
CNT = ROOT / "content"


def md_inline(text: str) -> str:
    text = text.replace(r"\*", "\x00")  # \* = literal asterisk (math: S*, y₁*)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text, flags=re.S)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r'<span class="m">\1</span>', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    return text.replace("\x00", "*")


def render(block: str) -> str:
    """Render one block. Lines starting with '# ' are build comments and are
    dropped. Blank lines become paragraph breaks, which works because every
    multi-paragraph slot sits inside a <p>...</p> wrapper."""
    block = re.sub(r"(?m)^[ \t]*# .*\n?", "", block)
    paras = [p for p in re.split(r"\n\s*\n", block.strip()) if p.strip()]
    return "</p>\n<p>".join(md_inline(p) for p in paras)


def load_blocks(path: pathlib.Path) -> dict:
    parts = re.split(r"<!--\s*block:\s*([\w-]+)\s*-->", path.read_text())
    return {parts[i]: parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def main() -> int:
    templates = sorted(TPL.rglob("*.html")) if TPL.exists() else []
    if not templates:
        print("build: no templates found under templates/")
        return 1
    failed = False
    for tpl in templates:
        rel = tpl.relative_to(TPL)
        cpath = (CNT / rel).with_suffix(".md")
        if not cpath.exists():
            print(f"build: ERROR: no content file {cpath} for templates/{rel}")
            failed = True
            continue
        blocks = load_blocks(cpath)
        used = set()
        missing = []

        def sub(m):
            k = m.group(1)
            used.add(k)
            if k not in blocks:
                missing.append(k)
                return m.group(0)
            return render(blocks[k])

        out = re.sub(r"\{\{([\w-]+)\}\}", sub, tpl.read_text())
        if missing:
            print(f"build: ERROR: {cpath.name} is missing block(s): {sorted(set(missing))}")
            failed = True
            continue
        unused = sorted(set(blocks) - used)
        if unused:
            print(f"build: warning: unused block(s) in {cpath.name}: {unused}")
        banner = (f"<!-- GENERATED FILE — do not edit. "
                  f"Source: templates/{rel} + content/{rel.with_suffix('.md')} ; "
                  f"rebuild with: python3 build.py -->\n")
        (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / rel).write_text(banner + out)
        print(f"built {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
