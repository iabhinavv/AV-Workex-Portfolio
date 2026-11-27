# Abhinav’s Workex

Static, responsive portfolio. Open `index.html` through a local web server:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Visit http://localhost:8765. The HTML, CSS, JavaScript and assets can be hosted directly on GitHub Pages; no production build or package install is required.

## Editing

- Career copy and timelines: the six root career HTML files.
- Layout and responsive styles: `assets/styles.css`.
- Career colours and portrait framing: `assets/themes.css`.
- SOP reading controls and print layout: `assets/sop-reader.js` and `assets/sop-reader.css`.
- Globe rendering: `assets/app.js`; colours are independent of career themes.
- In-place career navigation: `assets/navigation.js`.
- Shared mobile navigation: `assets/menu.js`.
- Lightweight viewport entrances and the visible timeline stream: `assets/motion.js`.

The CA Firm and Vayoo logos are the only company logos included. The favicon and header use the supplied portrait. Do not add HSBC, GWO SEVO or consulting-network logos without permission.

## Rebuilding documentation

The concise, editable SOP Markdown lives in `docs/source/`. The builder creates static HTML readers and complete branded PDFs in `assets/pdfs/`. Visitors need no document library or account.

```sh
python3 -m venv /tmp/workex-docs-env
/tmp/workex-docs-env/bin/pip install -r tools/requirements.txt
/tmp/workex-docs-env/bin/python tools/render_sops.py
```

`render_sops.py` generates contents links, collapsed detail sections, keyboard-accessible tables and the matching career theme. It also builds PDF copies through `tools/sop_pdf.py` and checks document anchors. To add another supplied SOP, put its Markdown in `docs/source/`, add its entry to `DOCUMENTS`, rebuild, and add its document card to the relevant career page.

## Documentation coverage

- CA Firm: the supplied CA firm master SOP, in its navy/teal theme.
- Affiliate Network: the supplied concise affiliate-network operations SOP, in its consulting theme. The page retains the original GWO SEVO attribution and presents it as an industry reference.
- GWO SEVO: the merchant/creator playbook and concise operations SOP, in its green/slate theme.
- HSBC and Vayoo intentionally have no SOP links, as requested.

The three Markdown guides are condensed from the supplied material into practical steps, owners, review points and hand-offs. Longer checks use native `<details>` sections. The two affiliate-operations readers share a source; the Affiliate Network version retains a short process-reference attribution. The original attached documents remain unchanged outside this repository.

## Verification

```sh
python3 tools/check_site.py
python3 tools/check_seo.py
node --check assets/app.js
node --check assets/navigation.js
node --check assets/menu.js
node tools/check_motion.js
node tools/check_sop_reader.js
python3 tools/check_sops.py
```

Also check career navigation, globe continuity, reader navigation and layouts at phone and desktop widths in a browser. Reduced-motion preferences are respected.

## Search metadata

The verified public base is https://iabhinavv.github.io/AV-Workex-Portfolio/. `tools/seo.py` owns page titles, descriptions, canonical links, social metadata, profile/page markup and `sitemap.xml`.

```sh
python3 tools/seo.py
python3 tools/check_seo.py
```

The SOP builder calls the SEO builder after rendering. Change `SITE_URL` there before publishing on another domain. The two concise SOP readers share a canonical; all other useful pages retain their own. A project-level robots file is not the hostname’s root robots policy.

`docs/seo-review.md` contains the findings, keyword intent map, primary sources, verification steps and the limits of the review. No search-volume, ranking, indexing or Core Web Vitals result is invented. Search-engine submission and publishing are separate actions.

Homepage education comes from the supplied CV. Keep the IIT Madras degree marked online and in progress until its status changes.

Motion uses short opacity/transform effects. Primary content remains in source HTML, with visible no-script and reduced-motion fallbacks. Two staggered travellers hand off between the six jobs, below the icon layer. The second starts six seconds after the first, when the first reaches Vayoo. Each takes ten seconds to reach GWO SEVO and repeats on a twelve-second cycle; the spine ends at the final job without an arrow. Motion pauses while the timeline is offscreen. Page entrances and scroll reveals run together, with brief staggered delays. Reduced-motion preferences disable these effects. Certificate issue dates are intentionally omitted; education uses plain entries rather than panels.

Headings and numeric typography use locally hosted Manrope (600 for headings and 700 for numbers). Font files and the SIL Open Font License are in `assets/fonts/`, sourced from Google Fonts. The Affiliate Network chapter separates website-inventory project leadership from $100K in agrotech project assets managed.


Each career page includes a responsive vector workflow between responsibilities and projects, styled by `assets/work-visuals.css`. The diagrams are ordinary HTML, accessible tables and decorative inline SVGs; they need no chart library. CA Firm and affiliate diagrams use the supplied SOPs. HSBC and Vayoo use the confirmed role descriptions. Financial workpapers contain categories and supporting schedules, not fabricated client balances, and marketing flows contain no invented campaign figures.

SOP readers offer Print / Save PDF, Download PDF, Expand details and Collapse details. Printing includes all checklists and restores the reader’s expansion choices afterward. The print layout and downloadable PDFs include Abhinav Verma’s watermark, name, LinkedIn, GitHub and email; PDF contact links are clickable on every page.
