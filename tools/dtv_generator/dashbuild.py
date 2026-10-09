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
STREAM = 'If(varDashStream = "ALL", "All streams", varDashStream)'
hdr = inflow('conHdr_Dsh', r(95), w='App.Width', fill=HDR_FILL, radius='0', extra={'DropShadow': 'DropShadow.None'}, children=[
    N('imgHdr_Dsh', 'Image@2.2.3', props={'Height': 'Parent.Height', 'Image': 'HeaderImage', 'ImagePosition': 'ImagePosition.Fill', 'Width': 'Parent.Width'}),
    N('btnBack_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_White', 'FontWeight': '""', 'Height': r(60), 'Icon': '"ChevronLeft"', 'OnSelect': 'Navigate(Home, ScreenTransition.UnCoverRight)', 'Size': r(24), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': r(60), 'X': f'DashX - {r(10)}', 'Y': r(18)}, **SBOX)),
    lbl('lblHdrT_Dsh', '"Audit Dashboard"', x=f'DashX + {r(55)}', y=r(12), w=f'DashW - {r(55)} - If({WIDE}, {r(250)}, {r(80)})', h=r(42), size=24, color='C_White', bold=True),
    lbl('lblHdrS_Dsh', f'{STREAM} & "  ·  " & varDashN & If(varDashN = 1, " DTV", " DTVs") & " audited  ·  latest audit each"', x=f'DashX + {r(55)}', y=r(53), w=f'DashW - {r(55)} - If({WIDE}, {r(250)}, {r(80)})', h=r(25), size=15, color='RGBA(255, 255, 255, 0.85)'),
    box('conEmail_Dsh', x=f'DashX + DashW - If({WIDE}, {r(230)}, {r(60)})', y=r(22), w=f'If({WIDE}, {r(230)}, {r(60)})', h=r(50), fill='RGBA(255, 255, 255, 0.16)', border='RGBA(255, 255, 255, 0.45)', radius=r(25), children=[
        N('btnEmail_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_White', 'DisplayMode': 'If(varSaving || varDashN = 0, DisplayMode.Disabled, DisplayMode.Edit)', 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'Icon': '"Mail"', 'OnSelect': 'Select(btnSend_Dsh)', 'Size': r(F(15)), 'Text': f'If({WIDE}, If(varSaving, "Sending...", "Email Me the Data"), "")', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(25)), **NOSB))]),
])

