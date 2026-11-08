# humebot-site

This repository contains **only the public HumeBot project website**. It is a small static site:
- HTML and CSS only, with one inline SVG diagram in two layouts;
- no build step, framework or scripts on the site; `tools/harness_diagram.py` (standard-library Python, run by hand) regenerates the diagram's SVG files in `assets/diagram/`;
- no analytics, cookies or forms.

Open `index.html` locally to preview it, or serve the directory with any static file server.

It is **separate from the HumeBot research and development repository**, which is not public. Nothing from that
repository is copied here wholesale.

## Rules for this repository

- **Substantive project claims are curated manually.** Every factual statement on the site is written by hand from
  project documents, checked against them, and published only with the faculty lead's approval; see
  `PUBLIC_CONTENT_SOURCES.md`.
- **Website content is never generated automatically from internal repository material.** That means no raw traces, prompts,
  schemas, decision logs, study records or internal paths.
- **No student data belongs in this repository**, ever.
- **No unpublished course materials or internal research records.** That includes lecture notes, evaluation records and
  decoding keys.
- **Screenshots and recordings** only if they show synthetic data and have been reviewed for release.
- No credentials, tokens or configuration secrets belong here.
- **HumeBot is an academic project.** The site must not imply University sponsorship, official status, endorsement,
  external funding or partnerships. It uses no University names, marks or logos beyond plain reference.

## Structure (V2, November 2026)

| file | purpose |
|---|---|
| `index.html` | Home: what HumeBot is, why it exists, the governing educational principle |
| `how-it-works.html` | How It Works: the three stages, verification, typed responses, the instructor's view, the proposed hosting arrangement |
| `demo.html` | Demo: a recorded walk through the Reading Desk, with captions and a transcript |
| `reports.html` | Reports: educational design, the overview for University IT, what has been evaluated, the decisions that remain |
| `open-weight-research.html` | Open-Weight Model Research, linked from Reports |
| `about.html`, `evidence.html`, `status.html`, `university-it.html` | Superseded-page notices for pages retired in November 2026, each linking to the current page |
| `assets/` | Stylesheet and favicon |
| `assets/screenshots/` | Screenshots of the development build from V1, synthetic data only |
| `assets/demo/` | The demonstration recording (WebM), its poster, captions (WebVTT) and key-moment screenshots, synthetic data only |
| `assets/diagram/`, `tools/harness_diagram.py` | The How It Works diagram (landscape and portrait SVG) and the script that generates it |

## History

- **2026-09-24.** Initial site: six pages and a one-page executive brief for University IT.
- **2026-11 (V1).** Reorganized as a single research-project home page; the earlier pages became superseded-page notices;
  the executive brief was withdrawn; a screenshot gallery and an Open-Weight Model Research page were added.
- **2026-11 (V2).** Reorganized into four pages, Home, How It Works, Demo and Reports, for an introduction to University IT
  and cloud-infrastructure colleagues; the governing educational principle added; a recorded demonstration added.

Earlier versions, including the withdrawn brief, remain in this repository's history.
