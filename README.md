# humebot-site

This repository contains **only the public HumeBot project website**. It is a small static site:
- HTML and CSS only;
- no build step, framework or scripts;
- no analytics, cookies or forms.

Open `index.html` locally to preview it.

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

## Structure

| file | purpose |
|---|---|
| `index.html` | The site: a single research-project home page |
| `open-weight-research.html` | Open-Weight Model Research: an overview of the project's open-weight research direction |
| `about.html`, `how-it-works.html`, `evidence.html`, `status.html`, `university-it.html` | Superseded-page notices for the pages retired in November 2026, each linking to the relevant part of the home page |
| `assets/` | Stylesheet and favicon |
| `assets/screenshots/` | Three screenshots of the development build, with synthetic data only |

## History

- **2026-09-24.** Initial site: six pages and a one-page executive brief for University IT.
- **2026-11 (V1).** Reorganized as a single research-project home page:
  - the earlier pages became superseded-page notices;
  - the executive brief was withdrawn;
  - a small gallery of development-build screenshots, with synthetic data, was added;
  - an Open-Weight Model Research page was added.

Earlier versions, including the withdrawn brief, remain in this repository's history.
