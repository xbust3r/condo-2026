#!/usr/bin/env python3
"""Convert all .md files in docs/ to HTML, preserving folder structure."""

import os
import html as html_mod
from pathlib import Path
import markdown_it

SRC = Path("/home/miguel/servers/condo-py/docs")
DST = Path("/home/miguel/servers/condo-py/docs/html")
DST.mkdir(exist_ok=True)

md_files = sorted(SRC.rglob("*.md"))
print(f"Found {len(md_files)} .md files")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    min-height: 100vh;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 20px 80px;
  }}
  h1 {{ color: #f0a500; font-size: 2em; margin-bottom: 0.5em; border-bottom: 2px solid #333; padding-bottom: 0.3em; }}
  h2 {{ color: #f0a500; font-size: 1.5em; margin-top: 1.5em; margin-bottom: 0.5em; }}
  h3 {{ color: #ffcc66; font-size: 1.2em; margin-top: 1.2em; margin-bottom: 0.4em; }}
  h4, h5, h6 {{ color: #ffdd88; margin-top: 1em; margin-bottom: 0.3em; }}
  p {{ margin-bottom: 0.8em; }}
  a {{ color: #6ab0f3; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{ background: #2a2a2a; padding: 2px 6px; border-radius: 3px; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9em; color: #ff7b72; }}
  pre {{ background: #1e1e1e; border: 1px solid #333; border-radius: 6px; padding: 14px; margin: 1em 0; overflow-x: auto; }}
  pre code {{ background: none; padding: 0; color: #d4d4d4; font-size: 0.88em; }}
  blockquote {{ border-left: 4px solid #f0a500; margin: 1em 0; padding: 0.5em 1em; background: #222; color: #b0b0b0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
  th, td {{ border: 1px solid #444; padding: 8px 12px; text-align: left; }}
  th {{ background: #2a2a2a; color: #f0a500; }}
  tr:nth-child(even) {{ background: #1f1f1f; }}
  hr {{ border: none; border-top: 1px solid #333; margin: 2em 0; }}
  ul, ol {{ margin: 0.8em 0 0.8em 1.5em; }}
  li {{ margin-bottom: 0.3em; }}
  img {{ max-width: 100%; border-radius: 4px; }}
</style>
</head>
<body>
<div class="container">
{content}
</div>
</body>
</html>"""

parser = markdown_it.MarkdownIt()

def convert_file(md_path):
    rel = md_path.relative_to(SRC)
    out_path = DST / rel.with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(md_path, encoding="utf-8") as f:
        text = f.read()

    # Strip front matter
    if text.startswith("---"):
        parts = text[3:].split("---", 1)
        if len(parts) == 2:
            text = parts[1].strip()

    # Extract title
    title = rel.stem.replace("-", " ").replace("_", " ").title()
    for line in text.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    content = parser.render(text)
    html = HTML_TEMPLATE.format(title=html_mod.escape(title), content=content)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

ok = 0
err = 0
for i, md_path in enumerate(md_files):
    try:
        convert_file(md_path)
        ok += 1
    except Exception as e:
        err += 1
        print(f"  ERROR {md_path}: {e}", file=sys.stderr)

print(f"\n✅ {ok} files converted, {err} errors")
print(f"   Output: {DST}")