"""Check static routes, fragments, assets and the requested portfolio boundaries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links = path, set(), []
        self.feed(path.read_text())
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'{self.path.name}: duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        for key in ('src', 'href'):
            if key in attrs:
                self.links.append(attrs[key])

pages = {p.resolve(): Page(p) for p in ROOT.glob('*.html')}
for path, page in pages.items():
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        assert target.is_file(), f'{path.name}: missing local target {link}'
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, f'{path.name}: missing fragment {link}'
    html = path.read_text()
    assert not re.search(r'Accra|current operating base', html, re.I), path.name
    assert 'assets/abhinav-portrait.png' in html, path.name
    assert 'assets/themes.css' in html, path.name
    assert not re.search(r'(hsbc|sho(o|u)gloo|gwo-sevo)[-_]logo', html, re.I), path.name
    assert 'globe-state' not in html and 'globe-caption' not in html, path.name
    if 'id="globe"' in html:
        assert html.count('class="moon"') == 1, f'{path.name}: one moon beside Earth'
        assert '<div class="globe-stage"><div class="globe-halo"></div>\n        <div class="moon"' in html
    else:
        assert 'class="moon"' not in html, f'{path.name}: no moon without Earth'

home = (ROOT / 'index.html').read_text()
assert 'Trained in Finance,<br>Love for numbers,<br><em>Business Driven.</em>' in home
assert 'Abhinav Verma . Finance, Enterpreneurship &amp; Business Development.' in home
assert 'View my GitHub' in home and 'https://github.com/iabhinavv' in home
assert 'https://iabhinavv.github.io/vayoo/' in (ROOT / 'vayoo.html').read_text()
assert 'ca-article.html#' not in home, 'CA timeline must open the top of the career page'
assert home.count('href="ca-article.html"') == 3, 'Navigation and both CA timeline cards'
for excluded in ('hsbc', 'vayoo'):
    assert 'sop-link' not in (ROOT / f'{excluded}.html').read_text()
assert 'affiliate-network-sop.html' in (ROOT / 'consulting.html').read_text()
assert 'Originally prepared for GWO SEVO' in (ROOT / 'affiliate-network-sop.html').read_text()
assert 'data-page="consulting"' in (ROOT / 'affiliate-network-sop.html').read_text()
assert 'ca-firm-sop.html' in (ROOT / 'ca-article.html').read_text()
assert 'gwo-sevo-sop.html' in (ROOT / 'gwo-sevo.html').read_text()
assert sum(p.read_text().count('Shoogloo') for p in ROOT.glob('*.html')) == 1
print(f'Passed: {len(pages)} HTML pages, local routes, fragments, assets, privacy and content checks.')
