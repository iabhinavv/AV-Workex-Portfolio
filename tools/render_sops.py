# Rebuild static SOP pages from the supplied Markdown. No runtime dependencies.
from pathlib import Path
from html import escape
import re
import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = [
    ("affiliate-network", "consulting", "Affiliate Network", "Affiliate network operations",
     "The affiliate operating model: merchant and publisher onboarding, campaign tracking, reporting and settlement.",
     "gwo-sevo-operations", "Originally prepared for GWO SEVO, this reference playbook explains the affiliate-network operating model."),
    ("gwo-sevo-operations", "gwo-sevo", "GWO SEVO", "Affiliate network operations",
     "A concise operating procedure for merchant acquisition, partner onboarding, tracking, reporting and settlement."),
    ("ca-firm", "ca-article", "CA Firm", "Audit, accounting & taxation",
     "Client files, reconciliations, audit workpapers and review controls."),
    ("gwo-sevo", "gwo-sevo", "GWO SEVO", "Affiliate & creator network",
     "Merchant development, creator onboarding, campaign workflows and reporting."),
]

def render(slug, page, name, title, description, source_slug=None, attribution=None):
    career = (ROOT / f"{page}.html").read_text()
    source = (ROOT / "docs/source" / f"{source_slug or slug}.md").read_text()
    # The reader supplies its own title and contents from the actual headings.
    source = re.sub(r"^# .+\n", "", source, count=1)
    source = re.sub(r"^\*\*Navigation:\*\*.*$", "", source, flags=re.M)
    source = re.sub(r"(?<![<(])(https?://[^\s<>]+)", r"<\1>", source)
    converter = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "sane_lists"],
                                  extension_configs={"toc": {"toc_depth": "2-3"}})
    content = converter.convert(source)
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
<link rel="stylesheet" href="assets/styles.css"><link rel="stylesheet" href="assets/themes.css">
<script defer src="assets/menu.js"></script>
</head><body data-page="{page}">
<a class="skip-link" href="#main">Skip to content</a><div class="sky" aria-hidden="true"></div>{header}
<main id="main" class="wrap document-main" tabindex="-1">
<header class="document-header">
<a class="back-link" href="{page}.html">Back to {escape(name)}</a>
{mark}<span class="eyebrow accent">{escape(name)} · Documentation</span>
<h1>{escape(title)}<br><em>Operating playbook.</em></h1><p class="lede">{escape(description)}</p>
</header>
{attribution_html}
<div class="document-layout">
<details class="document-contents" open><summary>In this document</summary><nav aria-label="Document contents">{converter.toc}</nav></details>
<article class="sop-content" aria-label="{escape(name)} standard operating procedure">{content}</article>
</div><div class="document-return"><a class="btn" href="{page}.html">Back to {escape(name)}</a></div>
</main>{footer}
</body></html>'''
    assert '<h2 id=' in html and 'class="table-scroll"' in html
    ids = set(re.findall(r'\bid="([^"]+)"', html))
    missing = {href for href in re.findall(r'href="#([^"]+)"', html) if href not in ids}
    assert not missing, f"Broken document anchors: {missing}"
    (ROOT / f"{slug}-sop.html").write_text(html)
    print(f"Built {slug}-sop.html")

if __name__ == "__main__":
    for document in DOCUMENTS:
        render(*document)
