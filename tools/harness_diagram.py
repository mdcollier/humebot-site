"""HumeBot workflow diagram: an AI model inside a normative harness. Emits two SVGs from one source (landscape for desktop,
portrait for phones) using the site's colour tokens as CSS variables with light-mode fallbacks, so the inlined figure
follows the page's light and dark schemes. Standard library only; no runtime dependency on the site.

    python3 harness_diagram.py OUT_DIR
"""
import pathlib
import re
import sys

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, Charter, Georgia, serif"
STYLE = f"""
  .paper {{ fill: var(--paper, #fcfbf8); }}
  .panel {{ fill: var(--panel, #f3f1eb); }}
  .ink {{ fill: var(--ink, #1b1e23); }}
  .muted {{ fill: var(--muted, #4b5260); }}
  .acc-s {{ stroke: var(--accent, #1f3a56); }}
  .acc-f {{ fill: var(--accent, #1f3a56); }}
  .gold-s {{ stroke: var(--gold, #b8862b); }}
  .gold-f {{ fill: var(--gold, #b8862b); }}
  .rule-s {{ stroke: var(--rule, #dad6cc); }}
  text {{ font-family: {FONT}; }}
  .serif {{ font-family: {SERIF}; }}
  .t-title {{ font-size: 22px; font-weight: 700; }}
  .t-label {{ font-size: 17px; font-weight: 600; }}
  .t-stage {{ font-size: 16px; font-weight: 600; }}
  .t-small {{ font-size: 13px; }}
  .t-rule {{ font-size: 11.5px; letter-spacing: .06em; text-transform: uppercase; font-weight: 600; }}
  .flow {{ fill: none; stroke-width: 2.5; }}
  .flow-thin {{ fill: none; stroke-width: 2; }}
  .govern {{ fill: none; stroke-width: 2.5; stroke-dasharray: 7 6; }}
  .frame {{ fill: none; stroke-width: 3.5; }}
  .frame-in {{ fill: none; stroke-width: 1.2; }}
"""


def defs(k=""):
    return f"""<defs>
    <marker id="head{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="acc-f"/></marker>
    <marker id="head-gold{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="gold-f"/></marker>
  </defs>
  <style>{STYLE}</style>"""


def text(x, y, s, cls='t-label ink', anchor='middle', extra=''):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" {extra}>{s}</text>'


def pill(x, y, w, h, label, sub=None, cls='paper acc-s'):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" class="{cls}" stroke-width="2"/>']
    cy = y + h / 2 + (0 if sub is None else -6)
    out.append(text(x + w / 2, cy + 6, label, 'serif t-label ink'))
    if sub:
        out.append(text(x + w / 2, cy + 24, sub, 't-small muted'))
    return '\n'.join(out)


def stage(cx, cy, r, label, n, label_dy=None):
    dy = label_dy if label_dy is not None else r + 26
    return '\n'.join([
        f'<circle cx="{cx}" cy="{cy}" r="{r}" class="paper acc-s" stroke-width="2.5"/>',
        text(cx, cy + 8, str(n), 'serif t-title acc-f'),
        text(cx, cy + dy, label, 't-stage ink')])


def book(x, y, w, h, title, sub):
    """Hume's verified text: a closed book, spine on the left."""
    return '\n'.join([
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" class="panel gold-s" stroke-width="2.5"/>',
        f'<line x1="{x+14}" y1="{y+4}" x2="{x+14}" y2="{y+h-4}" class="gold-s" stroke-width="2"/>',
        text(x + 14 + (w - 14) / 2, y + h / 2 - 2, title, 'serif t-label ink'),
        text(x + 14 + (w - 14) / 2, y + h / 2 + 18, sub, 't-small muted')])


def seal(cx, cy, r=24):
    """The verification gate on the harness boundary: a check inside a ring. The frame checks; the model does not."""
    return '\n'.join([
        f'<circle cx="{cx}" cy="{cy}" r="{r}" class="paper acc-s" stroke-width="3"/>',
        f'<path d="M{cx-11} {cy+1} L{cx-3} {cy+9} L{cx+12} {cy-8}" fill="none" class="acc-s" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'])


