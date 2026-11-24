# Abhinav’s Workex — SEO review and keyword map

Reviewed: 24 November 2026. Implementation is local in AV Workex; this run has not committed, pushed, published or submitted URLs to search engines.

## Evidence and scope

- Public site verified by a direct HTTP request: https://iabhinavv.github.io/AV-Workex-Portfolio/ returned **200**, with HTML content and no `X-Robots-Tag` response header. GitHub’s repository API returned `has_pages: true`.
- https://iabhinavv.github.io/robots.txt returned **404**. No root robots rules were available in that response. Crawl access and indexability are separate questions; these observations do not establish that Google has indexed the pages.
- The public project sitemap URL returned **404** before this patch. The local patch adds `sitemap.xml` with nine canonical URLs.
- Source inspection covered all ten HTML pages, their ordinary links, shared navigation and SOP generation. The portfolio content already exists in initial HTML; JavaScript enhances transitions rather than supplying the career text.
- Education was copied from the supplied CV: CA Intermediate, the IIT Madras BS marked online/in progress, and the two named certifications. Later user corrections about consulting outcomes, role dates and location privacy remain authoritative.
- The installed seo-technical skill’s linked `operating-contract.md`, `runtime-and-data.md`, `current-search-facts.md` and `technical-checks.md` files were absent at their resolved relative paths and were not found by filename search in the installed skills or Downloads. The supplied skill workflow was followed using source, HTTP and rendered observations, plus current primary Google documentation. No numerical SEO score is assigned.

## Findings, affected pages and changes

| Finding | Affected pages or templates | Patch and exact verification |
|---|---|---|
| Career titles primarily identified companies and the portfolio, with little personal search identity | Six career/home HTML pages | Distinct titles and descriptions now pair Abhinav Verma with the page’s actual work. `python3 tools/check_seo.py` checks uniqueness and exact metadata. |
| No canonical annotations; homepage has `/` and `index.html` forms | All ten HTML pages | Absolute canonical links use the verified HTTPS GitHub Pages base. `index.html` canonicalizes to `/`. Check the canonical after each browser navigation. |
| The concise SOP has two themed readers with the same underlying document | `affiliate-network-sop.html`, `gwo-sevo-operations-sop.html` | Both remain usable; the Affiliate reference canonical points to the original GWO operations SOP. That duplicate is omitted from the sitemap. The distinct longer GWO build record retains its own canonical. |
| Public sitemap missing at review | Site discovery | Add a nine-URL sitemap aligned with canonical intent. `python3 tools/check_seo.py` parses the XML and compares its URL set. |
| No identity or sharing metadata | All pages; homepage profile | Add Person/ProfilePage and WebSite markup on the homepage, WebPage and breadcrumbs on detail/reader pages, plus Open Graph and social preview metadata. No location, full-CA status, unearned credential, salary, job guarantee or review score is added. |
| Enhanced navigation updated only title and description | `assets/navigation.js` | Keep canonical, social, robots and JSON-LD metadata synchronized with the rendered route. Compare direct loads with tile/menu navigation. |
| Header chronology differed from career order | Every static page and generated reader | CA Firm → HSBC → Vayoo → Affiliate Network → GWO SEVO. Checks cover the full menu on all ten pages. |
| Homepage contained repeated introductory copy ahead of the career ledger | `index.html` | Shorten the hero, remove the screenshot’s heading/intro, start the ledger with 2021–present, add education immediately below, and move a concise “What I bring” to the end. Put broader context in the footer. |
| Crawl and index controls need deployment verification | Public host | Root robots response was 404; no observed `X-Robots-Tag` on the homepage. Local pages explicitly use `index, follow`. No project-level robots file was added: a file under `/AV-Workex-Portfolio/` is not the hostname’s authoritative `/robots.txt`. |
| Field/lab performance unknown | Entire site | No CrUX, Search Console, Lighthouse, LCP, INP or CLS measurements were obtained. Animation or asset costs are potential issues to measure, not demonstrated CWV failures. No CWV improvement claim is made. |

