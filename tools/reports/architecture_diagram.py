#!/usr/bin/env python3
"""Technical architecture figure for Report 1 (standard library only).

Draws the Reading Desk as deployed to a University platform: the browser, the University's
authenticating proxy, the application's three processes from one image, PostgreSQL, the
external inference API reached from the worker only, and the platform services. Solid
outlines are components implemented and tested in development; dashed outlines are
University or external services that have not been provisioned, tested or approved.

The viewBox is kept narrow (820 units across a 6.5-inch column) so that the smallest text
prints at about 7 points.

    python3 tools/reports/architecture_diagram.py reports/src/figures/architecture.svg
"""
import pathlib
import sys

W, H = 820, 560
STYLE = """
.t { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; fill: #1f1f1f; }
.title { font-size: 17px; font-weight: 600; }
.label { font-size: 13.5px; font-weight: 600; }
.tiny { font-size: 12px; fill: #5f6368; }
.burg { fill: #7a1e2e; }
.solid { fill: #fff; stroke: #7a1e2e; stroke-width: 1.6; }
.image { fill: #f7f4ef; stroke: #7a1e2e; stroke-width: 1.6; }
.proc { fill: #fff; stroke: #7a1e2e; stroke-width: 1.3; }
.dashed { fill: #fff; stroke: #5f6368; stroke-width: 1.4; stroke-dasharray: 6 4; }
.flow { fill: none; stroke: #1f1f1f; stroke-width: 1.6; }
.gold { fill: none; stroke: #d9a62b; stroke-width: 2.4; }
.legend-solid { fill: none; stroke: #7a1e2e; stroke-width: 1.6; }
.legend-dashed { fill: none; stroke: #5f6368; stroke-width: 1.4; stroke-dasharray: 6 4; }
"""


