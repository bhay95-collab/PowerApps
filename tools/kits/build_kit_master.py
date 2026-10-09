# Turns the RBWH DTK kit list (Word, one table per kit) into the three master lists for kit scanning.
#   python3 -I tools/kits/build_kit_master.py <RBWH_DTK_Kit_Lists.docx> <output folder>
# Writes (CSV, ready to import into SharePoint lists). Do NOT commit the outputs: this repo is public.
# Column names = SharePoint column names (Title holds the key: kit ID / item key / kit ID).
#   Kit_Register.csv  one row per physical kit (101): Title = kit ID (DTK-001, printed as the QR code), unit, location, kit type, bedside packs
#   Kit_Items.csv     catalogue of every distinct item: Title = item key, name, form number, kind, scan method, barcode value (to fill from the scan test)
#   Kit_Contents.csv  what each kit should hold: Title = kit ID, ItemKey (+ which folder/section, quantity for reference)
# Re-run whenever the Word document changes; KitIDs follow the order of kits in the document, so add new kits at the end.
import csv, re, sys, collections, os
import docx

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
d = docx.Document(src)

def clean(s):
    return re.sub(r'\s+', ' ', s.replace('–', '-').replace('—', '-')).strip()

kits, cur = [], None
for t in d.tables:
    head = [c.text.strip() for c in t.rows[0].cells]
    if head[:2] == ['Location', 'Kit Type']:
        r = [c.text.strip() for c in t.rows[1].cells]
        lines = [x.strip() for x in r[0].split('\n') if x.strip()]
        cur = {'unit': lines[0], 'where': ' '.join(lines[1:]), 'type': clean(r[1]), 'beds': r[2], 'items': []}
        kits.append(cur)
    elif head[0].startswith('Form / Item') and cur is not None:
        for row in t.rows[1:]:
            c = [clean(x.text) for x in row.cells]
            if c[1]:
                cur['items'].append({'section': c[0], 'name': c[1], 'form': c[2], 'method': c[3], 'code': c[4], 'unit': c[5], 'qty': c[6]})

GUIDE = {'QRG', 'Document', 'Checklist(s)'}
def kind(unit):
    if unit in ('Form(s)', 'Pack(s)'): return 'Form'
    if unit in GUIDE: return 'Printed guide'
    return 'Stationery'
def key(it):
    if it['form'] and it['form'] != 'N/A': return it['form'].upper()
    return re.sub(r'[^a-z0-9]+', '-', it['name'].lower()).strip('-')[:60]

# ---- catalogue: one row per distinct item (same form number = same item; names vary slightly between kits)
names = collections.defaultdict(collections.Counter); meta = {}
for k in kits:
    for it in k['items']:
        kk = key(it); names[kk][re.sub(r'\s*\((SW|MN)\d+\)$', '', it['name'])] += 1
        meta.setdefault(kk, it)
# Scan test 9 Oct 2026: form barcodes read exactly the form number (SW1171, SW626, MN383).
# 00201:12256 was the standard (non-downtime) fluid balance chart: the wrong form, which scanning now catches.
CONFIRMED = {'SW1171', 'SW626', 'MN383'}
def barcode(form):
    f = (form or '').strip().upper()
    return f if re.fullmatch(r'(SW|MN)\d+|00201:\d+', f) else ''
items = []
for kk, it in meta.items():
    kd = kind(it['unit'])
    barcoded = kd == 'Form' and bool(barcode(it['form']))  # forms with no form number (ESM) are ticked
    items.append({'Title': kk, 'ItemName': names[kk].most_common(1)[0][0], 'FormNumber': '' if it['form'] in ('', 'N/A') else it['form'],
                  'Kind': kd, 'ScanMethod': 'Scan barcode' if barcoded else 'Tick present', 'BarcodeValue': barcode(it['form']), 'BarcodeChecked': 'Yes' if barcode(it['form']) in CONFIRMED else '', 'CurrentVersion': '',
                  'OrderMethod': it['method'], 'OrderCode': '' if it['code'] in ('', 'N/A') else it['code']})
items.sort(key=lambda x: (x['Kind'] != 'Form', x['FormNumber'] or 'zzz', x['ItemName']))

# ---- kits and their contents
reg, contents = [], []
for i, k in enumerate(kits, 1):
    kid = f'DTK-{i:03d}'
    reg.append({'Title': kid, 'Unit': k['unit'], 'Location': k['where'], 'KitType': k['type'], 'BedsidePacks': k['beds']})
    per = collections.OrderedDict()
    for it in k['items']:
        kk = key(it)
        e = per.setdefault(kk, {'KitID': kid, 'ItemKey': kk, 'Sections': [], 'Quantity': []})
        if it['section'] not in e['Sections']: e['Sections'].append(it['section'])
        e['Quantity'].append(f"{it['qty']} {it['unit']}".strip())
    for e in per.values():
        contents.append({'Title': e['KitID'], 'ItemKey': e['ItemKey'], 'Sections': '; '.join(e['Sections']), 'Quantity': '; '.join(e['Quantity'])})

def write(name, rows):
    with open(os.path.join(out, name), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
write('Kit_Register.csv', reg); write('Kit_Items.csv', items); write('Kit_Contents.csv', contents)

types = collections.Counter(k['type'] for k in kits)
sets = collections.Counter(tuple(sorted({key(it) for it in k['items']})) for k in kits)
print(f'{len(reg)} kits, {len(types)} kit types, {len(sets)} different contents lists')
print(f'{len(items)} distinct items: ' + ', '.join(f'{n} {kd}' for kd, n in collections.Counter(x["Kind"] for x in items).items()))
print(f'{len(contents)} kit-content rows')
miss = [x for x in items if x['ScanMethod'] == 'Scan barcode' and not x['BarcodeChecked']]
print(f'{len(miss)} forms with an assumed barcode (= form number), not yet test-scanned: ' + ', '.join(f"{x['FormNumber']} {x['ItemName']}" for x in miss))