# ------------------------------------------------------------------ filters
selS = 'ThisItem.Key = varDashStream'
galStr = N('galStream_Dsh', 'Gallery@2.15.0', 'Horizontal', {'Height': r(52), 'Items': 'colDashPills', 'ShowScrollbar': 'false', 'TemplatePadding': '0',
    'TemplateSize': f'(Parent.Width - {r(32)}) / Max(1, CountRows(colDashPills))', 'Width': f'Parent.Width - {r(32)}', 'X': r(16), 'Y': r(12)}, [
    box('conStr_Dsh', x='3', y=r(2), w=f'Parent.TemplateWidth - {r(6)}', h=r(48), fill=f'If({selS}, C_Accent, C_White)', border=f'If({selS}, C_Accent, C_Line)', radius=r(24), children=[
        lbl('lblStr_Dsh', 'ThisItem.Label', x=r(4), w=f'Parent.Width - {r(8)}', h=r(48), size=14, color=f'If({selS}, C_White, C_Ink2)', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn('btnStr_Dsh', 'Set(varDashStream, ThisItem.Key);\nSelect(btnCalc_Dsh)')])])
filters = inflow('conFilters_Dsh', r(76), w='DashW', fill='C_White', border='C_Line', radius=r(20), children=[galStr])

# ------------------------------------------------------------------ KPI tiles
KPIS = [  # key, caption, value, sub, colour, focus
    ('Aud', 'DTVS AUDITED', 'varDashN & " / " & varDashRegN', 'Text(If(varDashRegN > 0, varDashCovN / varDashRegN, 0), "0%") & " of the register"', 'C_Ink', ''),
    ('Cov', 'NOT YET AUDITED', 'Max(0, varDashRegN - varDashCovN)', '"DTVs with no audit"', 'C_Accent', ''),
    ('Clr', 'ALL CLEAR', 'varDashClearN', 'Text(If(varDashN > 0, varDashClearN / varDashN, 0), "0%") & " of DTVs"', GREEN, 'Clear'),
    ('Fol', 'NEED FOLLOW-UP', 'varDashFollowN', 'Text(If(varDashN > 0, varDashFollowN / varDashN, 0), "0%") & " of DTVs"', RED, 'Follow'),
    ('Nf', 'DTV NOT FOUND', 'varDashNotFoundN', '"Tap to list them"', 'C_Amber', 'Found'),
]
TH = 112
twW = f'(DashW - 4 * {GAP}) / 5'; twN = f'(DashW - {GAP}) / 2'
tiles = []
for i, (k, cap, val, sub, col, foc) in enumerate(KPIS):
    sel = f'varDashFocus = "{foc}"' if foc else 'false'
    onsel = (f'Set(varDashFocus, If(varDashFocus = "{foc}", "", "{foc}"));\nSet(varDashWhyR, "")' if foc else 'Set(varDashFocus, "");\nSet(varDashWhyR, "");\nSet(varDashStage, "")')
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
    lbl('lblChkHint_Dsh', '"Green passed, red failed. Tap a row to list those DTVs below."', x=r(20), y=f'Parent.Height - {r(34)}', w=f'Parent.Width - {r(40)}', h=r(22), size=13, color='C_Muted')],
    sub='"Latest audit for each DTV"')

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
    lbl('lblWhyNone_Dsh', 'If(varDashWhyKind = "Print", "No print failures", "No login failures") & " so far"', x=r(20), y=r(150), w=f'Parent.Width - {r(40)}', h=r(30), size=15, color='C_Muted', align='Align.Center',
        visible='If(varDashWhyKind = "Print", varDashMaxPrint, varDashMaxLogin) = 0')],
    sub='"Tap a reason to list those DTVs"')

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
pCov = listpanel('Cov', 'COVERAGE BY STREAM', '"DTVs audited so far"', 'colDashCov', 'ThisItem.Short', 'ThisItem.Done & " / " & ThisItem.Total',
                 'If(ThisItem.Total > 0, ThisItem.Done / ThisItem.Total, 0)', 'If(ThisItem.Done >= ThisItem.Total && ThisItem.Total > 0, ' + GREEN + ', C_Accent)',
                 onsel='Set(varDashStream, If(varDashStream = ThisItem.Stream, "ALL", ThisItem.Stream));\nSelect(btnCalc_Dsh)', selexpr='varDashStream = ThisItem.Stream')
pEdu = listpanel('Edu', 'EDUCATION GIVEN', '"Share of DTVs (latest audit)"', 'colDashEdu', 'ThisItem.Item', 'ThisItem.N & "  ·  " & Text(If(varDashN > 0, ThisItem.N / varDashN, 0), "0%")',
                 'If(varDashN > 0, ThisItem.N / varDashN, 0)', 'C_Teal', empty='No education recorded yet')
# follow-up progress: compares each DTV's first audit with its latest. Is follow-up fixing things?
pStage = listpanel('Stage', 'FOLLOW-UP PROGRESS', '"First audit vs latest. Tap to list them"', 'colDashStage', 'ThisItem.Label', 'ThisItem.N',
                'If(varDashMaxStage > 0, ThisItem.N / varDashMaxStage, 0)', f'Switch(ThisItem.Key, "Fixed", {GREEN}, "New", C_Amber, {RED})',
                onsel='Set(varDashStage, If(varDashStage = ThisItem.Key, "", ThisItem.Key))', selexpr='varDashStage = ThisItem.Key', empty='No failures found yet')