def text(x, y, s, cls='t tiny', anchor='middle'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{s}</text>'


def lines(x, y, items, cls='t tiny', anchor='middle', dy=14):
    return '\n'.join(text(x, y + i * dy, s, cls, anchor) for i, s in enumerate(items))


def rect(x, y, w, h, cls, r=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}"/>'


def arrow(d, cls='flow', marker='arrow'):
    return f'<path d="{d}" class="{cls}" marker-end="url(#{marker})"/>'


def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="arch-title arch-desc">',
         '<title id="arch-title">HumeBot Reading Desk: proposed University deployment</title>',
         '<desc id="arch-desc">A browser reaches the University sign-in gateway, which authenticates every request and passes one identity header to the Reading Desk web process. The web process, a worker process and a one-off migration job run from one container image that also carries the pinned corpus, the replay bundle and the HumeBot verification core. The web and worker processes use a managed PostgreSQL database with append-only history. Only the worker calls the external inference API, sending the question text and corpus evidence and never a student identity. Platform services (secrets, registry, ingress, logs, monitoring) surround the application. Solid outlines mark components implemented and tested in development; dashed outlines mark University or external services that are not provisioned or approved.</desc>',
         f'<style>{STYLE}</style>',
         '<defs>'
         '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#1f1f1f"/></marker>'
         '<marker id="arrow-gold" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#d9a62b"/></marker>'
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']

    # --- browser ---
    p += [rect(10, 112, 142, 66, 'solid'),
          text(81, 140, 'Student / instructor', 't label'),
          text(81, 160, 'web browser · HTTPS', 't tiny')]
    p += [arrow('M154 145 L162 145')]

    # --- University proxy (dashed) ---
    p += [rect(164, 92, 150, 104, 'dashed'),
          text(239, 120, 'University sign-in', 't label'),
          text(239, 137, 'gateway (proposed)', 't label'),
          lines(239, 158, ['authenticating proxy', 'one identity header;', 'client copies stripped'], 't tiny', 'middle', 13)]
    p += [arrow('M316 145 L328 145')]

    # --- application image ---
    ix, iy, iw, ih = 330, 40, 290, 470
    p += [rect(ix, iy, iw, ih, 'image', 10),
          text(ix + iw / 2, iy + 26, 'Reading Desk application', 't title burg'),
          text(ix + iw / 2, iy + 44, 'one container image · non-root · read-only filesystem', 't tiny')]
    px, pw = ix + 20, iw - 40
    p += [rect(px, 96, pw, 84, 'proc'),
          text(px + 12, 118, 'web', 't label', 'start'),
          lines(px + 12, 136, ['Django · gunicorn · port 8000', 'pages, questions, Evidence Inspector',
                               '/healthz · /readyz'], 't tiny', 'start')]
    p += [rect(px, 192, pw, 98, 'proc'),
          text(px + 12, 214, 'worker', 't label', 'start'),
          lines(px + 12, 232, ['answers queued questions with the frozen', 'pipeline: analyze · select evidence · explain',
                               'the only process with outbound model calls', 're-verifies, then commits in one transaction'],
                't tiny', 'start')]
    p += [rect(px, 302, pw, 52, 'proc'),
          text(px + 12, 324, 'migrate', 't label', 'start'),
          text(px + 12, 342, 'one-off job per release (schema owner)', 't tiny', 'start')]
    p += [rect(px, 366, pw, 112, 'proc'),
          text(px + 12, 388, 'pinned in the image', 't label', 'start'),
          lines(px + 12, 406, ['HumeBot core: verification, contract, gates', 'corpus package: Enquiry I–IX, 1777 text',
                               'replay bundle: 20 recorded answers', 'both hash-pinned at release',
                               'no model weights · no student data'], 't tiny', 'start')]

    # --- inference API (dashed) ---
    p += [rect(636, 60, 172, 152, 'dashed'),
          text(722, 86, 'Approved inference', 't label'),
          text(722, 103, 'API (proposed)', 't label'),
          lines(722, 124, ['external provider · TLS', 'receives the question text', 'and the corpus evidence;',
                           'never a student identity', 'frozen settings; served', 'model checked against pin'], 't tiny')]
    p += [arrow('M602 232 C 622 232, 622 140, 634 140', 'gold', 'arrow-gold')]

    # --- PostgreSQL (dashed) ---
    p += [rect(636, 330, 172, 150, 'dashed'),
          text(722, 352, 'Managed PostgreSQL', 't label'),
          text(722, 369, '(proposed)', 't label'),
          lines(722, 390, ['TLS required', 'schemas: ops · instr · research', '(research stays empty)',
                           'roles: owner · app · admin', 'append-only history', 'backups; tested restore'], 't tiny')]
    p += [arrow('M602 150 C 622 150, 622 395, 634 395'),
          arrow('M602 262 C 622 262, 622 410, 634 410')]

    # --- platform services (dashed) ---
    p += [rect(330, 522, 478, 30, 'dashed'),
          text(569, 541, 'Platform services (proposed): secrets · registry · ingress and TLS · logs · monitoring', 't tiny')]

    # --- local development stand-ins ---
    p += [lines(16, 236, ['Local development only (never deployed):', 'synthetic sign-in page; mock model service',
                          'serving recorded answers; Compose stack.'], 't tiny', 'start', 14)]

    # --- legend ---
    p += ['<rect x="16" y="436" width="24" height="13" rx="3" class="legend-solid"/>',
          text(48, 447, 'implemented and tested in development', 't tiny', 'start'),
          '<rect x="16" y="458" width="24" height="13" rx="3" class="legend-dashed"/>',
          lines(48, 469, ['proposed University or external service:', 'not provisioned, tested or approved'], 't tiny', 'start', 14),
          '<path d="M16 503 L40 503" class="gold"/>',
          text(48, 507, 'outbound model call, worker only', 't tiny', 'start')]
    p.append('</svg>')
    return '\n'.join(p)


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'reports/src/figures/architecture.svg')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding='utf-8')
    print('wrote', out)


if __name__ == '__main__':
    main()
