# Rebuild the concise SOP readers and their complete PDF copies.
from pathlib import Path
from html import escape
import re
import markdown
from sop_pdf import render_pdf

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    ("affiliate-network", "consulting", "Affiliate Network", "Affiliate network operations",
     "A practical guide to merchant qualification, partner onboarding, campaign tracking, reporting and settlement.",
     "gwo-sevo-operations", "Process reference: GWO SEVO affiliate network operations."),
    ("gwo-sevo-operations", "gwo-sevo", "GWO SEVO", "Affiliate network operations",
     "Clear hand-offs from the merchant brief to partner activation, tracking, reporting and settlement."),
    ("ca-firm", "ca-article", "CA Firm", "Audit, accounting & taxation",
     "A practical workflow for client records, book finalisation, tax compliance, audit review and file closure."),
    ("gwo-sevo", "gwo-sevo", "GWO SEVO", "Affiliate & creator network",
     "A working guide to merchant development, creator shortlists, onboarding files, campaign delivery and reporting."),
]


def render(slug, page, name, title, description, source_slug=None, attribution=None):
    career = (ROOT / f"{page}.html").read_text()
    source = (ROOT / "docs/source" / f"{source_slug or slug}.md").read_text()
    source = re.sub(r"^# .+\n", "", source, count=1)
    converter = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists", "md_in_html"],
                                  extension_configs={"toc": {"toc_depth": "2"}})
    content = converter.convert(source)
    pdf_name = f"{slug}-sop.pdf"
    render_pdf(ROOT / "assets/pdfs" / pdf_name, title, name, page, content)
    content = re.sub(r"<table>(.*?)</table>",
                     r'<div class="table-scroll" role="region" aria-label="Reference table" tabindex="0"><table>\1</table></div>',
                     content, flags=re.S)
    header = re.search(r'<header class="topbar">.*?</header>', career, re.S).group()
    footer = re.search(r'<footer class="footer wrap">.*?</footer>', career, re.S).group()
    mark = re.search(r'<div class="company-mark">.*?</div>', career, re.S)
    mark = mark.group() if mark else ""
    attribution_html = f'<p class="document-attribution">{escape(attribution)}</p>' if attribution else ""
    html = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(name)} — {escape(title)} SOP | Abhinav’s Workex</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="icon" href="assets/abhinav-portrait.png" type="image/png">
<link rel="preload" href="assets/fonts/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css"><link rel="stylesheet" href="assets/themes.css"><link rel="stylesheet" href="assets/sop-reader.css">
<script defer src="assets/menu.js"></script><script defer src="assets/motion.js"></script><script defer src="assets/sop-reader.js"></script>
</head><body data-page="{page}">
<a class="skip-link" href="#main">Skip to content</a><div class="sky" aria-hidden="true"></div>{header}
<main id="main" class="wrap document-main" tabindex="-1">
<header class="document-header">
<a class="back-link" href="{page}.html">Back to {escape(name)}</a>
{mark}<span class="eyebrow accent">{escape(name)} · Documentation</span>
<h1>{escape(title)}<br><em>Operating playbook.</em></h1><p class="lede">{escape(description)}</p>
<p class="document-author">A practical process guide by <strong>Abhinav Verma</strong></p>
<div class="document-actions" role="group" aria-label="Document actions">
<button class="btn primary" type="button" data-sop-action="print">Print / Save PDF</button>
<a class="btn" href="assets/pdfs/{pdf_name}" download>Download PDF</a>
<button class="btn" type="button" data-sop-action="expand">Expand details</button>
<button class="btn" type="button" data-sop-action="collapse">Collapse details</button>
</div><p class="document-print-hint">PDF copies include all checklists, my name and contact links.</p>
</header>
{attribution_html}
<div class="document-layout">
<details class="document-contents" open><summary>In this document</summary><nav aria-label="Document contents">{converter.toc}</nav></details>
<article class="sop-content" aria-label="{escape(name)} standard operating procedure">{content}</article>
</div><div class="document-return"><a class="btn" href="{page}.html">Back to {escape(name)}</a></div>
</main>{footer}
<div class="sop-print-watermark" aria-hidden="true">ABHINAV VERMA</div>
<footer class="sop-print-footer"><strong>Abhinav Verma · Abhinav’s Workex</strong>
<a href="https://www.linkedin.com/in/iabhinavv">linkedin.com/in/iabhinavv</a> ·
<a href="https://github.com/iabhinavv">github.com/iabhinavv</a> ·
<a href="mailto:abhinaverma124@gmail.com">abhinaverma124@gmail.com</a></footer>
</body></html>'''
    assert '<h2 id=' in html and 'class="table-scroll"' in html and '<details>' in html
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    missing = {href for href in re.findall(r'href="#([^"]+)"', html) if href not in ids}
    assert not missing, f"Broken document anchors: {missing}"
    (ROOT / f"{slug}-sop.html").write_text(html)
    print(f"Built {slug}-sop.html and {pdf_name} ({len(source.split())} words)")


if __name__ == "__main__":
    for document in DOCUMENTS:
        render(*document)
    from seo import apply_site_seo
    apply_site_seo()