The canonical strategy follows [Google’s canonical URL guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls). Titles are concise and page-specific rather than repeated keyword lists, following [Google’s title-link guidance](https://developers.google.com/search/docs/appearance/title-link). Profile markup follows the [ProfilePage documentation](https://developers.google.com/search/docs/appearance/structured-data/profile-page); markup is not a promise of a rich result or ranking.

## Keyword research and page map

This is an intent and vocabulary map, not paid search-volume research. No monthly volume, keyword difficulty or expected ranking is asserted. Phrases were selected by matching the supplied career evidence to primary employer/industry terminology. They are used naturally in titles, descriptions, headings, skill copy and footer context; no meta-keywords tag or hidden keyword list is used.

| Page | Main search intent | Supporting terms and possible role families | Evidence boundary |
|---|---|---|---|
| Home | Abhinav Verma; finance consultant; business development consultant | Partnerships, financial modelling, entrepreneurship, commercial finance | Personal portfolio positioning based on the confirmed mix of roles, not a licensed investment-advice offer. |
| CA Firm | Audit, accounting and financial analysis experience | Reconciliations, internal audit, concurrent audit, financial reporting, client management | CA Intermediate and articleship/manager experience; does not describe Abhinav as a fully qualified Chartered Accountant. |
| HSBC | Insurance financial reporting experience | Financial reporting analyst, month-end accounting, financial statement finalisation, global entity reporting | Supported overseas entities; geographic markers do not imply travel. |
| Vayoo | Startup finance and operations | Co-founder, unit economics, budgeting, forecasting, pricing, finance operations; related FP&A/commercial-finance roles | Uses the documented founder work; does not invent an FP&A job title or qualification. |
| Affiliate Network | Affiliate website project leadership and agrotech financial modelling | Coupon websites, UK train tickets, booking engines, credit-card comparisons, capital planning and manufacturing projections | $100K in agrotech project assets managed only; affiliate work focused on website-inventory project leadership, with no affiliate revenue-generation claim. |
| GWO SEVO | Affiliate business development and partnerships | Merchant acquisition, B2B sales, partner development, pipeline management, commercial negotiation, market expansion planning | Actual total monthly client revenue remains $10K+; expansion planning remains distinct from realized expansion. |
| SOP readers | Audit/accounting SOP; affiliate network operations SOP | Workpapers, review controls, onboarding, campaign tracking, reporting, settlement | Supplied procedures retain their original history/draft/replication distinctions. |

Primary terminology sources:

- [EY Financial Modelling Services](https://www.ey.com/en_uk/services/strategy-transactions/valuation-modeling-economics/financial-modelling) connects modelling with business planning, forecasting, performance monitoring, cash flow and financial analysis. Relevant terms are selected only where supported by the portfolio; the broader service list is not copied as a personal capability claim.
- [Awin careers](https://www.awin.com/us/careers/vacancies) uses Partner Development Manager, Business Development and Partnerships terminology. These are vocabulary references, not a claim that a particular vacancy remains open or that the candidate meets every requirement.
- An Amazon-focused query returned aggregators rather than a sufficient primary employer result. Those snippets were not used as authoritative evidence in this map.

## Dependency-ordered implementation and verification

1. Confirm the public base URL before setting any canonical.
2. Apply concise source content, education and consistent header/footer links.
3. Add metadata and identity markup to initial HTML; identify the original SOP reader for duplicate canonicalization.
4. Generate the sitemap from the same page registry; update enhanced navigation metadata.
5. Regenerate the SOPs and run the checks below; verify rendered desktop/mobile parity, education ordering, ordinary links, and direct/animated route metadata.
6. After the owner publishes, verify the public metadata and sitemap responses again. Search Console, indexing status, Rich Results Test and field CWV remain external follow-up checks; none were submitted or claimed as passed in this run.

```sh
python3 tools/seo.py
python3 tools/check_site.py
python3 tools/check_seo.py
node --check assets/navigation.js
node --check assets/app.js
node --check assets/menu.js
```

Rebuilding `tools/render_sops.py` also reapplies SEO so it cannot silently remove metadata. If the production domain changes, edit `SITE_URL` in `tools/seo.py`, regenerate and re-run checks before publishing.

## Completed local verification

- All ten HTML routes and the new sitemap returned HTTP 200 from the local preview server.
- Both Python checks passed; JavaScript syntax and Git whitespace checks passed.
- Metadata regeneration was idempotent: a second run did not change any generated HTML or the sitemap.
- Browser checks at 1280, 768 and 320 pixels found no horizontal page overflow. The desktop hero paragraph occupied two text lines.
- Rendered section order was hero → career → education → What I bring. The removed screenshot heading/intro was absent, and both education records and certifications were visible.
- All five animated career transitions updated the title, canonical, Open Graph URL and a single JSON-LD block. Returning home restored the profile metadata and education section. The duplicate SOP reference pointed to the original GWO operations canonical.
- The corrected header order was visible on desktop, in the mobile menu and on a directly opened SOP reader. No browser warning/error logs appeared in these checks.

These are local implementation checks. The live GitHub Pages site still requires publishing these changes before its metadata and sitemap can be rechecked in production.