def desk(x, y, w, h, stacked):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="paper acc-s" stroke-width="2.5"/>',
           text(x + w / 2, y + 30, 'Reading Desk', 'serif t-label ink')]
    pad, top = 14, y + 46
    if stacked:
        ph = (h - 46 - pad * 3) / 2
        out += [f'<rect x="{x+pad}" y="{top}" width="{w-2*pad}" height="{ph}" rx="6" class="panel rule-s" stroke-width="1.5"/>',
                text(x + w / 2, top + ph / 2 + 5, "Hume's text", 't-stage ink'),
                f'<rect x="{x+pad}" y="{top+ph+pad}" width="{w-2*pad}" height="{ph}" rx="6" class="panel rule-s" stroke-width="1.5"/>',
                text(x + w / 2, top + ph + pad + ph / 2 - 4, "HumeBot's", 't-stage ink'),
                text(x + w / 2, top + ph + pad + ph / 2 + 16, "explanation", 't-stage ink')]
    else:
        pw = (w - 3 * pad) / 2
        ph = h - 46 - pad * 2
        out += [f'<rect x="{x+pad}" y="{top}" width="{pw}" height="{ph}" rx="6" class="panel rule-s" stroke-width="1.5"/>',
                text(x + pad + pw / 2, top + ph / 2 + 5, "Hume's text", 't-stage ink'),
                f'<rect x="{x+2*pad+pw}" y="{top}" width="{pw}" height="{ph}" rx="6" class="panel rule-s" stroke-width="1.5"/>',
                text(x + 2 * pad + pw * 1.5, top + ph / 2 + 5, "HumeBot's explanation", 't-stage ink')]
    return '\n'.join(out)


def frame(x, y, w, h):
    return '\n'.join([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" class="frame acc-s"/>',
                      f'<rect x="{x+7}" y="{y+7}" width="{w-14}" height="{h-14}" rx="16" class="frame-in acc-s"/>'])


DESC = "A student question enters HumeBot's normative harness. Inside, the AI model analyzes the question, selects evidence and explains; Hume's verified text supplies the evidence to the selection stage only; the software rules of the harness govern the evidence, the citations, the structure of the response and its verification. The answer leaves the harness only through a verification seal, to the Reading Desk, which shows Hume's text beside HumeBot's explanation. The instructor's dashed arrow ends at the harness boundary: course guidance and evidence inspection, not an input to the model. Instructor lectures and notes are not supplied to the generation model."


def landscape():
    W, H = 1060, 540
    fx, fy, fw, fh = 280, 110, 520, 400
    cy = fy + 160
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="hb-title hb-desc">',
             '<title id="hb-title">HumeBot: an AI model inside a normative harness</title>',
             f'<desc id="hb-desc">{DESC}</desc>',
             defs('-l'),
             pill(30, cy - 36, 200, 72, 'Student question'),
             f'<path d="M232 {cy} L{fx-4} {cy}" class="flow acc-s"/>',
             frame(fx, fy, fw, fh),
             text(fx + 24, fy + 40, "HumeBot's normative harness", 'serif t-title ink', 'start'),
             text(fx + fw / 2, fy + fh - 20, 'software rules: evidence · citations · structure · verification', 't-rule muted'),
             stage(fx + 100, cy, 40, 'Analyze', 1, label_dy=-58), f'<path d="M{fx+144} {cy} L{fx+216} {cy}" class="flow-thin acc-s"/>',
             stage(fx + 260, cy, 40, 'Select evidence', 2, label_dy=-58), f'<path d="M{fx+304} {cy} L{fx+376} {cy}" class="flow-thin acc-s"/>',
             stage(fx + 420, cy, 40, 'Explain', 3, label_dy=-58),
             book(fx + 160, fy + fh - 126, 200, 72, "Hume's verified text", 'Enquiry, 1777 edition'),
             f'<path d="M{fx+260} {fy+fh-128} L{fx+260} {cy+46}" class="flow-thin gold-s" marker-end="url(#head-gold-l)"/>',
             f'<path d="M{fx+462} {cy} L{fx+fw-28} {cy}" class="flow-thin acc-s"/>',
             seal(fx + fw, cy),
             f'<path d="M{fx+fw+26} {cy} L{fx+fw+74} {cy}" class="flow acc-s"/>',
             desk(fx + fw + 78, cy - 100, 180, 200, stacked=True),
             # the instructor, close above the harness: governance to the boundary, not a data flow into a stage
             pill(fx + 110, 12, 190, 56, 'Instructor'),
             f'<path d="M{fx+205} 70 L{fx+205} {fy-4}" class="govern gold-s"/>',
             text(fx + 222, 94, 'Course guidance · Evidence inspection', 't-small muted', 'start'),
             '</svg>']
    return '\n'.join(parts)


