"""Turns docs/release/PRIVACY_NOTICE_DRAFT.md into the public privacy.html (headings, paragraphs, lists, tables)."""
import html
import re
import sys

source, target = sys.argv[1], sys.argv[2]
lines = open(source, encoding="utf-8").read().splitlines()


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"&lt;(https?://[^&\s]+)&gt;", r'<a href="\1">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\b([\w.+-]+@[\w-]+\.[\w.]+)\b", r'<a href="mailto:\1">\1</a>', text)
    return text


body, i = [], 0
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
    elif line.startswith("Status:"):
        # Internal note for the repository copy; not part of the public page.
        while i < len(lines) and lines[i].strip():
            i += 1
    elif line.startswith("# "):
        body.append(f"<h1>{inline(line[2:])}</h1>")
        i += 1
    elif line.startswith("## "):
        body.append(f"<h2>{inline(line[3:])}</h2>")
        i += 1
    elif line.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([cell.strip() for cell in lines[i].strip().strip("|").split("|")])
            i += 1
        head, data = rows[0], [r for r in rows[2:]]
        body.append('<div class="table"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>")
        body.extend("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in data)
        body.append("</tbody></table></div>")
    elif line.startswith("- "):
        items = []
        while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("  ")):
            if lines[i].startswith("- "):
                items.append(lines[i][2:])
            else:
                items[-1] += " " + lines[i].strip()
            i += 1
        body.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>")
    else:
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ")):
            para.append(lines[i].strip())
            i += 1
        body.append(f"<p>{inline(' '.join(para))}</p>")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MichiSonae privacy policy</title>
<meta name="description" content="How the MichiSonae Android app handles your data.">
<style>
:root {{ --ink: #1d2b2f; --muted: #52646a; --line: #d5e2e4; --accent: #126f79; --bg: #fbfdfd; }}
@media (prefers-color-scheme: dark) {{ :root {{ --ink: #e4eeef; --muted: #a6b8bc; --line: #2f4347; --accent: #6cc3cc; --bg: #121b1d; }} }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }}
main {{ max-width: 860px; margin: 0 auto; padding: 32px 16px 64px; }}
h1 {{ font-size: 1.9rem; line-height: 1.25; margin: 0 0 8px; }}
h2 {{ font-size: 1.25rem; margin: 36px 0 8px; padding-top: 12px; border-top: 1px solid var(--line); }}
a {{ color: var(--accent); }}
code {{ font-size: .92em; }}
ul {{ padding-left: 1.3em; }}
li {{ margin: 6px 0; }}
.table {{ overflow-x: auto; margin: 12px 0; }}
table {{ border-collapse: collapse; width: 100%; font-size: .92rem; }}
th, td {{ text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--line); }}
th {{ color: var(--muted); font-weight: 600; }}
</style>
</head>
<body>
<main>
{chr(10).join(body)}
</main>
</body>
</html>
"""
open(target, "w", encoding="utf-8", newline="\n").write(page)
print(f"wrote {target}: {len(body)} blocks")
