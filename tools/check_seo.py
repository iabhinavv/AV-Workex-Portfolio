"""Check SEO identity, canonical/sitemap alignment and the requested homepage layout."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
from seo import ROOT, SITE_URL, PAGES, canonical_for, url_for

class Head(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.title, self.titles, self.in_title = '', 0, False
        self.metas, self.canonicals, self.schemas = {}, [], []
        self.schema_text, self.in_schema, self.h1_count = '', False, 0
        self.feed(html)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'title': self.in_title = True; self.titles += 1
        if tag == 'h1': self.h1_count += 1
        if tag == 'meta':
            key = a.get('name', a.get('property'))
            assert key not in self.metas, f'Duplicate meta: {key}'
            self.metas[key] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonicals.append(a['href'])
        if tag == 'script' and 'data-page-schema' in a:
            self.in_schema, self.schema_text = True, ''
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_schema: self.schema_text += data
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'script' and self.in_schema:
            self.schemas.append(json.loads(self.schema_text)); self.in_schema = False

titles, descriptions, expected_sitemap = set(), set(), set()
expected_nav = ['ca-article.html','hsbc.html','vayoo.html','consulting.html','gwo-sevo.html']
for filename, (title, description) in PAGES.items():
    html = (ROOT / filename).read_text()
    head = Head(html)
    assert head.title == title and head.titles == 1, filename
    assert head.title not in titles and head.metas['description'] not in descriptions, filename
    titles.add(head.title); descriptions.add(head.metas['description'])
    assert head.metas['description'] == description
    assert head.h1_count == 1 and len(head.schemas) == 1, filename
    assert head.canonicals == [canonical_for(filename)], filename
    assert head.metas['og:url'] == head.canonicals[0]
    assert head.metas['og:title'] == head.title == head.metas['twitter:title']
    assert head.metas['robots'] == 'index, follow'
    assert 'localhost' not in json.dumps(head.schemas) and '127.0.0.1' not in html
    assert SITE_URL in json.dumps(head.schemas)
    assert not any(key in json.dumps(head.schemas) for key in ['addressLocality','homeLocation','workLocation'])
    nav = re.search(r'<nav id="main-nav"[^>]*>(.*?)</nav>',html,re.S)[1]
    assert re.findall(r'href="([^"]+)"',nav) == expected_nav, filename
    if canonical_for(filename) == url_for(filename): expected_sitemap.add(url_for(filename))
    if filename == 'index.html':
        assert any(item['@type'] == 'ProfilePage' for item in head.schemas[0]['@graph'])
        assert any(item.get('name') == 'Abhinav Verma' for item in head.schemas[0]['@graph'])

sitemap = ET.parse(ROOT / 'sitemap.xml')
locations = [item.text for item in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert len(locations) == len(set(locations))
assert set(locations) == expected_sitemap
home = (ROOT / 'index.html').read_text()
assert home.index('id="career"') < home.index('id="education"') < home.index('class="section capabilities"')
assert 'Career milestones.' not in home and 'One connected skill set.' not in home
assert '2021–present · Finance, entrepreneurship &amp; consulting.' in home
assert len(re.search(r'<p class="lede">(.*?)</p>',home)[1]) <= 100
assert home.count('class="certificate"') == 9
assert home.count('class="education-entry"') == 2
assert '<time' not in re.search(r'<ul class="certificate-grid">.*?</ul>',home,re.S)[0]
for phrase in ['CA Intermediate','Institute of Chartered Accountants of India','2019–2023',
               'BS, Data Science &amp; Management','IIT Madras','2026–2030','Online · In progress',
               'Financial Risk Management with R','Ecommerce Unlocked']:
    assert phrase in home, phrase
print(f'Passed: {len(PAGES)} page identities, schemas, nav order, {len(locations)} sitemap URLs and homepage education/layout.')
