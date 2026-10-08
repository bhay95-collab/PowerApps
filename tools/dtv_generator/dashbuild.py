# DTV Audit app: Dashboard screen (desktop first, stacks to one column under 1000 wide).
#   cd tools/dtv_generator && python3 dashbuild.py   -> powerapps/dtv/DTV_Dashboard.pa.yaml
# Needs in App > Formulas: DashW, DashX, DashWide, DashGap (see powerapps/dtv/App_Formulas_additions.txt)
from dtvgen import *
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'powerapps', 'dtv') + os.sep
GREEN = "RGBA(30, 122, 80, 1)"; RED = "RGBA(176, 52, 40, 1)"; LINE = "RGBA(14, 42, 70, 0.22)"
WIDE = 'DashWide'; GAP = 'DashGap'
NOSB = {k: v for k, v in SBOX.items() if not k.startswith('Radius')}

def pillbtn(name, text, onsel, color, size=14, radius=24):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': color, 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'OnSelect': onsel, 'Size': r(F(size)), 'Text': text, 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(radius)), **NOSB))

def panel(name, title, children, sub=None):
    ch = [lbl(f'cap{name}_Dsh', f'"{title}"', x=r(20), y=r(16), w=f'Parent.Width - {r(40)}', h=r(22), size=14, color='C_Muted', bold=True)]
    if sub: ch.append(lbl(f'sub{name}_Dsh', sub, x=r(20), y=r(38), w=f'Parent.Width - {r(40)}', h=r(20), size=13, color='C_Muted'))
    return box(f'con{name}_Dsh', fill='C_White', border='C_Line', radius=r(20), children=ch + children)

def row(name, specs):
    """specs: [(panel, width fraction, height px)]. Side by side when DashWide, stacked otherwise."""
    n = len(specs); avail = f'(DashW - {n - 1} * {GAP})'
    acc = 0.0; yacc = []
    for i, (p, frac, h) in enumerate(specs):
        p.props['X'] = f'If({WIDE}, {avail} * {round(acc, 4)} + {i} * {GAP}, 0)' if i else '0'
        p.props['Width'] = f'If({WIDE}, {avail} * {frac}, DashW)'
        p.props['Height'] = r(h)
        p.props['Y'] = '0' if i == 0 else f'If({WIDE}, 0, {" + ".join(r(x) for x in yacc)} + {i} * {GAP})'
        acc += frac; yacc.append(h)
    hmax = max(h for _, _, h in specs)
    total = f'If({WIDE}, {r(hmax)}, {" + ".join(r(h) for _, _, h in specs)} + {n - 1} * {GAP})'
    return inflow(f'conRow{name}_Dsh', total, w='DashW', children=[s[0] for s in specs], extra={'DropShadow': 'DropShadow.None'})

def bar(name, x, y, w, h, frac, color, visible=None):
    """track + fill. frac = formula 0..1"""
    return box(f'conTrk{name}_Dsh', x=x, y=y, w=w, h=h, fill='C_Line', radius=r(6), visible=visible, children=[
        box(f'conBar{name}_Dsh', w=f'Parent.Width * Min(1, Max(0, {frac}))', h='Parent.Height', fill=color, radius=r(6))])

# ------------------------------------------------------------------ header
RANGE = 'Switch(varDashDays, 7, "Last 7 days", 30, "Last 30 days", 90, "Last 90 days", "All time")'
STREAM = 'If(varDashStream = "ALL", "All streams", varDashStream)'
hdr = inflow('conHdr_Dsh', r(95), w='App.Width', fill=HDR_FILL, radius='0', extra={'DropShadow': 'DropShadow.None'}, children=[
    N('imgHdr_Dsh', 'Image@2.2.3', props={'Height': 'Parent.Height', 'Image': 'HeaderImage', 'ImagePosition': 'ImagePosition.Fill', 'Width': 'Parent.Width'}),
    N('btnBack_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_White', 'FontWeight': '""', 'Height': r(60), 'Icon': '"ChevronLeft"', 'OnSelect': 'Navigate(Home, ScreenTransition.UnCoverRight)', 'Size': r(24), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': r(60), 'X': f'DashX - {r(10)}', 'Y': r(18)}, **SBOX)),
    lbl('lblHdrT_Dsh', '"Audit Dashboard"', x=f'DashX + {r(55)}', y=r(12), w=f'DashW - {r(55)} - If({WIDE}, {r(250)}, {r(80)})', h=r(42), size=24, color='C_White', bold=True),
    lbl('lblHdrS_Dsh', f'{RANGE} & "  ·  " & {STREAM} & "  ·  " & varDashN & If(varDashN = 1, " audit", " audits")', x=f'DashX + {r(55)}', y=r(53), w=f'DashW - {r(55)} - If({WIDE}, {r(250)}, {r(80)})', h=r(25), size=15, color='RGBA(255, 255, 255, 0.85)'),
    box('conEmail_Dsh', x=f'DashX + DashW - If({WIDE}, {r(230)}, {r(60)})', y=r(22), w=f'If({WIDE}, {r(230)}, {r(60)})', h=r(50), fill='RGBA(255, 255, 255, 0.16)', border='RGBA(255, 255, 255, 0.45)', radius=r(25), children=[
        N('btnEmail_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_White', 'DisplayMode': 'If(varSaving || varDashN = 0, DisplayMode.Disabled, DisplayMode.Edit)', 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'Icon': '"Mail"', 'OnSelect': 'Select(btnSend_Dsh)', 'Size': r(F(15)), 'Text': f'If({WIDE}, If(varSaving, "Sending...", "Email Me the Data"), "")', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(25)), **NOSB))]),
])

