"""Build crawlable metadata and a sitemap for the verified GitHub Pages site."""
from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE_URL = 'https://iabhinavv.github.io/AV-Workex-Portfolio/'
PAGES = {
    'index.html': ('Abhinav Verma | Finance & Business Development Consultant',
        'Abhinav Verma: finance-trained consultant with experience in B2B business development, partnerships, financial modelling, entrepreneurship and global reporting.'),
    'ca-article.html': ('Abhinav Verma | Audit, Accounting & Financial Analysis',
        'Abhinav Verma’s CA Firm experience: statutory, concurrent and internal audits, reconciliations, accounting, taxation, client management and team training.'),
    'hsbc.html': ('Abhinav Verma | HSBC Insurance Financial Reporting',
        'Abhinav Verma’s HSBC experience in global insurance accounting, financial statement finalisation, month-end work and stakeholder reporting for overseas entities.'),
    'vayoo.html': ('Abhinav Verma | Vayoo Co-founder, Finance & Operations',
        'Explore Abhinav Verma’s Vayoo co-founder experience in startup finance, unit economics, budgeting, pricing, suppliers, fulfilment and operating decisions.'),
    'consulting.html': ('Abhinav Verma | Affiliate Projects & Agrotech Finance',
        'Abhinav Verma’s affiliate website project leadership across coupons, UK train tickets, booking engines and credit-card comparisons, plus agrotech financial modelling.'),
    'gwo-sevo.html': ('Abhinav Verma | Affiliate Business Development & Partnerships',
        'Abhinav Verma’s GWO SEVO experience in B2B business development, merchant acquisition, affiliate partnerships, commercial negotiation and market expansion planning.'),
    'ca-firm-sop.html': ('Audit & Accounting SOP | Abhinav Verma',
        'CA Firm operating playbook covering client records, accounting, reconciliations, audit workpapers, taxation workflows, review controls and checklists.'),
    'gwo-sevo-sop.html': ('Affiliate & Creator Network Playbook | Abhinav Verma',
        'A concise affiliate and creator network playbook covering merchant pipelines, creator shortlists, onboarding, campaigns and reporting, with expandable checklists.'),
    'gwo-sevo-operations-sop.html': ('Affiliate Network Operations SOP | Abhinav Verma',
        'An affiliate network operations reference covering merchant acquisition, publisher onboarding, tracking, conversion validation, reporting and settlement.'),
    'affiliate-network-sop.html': ('Affiliate Operations Reference | Abhinav Verma',
        'An affiliate operations guide covering merchant and publisher onboarding, tracking, reporting and settlement, with expandable checklists and a printable PDF.'),
}
PARENTS = {'ca-firm-sop.html': 'ca-article.html', 'gwo-sevo-sop.html': 'gwo-sevo.html',
           'gwo-sevo-operations-sop.html': 'gwo-sevo.html', 'affiliate-network-sop.html': 'consulting.html'}
LABELS = {'ca-article.html': 'CA Firm', 'hsbc.html': 'HSBC', 'vayoo.html': 'Vayoo',
          'consulting.html': 'Affiliate Network', 'gwo-sevo.html': 'GWO SEVO'}


def url_for(filename):
    return SITE_URL if filename == 'index.html' else SITE_URL + filename


def canonical_for(filename):
    # Two themed readers use the same supplied SOP. Identify its original as primary.
    return url_for('gwo-sevo-operations-sop.html' if filename == 'affiliate-network-sop.html' else filename)


