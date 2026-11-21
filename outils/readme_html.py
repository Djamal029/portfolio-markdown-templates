# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.5"]
# ///
"""Génère README.html (guide mis en page, autonome) à partir de README.md.

Utilisation, depuis la racine du projet :  uv run outils/readme_html.py
"""

from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent


def gh_slug(value: str, separator: str) -> str:
    """Même forme d'ancre que GitHub, pour que les liens du sommaire fonctionnent partout."""
    value = re.sub(r"<[^>]+>", "", value).strip().lower()
    value = re.sub(r"[^\w\- ]", "", value)
    return value.replace(" ", separator)


CSS = """
:root{--bg:#fbfaf7;--surface:#fff;--surface-2:#f2f0ea;--text:#1c1917;--muted:#5a5550;--line:#e4e0d8;--accent:#0f766e;--code:#f4f2ec;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#131211;--surface:#1c1b19;--surface-2:#252320;--text:#ede9e3;--muted:#b0aaa2;--line:#34312d;--accent:#5fc4b8;--code:#201f1c;color-scheme:dark}}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:20px}
body{margin:0;background:var(--bg);color:var(--text);font:400 1rem/1.7 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.layout{display:grid;grid-template-columns:280px minmax(0,1fr);max-width:1280px;margin:0 auto}
nav.toc{position:sticky;top:0;height:100vh;overflow-y:auto;padding:32px 24px;border-right:1px solid var(--line)}
nav.toc p{font-weight:700;margin:0 0 10px}
nav.toc ul{list-style:none;margin:0;padding:0}
nav.toc li{margin:2px 0}
nav.toc a{display:block;padding:5px 10px;border-radius:8px;color:var(--muted);text-decoration:none;font-size:.93rem}
nav.toc a:hover{background:var(--surface-2);color:var(--text)}
main{padding:40px 56px 80px;min-width:0;max-width:900px}
h1{font-size:clamp(1.9rem,4vw,2.6rem);line-height:1.15;letter-spacing:-.02em;margin:0 0 16px}
h2{font-size:1.6rem;margin:56px 0 14px;padding-top:14px;border-top:1px solid var(--line);letter-spacing:-.01em}
h3{font-size:1.2rem;margin:32px 0 10px}
a{color:var(--accent)}
img{max-width:100%;height:auto;border-radius:12px;border:1px solid var(--line);box-shadow:0 6px 24px rgba(0,0,0,.08);display:block;margin:14px 0}
p img{display:inline-block}
blockquote{margin:16px 0;padding:12px 18px;border-left:4px solid var(--accent);background:var(--surface);border-radius:0 10px 10px 0;color:var(--muted)}
blockquote p{margin:0}
code{font-family:ui-monospace,"Cascadia Code",Consolas,monospace;font-size:.88em;background:var(--code);padding:.12em .4em;border-radius:5px}
pre{background:var(--code);border:1px solid var(--line);border-radius:12px;padding:14px 16px;overflow-x:auto;line-height:1.5}
pre code{background:none;padding:0;font-size:.86rem}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:.94rem;display:block;overflow-x:auto}
th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
th{background:var(--surface-2)}
hr{display:none}
li{margin:4px 0}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:4px}
@media (max-width:900px){.layout{grid-template-columns:1fr}nav.toc{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line);padding:20px 16px}main{padding:28px 16px 60px}}
"""


def main() -> None:
    import sys

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    source = (ROOT / "README.md").read_text(encoding="utf-8")
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc"],
        extension_configs={"toc": {"slugify": gh_slug, "toc_depth": "2"}},
    )
    body = md.convert(source)
    def flatten(tokens):
        for token in tokens:
            yield token
            yield from flatten(token["children"])

    items = "".join(
        f'<li><a href="#{t["id"]}">{t["name"]}</a></li>'
        for t in flatten(md.toc_tokens)
        if t["level"] == 2 and t["id"] != "sommaire"
    )
    # Le sommaire est dans la colonne de gauche : on retire celui du texte.
    body = re.sub(r'<h2 id="sommaire">.*?</ol>\s*', "", body, count=1, flags=re.S)
    # README.html est à la racine, comme README.md : les chemins d'images restent valables.
    body = re.sub(r"<blockquote>\s*<p>[^<]*<strong>README\.html</strong>.*?</blockquote>\s*", "", body, count=1, flags=re.S)
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guide du portfolio Markdown</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav class="toc" aria-label="Sommaire"><p>Sommaire</p><ul>{items}</ul></nav>
<main>
{body}
</main>
</div>
</body>
</html>
"""
    (ROOT / "README.html").write_text(page, encoding="utf-8")
    print("README.html généré.")


if __name__ == "__main__":
    main()