# ------------------------------------------------------------------ filters
selD = 'ThisItem.D = varDashDays'
galDays = N('galDays_Dsh', 'Gallery@2.15.0', 'Horizontal', {'Height': r(52), 'Items': 'Table({ L: "7 Days", D: 7 }, { L: "30 Days", D: 30 }, { L: "90 Days", D: 90 }, { L: "All Time", D: 0 })', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(110), 'Width': r(440), 'X': r(16), 'Y': r(12)}, [
    box('conDay_Dsh', x='3', y=r(2), w=f'Parent.TemplateWidth - {r(6)}', h=r(48), fill=f'If({selD}, C_Accent, C_White)', border=f'If({selD}, C_Accent, C_Line)', radius=r(24), children=[
        pillbtn('btnDay_Dsh', 'ThisItem.L', 'Set(varDashDays, ThisItem.D);\nSelect(btnLoad_Dsh)', f'If({selD}, C_White, C_Ink2)')])])
selS = 'ThisItem.Key = varDashStream'
galStr = N('galStream_Dsh', 'Gallery@2.15.0', 'Horizontal', {'Height': r(52), 'Items': 'colDashPills', 'ShowScrollbar': 'false', 'TemplatePadding': '0',
    'TemplateSize': f'If({WIDE}, Parent.Width - {r(478)}, Parent.Width - {r(32)}) / Max(1, CountRows(colDashPills))', 'Width': f'If({WIDE}, Parent.Width - {r(478)}, Parent.Width - {r(32)})', 'X': f'If({WIDE}, {r(462)}, {r(16)})', 'Y': f'If({WIDE}, {r(12)}, {r(72)})'}, [
    box('conStr_Dsh', x='3', y=r(2), w=f'Parent.TemplateWidth - {r(6)}', h=r(48), fill=f'If({selS}, C_Accent, C_White)', border=f'If({selS}, C_Accent, C_Line)', radius=r(24), children=[
        lbl('lblStr_Dsh', 'ThisItem.Label', x=r(4), w=f'Parent.Width - {r(8)}', h=r(48), size=14, color=f'If({selS}, C_White, C_Ink2)', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn('btnStr_Dsh', 'Set(varDashStream, ThisItem.Key);\nSelect(btnCalc_Dsh)')])])
filters = inflow('conFilters_Dsh', f'If({WIDE}, {r(76)}, {r(136)})', w='DashW', fill='C_White', border='C_Line', radius=r(20), children=[galDays, galStr])

# ------------------------------------------------------------------ KPI tiles
KPIS = [  # key, caption, value, sub, colour, focus
    ('Aud', 'AUDITS', 'varDashN', 'varDashReN & If(varDashReN = 1, " re-audit", " re-audits")', 'C_Ink', ''),
    ('Cov', 'DTVS COVERED', 'varDashCovN & " / " & varDashRegN', 'Text(If(varDashRegN > 0, varDashCovN / varDashRegN, 0), "0%") & " of DTVs audited"', 'C_Accent', ''),
    ('Clr', 'ALL CLEAR', 'varDashClearN', 'Text(If(varDashN > 0, varDashClearN / varDashN, 0), "0%") & " of audits"', GREEN, 'Clear'),
    ('Fol', 'NEED FOLLOW-UP', 'varDashFollowN', 'Text(If(varDashN > 0, varDashFollowN / varDashN, 0), "0%") & " of audits"', RED, 'Follow'),
    ('Nf', 'DTV NOT FOUND', 'varDashNotFoundN', '"Tap to list them"', 'C_Amber', 'Found'),
]
TH = 112
twW = f'(DashW - 4 * {GAP}) / 5'; twN = f'(DashW - {GAP}) / 2'
tiles = []
for i, (k, cap, val, sub, col, foc) in enumerate(KPIS):
    sel = f'varDashFocus = "{foc}"' if foc else 'false'
    onsel = (f'Set(varDashFocus, If(varDashFocus = "{foc}", "", "{foc}"));\nSet(varDashWhyR, "")' if foc else 'Set(varDashFocus, "");\nSet(varDashWhyR, "");\nSet(varDashBy, "")')
    t = box(f'conK{k}_Dsh', x=f'If({WIDE}, {i} * ({twW} + {GAP}), {i % 2} * ({twN} + {GAP}))', y=f'If({WIDE}, 0, {i // 2} * ({r(TH)} + {GAP}))', w=f'If({WIDE}, {twW}, {twN})', h=r(TH),
            fill=f'If({sel}, C_AccentSoft, C_White)', border=f'If({sel}, C_Accent, C_Line)', radius=r(20), children=[
        lbl(f'lblK{k}C_Dsh', f'"{cap}"', x=r(18), y=r(14), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Muted', bold=True),
        lbl(f'lblK{k}V_Dsh', val, x=r(18), y=r(34), w=f'Parent.Width - {r(36)}', h=r(46), size=36, color=col, bold=True),
        lbl(f'lblK{k}S_Dsh', sub, x=r(18), y=r(80), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Ink2'),
        tbtn(f'btnK{k}_Dsh', onsel)])
    tiles.append(t)
kpi = inflow('conKpi_Dsh', f'If({WIDE}, {r(TH)}, 3 * {r(TH)} + 2 * {GAP})', w='DashW', children=tiles, extra={'DropShadow': 'DropShadow.None'})

# ------------------------------------------------------------------ results by check
RH = 50
selC = 'varDashFocus = ThisItem.Key'
chk = ThisRow = 'ThisItem.Yes + ThisItem.No'
galChk = N('galChecks_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'7 * {r(RH)}', 'Items': 'colDashChecks', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(RH), 'Width': f'Parent.Width - {r(20)}', 'X': r(10), 'Y': r(62)}, [
    box('conChkSel_Dsh', x='0', y=r(3), w='Parent.TemplateWidth', h=r(RH - 6), fill=f'If({selC}, C_AccentSoft, RGBA(0, 0, 0, 0))', radius=r(12)),
    lbl('lblChk_Dsh', 'ThisItem.Label', x=r(10), y='0', w=r(180), h=r(RH), size=15, color='C_Ink', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    box('conChkTrk_Dsh', x=r(195), y=r(18), w=f'Parent.TemplateWidth - {r(195)} - {r(175)}', h=r(14), fill='C_Line', radius=r(7), children=[
        box('conChkYes_Dsh', w=f'Parent.Width * If({chk} > 0, ThisItem.Yes / ({chk}), 0)', h='Parent.Height', fill=GREEN, radius=r(7)),
        box('conChkNo_Dsh', x=f'Parent.Width * If({chk} > 0, ThisItem.Yes / ({chk}), 0)', w=f'Parent.Width * If({chk} > 0, ThisItem.No / ({chk}), 0)', h='Parent.Height', fill=RED, radius=r(7))]),
    lbl('lblChkN_Dsh', f'If({chk} = 0, "Not checked", If(ThisItem.No > 0, ThisItem.No & " failed", "All passed") & "  ·  " & ({chk}) & " checked")', x=f'Parent.TemplateWidth - {r(168)}', y='0', w=r(160), h=r(RH), size=14,
        color=f'If(ThisItem.No > 0, {RED}, If({chk} = 0, C_Muted, {GREEN}))', bold=True, align='Align.Right', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnChk_Dsh', f'Set(varDashFocus, If({selC}, "", ThisItem.Key));\nSet(varDashWhyR, "");\nIf(ThisItem.Key in ["Print", "Login"], Set(varDashWhyKind, ThisItem.Key))'),
])
pChecks = panel('Checks', 'RESULTS BY CHECK', [galChk,
    lbl('lblChkHint_Dsh', '"Green passed, red failed. Tap a row to list those audits below."', x=r(20), y=f'Parent.Height - {r(34)}', w=f'Parent.Width - {r(40)}', h=r(22), size=13, color='C_Muted')],
    sub='"Each audit counted once per check"')

# ------------------------------------------------------------------ why it failed
WH = 56
def kindpill(k, label, x):
    sel = f'varDashWhyKind = "{k}"'
    return box(f'conWhy{k}_Dsh', x=x, y=r(14), w=r(96), h=r(36), fill=f'If({sel}, C_Accent, C_White)', border=f'If({sel}, C_Accent, C_Line)', radius=r(18), children=[
        pillbtn(f'btnWhy{k}_Dsh', f'"{label}"', f'Set(varDashWhyKind, "{k}")', f'If({sel}, C_White, C_Ink2)', size=13, radius=18)])
mx = 'If(varDashWhyKind = "Print", varDashMaxPrint, varDashMaxLogin)'
selW = 'varDashWhyR = ThisItem.Reason'
galWhy = N('galWhy_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'6 * {r(WH)}', 'Items': 'Filter(colDashWhy, Kind = varDashWhyKind)', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(WH), 'Width': f'Parent.Width - {r(20)}', 'X': r(10), 'Y': r(62)}, [
    box('conWhySel_Dsh', x='0', y=r(2), w='Parent.TemplateWidth', h=r(WH - 4), fill=f'If({selW}, C_AccentSoft, RGBA(0, 0, 0, 0))', radius=r(12)),
    lbl('lblWhy_Dsh', 'ThisItem.Reason', x=r(10), y=r(4), w=f'Parent.TemplateWidth - {r(70)}', h=r(24), size=14, color='C_Ink', bold=True),
    bar('Why', r(10), r(32), f'Parent.TemplateWidth - {r(70)}', r(12), f'If({mx} > 0, ThisItem.N / {mx}, 0)', RED),
    lbl('lblWhyN_Dsh', 'ThisItem.N', x=f'Parent.TemplateWidth - {r(56)}', y='0', w=r(46), h=r(WH), size=19, color=f'If(ThisItem.N > 0, {RED}, C_Muted)', bold=True, align='Align.Right', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnWhy_Dsh', f'If({selW}, Set(varDashWhyR, ""); Set(varDashFocus, ""), Set(varDashWhyR, ThisItem.Reason); Set(varDashFocus, varDashWhyKind))'),
])
pWhy = panel('Why', 'WHY IT FAILED', [kindpill('Print', 'Print', f'Parent.Width - {r(216)}'), kindpill('Login', 'Login', f'Parent.Width - {r(112)}'), galWhy,
    lbl('lblWhyNone_Dsh', 'If(varDashWhyKind = "Print", "No print failures", "No login failures") & " in this period"', x=r(20), y=r(150), w=f'Parent.Width - {r(40)}', h=r(30), size=15, color='C_Muted', align='Align.Center',
        visible='If(varDashWhyKind = "Print", varDashMaxPrint, varDashMaxLogin) = 0')],
    sub='"Tap a reason to list those audits"')

# ------------------------------------------------------------------ coverage / education / auditors
SH = 56
def listpanel(name, title, sub, items, label, value, frac, color, onsel=None, selexpr=None, empty=None):
    ch = []
    if selexpr: ch.append(box(f'con{name}Sel_Dsh', x='0', y=r(2), w='Parent.TemplateWidth', h=r(SH - 4), fill=f'If({selexpr}, C_AccentSoft, RGBA(0, 0, 0, 0))', radius=r(12)))
    ch += [lbl(f'lbl{name}_Dsh', label, x=r(10), y=r(4), w=f'Parent.TemplateWidth - {r(120)}', h=r(24), size=14, color='C_Ink', bold=True),
           lbl(f'lbl{name}N_Dsh', value, x=f'Parent.TemplateWidth - {r(110)}', y=r(4), w=r(100), h=r(24), size=14, color='C_Ink2', bold=True, align='Align.Right'),
           bar(name, r(10), r(32), f'Parent.TemplateWidth - {r(20)}', r(12), frac, color)]
    if onsel: ch.append(tbtn(f'btn{name}_Dsh', onsel))
    g = N(f'gal{name}_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'5 * {r(SH)}', 'Items': items, 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(SH), 'Width': f'Parent.Width - {r(20)}', 'X': r(10), 'Y': r(62)}, ch)
    kids = [g]
    if empty: kids.append(lbl(f'lbl{name}None_Dsh', f'"{empty}"', x=r(20), y=r(150), w=f'Parent.Width - {r(40)}', h=r(30), size=15, color='C_Muted', align='Align.Center', visible=f'CountRows(gal{name}_Dsh.AllItems) = 0 || Sum(gal{name}_Dsh.AllItems, N) = 0'))
    return panel(name, title, kids, sub=sub)
pCov = listpanel('Cov', 'COVERAGE BY STREAM', '"DTVs audited in this period"', 'colDashCov', 'ThisItem.Short', 'ThisItem.Done & " / " & ThisItem.Total',
                 'If(ThisItem.Total > 0, ThisItem.Done / ThisItem.Total, 0)', 'If(ThisItem.Done >= ThisItem.Total && ThisItem.Total > 0, ' + GREEN + ', C_Accent)',
                 onsel='Set(varDashStream, If(varDashStream = ThisItem.Stream, "ALL", ThisItem.Stream));\nSelect(btnCalc_Dsh)', selexpr='varDashStream = ThisItem.Stream')
pEdu = listpanel('Edu', 'EDUCATION GIVEN', '"Share of audits where it was given"', 'colDashEdu', 'ThisItem.Item', 'ThisItem.N & "  ·  " & Text(If(varDashN > 0, ThisItem.N / varDashN, 0), "0%")',
                 'If(varDashN > 0, ThisItem.N / varDashN, 0)', 'C_Teal', empty='No education recorded in this period')
pBy = listpanel('By', 'AUDITORS', '"Top 5 by audits. Tap to list their audits"', 'colDashBy', 'ThisItem.Auditor', 'ThisItem.N',
                'If(varDashMaxBy > 0, ThisItem.N / varDashMaxBy, 0)', 'C_Accent',
                onsel='Set(varDashBy, If(varDashBy = ThisItem.Auditor, "", ThisItem.Auditor))', selexpr='varDashBy = ThisItem.Auditor', empty='No audits in this period')

# ------------------------------------------------------------------ audit list
FOCUS = ('Concat(Filter(Table({ t: Switch(varDashFocus, "Follow", "Needs follow-up", "Clear", "All clear", "Found", "DTV not found", "Login", "Login failed", "PList", "Patient list failed", '
         '"Print", "Print failed", "Folder", "Folder and kit not found", "List", "No contents list", "Match", "Kit does not match", "") }, { t: varDashWhyR }, '
         '{ t: If(IsBlank(varDashBy), "", "By " & varDashBy) }), !IsBlank(t)), t, "  ·  ")')
ITEMS = '''SortByColumns(
    Filter(
        colDash,
        Switch(
            varDashFocus,
            "Follow", Follow,
            "Clear", !Follow,
            "Found", FoundRes = "No",
            "Login", LoginRes = "No" && (IsBlank(varDashWhyR) || LoginWhy = varDashWhyR),
            "PList", PListRes = "No",
            "Print", PrintRes = "No" && (IsBlank(varDashWhyR) || PrintWhy = varDashWhyR),
            "Folder", FolderRes = "No",
            "List", ListRes = "No",
            "Match", MatchRes = "No",
            true
        )
        && (IsBlank(varDashBy) || Auditor = varDashBy)
        && (IsBlank(Trim(txtSearch_Dsh.Text)) || Lower(Trim(txtSearch_Dsh.Text)) in Lower(Dept & " " & Loc & " " & Title & " " & Auditor))
    ),
    "When",
    SortOrder.Descending
)'''
LH = 108
DETAIL = ('Concat(Filter(Table({ t: If(IsBlank(ThisItem.LoginWhy), "", "Login: " & ThisItem.LoginWhy) }, { t: If(IsBlank(ThisItem.PrintWhy), "", "Print: " & ThisItem.PrintWhy) }, '
          '{ t: If(IsBlank(ThisItem.Missing), "", "Missing: " & ThisItem.Missing) }, { t: If(IsBlank(ThisItem.Extra), "", "Extra: " & ThisItem.Extra) }, '
          '{ t: If(IsBlank(ThisItem.Issues), "", "Ward: " & ThisItem.Issues) }, { t: ThisItem.Notes }, { t: ThisItem.LoginNotes }, { t: ThisItem.PrintNotes }), !IsBlank(Trim(t))), Trim(t), "  ·  ")')
lrow = box('conRow_Dsh', x='1', y=r(5), w=f'Parent.TemplateWidth - {r(12)}', h=r(LH - 10), fill='C_White', border='C_Line', radius=r(16), children=[
    box('conStripe_Dsh', w=r(8), h='Parent.Height', fill=f'If(ThisItem.Follow, {RED}, {GREEN})', extra={'RadiusTopLeft': r(16), 'RadiusBottomLeft': r(16), 'RadiusTopRight': '0', 'RadiusBottomRight': '0'}),
    lbl('lblRowT_Dsh', 'ThisItem.Dept & If(IsBlank(ThisItem.Loc), "", "  ·  " & ThisItem.Loc)', x=r(22), y=r(8), w=f'Parent.Width - {r(240)}', h=r(24), size=16, color='C_Ink', bold=True),
    lbl('lblRowW_Dsh', 'Text(ThisItem.When, "ddd d mmm yyyy, h:mm AM/PM")', x=f'Parent.Width - {r(220)}', y=r(8), w=r(206), h=r(24), size=13, color='C_Ink2', bold=True, align='Align.Right'),
    lbl('lblRowS_Dsh', 'ThisItem.Title & "  ·  " & ThisItem.Stream & "  ·  " & ThisItem.Auditor & If(ThisItem.ReAudit, "  ·  Re-audit", "")', x=r(22), y=r(32), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Muted'),
    lbl('lblRowI_Dsh', 'If(ThisItem.Follow, ThisItem.Fails, "All clear")', x=r(22), y=r(54), w=f'Parent.Width - {r(36)}', h=r(20), size=14, color=f'If(ThisItem.Follow, {RED}, {GREEN})', bold=True),
    lbl('lblRowD_Dsh', DETAIL, x=r(22), y=r(74), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Ink2'),
])
galList = N('galList_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'Parent.Height - {r(128)}', 'Items': ITEMS, 'TemplatePadding': '0', 'TemplateSize': r(LH), 'Width': f'Parent.Width - {r(28)}', 'X': r(16), 'Y': r(118)}, [lrow])
nf = '!IsBlank(varDashFocus) || !IsBlank(varDashWhyR) || !IsBlank(varDashBy)'
pList = panel('List', 'AUDITS', [
    lbl('lblListN_Dsh', 'CountRows(galList_Dsh.AllItems) & If(CountRows(galList_Dsh.AllItems) = 1, " audit", " audits") & If(' + nf + ', " match", " in this period") & ", newest first"', x=r(20), y=r(38), w=f'Parent.Width - {r(40)}', h=r(22), size=14, color='C_Ink2', bold=True),
    box('conFocus_Dsh', x=r(20), y=r(66), w=f'If({WIDE}, Parent.Width - {r(400)}, Parent.Width - {r(40)})', h=r(40), fill='C_AccentSoft', border='C_Accent', radius=r(20), visible=nf, children=[
        lbl('lblFocus_Dsh', '"Showing: " & ' + FOCUS, x=r(16), w=f'Parent.Width - {r(130)}', h=r(40), size=14, color='C_Accent', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        lbl('lblFocusX_Dsh', '"Clear  ✕"', x=f'Parent.Width - {r(110)}', w=r(96), h=r(40), size=14, color='C_Accent', bold=True, align='Align.Right', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn('btnFocusX_Dsh', 'Set(varDashFocus, "");\nSet(varDashWhyR, "");\nSet(varDashBy, "")')]),
    box('conSearch_Dsh', x=f'Parent.Width - {r(360)}', y=r(14), w=r(340), h=r(44), fill='C_White', border=LINE, radius=r(14), visible=WIDE, children=[
        ico('icoSearch_Dsh', 'Search', r(12), r(11), 22, 'C_Muted'),
        N('txtSearch_Dsh', 'Classic/TextInput@2.3.2', props={'BorderStyle': 'BorderStyle.None', 'Color': 'C_Ink', 'Default': '""', 'DelayOutput': 'true', 'Fill': 'RGBA(0, 0, 0, 0)', 'Font': 'AppFont', 'Height': 'Parent.Height', 'HintText': '"Search department, location, tag, auditor"', 'Size': r(F(14)), 'Width': f'Parent.Width - {r(44)}', 'X': r(40)})]),
    lbl('lblListNone_Dsh', 'If(varDashN = 0, "No audits in this period", "No audits match")', x=r(20), y=r(200), w=f'Parent.Width - {r(40)}', h=r(30), size=16, color='C_Muted', align='Align.Center', visible='CountRows(galList_Dsh.AllItems) = 0'),
    galList])
pList.props.update({'Width': 'DashW', 'Height': r(760), 'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'LayoutMinHeight': r(760)})

loading = lbl('lblLoading_Dsh', '"Loading audits..."', w='DashW', h=r(26), size=15, color='C_Muted', align='Align.Center', visible='varDashLoading',
              extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(26)})
endS = inflow('conEnd_Dsh', r(16), w='DashW', extra={'DropShadow': 'DropShadow.None'})
bodyP = {'AlignInContainer': 'AlignInContainer.SetByContainer', 'DropShadow': 'DropShadow.None', 'LayoutAlignItems': 'LayoutAlignItems.Start', 'LayoutDirection': 'LayoutDirection.Vertical', 'LayoutGap': GAP,
         'LayoutMinHeight': r(250), 'LayoutOverflowY': 'LayoutOverflow.Scroll', 'PaddingBottom': r(10), 'PaddingLeft': 'DashX', 'PaddingRight': 'DashX', 'PaddingTop': r(18), 'Width': 'App.Width'}
bodyP.update(rad('0'))
body = N('conBody_Dsh', 'GroupContainer@1.5.0', 'AutoLayout', bodyP, [
    filters, loading, kpi,
    row('A', [(pChecks, 0.58, 470), (pWhy, 0.42, 470)]),
    row('B', [(pCov, 1 / 3, 360), (pEdu, 1 / 3, 360), (pBy, 1 / 3, 360)]),
    pList, endS])

# ------------------------------------------------------------------ hidden logic buttons
def hidden(name, onselect):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'FontWeight': '""', 'Height': '1', 'OnSelect': onselect, 'Size': r(11), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Visible': 'false', 'Width': '1'}, **SBOX))

SHORT = 'Trim(First(Split(Substitute(s.Value, ",", "&"), "&")).Value)'
LOAD = f'''// LOAD: audits in the chosen period, flattened to plain text columns (one row per audit)
Set(varDashLoading, true);
Refresh(Audit_Results);
ClearCollect(colDashReg, DTV_Register);
If(
    varDashDays > 0,
    ClearCollect(colDashSrc, Filter(Audit_Results, Created >= DateAdd(Today(), -varDashDays, TimeUnit.Days))),
    ClearCollect(colDashSrc, Audit_Results)
);
ClearCollect(
    colDashRows,
    ForAll(
        colDashSrc As a,
        With(
            {{
                d: LookUp(colDashReg, Title = a.Title),
                fails: If(
                    a.DTVFound.Value = "No",
                    "DTV not found",
                    Concat(
                        Filter(
                            Table(
                                {{ p: If(a.LoginWorked.Value = "No", "Login", "") }},
                                {{ p: If(a.PatientListWorked.Value = "No", "Patient list", "") }},
                                {{ p: If(a.PrintWorked.Value = "No", "Print", "") }},
                                {{ p: If(a.FolderFound.Value = "No", "Kit not found", "") }},
                                {{ p: If(a.ContentsListInFolder.Value = "No", "No contents list", "") }},
                                {{ p: If(a.KitMatched.Value = "No", "Kit mismatch", "") }}
                            ),
                            p <> ""
                        ),
                        p,
                        " · "
                    )
                )
            }},
            {{
                AID: a.ID,
                Title: a.Title,
                Dept: Coalesce(d.Department, a.DisplayName, a.Title),
                Loc: Coalesce(d.DTVLocation, ""),
                Stream: Coalesce(a.Stream, d.Stream, ""),
                When: a.Created,
                Auditor: a.'Created By'.DisplayName,
                FoundRes: a.DTVFound.Value,
                LoginRes: a.LoginWorked.Value,
                LoginWhy: a.LoginFailReason.Value,
                LoginNotes: a.LoginNotes,
                PListRes: a.PatientListWorked.Value,
                PrintRes: a.PrintWorked.Value,
                PrintWhy: a.PrintFailReason.Value,
                PrintNotes: a.PrintNotes,
                FolderRes: a.FolderFound.Value,
                ListRes: a.ContentsListInFolder.Value,
                MatchRes: a.KitMatched.Value,
                Missing: a.MissingItems,
                Extra: a.ExtraItems,
                Spoke: a.SpokeTo,
                Edu: Concat(a.EducationGiven, Value, "; "),
                Issues: a.IssuesRaised,
                Notes: a.Notes,
                ReAudit: !IsBlank(a.ReAudit),
                Fails: fails,
                Follow: !IsBlank(fails)
            }}
        )
    )
);
Clear(colDashSrc);
// coverage by stream (period only, not the stream filter): shared DTVs (Stream = "All") count in every stream
ClearCollect(
    colDashCov,
    ForAll(
        Filter(Distinct(colDashReg, Stream), !IsBlank(Value) && Value <> "All") As s,
        With(
            {{ tot: Filter(colDashReg, Stream = s.Value || Stream = "All") }},
            {{
                Stream: s.Value,
                Short: {SHORT},
                Total: CountRows(tot),
                Done: CountRows(Filter(tot, Title in colDashRows.Title))
            }}
        )
    )
);
Set(varDashLoading, false);
Select(btnCalc_Dsh)'''

PRINTS = ['Printer offline or not found', 'No printer set up on DTV', 'Sent to print nothing came out', 'Printed on wrong printer', 'Error message (auditor types it)', 'Other (type it)']
LOGINS = ['Password/Username is wrong', 'Unable to access DTV', 'Other']
EDU = ['Downtime Escalation Pathway', 'Downtime Process', 'Downtime Coordinator', "Key's Location", 'DMN Resourcing Page']
CHECKS = [('Found', 'DTV Found', 'FoundRes'), ('Login', 'Login', 'LoginRes'), ('PList', 'Patient List', 'PListRes'), ('Print', 'Print', 'PrintRes'),
          ('Folder', 'Folder and Kit Found', 'FolderRes'), ('List', 'Contents List', 'ListRes'), ('Match', 'Kit Matches List', 'MatchRes')]
whyrows = ',\n            '.join([f'{{ K: "Print", R: "{t}" }}' for t in PRINTS] + [f'{{ K: "Login", R: "{t}" }}' for t in LOGINS])
chkrows = ',\n    '.join(f'{{ Key: "{k}", Label: "{l}", Yes: CountIf(colDash, {c} = "Yes"), No: CountIf(colDash, {c} = "No") }}' for k, l, c in CHECKS)
edurows = ', '.join(f'{{ V: "{e}" }}' for e in EDU)
CALC = f'''// CALC: apply the stream filter, then every number and chart on the screen
ClearCollect(colDash, Filter(colDashRows, varDashStream = "ALL" || Stream = varDashStream || Stream = "All"));
Set(varDashN, CountRows(colDash));
Set(varDashReN, CountIf(colDash, ReAudit));
Set(varDashFollowN, CountIf(colDash, Follow));
Set(varDashClearN, varDashN - varDashFollowN);
Set(varDashNotFoundN, CountIf(colDash, FoundRes = "No"));
ClearCollect(colDashRegS, Filter(colDashReg, varDashStream = "ALL" || Stream = varDashStream || Stream = "All"));
Set(varDashRegN, CountRows(colDashRegS));
Set(varDashCovN, CountRows(Filter(colDashRegS, Title in colDash.Title)));
ClearCollect(
    colDashChecks,
    {chkrows}
);
ClearCollect(
    colDashWhy,
    ForAll(
        Table(
            {whyrows}
        ) As t,
        {{
            Kind: t.K,
            Reason: t.R,
            N: If(t.K = "Print", CountIf(colDash, PrintRes = "No" && PrintWhy = t.R), CountIf(colDash, LoginRes = "No" && LoginWhy = t.R))
        }}
    )
);
Set(varDashMaxPrint, Max(Filter(colDashWhy, Kind = "Print"), N));
Set(varDashMaxLogin, Max(Filter(colDashWhy, Kind = "Login"), N));
ClearCollect(colDashEdu, ForAll(Table({edurows}) As e, {{ Item: e.V, N: CountIf(colDash, e.V in Edu) }}));
ClearCollect(colDashBy, FirstN(SortByColumns(AddColumns(GroupBy(colDash, Auditor, Rows), N, CountRows(Rows)), "N", SortOrder.Descending), 5));
Set(varDashMaxBy, Max(colDashBy, N))'''

# ---- email: branded summary + CSV of every audit in the period and stream
def q(expr):
    return f'Char(34) & Substitute(Substitute(Substitute(Coalesce({expr}, ""), Char(34), Char(34) & Char(34)), Char(13), " "), Char(10), " ") & Char(34)'
CSV_COLS = [('Audit Date', 'Text(When, "yyyy-mm-dd hh:mm")'), ('Asset Tag', 'Title'), ('Department', 'Dept'), ('Location', 'Loc'), ('Stream', 'Stream'), ('Auditor', 'Auditor'),
            ('Re-audit', 'If(ReAudit, "Yes", "No")'), ('Result', 'If(Follow, "Needs follow-up", "All clear")'), ('Issues Summary', 'Fails'),
            ('DTV Found', 'FoundRes'), ('Login Worked', 'LoginRes'), ('Login Fail Reason', 'LoginWhy'), ('Login Notes', 'LoginNotes'), ('Patient List Worked', 'PListRes'),
            ('Print Worked', 'PrintRes'), ('Print Fail Reason', 'PrintWhy'), ('Print Notes', 'PrintNotes'), ('Folder and Kit Found', 'FolderRes'), ('Contents List In Folder', 'ListRes'),
            ('Kit Matched', 'MatchRes'), ('Missing Items', 'Missing'), ('Extra Items', 'Extra'), ('Spoke To', 'Spoke'), ('Education Given', 'Edu'), ('Issues Raised', 'Issues'), ('Notes', 'Notes')]
csv_head = ','.join(c for c, _ in CSV_COLS)
csv_row = ' & "," &\n            '.join(q(e) for _, e in CSV_COLS)
TH_ = "padding:10px 12px;font-size:11px;letter-spacing:1px;color:#8C9BAE;border-bottom:2px solid #1A5A99;"
TD_ = "padding:10px 12px;border-top:1px solid #E3EAF1;"
SEC = "padding:20px 32px 6px 32px;font-size:11px;letter-spacing:2px;font-weight:700;color:#8C9BAE;"
TBL = "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0' style='border-collapse:separate;border-spacing:0;width:100%;font-size:14px;border:1px solid #E3EAF1;border-radius:14px;overflow:hidden;'>"
def kcell(label, val, sub, col):
    return (f'''"<td width='20%' valign='top' style='padding:4px;'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0'><tr><td bgcolor='#F4F9FC' style='background-color:#F4F9FC;border:1px solid #E3EAF1;border-radius:12px;padding:12px 12px;'>" &
                "<div style='font-size:10px;letter-spacing:1px;font-weight:700;color:#8C9BAE;'>{label}</div>" &
                "<div style='font-size:24px;font-weight:700;color:{col};padding-top:4px;'>" & {val} & "</div>" &
                "<div style='font-size:12px;color:#3A5068;padding-top:2px;'>" & {sub} & "</div>" &
            "</td></tr></table></td>" &''')
SEND = f'''// EMAIL: branded summary + CSV of every audit in the chosen period and stream (Office 365 Outlook connector)
If(
    varDashN = 0,
    Notify("No audits in this period to send.", NotificationType.Information),
    Set(varSaving, true);
    Set(varDashRange, {RANGE});
    Set(varDashStreamLbl, {STREAM});
    // ---- CSV (UTF-8 mark first so Excel shows names correctly)
    Set(
        varDashCsv,
        UniChar(65279) & "{csv_head}" & Char(13) & Char(10) &
        Concat(
            SortByColumns(colDash, "When", SortOrder.Descending),
            {csv_row},
            Char(13) & Char(10)
        )
    );
    // ---- HTML summary
    Set(
        varDashEmail,
        Substitute(Substitute(EmailHead, "{{{{TITLE}}}}", "DTV Audit Summary"), "{{{{SUB}}}}", varDashRange & "&nbsp;&nbsp;|&nbsp;&nbsp;" & varDashStreamLbl & "&nbsp;&nbsp;|&nbsp;&nbsp;" & varDashN & If(varDashN = 1, " audit", " audits")) &

        // greeting
        "<tr><td style='padding:28px 32px 8px 32px;font-size:15px;line-height:22px;color:#3A5068;'>" &
            "Hi " & First(Split(User().FullName, " ")).Value & ",<br><br>" &
            "Here is the ieMR Downtime Viewer audit summary for <b style='color:#0E1C2A;'>" & Lower(varDashRange) & "</b> (" & varDashStreamLbl & "). " &
            "Every audit in this view is in the attached CSV file, which opens in Excel." &
        "</td></tr>" &

        // KPI tiles
        "<tr><td style='padding:16px 28px 4px 28px;'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0'><tr>" &
            {kcell('AUDITS', 'varDashN', 'varDashReN & " re-audits"', '#0E1C2A')}
            {kcell('DTVS COVERED', 'varDashCovN & " / " & varDashRegN', 'Text(If(varDashRegN > 0, varDashCovN / varDashRegN, 0), "0%") & " audited"', '#1A5A99')}
            {kcell('ALL CLEAR', 'varDashClearN', 'Text(If(varDashN > 0, varDashClearN / varDashN, 0), "0%") & " of audits"', '#1E7A50')}
            {kcell('FOLLOW-UP', 'varDashFollowN', 'Text(If(varDashN > 0, varDashFollowN / varDashN, 0), "0%") & " of audits"', '#B03428')}
            {kcell('NOT FOUND', 'varDashNotFoundN', '"DTVs"', '#B26900')}
        "</tr></table></td></tr>" &

        // results by check
        "<tr><td style='{SEC}'>RESULTS BY CHECK</td></tr>" &
        "<tr><td style='padding:6px 32px 8px 32px;'>" &
        "{TBL}" &
            "<tr bgcolor='#F2F6FA' style='background-color:#F2F6FA;'>" &
                "<th align='left' style='{TH_}border-radius:14px 0 0 0;'>CHECK</th>" &
                "<th align='left' style='{TH_}'>PASSED / FAILED</th>" &
                "<th align='right' style='{TH_}border-radius:0 14px 0 0;'>FAILED</th>" &
            "</tr>" &
            Concat(
                colDashChecks,
                With(
                    {{ tot: Yes + No, pc: If(Yes + No > 0, Round(Yes * 100 / (Yes + No), 0), 0) }},
                    "<tr>" &
                        "<td style='{TD_}font-weight:600;color:#0E1C2A;'>" & Label & "</td>" &
                        "<td style='{TD_}' width='45%'>" &
                            If(
                                tot = 0,
                                "<span style='color:#8C9BAE;'>Not checked</span>",
                                "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0'><tr>" &
                                    If(pc > 0, "<td width='" & pc & "%' height='10' bgcolor='#1E7A50' style='background-color:#1E7A50;height:10px;font-size:0;line-height:0;'>&nbsp;</td>", "") &
                                    If(pc < 100, "<td width='" & (100 - pc) & "%' height='10' bgcolor='#B03428' style='background-color:#B03428;height:10px;font-size:0;line-height:0;'>&nbsp;</td>", "") &
                                "</tr></table>"
                            ) &
                        "</td>" &
                        "<td align='right' style='{TD_}font-weight:700;color:" & If(No > 0, "#B03428", "#1E7A50") & ";'>" & No & " of " & tot & "</td>" &
                    "</tr>"
                )
            ) &
        "</table></td></tr>" &

        // why it failed
        If(
            varDashMaxPrint + varDashMaxLogin > 0,
            "<tr><td style='{SEC}'>WHY IT FAILED</td></tr>" &
            "<tr><td style='padding:6px 32px 8px 32px;'>" &
            "{TBL}" &
                Concat(
                    Filter(colDashWhy, N > 0),
                    "<tr>" &
                        "<td style='{TD_}color:#8C9BAE;font-size:12px;font-weight:700;' width='70'>" & Upper(Kind) & "</td>" &
                        "<td style='{TD_}color:#0E1C2A;'>" & Reason & "</td>" &
                        "<td align='right' style='{TD_}font-weight:700;color:#B03428;'>" & N & "</td>" &
                    "</tr>"
                ) &
            "</table></td></tr>",
            ""
        ) &

        // coverage by stream
        "<tr><td style='{SEC}'>COVERAGE BY STREAM</td></tr>" &
        "<tr><td style='padding:6px 32px 8px 32px;'>" &
        "{TBL}" &
            Concat(
                colDashCov,
                "<tr>" &
                    "<td style='{TD_}font-weight:600;color:#0E1C2A;'>" & Stream & "</td>" &
                    "<td align='right' style='{TD_}color:#3A5068;'>" & Done & " of " & Total & " DTVs</td>" &
                    "<td align='right' style='{TD_}font-weight:700;color:" & If(Done >= Total && Total > 0, "#1E7A50", "#1A5A99") & ";' width='60'>" & Text(If(Total > 0, Done / Total, 0), "0%") & "</td>" &
                "</tr>"
            ) &
        "</table></td></tr>" &

        // needs follow-up (newest 30)
        If(
            varDashFollowN > 0,
            "<tr><td style='{SEC}'>NEEDS FOLLOW-UP</td></tr>" &
            "<tr><td style='padding:6px 32px 8px 32px;'>" &
            "{TBL}" &
                "<tr bgcolor='#F2F6FA' style='background-color:#F2F6FA;'>" &
                    "<th align='left' style='{TH_}border-radius:14px 0 0 0;'>DTV</th>" &
                    "<th align='left' style='{TH_}'>DATE</th>" &
                    "<th align='left' style='{TH_}border-radius:0 14px 0 0;'>ISSUE</th>" &
                "</tr>" &
                Concat(
                    FirstN(SortByColumns(Filter(colDash, Follow), "When", SortOrder.Descending), 30),
                    "<tr>" &
                        "<td style='{TD_}'><b style='color:#0E1C2A;'>" & Dept & "</b><br><span style='font-size:12px;color:#8C9BAE;'>" & Loc & "&nbsp;&nbsp;|&nbsp;&nbsp;" & Title & "</span></td>" &
                        "<td style='{TD_}color:#3A5068;white-space:nowrap;'>" & Text(When, "d mmm") & "</td>" &
                        "<td style='{TD_}color:#B03428;font-weight:600;'>" & Fails & "</td>" &
                    "</tr>"
                ) &
            "</table>" &
            If(varDashFollowN > 30, "<div style='font-size:12px;color:#8C9BAE;padding-top:8px;'>+ " & (varDashFollowN - 30) & " more in the attached file.</div>", "") &
            "</td></tr>",
            ""
        ) &

        // sign-off
        "<tr><td style='padding:20px 32px 28px 32px;font-size:15px;line-height:22px;color:#3A5068;'>Thanks,<br><b style='color:#0E1C2A;'>" & User().FullName & "</b></td></tr>" &

        Substitute(EmailFoot, "{{{{NOTE}}}}", "This email and its attachment contain staff names. Please handle them in line with your privacy policy.")
    );
    If(
        IsError(
            Office365Outlook.SendEmailV2(
                User().Email,
                "DTV Audit Summary: " & varDashRange & " (" & varDashStreamLbl & ")",
                varDashEmail,
                {{
                    IsHtml: true,
                    Attachments: Table({{ Name: "DTV_Audits_" & Text(Today(), "yyyy-mm-dd") & ".csv", ContentBytes: varDashCsv }})
                }}
            )
        ),
        Notify("Could not send the email. Check your connection and try again.", NotificationType.Error),
        Notify("Email sent to " & User().Email & ".", NotificationType.Success)
    );
    Set(varSaving, false)
)'''

ONV = f'''If(IsBlank(varDashDays), Set(varDashDays, 30));
If(IsBlank(varDashStream), Set(varDashStream, "ALL"));
If(IsBlank(varDashWhyKind), Set(varDashWhyKind, "Print"));
Set(varDashFocus, "");
Set(varDashWhyR, "");
Set(varDashBy, "");
Set(varSaving, false);
Reset(txtSearch_Dsh);
// stream pills: All, then one per stream (short name = text before the first "&" or ",")
ClearCollect(colDashPills, {{ Label: "All Streams", Key: "ALL" }});
ForAll(
    Filter(Distinct(DTV_Register, Stream), !IsBlank(Value) && Value <> "All") As s,
    Collect(colDashPills, {{ Label: {SHORT}, Key: s.Value }})
);
Select(btnLoad_Dsh)'''

kids = [vroot('conRoot_Dsh', [hdr, body]), hidden('btnLoad_Dsh', LOAD), hidden('btnCalc_Dsh', CALC), hidden('btnSend_Dsh', SEND)]
open(OUT + 'DTV_Dashboard.pa.yaml', 'w').write(screen('Dashboard', {'Fill': 'C_Bg', 'OnVisible': ONV}, kids))
print('built Dashboard')
