"""Validate concise SOP readers and the PDF author/contact details on every page."""
from pathlib import Path
from html.parser import HTMLParser
import re
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
SLUGS=['ca-firm','affiliate-network','gwo-sevo','gwo-sevo-operations']

class Reader(HTMLParser):
    def __init__(self,html):
        super().__init__();self.article=False;self.closed_details=0;self.text=[];self.feed(html)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='article':self.article=True
        if self.article and tag=='details':
            assert 'open' not in attrs,'Details should be collapsed initially'
            self.closed_details+=1
    def handle_endtag(self,tag):
        if tag=='article':self.article=False
    def handle_data(self,data):
        if self.article:self.text.append(data)

for slug in SLUGS:
    html=(ROOT/f'{slug}-sop.html').read_text()
    reader=Reader(html)
    text=' '.join(reader.text)
    assert len(text.split())<1200,slug
    assert reader.closed_details>=3,slug
    assert not re.search(r'\bAI\b|ChatGPT|replication standard|source and adoption|supplied|draft for|publication boundary|planning ZIP',text,re.I),slug
    for phrase in ['data-sop-action="print"','data-sop-action="expand"','data-sop-action="collapse"','class="sop-print-watermark"','class="sop-print-footer"','assets/sop-reader.css','assets/sop-reader.js']:
        assert phrase in html,(slug,phrase)
    assert f'href="assets/pdfs/{slug}-sop.pdf" download' in html
    pdf=PdfReader(ROOT/'assets/pdfs'/f'{slug}-sop.pdf')
    assert 1<=len(pdf.pages)<=4,slug
    assert pdf.metadata.author=='Abhinav Verma'
    for page in pdf.pages:
        page_text=page.extract_text()
        for phrase in ['ABHINAV VERMA','Abhinav Verma','linkedin.com/in/iabhinavv','github.com/iabhinavv','abhinaverma124@gmail.com']:
            assert phrase in page_text,(slug,phrase)
        urls={annotation.get_object().get('/A',{}).get('/URI') for annotation in page.get('/Annots',[])}
        assert {'https://www.linkedin.com/in/iabhinavv','https://github.com/iabhinavv','mailto:abhinaverma124@gmail.com'}<=urls,slug
print('Passed: four concise readers, collapsed details, printable branding and contact links on every PDF page.')
