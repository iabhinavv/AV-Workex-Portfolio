# Abhinav’s Workex

Static, responsive portfolio. Open `index.html` through a local web server:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Visit http://localhost:8765. The HTML, CSS, JavaScript and assets can be hosted directly on GitHub Pages; no production build or package install is required.

## Editing

- Career copy and timelines: the six root career HTML files.
- Layout and responsive styles: `assets/styles.css`.
- Career colours, portrait framing and document reader: `assets/themes.css`.
- Globe rendering: `assets/app.js`; colours are independent of career themes.
- In-place career navigation: `assets/navigation.js`.
- Shared mobile navigation: `assets/menu.js`.

The CA Firm and Vayoo logos are the only company logos included. The favicon and header use the supplied portrait. Do not add HSBC, GWO SEVO or consulting-network logos without permission.

## Rebuilding documentation

The supplied Markdown lives in `docs/source/`. Generated SOP HTML is saved as ordinary static pages, so visitors need no Markdown library.

```sh
python3 -m venv /tmp/workex-docs-env
/tmp/workex-docs-env/bin/pip install -r tools/requirements.txt
/tmp/workex-docs-env/bin/python tools/render_sops.py
```

`render_sops.py` generates contents links, scrollable keyboard-accessible tables and the matching career theme. It checks internal document anchors during generation. To add another supplied SOP, put its Markdown in `docs/source/`, add its entry to `DOCUMENTS`, rebuild, and add its document card to the relevant career page.

## Documentation coverage

- CA Firm: the supplied CA firm master SOP, in its navy/teal theme.
- Affiliate Network: the supplied concise affiliate-network operations SOP, in its consulting theme. The page retains the original GWO SEVO attribution and presents it as an industry reference.
- GWO SEVO: the detailed build record and concise operations SOP, in its green/slate theme.
- HSBC and Vayoo intentionally have no SOP links, as requested.

All three supplied Markdown files are preserved in `docs/source/`. The Affiliate Network reader and GWO SEVO reader share the same concise source, avoiding duplicate Markdown copies. No new SOP content or historical project outcomes were invented.

## Verification

```sh
python3 tools/check_site.py
node --check assets/app.js
node --check assets/navigation.js
node --check assets/menu.js
```

Also check career navigation, globe continuity, reader navigation and layouts at phone and desktop widths in a browser. Reduced-motion preferences are respected.