# ------------------------------------------------------------------ audit list
FOCUS = ('Concat(Filter(Table({ t: Switch(varDashFocus, "Follow", "Needs follow-up", "Clear", "All clear", "Found", "DTV not found", "Login", "Login failed", "PList", "Patient list failed", '
         '"Print", "Print failed", "Folder", "Folder and kit not found", "List", "No contents list", "Match", "Kit does not match", "") }, { t: varDashWhyR }, '
         '{ t: Switch(varDashStage, "Waiting", "Failed, not re-audited", "Still", "Still failing after re-audit", "Fixed", "Fixed on re-audit", "New", "New issue on re-audit", "") }), !IsBlank(t)), t, "  ·  ")')
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
        && (IsBlank(varDashStage) || Stage = varDashStage)
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
    lbl('lblRowT_Dsh', 'ThisItem.Dept & If(IsBlank(ThisItem.Loc), "", "  ·  " & ThisItem.Loc)', x=r(22), y=r(8), w=f'Parent.Width - {r(270)}', h=r(24), size=16, color='C_Ink', bold=True),
    lbl('lblRowW_Dsh', 'Text(ThisItem.When, "ddd d mmm yyyy, h:mm AM/PM")', x=f'Parent.Width - {r(250)}', y=r(8), w=r(206), h=r(24), size=13, color='C_Ink2', bold=True, align='Align.Right'),
    lbl('lblRowS_Dsh', 'ThisItem.Title & "  ·  " & ThisItem.Stream & "  ·  " & ThisItem.Auditor & If(ThisItem.AuditN > 1, "  ·  " & ThisItem.AuditN & " audits, showing latest", "")', x=r(22), y=r(32), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Muted'),
    lbl('lblRowI_Dsh', 'If(ThisItem.Follow, ThisItem.Fails, "All clear")', x=r(22), y=r(54), w=f'Parent.Width - {r(36)}', h=r(20), size=14, color=f'If(ThisItem.Follow, {RED}, {GREEN})', bold=True),
    lbl('lblRowD_Dsh', DETAIL, x=r(22), y=r(74), w=f'Parent.Width - {r(70)}', h=r(20), size=13, color='C_Ink2'),
    ico('icoRowGo_Dsh', 'ChevronRight', f'Parent.Width - {r(40)}', r(40), 24, 'C_Muted'),
    tbtn('btnRow_Dsh', 'Set(varDashSel, LookUp(colDashSrc, ID = ThisItem.AID));\nSet(varDashShowDet, true)'),
])
galList = N('galList_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'Parent.Height - {r(128)}', 'Items': ITEMS, 'TemplatePadding': '0', 'TemplateSize': r(LH), 'Width': f'Parent.Width - {r(28)}', 'X': r(16), 'Y': r(118)}, [lrow])
nf = '!IsBlank(varDashFocus) || !IsBlank(varDashWhyR) || !IsBlank(varDashStage)'
pList = panel('List', 'DTVS', [
    lbl('lblListN_Dsh', 'CountRows(galList_Dsh.AllItems) & If(CountRows(galList_Dsh.AllItems) = 1, " DTV", " DTVs") & If(' + nf + ', " match", " audited") & ", latest audit each, newest first"', x=r(20), y=r(38), w=f'Parent.Width - {r(40)}', h=r(22), size=14, color='C_Ink2', bold=True),
    box('conFocus_Dsh', x=r(20), y=r(66), w=f'If({WIDE}, Parent.Width - {r(400)}, Parent.Width - {r(40)})', h=r(40), fill='C_AccentSoft', border='C_Accent', radius=r(20), visible=nf, children=[
        lbl('lblFocus_Dsh', '"Showing: " & ' + FOCUS, x=r(16), w=f'Parent.Width - {r(130)}', h=r(40), size=14, color='C_Accent', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        lbl('lblFocusX_Dsh', '"Clear  ✕"', x=f'Parent.Width - {r(110)}', w=r(96), h=r(40), size=14, color='C_Accent', bold=True, align='Align.Right', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn('btnFocusX_Dsh', 'Set(varDashFocus, "");\nSet(varDashWhyR, "");\nSet(varDashStage, "")')]),
    box('conSearch_Dsh', x=f'Parent.Width - {r(360)}', y=r(14), w=r(340), h=r(44), fill='C_White', border=LINE, radius=r(14), visible=WIDE, children=[
        ico('icoSearch_Dsh', 'Search', r(12), r(11), 22, 'C_Muted'),
        N('txtSearch_Dsh', 'Classic/TextInput@2.3.2', props={'BorderStyle': 'BorderStyle.None', 'Color': 'C_Ink', 'Default': '""', 'DelayOutput': 'true', 'Fill': 'RGBA(0, 0, 0, 0)', 'Font': 'AppFont', 'Height': 'Parent.Height', 'HintText': '"Search department, location, tag, auditor"', 'Size': r(F(14)), 'Width': f'Parent.Width - {r(44)}', 'X': r(40)})]),
    lbl('lblListNone_Dsh', 'If(varDashN = 0, "No DTVs audited yet", "No DTVs match")', x=r(20), y=r(200), w=f'Parent.Width - {r(40)}', h=r(30), size=16, color='C_Muted', align='Align.Center', visible='CountRows(galList_Dsh.AllItems) = 0'),
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
    row('B', [(pCov, 1 / 3, 360), (pEdu, 1 / 3, 360), (pStage, 1 / 3, 360)]),
    pList, endS])

# ------------------------------------------------------------------ wrap gallery rows
def wrap(g, rowname):
    for k in g.children:
        for pk, pv in list(k.props.items()):
            k.props[pk] = str(pv).replace('Parent.TemplateWidth', 'Parent.Width')
    g.children = [box(rowname, x='0', y='0', w='Parent.TemplateWidth', h='Parent.TemplateHeight', children=g.children)]
wrap(galChk, 'conChkRow_Dsh'); wrap(galWhy, 'conWhyRow_Dsh')
for pnl, nm in ((pCov, 'Cov'), (pEdu, 'Edu'), (pStage, 'Stage')):
    wrap(next(c for c in pnl.children if c.name == f'gal{nm}_Dsh'), f'con{nm}Row_Dsh')

# ------------------------------------------------------------------ hidden logic buttons
def hidden(name, onselect):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'FontWeight': '""', 'Height': '1', 'OnSelect': onselect, 'Size': r(11), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Visible': 'false', 'Width': '1'}, **SBOX))

SHORT = 'Trim(First(Split(Substitute(s.Value, ",", "&"), "&")).Value)'
LOAD = f'''// LOAD: every audit, flattened to plain text columns (one row per DTV, latest audit)
Set(varDashLoading, true);
Refresh(Audit_Results);
ClearCollect(colDashReg, DTV_Register);
// newest first, so LookUp below returns each DTV's latest audit
ClearCollect(colDashSrc, SortByColumns(Audit_Results, "Created", SortOrder.Descending));
// FINAL STATE: one row per DTV = its latest audit (earlier audits and re-audits are replaced)
ClearCollect(
    colDashRows,
    ForAll(
        Distinct(colDashSrc, Title) As u,
        With(
            {{
                a: LookUp(colDashSrc, Title = u.Value),
                f: Last(Filter(colDashSrc, Title = u.Value)),
                cnt: CountIf(colDashSrc, Title = u.Value)
            }},
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
                Follow: !IsBlank(fails),
                AuditN: cnt,
                // first audit vs latest: Waiting = failed, no re-audit yet; Still = failed both; Fixed = failed then clear; New = clear then failed
                Stage: With(
                    {{
                        firstFail: f.DTVFound.Value = "No" || f.LoginWorked.Value = "No" || f.PatientListWorked.Value = "No" || f.PrintWorked.Value = "No"
                            || f.FolderFound.Value = "No" || f.ContentsListInFolder.Value = "No" || f.KitMatched.Value = "No"
                    }},
                    If(
                        cnt > 1,
                        If(firstFail, If(IsBlank(fails), "Fixed", "Still"), If(IsBlank(fails), "Clear", "New")),
                        If(IsBlank(fails), "Clear", "Waiting")
                    )
                )
            }}
        )
        )
    )
);
// colDashSrc is kept: the audit detail panel reads the full record (photo, notes) from it
// coverage by stream (ignores the stream filter): shared DTVs (Stream = "All") count in every stream
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
ClearCollect(
    colDashStage,
    {{ Key: "Waiting", Label: "Failed, not re-audited yet", N: CountIf(colDash, Stage = "Waiting") }},
    {{ Key: "Still", Label: "Still failing after re-audit", N: CountIf(colDash, Stage = "Still") }},
    {{ Key: "Fixed", Label: "Fixed on re-audit", N: CountIf(colDash, Stage = "Fixed") }},
    {{ Key: "New", Label: "New issue on re-audit", N: CountIf(colDash, Stage = "New") }}
);
Set(varDashMaxStage, Max(colDashStage, N))'''

# ---- email: branded summary + CSV of every audit in the period and stream
def q(expr):
    return f'Char(34) & Substitute(Substitute(Substitute(Coalesce({expr}, ""), Char(34), Char(34) & Char(34)), Char(13), " "), Char(10), " ") & Char(34)'
CSV_COLS = [('Audit Date', 'Text(When, "yyyy-mm-dd hh:mm")'), ('Asset Tag', 'Title'), ('Department', 'Dept'), ('Location', 'Loc'), ('Stream', 'Stream'), ('Auditor', 'Auditor'),
            ('Audits Done', 'Text(AuditN)'), ('Follow-up Status', 'Switch(Stage, "Waiting", "Failed, not re-audited yet", "Still", "Still failing after re-audit", "Fixed", "Fixed on re-audit", "New", "New issue on re-audit", "Clear")'), ('Latest Was Re-audit', 'If(ReAudit, "Yes", "No")'), ('Result', 'If(Follow, "Needs follow-up", "All clear")'), ('Issues Summary', 'Fails'),
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
SEND = f'''// EMAIL: branded summary + CSV of the final state of every DTV (latest audit each) in the chosen stream (sent by the flow DTVDashboardEmail)
If(
    varDashN = 0,
    Notify("No DTVs audited yet.", NotificationType.Information),
    Set(varSaving, true);
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
        Substitute(Substitute(EmailHead, "{{{{TITLE}}}}", "DTV Audit Summary"), "{{{{SUB}}}}", varDashStreamLbl & "&nbsp;&nbsp;|&nbsp;&nbsp;" & varDashN & If(varDashN = 1, " DTV", " DTVs")) &

        // greeting
        "<tr><td style='padding:28px 32px 8px 32px;font-size:15px;line-height:22px;color:#3A5068;'>" &
            "Hi " & First(Split(User().FullName, " ")).Value & ",<br><br>" &
            "Here is the current state of every audited ieMR Downtime Viewer (<b style='color:#0E1C2A;'>" & varDashStreamLbl & "</b>). " &
            "Each DTV is counted once, using its latest audit. The attached CSV file (opens in Excel) has one row per DTV." &
        "</td></tr>" &

        // KPI tiles
        "<tr><td style='padding:16px 28px 4px 28px;'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0'><tr>" &
            {kcell('DTVS AUDITED', 'varDashN', '"of " & varDashRegN & " on register"', '#0E1C2A')}
            {kcell('NOT AUDITED', 'Max(0, varDashRegN - varDashCovN)', '"DTVs"', '#1A5A99')}
            {kcell('ALL CLEAR', 'varDashClearN', 'Text(If(varDashN > 0, varDashClearN / varDashN, 0), "0%") & " of DTVs"', '#1E7A50')}
            {kcell('FOLLOW-UP', 'varDashFollowN', 'Text(If(varDashN > 0, varDashFollowN / varDashN, 0), "0%") & " of DTVs"', '#B03428')}
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

        // follow-up progress
        If(
            varDashMaxStage > 0,
            "<tr><td style='{SEC}'>FOLLOW-UP PROGRESS</td></tr>" &
            "<tr><td style='padding:6px 32px 8px 32px;'>" &
            "{TBL}" &
                Concat(
                    colDashStage,
                    "<tr>" &
                        "<td style='{TD_}font-weight:600;color:#0E1C2A;'>" & Label & "</td>" &
                        "<td align='right' style='{TD_}font-weight:700;color:" & Switch(Key, "Fixed", "#1E7A50", "New", "#B26900", "#B03428") & ";' width='60'>" & N & "</td>" &
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
    // the flow sends it: Power Apps cannot attach a text file itself
    If(
        IsError(
            DTVDashboardEmail.Run(
                User().Email,
                "DTV Audit Summary (" & varDashStreamLbl & ")",
                varDashEmail,
                "DTV_Audits_" & Text(Today(), "yyyy-mm-dd") & ".csv",
                varDashCsv
            )
        ),
        Notify("Could not send the email. Check your connection and try again.", NotificationType.Error),
        Notify("Email sent to " & User().Email & ".", NotificationType.Success)
    );
    Set(varSaving, false)
)'''

ONV = f'''If(IsBlank(varDashStream), Set(varDashStream, "ALL"));
If(IsBlank(varDashWhyKind), Set(varDashWhyKind, "Print"));
Set(varDashFocus, "");
Set(varDashWhyR, "");
Set(varDashStage, "");
Set(varSaving, false);
Set(varDashShowDet, false);
Reset(txtSearch_Dsh);
// stream pills: All, then one per stream (short name = text before the first "&" or ",")
ClearCollect(colDashPills, {{ Label: "All Streams", Key: "ALL" }});
ForAll(
    Filter(Distinct(DTV_Register, Stream), !IsBlank(Value) && Value <> "All") As s,
    Collect(colDashPills, {{ Label: {SHORT}, Key: s.Value }})
);
Select(btnLoad_Dsh)'''


# ------------------------------------------------------------------ audit detail (drill-in)
S_ = 'varDashSel'
REG = f'LookUp(colDashReg, Title = {S_}.Title)'
FAILS_SEL = (f'{S_}.DTVFound.Value = "No" || {S_}.LoginWorked.Value = "No" || {S_}.PatientListWorked.Value = "No" || {S_}.PrintWorked.Value = "No" '
             f'|| {S_}.FolderFound.Value = "No" || {S_}.ContentsListInFolder.Value = "No" || {S_}.KitMatched.Value = "No"')
DETW = f'Min(App.Width - {r(48)}, {r(980)})'
IW2 = f'{DETW} - {r(64)}'
def dlbl(name, text, h, size=15, color='C_Ink', bold=False, wrap=False, auto=False, visible=None):
    x = {'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'LayoutMinHeight': r(h)}
    if auto: x['AutoHeight'] = 'true'
    return lbl(name, text, w=IW2, h=r(h), size=size, color=color, bold=bold, wrap=wrap, visible=visible, extra=x)
def dcap(name, text, visible=None):
    return dlbl(name, f'"{text}"', 30, size=13, color='C_Muted', bold=True, visible=visible)
def answer(v):
    return f'Coalesce({S_}.{v}.Value, "Skipped")'
def acol(v):
    return f'Switch({S_}.{v}.Value, "Yes", {GREEN}, "No", {RED}, C_Muted)'
QS = [('Found', 'DTV found', 'DTVFound'), ('Login', 'Login', 'LoginWorked'), ('PList', 'Patient list opened', 'PatientListWorked'), ('Print', 'Print', 'PrintWorked'),
      ('Folder', 'Yellow folder and kit found', 'FolderFound'), ('List', 'Contents list in folder', 'ContentsListInFolder'), ('Match', 'Kit matches the list', 'KitMatched')]
QH = 46
qrows = []
for i, (k, label, col) in enumerate(QS):
    qrows += [
        box(f'conQ{k}Ln_Dsh', x='0', y=r(i * QH), w='Parent.Width', h='1', fill='C_Line') if i else None,
        lbl(f'lblQ{k}_Dsh', f'"{label}"', x=r(16), y=r(i * QH), w=f'Parent.Width - {r(160)}', h=r(QH), size=15, color='C_Ink2', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        box(f'conQ{k}A_Dsh', x=f'Parent.Width - {r(126)}', y=r(i * QH + 9), w=r(110), h=r(28), fill=f'Switch({S_}.{col}.Value, "Yes", RGBA(30, 122, 80, 0.12), "No", RGBA(176, 52, 40, 0.12), C_Bg)', radius=r(14), children=[
            lbl(f'lblQ{k}A_Dsh', answer(col), w='Parent.Width', h=r(28), size=13, color=acol(col), bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})])]
qrows = [q for q in qrows if q]
checks = inflow('conDetChecks_Dsh', r(len(QS) * QH), w=IW2, fill='C_White', border='C_Line', radius=r(14), children=qrows)
def pair(k, cap, expr):
    vis = f'!IsBlank(Trim({expr}))'
    return [dlbl(f'lblD{k}C_Dsh', f'"{cap}"', 24, size=13, color='C_Muted', bold=True, visible=vis),
            dlbl(f'lblD{k}V_Dsh', expr, 26, size=16, color='C_Ink', wrap=True, auto=True, visible=vis)]
details = (pair('LWhy', 'WHY LOGIN FAILED', f'{S_}.LoginFailReason.Value') + pair('LNote', 'LOGIN NOTES', f'{S_}.LoginNotes')
           + pair('PWhy', 'WHY PRINT FAILED', f'{S_}.PrintFailReason.Value') + pair('PNote', 'PRINT NOTES / ERROR MESSAGE', f'{S_}.PrintNotes')
           + pair('Miss', 'MISSING FROM THE KIT', f'{S_}.MissingItems') + pair('Extra', 'EXTRA IN THE KIT', f'{S_}.ExtraItems')
           + pair('Spoke', 'SPOKE TO', f'{S_}.SpokeTo') + pair('Edu', 'EDUCATION GIVEN', f'Concat({S_}.EducationGiven, Value, ", ")')
           + pair('Iss', 'ISSUES RAISED BY STAFF', f'{S_}.IssuesRaised') + pair('Note', 'AUDITOR NOTES', f'{S_}.Notes'))
noDetail = dlbl('lblDetNone_Dsh', '"No comments recorded on this audit"', 30, size=15, color='C_Muted',
                visible=f'IsBlank(Trim({S_}.LoginNotes & {S_}.PrintNotes & {S_}.MissingItems & {S_}.ExtraItems & {S_}.SpokeTo & {S_}.IssuesRaised & {S_}.Notes & {S_}.LoginFailReason.Value & {S_}.PrintFailReason.Value)) && CountRows({S_}.EducationGiven) = 0')
photo = inflow('conDetPhoto_Dsh', f'If(IsBlank({S_}.AuditPhoto), {r(50)}, {r(420)})', w=IW2, fill='C_Bg', radius=r(14), children=[
    N('imgDetPhoto_Dsh', 'Image@2.2.3', props={'Height': f'Parent.Height - {r(16)}', 'Image': f'{S_}.AuditPhoto', 'ImagePosition': 'ImagePosition.Fit', 'Visible': f'!IsBlank({S_}.AuditPhoto)', 'Width': f'Parent.Width - {r(16)}', 'X': r(8), 'Y': r(8)}),
    lbl('lblDetNoPhoto_Dsh', '"No photo taken"', x=r(16), w=f'Parent.Width - {r(32)}', h=r(50), size=15, color='C_Muted', visible=f'IsBlank({S_}.AuditPhoto)', extra={'VerticalAlign': 'VerticalAlign.Middle'})])
HH = 52
selH = f'ThisItem.ID = {S_}.ID'
hrow = box('conHistRow_Dsh', x='0', y='0', w='Parent.TemplateWidth', h='Parent.TemplateHeight', children=[
    box('conHistSel_Dsh', x='0', y=r(3), w='Parent.Width', h=r(HH - 6), fill=f'If({selH}, C_AccentSoft, C_White)', border=f'If({selH}, C_Accent, C_Line)', radius=r(12)),
    lbl('lblHistW_Dsh', 'Text(ThisItem.Created, "ddd d mmm yyyy, h:mm AM/PM") & If(IsBlank(ThisItem.ReAudit), "", "  ·  Re-audit")', x=r(14), y='0', w=f'Parent.Width * 0.45', h=r(HH), size=14, color='C_Ink', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    lbl('lblHistB_Dsh', "ThisItem.'Created By'.DisplayName", x='Parent.Width * 0.45', y='0', w=f'Parent.Width * 0.3', h=r(HH), size=14, color='C_Ink2', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    lbl('lblHistR_Dsh', f'If(ThisItem.DTVFound.Value = "No" || ThisItem.LoginWorked.Value = "No" || ThisItem.PatientListWorked.Value = "No" || ThisItem.PrintWorked.Value = "No" || ThisItem.FolderFound.Value = "No" || ThisItem.ContentsListInFolder.Value = "No" || ThisItem.KitMatched.Value = "No", "Needs follow-up", "All clear")',
        x='Parent.Width * 0.75', y='0', w=f'Parent.Width * 0.25 - {r(14)}', h=r(HH), size=14, bold=True, align='Align.Right',
        color=f'If(ThisItem.DTVFound.Value = "No" || ThisItem.LoginWorked.Value = "No" || ThisItem.PatientListWorked.Value = "No" || ThisItem.PrintWorked.Value = "No" || ThisItem.FolderFound.Value = "No" || ThisItem.ContentsListInFolder.Value = "No" || ThisItem.KitMatched.Value = "No", {RED}, {GREEN})', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnHist_Dsh', f'Set({S_}, ThisItem)')])
HIST = f'Filter(colDashSrc, Title = {S_}.Title)'
hist = N('galDetHist_Dsh', 'Gallery@2.15.0', 'Vertical', {'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'Height': f'Max(1, CountRows({HIST})) * {r(HH)}',
         'Items': HIST, 'LayoutMinHeight': f'Max(1, CountRows({HIST})) * {r(HH)}', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(HH), 'Width': IW2}, [hrow])
META = [('When', 'AUDITED', f'Text({S_}.Created, "ddd d mmm yyyy, h:mm AM/PM")'), ('By', 'AUDITOR', f"{S_}.'Created By'.DisplayName"),
        ('Type', 'TYPE', f'If(IsBlank({S_}.ReAudit), "First audit", "Re-audit")'), ('Acc', 'LOGIN ACCOUNT', f'Coalesce({REG}.LoginAccount, "—")')]
mw = f'({IW2}) / 4'
meta = inflow('conDetMeta_Dsh', r(70), w=IW2, fill='C_Bg', radius=r(14), children=sum([[
    lbl(f'lblM{k}C_Dsh', f'"{c}"', x=f'{i} * {mw} + {r(16)}', y=r(12), w=f'{mw} - {r(24)}', h=r(20), size=13, color='C_Muted', bold=True),
    lbl(f'lblM{k}V_Dsh', v, x=f'{i} * {mw} + {r(16)}', y=r(34), w=f'{mw} - {r(24)}', h=r(26), size=15, color='C_Ink', bold=True)] for i, (k, c, v) in enumerate(META)], []))
endD = inflow('conDetEnd_Dsh', r(16), w=IW2, extra={'DropShadow': 'DropShadow.None'})
detP = {'AlignInContainer': 'AlignInContainer.SetByContainer', 'DropShadow': 'DropShadow.None', 'Height': f'Parent.Height - {r(108)}', 'LayoutAlignItems': 'LayoutAlignItems.Start',
        'LayoutDirection': 'LayoutDirection.Vertical', 'LayoutGap': r(8), 'LayoutOverflowY': 'LayoutOverflow.Scroll', 'PaddingBottom': r(8), 'PaddingLeft': r(32), 'PaddingRight': r(32),
        'PaddingTop': r(6), 'Width': 'Parent.Width', 'X': '0', 'Y': r(100)}
detP.update(rad('0'))
detBody = N('conDetBody_Dsh', 'GroupContainer@1.5.0', 'AutoLayout', detP,
            [meta, dcap('capDetChk_Dsh', 'ANSWERS'), checks, dcap('capDetCom_Dsh', 'COMMENTS AND DETAILS')] + details + [noDetail,
             dcap('capDetPhoto_Dsh', 'PHOTO'), photo, dcap('capDetHist_Dsh', 'EVERY AUDIT OF THIS DTV  ·  TAP ONE TO VIEW IT'), hist, endD])
isFail = f'({FAILS_SEL})'
card = box('conDetCard_Dsh', x=f'(App.Width - {DETW}) / 2', y=r(24), w=DETW, h=f'App.Height - {r(48)}', fill='C_White', radius=r(22), extra={'DropShadow': 'DropShadow.Bold'}, children=[
    box('conDetStripe_Dsh', w=r(10), h=r(100), fill=f'If({isFail}, {RED}, {GREEN})', extra={'RadiusTopLeft': r(22), 'RadiusBottomLeft': '0', 'RadiusTopRight': '0', 'RadiusBottomRight': '0'}),
    lbl('lblDetT_Dsh', f'Coalesce({REG}.Department, {S_}.DisplayName, {S_}.Title)', x=r(32), y=r(16), w=f'Parent.Width - {r(300)}', h=r(36), size=22, color='C_Ink', bold=True),
    lbl('lblDetS_Dsh', f'Coalesce({REG}.DTVLocation, "") & "  ·  " & {S_}.Title & "  ·  " & {S_}.Stream & "  ·  " & {REG}.Building & " " & {REG}.Floor', x=r(32), y=r(54), w=f'Parent.Width - {r(300)}', h=r(26), size=15, color='C_Ink2'),
    box('conDetRes_Dsh', x=f'Parent.Width - {r(260)}', y=r(28), w=r(170), h=r(40), fill=f'If({isFail}, RGBA(176, 52, 40, 0.12), RGBA(30, 122, 80, 0.12))', radius=r(20), children=[
        lbl('lblDetRes_Dsh', f'If({isFail}, "Needs Follow-up", "All Clear")', w='Parent.Width', h=r(40), size=15, color=f'If({isFail}, {RED}, {GREEN})', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})]),
    N('btnDetClose_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_Ink2', 'FontWeight': '""', 'Height': r(56), 'Icon': '"DismissCircle"', 'OnSelect': 'Set(varDashShowDet, false)', 'Size': r(24), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': r(56), 'X': f'Parent.Width - {r(72)}', 'Y': r(20)}, **SBOX)),
    box('conDetLine_Dsh', x='0', y=r(99), w='Parent.Width', h='1', fill='C_Line'),
    detBody])
overlay = box('conDetail_Dsh', x='0', y='0', w='App.Width', h='App.Height', fill='RGBA(14, 28, 42, 0.45)', visible='varDashShowDet', children=[
    tbtn('btnDetVeil_Dsh', 'Set(varDashShowDet, false)'), card])

kids = [vroot('conRoot_Dsh', [hdr, body]), overlay, hidden('btnLoad_Dsh', LOAD), hidden('btnCalc_Dsh', CALC), hidden('btnSend_Dsh', SEND)]
open(OUT + 'DTV_Dashboard.pa.yaml', 'w').write(screen('Dashboard', {'Fill': 'C_Bg', 'OnVisible': ONV}, kids))
print('built Dashboard')
