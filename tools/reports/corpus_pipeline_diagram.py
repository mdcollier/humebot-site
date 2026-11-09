#!/usr/bin/env python3
"""Corpus production and verification figure for Report 3 (standard library only).

Two rows of four steps. The first runs from the page image to the diplomatic text: two
independent OCR readings, a full reading of every leaf against the image with every decision
recorded, and an assembly that emits characters only from the OCR files and the recorded
edits, which an independent program must reproduce byte for byte. The second runs from the
diplomatic text to the reader: deterministic normalization, identifiers and a citation index,
the hash-pinned corpus package, and the Reading Desk, which constructs displayed quotations
from the package and verifies them.

    python3 tools/reports/corpus_pipeline_diagram.py reports/src/figures/corpus-pipeline.svg
"""
import pathlib
import sys

W, H = 820, 330
STYLE = """
.t { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; fill: #1f1f1f; }
.label { font-size: 14px; font-weight: 600; }
.tiny { font-size: 12px; fill: #5f6368; }
.row { font-size: 11px; fill: #7a1e2e; font-weight: 600; letter-spacing: 0.08em; }
.box { fill: #fff; stroke: #7a1e2e; stroke-width: 1.5; }
.evid { fill: #f7f4ef; stroke: #7a1e2e; stroke-width: 1.8; }
.flow { fill: none; stroke: #1f1f1f; stroke-width: 1.5; }
"""


def text(x, y, s, cls='t tiny', anchor='middle'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def lines(x, y, items, cls='t tiny', anchor='middle', dy=14):
    return '\n'.join(text(x, y + i * dy, s, cls, anchor) for i, s in enumerate(items))


def rect(x, y, w, h, cls, r=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>'


def arrow(d):
    return f'<path d="{d}" class="flow" marker-end="url(#arrow)"/>'


def box(x, y, w, h, title, body, cls='box'):
    cx = x + w / 2
    return '\n'.join([rect(x, y, w, h, cls), text(cx, y + 22, title, 't label'), lines(cx, y + 42, body)])


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="cp-title cp-desc">',
         '<title id="cp-title">From page image to verified displayed text</title>',
         '<desc id="cp-desc">Row one: a page image of the 1777 printing is read by two independent OCR engines; every leaf is then read in full against the image and every decision is recorded; an assembler emits characters only from the OCR files and the recorded edits, producing the diplomatic text, which an independent reconstruction must reproduce byte for byte. Row two: a deterministic normalization produces the reading text; every unit receives a stable identifier and a citation URI; a hash-pinned corpus package carries the text into the Reading Desk, which constructs displayed quotations from it and verifies them.</desc>',
         f'<style>{STYLE}</style>',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#1f1f1f"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    bw, bh, gap = 184, 82, 16
    xs = [16 + i * (bw + gap) for i in range(4)]
    y1 = 32
    p.append(text(16, 18, 'FROM PAGE IMAGE TO DIPLOMATIC TEXT', 't row', 'start'))
    row1 = [('Page image', ['a leaf of the 1777 printing,', 'identified by checksum']),
            ('Two OCR readings', ['independent engines; where', 'they disagree, a site to decide']),
            ('Full reading of every leaf', ['read against the image;', 'every decision recorded']),
            ('Diplomatic text', ['only OCR characters and', 'recorded edits; page-faithful'])]
    for i, (t, b) in enumerate(row1):
        p.append(box(xs[i], y1, bw, bh, t, b, 'evid' if i == 3 else 'box'))
        if i < 3:
            p.append(arrow(f'M{xs[i] + bw + 2} {y1 + bh / 2} L{xs[i + 1] - 3} {y1 + bh / 2}'))
    p.append(text(xs[3] + bw, y1 + bh + 17, 'an independent reconstruction must match it byte for byte', 't tiny', 'end'))
    y2 = 190
    p.append(arrow(f'M{xs[3] + bw / 2} {y1 + bh + 26} L{xs[3] + bw / 2} {y1 + bh + 40} L{xs[0] + bw / 2} {y1 + bh + 40} L{xs[0] + bw / 2} {y2 - 3}'))
    p.append(text(16, y2 - 12, 'FROM DIPLOMATIC TEXT TO THE READER', 't row', 'start'))
    row2 = [('Normalized text', ['a deterministic derivative for', 'reading; versioned rules']),
            ('Identifiers and index', ['216 units; E.4.19 and', 'urn:hume:ehu:4.19']),
            ('Corpus package', ['built from the sealed baseline;', 'SHA-256 pinned at release']),
            ('Reading Desk', ['quotations constructed from the', 'package and verified at display'])]
    for i, (t, b) in enumerate(row2):
        p.append(box(xs[i], y2, bw, bh, t, b, 'evid' if i == 2 else 'box'))
        if i < 3:
            p.append(arrow(f'M{xs[i] + bw + 2} {y2 + bh / 2} L{xs[i + 1] - 3} {y2 + bh / 2}'))
    p.append(text(xs[2] + bw / 2, y2 + bh + 17, 'engineering baseline: rebuild from the frozen sources is byte-identical', 't tiny'))
    p.append('<rect x="16" y="306" width="22" height="12" rx="3" class="evid"/>')
    p.append(text(44, 316, 'the evidential text and its hash-pinned package', 't tiny', 'start'))
    p.append('</svg>')
    return '\n'.join(p)


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'reports/src/figures/corpus-pipeline.svg')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding='utf-8')
    print('wrote', out)


if __name__ == '__main__':
    main()
