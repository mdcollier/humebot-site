#!/usr/bin/env python3
"""Build the HumeBot project reports as PDFs from their Markdown sources.

One template, six reports. Each source file in reports/src/ is a Markdown document with a
small front-matter block (key: value lines between two '---' lines) giving the report's
number, title, subtitle, audience, version, date, status line and PDF file name. The body is
ordinary Markdown (python-markdown "extra" syntax: tables, definition lists, footnotes,
attribute lists such as `{: .unnumbered }` on a heading, and HTML blocks with markdown="1").

Two rendering modes:

* ``single`` (default, used for publication): cover and body are rendered as ONE document by
  headless Chrome with ``tagged=True`` and ``outline=True``, so the PDF carries an accessible
  structure tree, a document language and heading bookmarks. Chrome's running header and
  footer then appear on every page, the cover included (Chrome cannot vary them per page),
  and the page count includes the cover. Document metadata (author, subject) is added with
  pypdf by cloning the document, which preserves the structure tree.
* ``merged`` (the earlier review-draft behaviour): cover and body rendered separately so the
  running header and footer appear only on body pages, then joined with pypdf. The join
  drops the accessibility structure tree, so this mode is not used for publication.

Usage, from the repository root:

    python3 tools/reports/build_reports.py                 # every report, single mode
    python3 tools/reports/build_reports.py --only 03        # one report, by file-name prefix
    python3 tools/reports/build_reports.py --mode merged    # the review-draft layout
    python3 tools/reports/build_reports.py --html-only --workdir /tmp/x   # inspect the HTML

Requirements (Python 3.9+): markdown, pypdf and playwright, with a Chrome or Chromium that
Playwright can drive (``channel="chrome"`` is tried first, then Playwright's own Chromium).
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
WEBSITE = 'https://mdcollier.github.io/humebot-site/'

MARGIN = {'top': '0.95in', 'bottom': '0.9in', 'left': '1in', 'right': '1in'}

# Chrome renders these templates in the page margins. They take only inline styles (single
# quotes inside, because the string sits in a double-quoted attribute), and a font size must
# be given explicitly. The classes pageNumber and totalPages are filled in by Chrome.
_BAR = ("font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 8px; color: #6b6b6b; "
        "width: 100%; box-sizing: border-box; padding: 0 1in; display: flex; justify-content: space-between; "
        "align-items: baseline;")
HEADER = '<div style="{bar} margin-top: 0.42in;"><span>{left}</span><span>{right}</span></div>'
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


def cover_block(meta: dict, single: bool) -> str:
    draft = meta.get('draft', 'false').lower() == 'true'
    draft_line = '<p class="draft">Review draft — not yet released</p>' if draft else ''
    # In single mode the running footer already carries the standing line, so the cover keeps
    # only the website.
    standing = (f'<p class="standing">The HumeBot project website: <a class="url" href="{esc(WEBSITE)}">{esc(WEBSITE)}</a></p>' if single
                else f'<p class="standing">{esc(STANDING)}<br>The HumeBot project website: <a class="url" href="{esc(WEBSITE)}">{esc(WEBSITE)}</a></p>')
    return f'''<section class="cover" aria-label="Cover">
  <p class="kicker">HumeBot · Project report {esc(meta["number"])}</p>
  <h1>{esc(meta["title"])}</h1>
  <p class="subtitle">{esc(meta["subtitle"])}</p>
  <div class="gold-rule" aria-hidden="true"></div>
  <p class="author">{esc(AUTHOR)}</p>
  <p class="affiliation">Professor of Philosophy · {esc(AFFILIATION)}</p>
  <dl class="meta">
    <div><dt>Audience</dt><dd>{esc(meta["audience"])}</dd></div>
    <div><dt>Version</dt><dd>{esc(meta["version"])}</dd></div>
    <div><dt>Date</dt><dd>{esc(meta["date"])}</dd></div>
    <div><dt>Project status</dt><dd>{esc(meta["status"])}</dd></div>
  </dl>
  {draft_line}
  {standing}
</section>'''


def head(meta: dict, css: str, base: str | None) -> str:
    base_tag = f'<base href="{base}">' if base else ''
    return (f'<head><meta charset="utf-8">{base_tag}<title>{esc(meta["title"])}</title>'
            f'<meta name="author" content="{esc(AUTHOR)}"><meta name="description" content="{esc(meta["subtitle"])}">'
            f'<style>{css}</style></head>')


def cover_html(meta: dict, css: str) -> str:
    return f'<!doctype html>\n<html lang="en">{head(meta, css, None)}<body class="cover-page">\n{cover_block(meta, single=False)}\n</body></html>'


def body_html(meta: dict, inner: str, css: str, base: str) -> str:
    return f'<!doctype html>\n<html lang="en">{head(meta, css, base)}<body class="body-page">\n<main class="report">\n{inner}\n</main>\n</body></html>'


def single_html(meta: dict, inner: str, css: str, base: str) -> str:
    return (f'<!doctype html>\n<html lang="en">{head(meta, css, base)}<body class="single-page">\n'
            f'{cover_block(meta, single=True)}\n<main class="report">\n{inner}\n</main>\n</body></html>')


def _launch(p):
    try:
        return p.chromium.launch(channel='chrome', headless=True)
    except Exception:
        return p.chromium.launch(headless=True)


def _templates(meta: dict) -> tuple[str, str]:
    header = HEADER.format(bar=_BAR, left=esc(f'HumeBot · Report {meta["number"]} · {meta["short"]}'),
                           right=esc(f'Version {meta["version"]} · {meta["date"]}'))
    footer = FOOTER.format(bar=_BAR, left=esc(f'{AFFILIATION} · Faculty-led project report · not an official University publication'))
    return header, footer


def _metadata(meta: dict) -> dict:
    return {
        '/Title': f'{meta["title"]} (Version {meta["version"]})',
        '/Author': AUTHOR,
        '/Subject': meta['subtitle'],
        '/Creator': 'HumeBot report builder (tools/reports/build_reports.py)',
        '/CreationDate': dt.datetime.now().strftime("D:%Y%m%d%H%M%S"),
    }


def build_one(src: pathlib.Path, out_dir: pathlib.Path, workdir: pathlib.Path, html_only: bool, mode: str) -> pathlib.Path | None:
    meta, body_md = parse_source(src)
    css = CSS.read_text(encoding='utf-8')
    inner = render_markdown(body_md)
    base = SRC.resolve().as_uri() + '/'
    stem = src.stem
    if mode == 'single':
        (workdir / f'{stem}.single.html').write_text(single_html(meta, inner, css, base), encoding='utf-8')
    else:
        (workdir / f'{stem}.cover.html').write_text(cover_html(meta, css), encoding='utf-8')
        (workdir / f'{stem}.body.html').write_text(body_html(meta, inner, css, base), encoding='utf-8')
    if html_only:
        print(f'{stem}: HTML written to {workdir}')
        return None

    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader, PdfWriter

    header, footer = _templates(meta)
    out = out_dir / meta['pdf']
    with sync_playwright() as p:
        browser = _launch(p)
        page = browser.new_page()
        if mode == 'single':
            raw = workdir / f'{stem}.single.pdf'
            page.goto((workdir / f'{stem}.single.html').resolve().as_uri(), wait_until='load')
            page.pdf(path=str(raw), format='Letter', print_background=True, tagged=True, outline=True,
                     display_header_footer=True, header_template=header, footer_template=footer, margin=MARGIN)
            browser.close()
            # Metadata is added by cloning, which keeps the structure tree, language and outline.
            reader = PdfReader(str(raw))
            writer = PdfWriter(clone_from=reader)
            writer.add_metadata(_metadata(meta))
            with out.open('wb') as fh:
                writer.write(fh)
        else:
            cover_pdf = workdir / f'{stem}.cover.pdf'
            body_pdf = workdir / f'{stem}.body.pdf'
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
            writer.add_metadata(_metadata(meta))
            with out.open('wb') as fh:
                writer.write(fh)

    reader = PdfReader(str(out))
    root = reader.trailer['/Root']
    tagged = '/StructTreeRoot' in root
    print(f'{stem}: {out.name} ({len(reader.pages)} pages; mode {mode}; tagged {"yes" if tagged else "no"}; '
          f'outline {"yes" if "/Outlines" in root else "no"})')
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('--src', type=pathlib.Path, default=SRC, help='directory of Markdown sources')
    ap.add_argument('--out', type=pathlib.Path, default=OUT, help='directory for the PDFs')
    ap.add_argument('--only', help='build only sources whose file name starts with this prefix')
    ap.add_argument('--mode', choices=('single', 'merged'), default='single', help='single tagged document (default) or merged cover + body')
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
        build_one(src, args.out, workdir, args.html_only, args.mode)
    print('intermediate files:', workdir)


if __name__ == '__main__':
    main()
