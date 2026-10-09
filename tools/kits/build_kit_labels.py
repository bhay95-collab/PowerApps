# Printable kit labels: one QR code per kit (value = kit ID, e.g. DTK-014) with the unit and kit type underneath.
#   python3 -I tools/kits/build_kit_labels.py <Kit_Register.csv> <out.pdf>
# A4, 2 x 4 labels per page (large enough to scan from a box lid). Do not commit the PDF (public repo).
import csv, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

src, out = sys.argv[1], sys.argv[2]
kits = list(csv.DictReader(open(src, encoding='utf-8-sig')))
W, H = A4
COLS, ROWS = 2, 4
MX, MY = 12 * mm, 12 * mm
CW, CH = (W - 2 * MX) / COLS, (H - 2 * MY) / ROWS
INK = (14 / 255, 28 / 255, 42 / 255); TEAL = (7 / 255, 95 / 255, 115 / 255); MUTED = (140 / 255, 155 / 255, 174 / 255)

def fit(c, text, font, size, maxw):
    while size > 6 and c.stringWidth(text, font, size) > maxw: size -= 0.5
    return size

c = canvas.Canvas(out, pagesize=A4)
c.setTitle('DTV Kit QR Labels')
for i, k in enumerate(kits):
    if i and i % (COLS * ROWS) == 0: c.showPage()
    col, row = (i % (COLS * ROWS)) % COLS, (i % (COLS * ROWS)) // COLS
    x0, y0 = MX + col * CW, H - MY - (row + 1) * CH
    c.setStrokeColorRGB(*MUTED); c.setDash(2, 3); c.roundRect(x0 + 3 * mm, y0 + 3 * mm, CW - 6 * mm, CH - 6 * mm, 4 * mm); c.setDash()
    c.setFillColorRGB(*TEAL); c.roundRect(x0 + 3 * mm, y0 + CH - 13 * mm, CW - 6 * mm, 10 * mm, 4 * mm, fill=1, stroke=0)
    c.rect(x0 + 3 * mm, y0 + CH - 13 * mm, CW - 6 * mm, 5 * mm, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1); c.setFont('Helvetica-Bold', 9); c.drawString(x0 + 7 * mm, y0 + CH - 9.5 * mm, 'ieMR DOWNTIME KIT  ·  SCAN TO AUDIT')
    q = 38 * mm
    w = QrCodeWidget(k['Title']); w.barLevel = 'M'
    b = w.getBounds(); d = Drawing(q, q, transform=[q / (b[2] - b[0]), 0, 0, q / (b[3] - b[1]), 0, 0]); d.add(w)
    renderPDF.draw(d, c, x0 + 6 * mm, y0 + CH - 13 * mm - q - 2 * mm)
    tx, tw = x0 + 6 * mm + q + 4 * mm, CW - q - 18 * mm
    c.setFillColorRGB(*INK); c.setFont('Helvetica-Bold', 22); c.drawString(tx, y0 + CH - 26 * mm, k['Title'])
    c.setFont('Helvetica-Bold', fit(c, k['Unit'], 'Helvetica-Bold', 11, tw)); c.drawString(tx, y0 + CH - 34 * mm, k['Unit'])
    c.setFillColorRGB(*MUTED); c.setFont('Helvetica', fit(c, k['Location'], 'Helvetica', 9, tw)); c.drawString(tx, y0 + CH - 40 * mm, k['Location'])
    c.setFillColorRGB(*TEAL)
    words, line, ly = k['KitType'].split(), '', y0 + 16 * mm
    lines = []
    for wd in words:
        if c.stringWidth((line + ' ' + wd).strip(), 'Helvetica-Bold', 8.5) > CW - 14 * mm: lines.append(line); line = wd
        else: line = (line + ' ' + wd).strip()
    lines.append(line)
    c.setFont('Helvetica-Bold', 8.5)
    for j, ln in enumerate(lines[:2]): c.drawString(x0 + 7 * mm, ly - j * 4 * mm, ln)
    c.setFillColorRGB(*MUTED); c.setFont('Helvetica', 7); c.drawString(x0 + 7 * mm, y0 + 6 * mm, 'If the QR code will not scan, type the kit ID in the app.')
c.save()
print(f'{len(kits)} labels, {(len(kits) + COLS * ROWS - 1) // (COLS * ROWS)} pages -> {out}')