def schema_for(filename, title, description):
    person_id = SITE_URL + '#abhinav-verma'
    page_url = url_for(filename)
    page = {'@type': 'ProfilePage' if filename == 'index.html' else 'WebPage',
            '@id': page_url + '#webpage', 'url': page_url, 'name': title,
            'description': description, 'inLanguage': 'en',
            'isPartOf': {'@id': SITE_URL + '#website'}}
    graph = [{'@type': 'WebSite', '@id': SITE_URL + '#website', 'url': SITE_URL,
              'name': 'Abhinav’s Workex', 'publisher': {'@id': person_id}}, page]
    if filename == 'index.html':
        person = {'@type': 'Person', '@id': person_id, 'name': 'Abhinav Verma',
                  'url': SITE_URL, 'image': SITE_URL + 'assets/abhinav-portrait.png',
                  'description': 'Finance-trained business development consultant with experience in partnerships, financial modelling and entrepreneurship.',
                  'sameAs': ['https://www.linkedin.com/in/iabhinavv', 'https://github.com/iabhinavv'],
                  'knowsAbout': ['Business development', 'Partnership development', 'Financial modelling',
                                 'Budgeting and forecasting', 'Affiliate marketing', 'Financial reporting']}
        graph.insert(0, person)
        page['mainEntity'] = {'@id': person_id}
    else:
        page['about'] = {'@id': person_id}
        trail = [('Home', SITE_URL)]
        if filename in PARENTS:
            parent = PARENTS[filename]
            trail.append((LABELS[parent], url_for(parent)))
        trail.append((LABELS.get(filename, title.split(' | ')[0]), page_url))
        breadcrumb = {'@type': 'BreadcrumbList', '@id': page_url + '#breadcrumbs',
                      'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': name, 'item': url}
                                          for i, (name, url) in enumerate(trail, 1)]}
        graph.append(breadcrumb)
        page['breadcrumb'] = {'@id': breadcrumb['@id']}
    return {'@context': 'https://schema.org', '@graph': graph}


def apply_site_seo():
    for filename, (title, description) in PAGES.items():
        p = ROOT / filename
        html = p.read_text()
        html = re.sub(r'<title>.*?</title>', '<title>' + escape(title) + '</title>', html, count=1, flags=re.S)
        html = re.sub(r'\s*<meta\b[^>]*(?:name="(?:description|robots|twitter:[^"]+)"|property="og:[^"]+")[^>]*>', '', html)
        html = re.sub(r'\s*<link\b[^>]*rel="canonical"[^>]*>', '', html)
        html = re.sub(r'\s*<script\b[^>]*data-page-schema[^>]*>.*?</script>', '', html, flags=re.S)
        canonical = canonical_for(filename)
        attrs = [('name', 'description', description), ('name', 'robots', 'index, follow'),
                 ('property', 'og:type', 'profile' if filename == 'index.html' else 'website'),
                 ('property', 'og:site_name', 'Abhinav’s Workex'), ('property', 'og:title', title),
                 ('property', 'og:description', description), ('property', 'og:url', canonical),
                 ('property', 'og:image', SITE_URL + 'assets/abhinav-portrait.png'),
                 ('property', 'og:image:alt', 'Abhinav Verma'), ('property', 'og:image:width', '800'),
                 ('property', 'og:image:height', '800'), ('name', 'twitter:card', 'summary'),
                 ('name', 'twitter:title', title), ('name', 'twitter:description', description),
                 ('name', 'twitter:image', SITE_URL + 'assets/abhinav-portrait.png')]
        tags = [f'<meta {key}="{name}" content="{escape(value, quote=True)}">' for key, name, value in attrs]
        tags.insert(0, f'<link rel="canonical" href="{canonical}">')
        data = json.dumps(schema_for(filename, title, description), ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
        tags.append(f'<script type="application/ld+json" data-page-schema>{data}</script>')
        html = html.replace('</head>', '\n  ' + '\n  '.join(tags) + '\n</head>', 1)
        p.write_text(html)
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    sitemap = ET.Element(f'{{{ns}}}urlset')
    for filename in PAGES:
        if canonical_for(filename) != url_for(filename):
            continue
        item = ET.SubElement(sitemap, f'{{{ns}}}url')
        ET.SubElement(item, f'{{{ns}}}loc').text = url_for(filename)
    ET.ElementTree(sitemap).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    print(f'Built metadata for {len(PAGES)} pages and a {len(sitemap)}-URL sitemap.')


if __name__ == '__main__':
    apply_site_seo()