def portrait():
    W, H = 640, 1010
    fx, fy, fw, fh = 40, 170, 560, 560
    sx = fx + 110
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="hbp-title hbp-desc">',
             '<title id="hbp-title">HumeBot: an AI model inside a normative harness</title>',
             f'<desc id="hbp-desc">{DESC}</desc>',
             defs('-p'),
             pill(40, 30, 240, 72, 'Student question'),
             f'<path d="M160 104 L160 {fy-4}" class="flow acc-s"/>',
             pill(380, 38, 190, 56, 'Instructor'),
             f'<path d="M475 96 L475 {fy-4}" class="govern gold-s"/>',
             text(462, 124, 'Course guidance ·', 't-small muted', 'end'),
             text(462, 142, 'Evidence inspection', 't-small muted', 'end'),
             frame(fx, fy, fw, fh),
             text(fx + 24, fy + 40, "HumeBot's normative harness", 'serif t-title ink', 'start'),
             text(fx + fw / 2, fy + fh - 60, 'software rules: evidence · citations', 't-rule muted'),
             text(fx + fw / 2, fy + fh - 40, 'structure · verification', 't-rule muted'),
             stage(sx, fy + 130, 42, '', 1, label_dy=0), text(sx + 64, fy + 136, 'Analyze', 't-stage ink', 'start'),
             f'<path d="M{sx} {fy+176} L{sx} {fy+234}" class="flow-thin acc-s"/>',
             stage(sx, fy + 280, 42, '', 2, label_dy=0), text(sx + 64, fy + 286, 'Select evidence', 't-stage ink', 'start'),
             f'<path d="M{sx} {fy+326} L{sx} {fy+384}" class="flow-thin acc-s"/>',
             stage(sx, fy + 430, 42, '', 3, label_dy=0), text(sx + 64, fy + 436, 'Explain', 't-stage ink', 'start'),
             book(fx + 330, fy + 350, 200, 80, "Hume's verified text", 'Enquiry, 1777 edition'),
             f'<path d="M{fx+330} {fy+380} L{sx+40} {fy+318}" class="flow-thin gold-s" marker-end="url(#head-gold-p)"/>',
             f'<path d="M{sx} {fy+476} L{sx} {fy+fh-30}" class="flow-thin acc-s"/>',
             seal(sx, fy + fh),
             f'<path d="M{sx} {fy+fh+28} L{sx} {fy+fh+72}" class="flow acc-s"/>',
             desk(40, fy + fh + 78, 560, 170, stacked=False),
             '</svg>']
    return '\n'.join(parts)


CLASSES = ('paper', 'panel', 'ink', 'muted', 'acc-s', 'acc-f', 'gold-s', 'gold-f', 'rule-s', 'serif', 't-title', 't-label', 't-stage',
           't-small', 't-rule', 'flow-thin', 'flow', 'govern', 'frame-in', 'frame')


def finish(svg, k):
    """Marker references on the paths (inline SVG styles are global to the page), then class names namespaced to hbd-."""
    svg = re.sub(r'class="(flow(?:-thin)? acc-s)"/>', rf'class="\1" marker-end="url(#head{k})"/>', svg)
    svg = re.sub(r'class="govern gold-s"/>', rf'class="govern gold-s" marker-end="url(#head-gold{k})"/>', svg)
    def ns(m):
        return 'class="' + ' '.join('hbd-' + c for c in m.group(1).split()) + '"'
    svg = re.sub(r'class="([^"]+)"', ns, svg)
    for c in sorted(CLASSES, key=len, reverse=True):
        svg = re.sub(rf'(?<![\w-])\.{re.escape(c)}(?![\w-])', f'.hbd-{c}', svg)
    return svg


def main():
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    (out / 'harness-landscape.svg').write_text(finish(landscape(), '-l'), encoding='utf-8')
    (out / 'harness-portrait.svg').write_text(finish(portrait(), '-p'), encoding='utf-8')
    print('wrote', out / 'harness-landscape.svg', out / 'harness-portrait.svg')


if __name__ == '__main__':
    main()
