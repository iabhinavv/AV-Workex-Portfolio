"""Build a complete, branded PDF from the same content used by the SOP reader."""
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle

CONTACTS = [
    ('linkedin.com/in/iabhinavv', 'https://www.linkedin.com/in/iabhinavv'),
    ('github.com/iabhinavv', 'https://github.com/iabhinavv'),
    ('abhinaverma124@gmail.com', 'mailto:abhinaverma124@gmail.com'),
]
PALETTES = {'ca-article': '#003366', 'consulting': '#1b4156', 'gwo-sevo': '#0f5c2c'}


def render_pdf(destination, title, name, theme, content):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    accent = colors.HexColor(PALETTES[theme])
    styles = getSampleStyleSheet()
    body = ParagraphStyle('SOP body', fontName='Helvetica', fontSize=9.5, leading=14,
                          spaceAfter=8, textColor=colors.HexColor('#243746'), alignment=TA_LEFT)
    heading = ParagraphStyle('SOP heading', parent=styles['Heading2'], fontName='Helvetica-Bold',
                             fontSize=13, leading=17, spaceBefore=15, spaceAfter=8,
                             textColor=accent, keepWithNext=True)
    detail = ParagraphStyle('SOP detail', parent=heading, fontSize=10.5, leading=14,
                            spaceBefore=10, spaceAfter=6)
    item = ParagraphStyle('SOP list', parent=body, leftIndent=13, firstLineIndent=-10, spaceAfter=5)
    cell = ParagraphStyle('SOP cell', parent=body, fontSize=8.3, leading=11.5, spaceAfter=0)
    table_head = ParagraphStyle('SOP table heading', parent=cell, fontName='Helvetica-Bold', textColor=colors.white)
    document = SimpleDocTemplate(str(destination), pagesize=A4, rightMargin=18*mm,
                                 leftMargin=18*mm, topMargin=25*mm, bottomMargin=28*mm,
                                 title=f'{name}: {title}', author='Abhinav Verma',
                                 subject='Standard operating procedure', creator='Abhinav’s Workex')
    story = [Paragraph(escape(name.upper()) + ' · PROCESS GUIDE', detail),
             Paragraph(escape(title), ParagraphStyle('SOP title', parent=heading, fontSize=24, leading=28,
                                                     spaceBefore=3, spaceAfter=12)),
             Paragraph('By Abhinav Verma', body), Spacer(1, 5)]

    def inline(node):
        value = escape(node.text or '')
        for child in node:
            text = inline(child)
            if child.tag in ('strong', 'b'): text = '<b>' + text + '</b>'
            elif child.tag in ('em', 'i'): text = '<i>' + text + '</i>'
            elif child.tag == 'code': text = '<font name="Courier">' + text + '</font>'
            elif child.tag == 'br': text = '<br/>'
            elif child.tag == 'a' and child.get('href', '').startswith(('https://', 'mailto:')):
                text = '<a href="' + escape(child.get('href'), quote=True) + '">' + text + '</a>'
            value += text + escape(child.tail or '')
        return value

    def blocks(parent):
        for node in parent:
            if node.tag in ('h2', 'h3'):
                story.append(Paragraph(inline(node), heading if node.tag == 'h2' else detail))
            elif node.tag == 'p': story.append(Paragraph(inline(node), body))
            elif node.tag in ('ul', 'ol'):
                for index, li in enumerate(node.findall('li'), 1):
                    prefix = f'{index}. ' if node.tag == 'ol' else '• '
                    story.append(Paragraph(prefix + inline(li), item))
                story.append(Spacer(1, 3))
            elif node.tag == 'table':
                rows = []
                for index, row in enumerate(node.iter('tr')):
                    rows.append([Paragraph(inline(td), table_head if index == 0 else cell) for td in row])
                table = LongTable(rows, colWidths=[document.width/len(rows[0])]*len(rows[0]),
                                  repeatRows=1, hAlign='LEFT')
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), accent),
                    ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#d9e0e5')),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ]))
                story.extend([table, Spacer(1, 12)])
            elif node.tag == 'details':
                summary = node.find('summary')
                if summary is not None: story.append(Paragraph(inline(summary), detail))
                blocks(node)
            elif node.tag in ('div', 'section'): blocks(node)

    blocks(ET.fromstring('<article>' + content + '</article>'))

    def page_brand(canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setFillColor(accent)
        canvas.setFillAlpha(.055)
        canvas.translate(width/2, height/2)
        canvas.rotate(35)
        canvas.setFont('Helvetica-Bold', 49)
        canvas.drawCentredString(0, 0, 'ABHINAV VERMA')
        canvas.restoreState()
        canvas.saveState()
        canvas.setFillColor(accent)
        canvas.setFont('Helvetica-Bold', 8.5)
        canvas.drawString(18*mm, height-15*mm, 'ABHINAV VERMA')
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(width-18*mm, height-15*mm, name + ' | Operating playbook')
        canvas.setStrokeColor(colors.HexColor('#d9e0e5'))
        canvas.line(18*mm, 23*mm, width-18*mm, 23*mm)
        canvas.setFillColor(colors.HexColor('#243746'))
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawString(18*mm, 18*mm, 'Abhinav Verma · Abhinav’s Workex')
        canvas.drawRightString(width-18*mm, 18*mm, f'Page {doc.page}')
        canvas.setFont('Helvetica', 7.5)
        x, y = 18*mm, 12*mm
        for index, (label, url) in enumerate(CONTACTS):
            if index:
                separator = '  |  '
                canvas.drawString(x, y, separator)
                x += canvas.stringWidth(separator, 'Helvetica', 7.5)
            span = canvas.stringWidth(label, 'Helvetica', 7.5)
            canvas.drawString(x, y, label)
            canvas.linkURL(url, (x, y-2, x+span, y+8), relative=0, thickness=0)
            x += span
        canvas.restoreState()

    document.build(story, onFirstPage=page_brand, onLaterPages=page_brand)
