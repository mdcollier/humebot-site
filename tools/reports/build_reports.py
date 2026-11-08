#!/usr/bin/env python3
"""Build the HumeBot project reports as PDFs from their Markdown sources.

One template, four reports. Each source file in reports/src/ is a Markdown document with a
small front-matter block (key: value lines between two '---' lines) giving the report's
number, title, subtitle, audience, version, date, status line and PDF file name. The body is
ordinary Markdown (python-markdown "extra" syntax: tables, definition lists, footnotes,
attribute lists such as `{: .unnumbered }` on a heading, and HTML blocks with markdown="1").

The build renders a cover page and the body separately with headless Chrome (Playwright),
so that the running header and footer appear on every body page and never on the cover,
and then joins them into one PDF with the document's metadata.

Usage, from the repository root:

    python3 tools/reports/build_reports.py            # every report in reports/src
    python3 tools/reports/build_reports.py --only 03  # one report, by file-name prefix
    python3 tools/reports/build_reports.py --html-only --workdir /tmp/x   # inspect the HTML

Requirements (Python 3.9+): markdown, pypdf and playwright, with a Chrome or Chromium that
Playwright can drive (`channel="chrome"` is tried first, then Playwright's own Chromium).
Figures referenced from the sources resolve relative to reports/src/.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / 'reports' / 'src'
OUT = ROOT / 'reports'
CSS = pathlib.Path(__file__).with_name('report.css')

AUTHOR = 'Mark Collier'
AFFILIATION = 'University of Minnesota Morris'
STANDING = 'A faculty-led project report. Not an official University publication.'

MARGIN = {'top': '0.95in', 'bottom': '0.9in', 'left': '1in', 'right': '1in'}

# Chrome renders these templates in the page margins. They take only inline styles, and a
# font size must be given explicitly. The classes pageNumber and totalPages are filled in.
# Single quotes only inside these inline styles: the string is placed in a double-quoted attribute.
_BAR = ("font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 8px; color: #6b6b6b; "
        "width: 100%; box-sizing: border-box; padding: 0 1in; display: flex; justify-content: space-between; "
        "align-items: baseline;")
HEADER = ('<div style="{bar} margin-top: 0.42in;"><span>{left}</span><span>{right}</span></div>')
FOOTER = ('<div style="{bar} margin-bottom: 0.42in;"><span>{left}</span>'
          '<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')


def parse_source(path: pathlib.Path) -> tuple[dict, str]:
    text = path.read_text(encoding='utf-8')
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    if not m:
        sys.exit(f'{path}: missing front matter')
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        key, _, value = line.partition(':')
        meta[key.strip()] = value.strip()
    for key in ('number', 'title', 'subtitle', 'audience', 'version', 'date', 'status', 'pdf', 'short'):
        if key not in meta:
            sys.exit(f'{path}: front matter lacks "{key}"')
    return meta, m.group(2)


def render_markdown(body: str) -> str:
    import markdown
    return markdown.markdown(body, extensions=['extra', 'sane_lists', 'smarty'], output_format='html5')


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def cover_html(meta: dict, css: str) -> str:
    draft = meta.get('draft', 'false').lower() == 'true'
    draft_line = '<p class="draft">Review draft — not yet released</p>' if draft else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{esc(meta["title"])}</title>
<style>{css}</style></head>
<body class="cover-page">
<div class="cover">
  <p class="kicker">HumeBot · Project report {esc(meta["number"])}</p>
  <h1>{esc(meta["title"])}</h1>
  <p class="subtitle">{esc(meta["subtitle"])}</p>
  <div class="gold-rule"></div>
  <p class="author">{esc(AUTHOR)}</p>
  <p class="affiliation">Professor of Philosophy · {esc(AFFILIATION)}</p>
  <dl class="meta">
    <div><dt>Audience</dt><dd>{esc(meta["audience"])}</dd></div>
    <div><dt>Version</dt><dd>{esc(meta["version"])}</dd></div>
    <div><dt>Date</dt><dd>{esc(meta["date"])}</dd></div>
    <div><dt>Project status</dt><dd>{esc(meta["status"])}</dd></div>
  </dl>
  {draft_line}
  <p class="standing">{esc(STANDING)}<br>The HumeBot project website: <span class="url">https://mdcollier.github.io/humebot-site/</span></p>
</div>
</body></html>'''


def body_html(meta: dict, inner: str, css: str, base: str) -> str:
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><base href="{base}"><title>{esc(meta["title"])}</title>
<style>{css}</style></head>
<body class="body-page">
<main class="report">
{inner}
</main>
</body></html>'''


def build_one(src: pathlib.Path, out_dir: pathlib.Path, workdir: pathlib.Path, html_only: bool) -> pathlib.Path | None:
    meta, body_md = parse_source(src)
    css = CSS.read_text(encoding='utf-8')
    inner = render_markdown(body_md)
    cover = cover_html(meta, css)
    body = body_html(meta, inner, css, SRC.resolve().as_uri() + '/')
    stem = src.stem
    (workdir / f'{stem}.cover.html').write_text(cover, encoding='utf-8')
    (workdir / f'{stem}.body.html').write_text(body, encoding='utf-8')
    if html_only:
        print(f'{stem}: HTML written to {workdir}')
        return None

    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter

    cover_pdf = workdir / f'{stem}.cover.pdf'
    body_pdf = workdir / f'{stem}.body.pdf'
    header = HEADER.format(bar=_BAR, left=esc(f'HumeBot · Report {meta["number"]} · {meta["short"]}'),
                           right=esc(f'Version {meta["version"]} · {meta["date"]}'))
    footer = FOOTER.format(bar=_BAR, left=esc(f'{AFFILIATION} · Faculty-led project report · not an official University publication'))
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel='chrome', headless=True)
        except Exception:
            browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto((workdir / f'{stem}.cover.html').resolve().as_uri(), wait_until='load')
        page.pdf(path=str(cover_pdf), format='Letter', print_background=True,
                 margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
        page.goto((workdir / f'{stem}.body.html').resolve().as_uri(), wait_until='load')
        page.pdf(path=str(body_pdf), format='Letter', print_background=True, display_header_footer=True,
                 header_template=header, footer_template=footer, margin=MARGIN)
        browser.close()

    writer = PdfWriter()
    for part in (cover_pdf, body_pdf):
        writer.append(PdfReader(str(part)))
    writer.add_metadata({
        '/Title': f'{meta["title"]} (Version {meta["version"]})',
        '/Author': AUTHOR,
        '/Subject': meta['subtitle'],
        '/Creator': 'HumeBot report builder (tools/reports/build_reports.py)',
        '/Producer': 'Chromium via Playwright; pypdf',
        '/CreationDate': dt.datetime.now().strftime("D:%Y%m%d%H%M%S"),
    })
    out = out_dir / meta['pdf']
    with out.open('wb') as fh:
        writer.write(fh)
    pages = len(PdfReader(str(out)).pages)
    print(f'{stem}: {out.name} ({pages} pages; cover + {pages - 1} body pages)')
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--src', type=pathlib.Path, default=SRC, help='directory of Markdown sources')
    ap.add_argument('--out', type=pathlib.Path, default=OUT, help='directory for the PDFs')
    ap.add_argument('--only', help='build only sources whose file name starts with this prefix')
    ap.add_argument('--workdir', type=pathlib.Path, help='where to keep the intermediate HTML and PDF parts')
    ap.add_argument('--html-only', action='store_true', help='write the HTML and stop')
    args = ap.parse_args()
    workdir = args.workdir or pathlib.Path(tempfile.mkdtemp(prefix='humebot-reports-'))
    workdir.mkdir(parents=True, exist_ok=True)
    args.out.mkdir(parents=True, exist_ok=True)
    sources = sorted(p for p in args.src.glob('*.md') if not args.only or p.name.startswith(args.only))
    if not sources:
        sys.exit(f'no sources in {args.src}' + (f' starting with {args.only}' if args.only else ''))
    for src in sources:
        build_one(src, args.out, workdir, args.html_only)
    print('intermediate files:', workdir)


if __name__ == '__main__':
    main()
