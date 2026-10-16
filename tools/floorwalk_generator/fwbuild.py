# Floorwalking Ideas app (RBWH post go-live optimisation): builds every screen + App Formulas.
#   cd tools/floorwalk_generator && python3 fwbuild.py   -> powerapps/floorwalk/*
# Phone + desktop: forms use UI/PageW/Gutter (column stops at 720 wide), the dashboard uses DashW/DashWide.
# Data: SharePoint list Floorwalk_Ideas (CITTA site) + Office 365 Users (stakeholder search).
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dtv_generator'))
from dtvgen import *
from services import SERVICES

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'powerapps', 'floorwalk') + os.sep
os.makedirs(OUT, exist_ok=True)
LIST = 'Floorwalk_Ideas'
GREEN = "RGBA(30, 122, 80, 1)"; RED = "RGBA(176, 52, 40, 1)"; LINE = "RGBA(14, 42, 70, 0.22)"; TR = "RGBA(0, 0, 0, 0)"
W = f"PageW - {r(40)}"; PADX = r(18); IW = f"Parent.Width - {r(36)}"
NOSB = {k: v for k, v in SBOX.items() if not k.startswith('Radius')}
STREAMS = [("Surgical & Critical Care", "Surg & CC"), ("Women's, Cancer & Mental Health", "WCMH"), ("Internal Medicine & Emergency", "IM & ED"), ("Operational Support Services", "Ops Support"), ("Other", "Other"), ("No service", "No service")]
# first 4 = real CITTA streams (dashboard pills). "Other" = service picked but no clear stream. "No service" = no service picked (stream left blank in the list).
THEMES = ["Workflow/Business Rules", "Functionality", "Downtime", "Resource Development", "Other"]
STATUSES = ["New", "Under Review", "Actioned", "Not Progressing"]
PRIS = ["Low", "Medium", "High"]
# ieMR areas = the CITTA "Apps and Functions Portfolios" (+ Other)
MODULES = ["ESM", "OERR", "Medicines", "Maternity", "FirstNet", "SAA / SurgiNet", "Powertrials", "Radiology", "Nursing Workflows", "Medical Workflows", "Pathology", "AH Workflows", "Community", "Devices", "Other / Not Sure"]
PRI_COL = f'Switch({{p}}, "High", {RED}, "Medium", C_Amber, C_Teal)'
STAT_COL = f'Switch({{s}}, "New", C_Accent, "Under Review", C_Amber, "Actioned", {GREEN}, C_Muted)'
STAT_SOFT = 'Switch({s}, "New", RGBA(26, 90, 153, 0.12), "Under Review", RGBA(178, 105, 0, 0.12), "Actioned", RGBA(30, 122, 80, 0.12), RGBA(140, 155, 174, 0.18))'
def pcol(e): return PRI_COL.replace('{p}', e)
def scol(e): return STAT_COL.replace('{s}', e)
def ssoft(e): return STAT_SOFT.replace('{s}', e)

def pillbtn(name, text, onsel, color, size=15, radius=24, display=None):
    p = dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': color, 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'OnSelect': onsel, 'Size': r(F(size)), 'Text': text, 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(radius)), **NOSB)
    if display: p['DisplayMode'] = display
    return N(name, 'ModernButton@1.0.0', props=p)
def tin(name, hint, x, y, w, h, multi=False, default='""', vis=None, size=15):
    p = {'BorderColor': LINE, 'BorderThickness': '1', 'Color': 'C_Ink', 'Default': default, 'FocusedBorderColor': 'C_Accent', 'FocusedBorderThickness': '2', 'Font': 'AppFont', 'Height': h, 'HintText': f'"{hint}"', 'Size': r(F(size)), 'Width': w, 'X': x, 'Y': y}
    if multi: p['Mode'] = 'TextMode.MultiLine'
    p.update(rad(r(12)))
    if vis: p['Visible'] = vis
    return N(name, 'Classic/TextInput@2.3.2', props=p)
def search_input(name, hint, size=16):
    return N(name, 'Classic/TextInput@2.3.2', props={'BorderStyle': 'BorderStyle.None', 'Color': 'C_Ink', 'Default': '""', 'DelayOutput': 'true', 'Fill': TR, 'Font': 'AppFont', 'Height': 'Parent.Height', 'HintText': f'"{hint}"', 'Size': r(F(size)), 'Width': f'Parent.Width - {r(54)}', 'X': r(46)})
def card(name, h, children, vis=None):
    return inflow(name, f'Round(({h}) * UI, 0)', fill='C_White', border='C_Line', radius=r(20), children=children, visible=vis)
def cap(name, text, y=r(14), x=PADX, w=IW):
    return lbl(name, f'"{text}"', x=x, y=y, w=w, h=r(22), size=14, color='C_Muted', bold=True)
def ques(name, text, y=r(38)):
    return lbl(name, f'"{text}"', x=PADX, y=y, w=IW, h=r(28), size=16, color='C_Ink', bold=True)
def sublbl(name, text, y, vis=None):
    return lbl(name, f'"{text}"', x=PADX, y=y, w=IW, h=r(24), size=15, color='C_Ink2', bold=True, visible=vis)
def choice(name, var, val, x, y, w, h=44, vis=None, label=None, size=14):
    sel = f'{var} = "{val}"'
    return box(f'con{name}', x=x, y=y, w=w, h=r(h), fill=f'If({sel}, C_AccentSoft, C_White)', border=f'If({sel}, C_Accent, C_Line)', radius=r(h // 2), visible=vis, children=[
        pillbtn(f'btn{name}', label or f'"{val}"', f'Set({var}, "{val}")', f'If({sel}, C_Accent, C_Ink2)', size=size, radius=h // 2)])
def colorpill(name, var, val, x, y, w, col, h=48, onsel=None, size=15):
    sel = f'{var} = "{val}"'
    return box(f'con{name}', x=x, y=y, w=w, h=r(h), fill=f'If({sel}, {col}, C_White)', border=f'If({sel}, {col}, C_Line)', radius=r(h // 2), children=[
        pillbtn(f'btn{name}', f'"{val}"', onsel or f'Set({var}, "{val}")', f'If({sel}, C_White, C_Ink2)', size=size, radius=h // 2)])
def hidden(name, onselect):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'FontWeight': '""', 'Height': '1', 'OnSelect': onselect, 'Size': r(11), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Visible': 'false', 'Width': '1'}, **SBOX))
def iconbtn(name, icon, onsel, x, y, size=56, color='C_Ink2', isize=24):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': color, 'FontWeight': '""', 'Height': r(size), 'Icon': f'"{icon}"', 'OnSelect': onsel, 'Size': r(isize), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': r(size), 'X': x, 'Y': y}, **SBOX))
def wrap(g, rowname):
    """gallery rows: everything inside ONE container (controls placed straight in a template land at X = 0 in Studio)"""
    for k in g.children:
        for pk, pv in list(k.props.items()):
            k.props[pk] = str(pv).replace('Parent.TemplateWidth', 'Parent.Width').replace('Parent.TemplateHeight', 'Parent.Height')
    g.children = [box(rowname, x='0', y='0', w='Parent.TemplateWidth', h='Parent.TemplateHeight', children=g.children)]
    return g

# a pop-up: bottom sheet on phones, centred dialog from 720 wide. Children are placed inside the sheet.
SHW = 'Min(App.Width, SheetW)'
def sheet(sfx, key, visvar, title, children, h=640):
    SH = f'Min(App.Height - {r(50)}, {r(h)})'
    sh = box(f'conSheet{key}_{sfx}', x=f'(App.Width - {SHW}) / 2', y=f'If(App.Width >= 720, (App.Height - {SH}) / 2, App.Height - {SH})', w=SHW, h=SH, fill='C_White', radius=r(24), children=[
        box(f'conHandle{key}_{sfx}', x=f'(Parent.Width - {r(44)}) / 2', y=r(8), w=r(44), h=r(5), fill='C_Line', radius=r(3)),
        lbl(f'lblSheet{key}_{sfx}', f'"{title}"', x=r(20), y=r(20), w=f'Parent.Width - {r(90)}', h=r(34), size=22, color='C_Ink', bold=True),
        iconbtn(f'btnClose{key}_{sfx}', 'DismissCircle', f'Set({visvar}, false)', f'Parent.Width - {r(66)}', r(10)),
    ] + children)
    return box(f'conOverlay{key}_{sfx}', x='0', y='0', w='App.Width', h='App.Height', fill='RGBA(14, 28, 42, 0.45)', visible=visvar, children=[
        tbtn(f'btnVeil{key}_{sfx}', f'Set({visvar}, false)'), sh])

# ================================================================== APP FORMULAS
svc_rows = ',\n    '.join('{ Service: "%s", Line: "%s", Stream: "%s" }' % (s.replace('"', "'"), l, st) for l, s, st in SERVICES)
FORMULAS = f'''// =====================================================================
// Floorwalking Ideas app > App > Formulas  (paste the whole file)
// Same colours, font, header art and sizing as every other STARS app.
// Generated by tools/floorwalk_generator/fwbuild.py: change it there, not here.
// =====================================================================
// ---- colours
C_Ink = RGBA(14, 28, 42, 1);
C_Ink2 = RGBA(58, 80, 104, 1);
C_Muted = RGBA(140, 155, 174, 1);
C_Bg = RGBA(235, 242, 248, 1);
C_Bg2 = RGBA(244, 249, 252, 1);
C_Line = RGBA(14, 42, 70, 0.12);
C_White = RGBA(255, 255, 255, 1);
C_Accent = RGBA(26, 90, 153, 1);
C_AccentDark = RGBA(18, 64, 112, 1);
C_AccentSoft = RGBA(26, 90, 153, 0.10);
C_Good = RGBA(12, 122, 82, 1);
C_GoodBg = RGBA(232, 246, 240, 1);
C_Danger = RGBA(180, 26, 26, 1);
C_DangerBg = RGBA(254, 242, 242, 1);
C_Amber = RGBA(178, 105, 0, 1);
C_AmberBg = RGBA(255, 246, 229, 1);
C_Teal = RGBA(0, 144, 153, 1);

// ---- font and header art
AppFont = Font.'Segoe UI';
HeaderImage = "data:image/svg+xml;utf8," & EncodeUrl("<svg xmlns='http://www.w3.org/2000/svg' width='400' height='80' viewBox='0 0 400 80' preserveAspectRatio='none'><defs><linearGradient id='a' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#001D46'/><stop offset='0.48' stop-color='#075F73'/><stop offset='1' stop-color='#00838A'/></linearGradient></defs><rect width='400' height='80' fill='url(#a)'/></svg>");

// ---- screen size (phone, tablet and desktop browser)
// UI scales every text size, button, row and gap (0.9 to 1.25).
UI = Max(0.9, Min(1.25, Min(App.Width, App.Height * 0.55) / 390));
// Capture + Home: one column, stops growing at 720 wide (centred on desktop)
PageW = Min(App.Width, 720);
Gutter = (App.Width - PageW) / 2;
SheetW = Min(App.Width, 600);
// Dashboard: content up to 1400 wide; panels side by side from 1000 wide, one column on phones
DashW = Min(App.Width - Round(48 * UI, 0), 1400);
DashX = (App.Width - DashW) / 2;
DashWide = App.Width >= 1000;
DashGap = Round(16 * UI, 0);

// ---- who is using the app (the floorwalker). SharePoint also records Created By on every idea.
MeEmail = Lower(User().Email);
MeName = User().FullName;
MeFirst = With({{ n: User().FullName }}, If("," in n, Trim(Last(Split(n, ",")).Value), First(Split(n, " ")).Value));

// ---- patient safety alerts: who gets the email when a floorwalker ticks "Could this harm a patient? Yes".
// Put the CITTA safety lead's address (or a shared mailbox) between the quotes. Several: separate with ";". Empty = no email.
SafetyAlertTo = "";

// ---- email look (same as every other STARS email)
EmailHead =
    "<html><body style='margin:0;padding:0;background-color:#EBF2F8;'>" &
    "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0' bgcolor='#EBF2F8' style='background-color:#EBF2F8;'><tr><td align='center' style='padding:24px 12px;'>" &
    "<table role='presentation' width='680' cellpadding='0' cellspacing='0' border='0' bgcolor='#FFFFFF' style='width:680px;max-width:100%;background-color:#FFFFFF;border:1px solid #D6E0EA;border-radius:18px;border-collapse:separate;border-spacing:0;overflow:hidden;font-family:Segoe UI,Arial,sans-serif;color:#0E1C2A;'>" &
    "<tr><td style='padding:0;font-size:0;line-height:0;border-radius:18px 18px 0 0;overflow:hidden;'>" &
    "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0' style='width:100%;border-collapse:collapse;'><tr>" &
    Concat(
        ["#001F47","#01234A","#01284D","#022C50","#023053","#033556","#033959","#033D5C","#04425F","#044662","#054A65","#054E68","#06536B","#06576E","#075B70","#075F73","#076175","#066476","#066677","#056879","#056A7A","#046C7B","#046E7D","#04717E","#037380","#037581","#027782","#027984","#017B85","#017E87","#018088","#008289"],
        "<td width='3.125%' height='14' bgcolor='" & Value & "' style='background-color:" & Value & ";height:14px;font-size:0;line-height:0;'>&nbsp;</td>"
    ) &
    "</tr></table></td></tr>" &
    "<tr><td bgcolor='#075F73' style='background-color:#075F73;padding:24px 32px 26px 32px;'>" &
    "<div style='font-size:11px;letter-spacing:2px;font-weight:600;color:#BFE3E8;'>RBWH POST GO-LIVE  ·  CITTA</div>" &
    "<div style='font-size:26px;font-weight:700;color:#FFFFFF;padding-top:6px;'>{{{{TITLE}}}}</div>" &
    "<div style='font-size:14px;color:#DCEFF2;padding-top:4px;'>{{{{SUB}}}}</div>" &
    "</td></tr>";

EmailFoot =
    "<tr><td bgcolor='#F4F9FC' style='background-color:#F4F9FC;padding:16px 32px;border-top:1px solid #E3EAF1;border-radius:0 0 18px 18px;font-size:12px;line-height:18px;color:#8C9BAE;'>" &
    "Sent from the Floorwalking Ideas app by " & User().FullName & ".<br>{{{{NOTE}}}}" &
    "</td></tr></table></td></tr></table></body></html>";

// ---- choices (the app writes these exact words into the list)
StreamList = Table(
    {', '.join('{ Key: "%s", Short: "%s" }' % s for s in STREAMS)}
);
ThemeList = [{', '.join(f'"{t}"' for t in THEMES)}];
StatusList = [{', '.join(f'"{t}"' for t in STATUSES)}];

// ---- RBWH services (service + sub-service) and the CITTA stream each belongs to.
// From the "Service Allocations" sheet (RBWH Stakeholder Directory & Allocations, Oct 2026).
// The stream is set behind the scenes from the service (floorwalkers don't see it). No service = stream left blank.
// To add a service: add a row in tools/floorwalk_generator/services.py and re-run (Stream must match StreamList).
ServiceMap = Table(
    {svc_rows}
);
'''
open(OUT + 'App_Formulas.txt', 'w').write(FORMULAS)

# ================================================================== HOME
hdrH = inflow('conHdr_Hm', r(165), w='App.Width', fill=HDR_FILL, radius='0', children=[
    N('imgHdr_Hm', 'Image@2.2.3', props={'Height': 'Parent.Height', 'Image': 'HeaderImage', 'ImagePosition': 'ImagePosition.Fill', 'Width': 'Parent.Width'}),
    lbl('lblKicker_Hm', '"RBWH POST GO-LIVE"', x=f"Gutter + {r(25)}", y=r(33), w=f"PageW - {r(50)}", h=r(23), size=14, color='RGBA(255, 255, 255, 0.8)', bold=True),
    lbl('lblTitle_Hm', '"Floorwalking Ideas"', x=f"Gutter + {r(25)}", y=r(45), w=f"PageW - {r(50)}", h=r(70), size=36, color='C_White', bold=True),
    lbl('lblHello_Hm', '"Hi " & MeFirst & "  ·  " & Text(Today(), "dddd d mmmm")', x=f"Gutter + {r(25)}", y=r(110), w=f"PageW - {r(50)}", h=r(28), size=16, color='RGBA(255, 255, 255, 0.9)'),
])
heroH = inflow('conHero_Hm', r(120), fill='C_Accent', radius=r(25), children=[
    box('conHeroIc_Hm', x=r(20), y=r(32), w=r(56), h=r(56), fill='RGBA(255, 255, 255, 0.16)', radius=r(28), children=[ico('icoHero_Hm', 'Edit', r(11), r(11), 34, 'C_White', True)]),
    lbl('lblHeroT_Hm', '"Capture an Idea"', x=r(92), y=r(32), w=f"Parent.Width - {r(108)}", h=r(32), size=24, color='C_White', bold=True),
    lbl('lblHeroS_Hm', '"Takes under a minute"', x=r(92), y=r(66), w=f"Parent.Width - {r(108)}", h=r(22), size=15, color='RGBA(255, 255, 255, 0.85)'),
    tbtn('btnHero_Hm', 'Navigate(Capture, ScreenTransition.Cover)'),
])
capH = lbl('capOther_Hm', '"SEE WHAT IS COMING IN"', w=W, h=r(23), size=14, color='C_Muted', bold=True, extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(23)})
def tileH(k, icon, title, subtitle, onsel, amber=False):
    return inflow(f'conTile{k}_Hm', r(90), fill='C_White', border='C_Line', radius=r(20), children=[
        box(f'conTileIc{k}_Hm', x=r(18), y=r(18), w=r(55), h=r(55), fill='C_AmberBg' if amber else 'C_AccentSoft', radius=r(28), children=[ico(f'icoTile{k}_Hm', icon, r(13), r(13), 30, 'C_Amber' if amber else 'C_Accent', True)]),
        lbl(f'lblTileT{k}_Hm', f'"{title}"', x=r(88), y=r(18), w=f"Parent.Width - {r(130)}", h=r(26), size=19, color='C_Ink', bold=True),
        lbl(f'lblTileS{k}_Hm', subtitle, x=r(88), y=r(46), w=f"Parent.Width - {r(130)}", h=r(22), size=15, color='C_Muted'),
        ico(f'icoTileGo{k}_Hm', 'ChevronRight', f"Parent.Width - {r(38)}", r(33), 24, 'C_Muted'),
        tbtn(f'btnTile{k}_Hm', onsel)])
t1 = tileH('Dash', 'AppsList', 'Ideas Dashboard', '"Overview and every idea"', 'Set(varDashMine, false);\nNavigate(Dashboard, ScreenTransition.Cover)')
t2 = tileH('Mine', 'Person', 'My Ideas', 'varHmMineAllN & If(varHmMineAllN = 1, " idea", " ideas") & " captured by you"', 'Set(varDashMine, true);\nNavigate(Dashboard, ScreenTransition.Cover)', amber=True)
endH = inflow('conEnd_Hm', r(16), extra={'DropShadow': 'DropShadow.None'})

# ================================================================== CAPTURE
S = 'Cap'
# ---- 1 · where: service (search sheet), BAU stream (auto from service), location
hasSvc = '!IsBlank(varSvc.Service)'
svcField = box('conSvcField_Cap', x=PADX, y=r(66), w=IW, h=r(52), fill='C_White', border=LINE, radius=r(14), children=[
    ico('icoSvc_Cap', 'Search', r(14), r(14), 24, 'C_Muted'),
    lbl('lblSvc_Cap', f'If({hasSvc}, varSvc.Service, "Search services")', x=r(48), w=f'Parent.Width - {r(100)}', h=r(52), size=16, color=f'If({hasSvc}, C_Ink, C_Muted)', bold=hasSvc != '', extra={'VerticalAlign': 'VerticalAlign.Middle', 'FontWeight': f'If({hasSvc}, FontWeight.Bold, FontWeight.Normal)'}),
    ico('icoSvcGo_Cap', 'ChevronRight', f'Parent.Width - {r(38)}', r(14), 24, 'C_Muted'),
    tbtn('btnSvc_Cap', 'Reset(txtSvcSearch_Cap);\nSet(varShowSvc, true)'),
    N('btnSvcClear_Cap', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_Muted', 'FontWeight': '""', 'Height': r(50), 'Icon': '"DismissCircle"', 'OnSelect': 'Set(varSvc, Blank())', 'Size': r(22), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Visible': hasSvc, 'Width': r(50), 'X': f'Parent.Width - {r(51)}', 'Y': '0'}, **SBOX)),
])
where = card('conWhere_Cap', '226', [
    cap('cap_Where', '1  ·  WHERE'),
    sublbl('lblSvcQ_Cap', 'Service (optional)', r(40)),
    svcField,
    sublbl('lblLocQ_Cap', 'Location', r(130)),
    tin('txtLoc_Cap', 'Ward, unit or area (e.g. 7B North)', PADX, r(156), IW, r(52)),
])

# ---- 2 · stakeholder: Office 365 directory search, or type a name
DIR = 'varStakeMode = "Dir"'; MAN = 'varStakeMode = "Manual"'; NONE = 'IsBlank(varStakeMode)'
HASSTAKE = f'(({DIR} && !IsBlank(varStake.Name)) || ({MAN} && !IsBlank(Trim(txtStakeName_Cap.Text))))'
hw = f"Round((Parent.Width - {r(36)} - {r(12)}) / 2, 0)"
def ynp(val, col, x):
    sel = f'varFollow = "{val}"'
    return box(f'conFol{val}_Cap', x=x, y=r(198), w=hw, h=r(48), fill=f'If({sel}, {col}, C_White)', border=f'If({sel}, {col}, C_Line)', radius=r(24), visible=f'!{NONE}', children=[
        pillbtn(f'btnFol{val}_Cap', f'"{val}"', f'Set(varFollow, "{val}")', f'If({sel}, C_White, C_Muted)')])
stakeField = box('conStakeField_Cap', x=PADX, y=r(74), w=IW, h=r(52), fill='C_White', border=LINE, radius=r(14), visible=NONE, children=[
    ico('icoStake_Cap', 'People', r(14), r(14), 24, 'C_Muted'),
    lbl('lblStakeHint_Cap', '"Search the staff directory"', x=r(48), w=f'Parent.Width - {r(100)}', h=r(52), size=16, color='C_Muted', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    ico('icoStakeGo_Cap', 'ChevronRight', f'Parent.Width - {r(38)}', r(14), 24, 'C_Muted'),
    tbtn('btnStake_Cap', 'Reset(txtStakeSearch_Cap);\nSet(varShowStake, true)')])
typeName = box('conTypeName_Cap', x=PADX, y=r(136), w=IW, h=r(44), fill='C_White', border='C_Accent', radius=r(22), visible=NONE, children=[
    pillbtn('btnTypeName_Cap', '"Not in the Directory? Type a Name"', 'Set(varStakeDefault, "");\nSet(varStakeMode, "Manual");\nReset(txtStakeName_Cap)', 'C_Accent', size=14, radius=22)])
person = box('conPerson_Cap', x=PADX, y=r(74), w=IW, h=r(84), fill='C_AccentSoft', border='C_Accent', radius=r(16), visible=DIR, children=[
    lbl('lblPerName_Cap', 'varStake.Name', x=r(16), y=r(8), w=f'Parent.Width - {r(76)}', h=r(26), size=17, color='C_Ink', bold=True),
    lbl('lblPerJob_Cap', 'Coalesce(varStake.Job, "No job title listed") & If(IsBlank(varStake.Dept), "", "  ·  " & varStake.Dept)', x=r(16), y=r(34), w=f'Parent.Width - {r(76)}', h=r(22), size=14, color='C_Ink2'),
    lbl('lblPerMail_Cap', 'varStake.Email', x=r(16), y=r(56), w=f'Parent.Width - {r(76)}', h=r(20), size=13, color='C_Muted'),
    iconbtn('btnPerClear_Cap', 'DismissCircle', 'Set(varStake, Blank());\nSet(varStakeMode, Blank());\nSet(varFollow, Blank())', f'Parent.Width - {r(58)}', r(14), size=56, color='C_Ink2')])
manName = tin('txtStakeName_Cap', 'Name and role (e.g. Jo Smith, NUM 7B)', PADX, r(74), IW, r(52), default='varStakeDefault', vis=MAN)
backDir = box('conBackDir_Cap', x=PADX, y=r(132), w=IW, h=r(30), visible=MAN, children=[
    lbl('lblBackDir_Cap', '"Search the directory instead"', w='Parent.Width', h=r(30), size=14, color='C_Accent', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnBackDir_Cap', 'Set(varStakeMode, Blank());\nSet(varFollow, Blank());\nReset(txtStakeSearch_Cap);\nSet(varShowStake, true)')])
stake = card('conStake_Cap', f'If({DIR}, 264, {MAN}, If(varFollow = "Yes", 292, 264), 198)', [
    cap('cap_Stake', '8  ·  STAKEHOLDER (OPTIONAL)'),
    ques('q_Stake', 'Who raised it?'),
    stakeField, typeName, person, manName, backDir,
    sublbl('lblFolQ_Cap', 'Do they want follow-up?', r(170), vis=f'!{NONE}'),
    ynp('Yes', GREEN, PADX), ynp('No', RED, f'{PADX} + {hw} + {r(12)}'),
    lbl('lblFolWarn_Cap', '"No email for them. Put contact details in the idea."', x=PADX, y=r(254), w=IW, h=r(20), size=13, color='C_Amber', bold=True, visible=f'{MAN} && varFollow = "Yes"'),
])

# ---- 2 · the idea: one-line summary (saved in Title) — drives the duplicate check
idea = card('conIdea_Cap', '170', [
    cap('cap_Idea', '2  ·  THE IDEA'), ques('q_Idea', 'Sum it up in one line'),
    N('txtSummary_Cap', 'Classic/TextInput@2.3.2', props=dict({'BorderColor': LINE, 'BorderThickness': '1', 'Color': 'C_Ink', 'Default': '""', 'DelayOutput': 'true', 'FocusedBorderColor': 'C_Accent', 'FocusedBorderThickness': '2', 'Font': 'AppFont', 'Height': r(52), 'HintText': '"e.g. Can\'t find the fluid balance chart"', 'MaxLength': '120', 'Size': r(F(15)), 'Width': IW, 'X': PADX, 'Y': r(74)}, **rad(r(12)))),
    lbl('lblSumHint_Cap', '"We check for similar ideas as you type."', x=PADX, y=r(132), w=IW, h=r(20), size=13, color='C_Muted')])

# ---- similar ideas already logged: "Me Too" adds a vote instead of a duplicate
STOP = '["with", "when", "that", "this", "from", "have", "they", "there", "their", "them", "then", "than", "into", "would", "should", "could", "need", "needs", "about", "after", "before", "where", "what", "which", "patient", "patients", "staff", "ward", "wards", "ieMR", "iemr", "using", "being", "does", "doesn\'t", "can\'t", "cant", "dont", "don\'t"]'
SIM = f'''With(
    {{
        w: Filter(
            Split(Lower(Trim(txtSummary_Cap.Text)), " "),
            Len(Value) >= 4 && !(Value in {STOP})
        )
    }},
    If(
        CountRows(w) = 0,
        FirstN(colIdeas_Cap, 0),
        FirstN(
            SortByColumns(
                Filter(
                    AddColumns(colIdeas_Cap, Score, CountRows(Filter(w, Value in Hay))),
                    Score >= Min(2, CountRows(w))
                ),
                "Score",
                SortOrder.Descending,
                "Votes",
                SortOrder.Descending
            ),
            3
        )
    )
)'''
SR = 84
voted = '((";" & MeEmail & ";") in ThisItem.Voters || ThisItem.Creator = MeEmail)'
galSim = wrap(N('galSim_Cap', 'Gallery@2.15.0', 'Vertical', {'Height': f'Max(1, CountRows(Self.AllItems)) * {r(SR)}', 'Items': SIM, 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(SR), 'Width': IW, 'X': PADX, 'Y': r(70)}, [
    box('conSimRow_Cap', x='0', y=r(4), w='Parent.TemplateWidth', h=r(SR - 8), fill='C_White', border='C_Line', radius=r(14), children=[
        lbl('lblSimT_Cap', 'ThisItem.Summary', x=r(14), y=r(10), w=f'Parent.Width - {r(140)}', h=r(24), size=15, color='C_Ink', bold=True),
        lbl('lblSimS_Cap', 'If(IsBlank(ThisItem.Service), "No service", ThisItem.Service) & "  ·  " & ThisItem.Status & If(ThisItem.Votes > 0, "  ·  +" & ThisItem.Votes, "")', x=r(14), y=r(38), w=f'Parent.Width - {r(140)}', h=r(22), size=13, color='C_Muted'),
        box('conSimVote_Cap', x=f'Parent.Width - {r(120)}', y=r(16), w=r(108), h=r(44), fill=f'If({voted}, C_GoodBg, C_Accent)', radius=r(22), children=[
            pillbtn('btnSimVote_Cap', f'If({voted}, "✓ Added", "Me Too")', 'Set(varVoteID, ThisItem.ID);\nSelect(btnVote_Cap)', f'If({voted}, {GREEN}, C_White)', size=14, radius=22,
                    display=f'If({voted} || varSaving || !Connection.Connected, DisplayMode.Disabled, DisplayMode.Edit)')])])]), 'conSimWrap_Cap')
simN = 'CountRows(galSim_Cap.AllItems)'
similar = card('conSimilar_Cap', f'84 + Max(1, {simN}) * {SR}', [
    lbl('cap_Sim', '"ALREADY LOGGED?"', x=PADX, y=r(14), w=IW, h=r(22), size=14, color='C_Amber', bold=True),
    lbl('q_Sim', '"Tap Me Too instead of adding it again"', x=PADX, y=r(38), w=IW, h=r(26), size=15, color='C_Ink', bold=True),
    galSim], vis=f'{simN} > 0')
similar.props['Fill'] = 'C_AmberBg'; similar.props['BorderColor'] = 'RGBA(178, 105, 0, 0.35)'

# ---- 3 · more detail (optional)
detail = card('conDetail_Cap', '232', [
    cap('cap_Detail', '3  ·  MORE DETAIL (OPTIONAL)'), ques('q_Detail', 'What happens now? What would help?'),
    tin('txtIdea_Cap', 'Screen or form name, steps, workaround in use', PADX, r(74), IW, r(140), multi=True)])

# ---- 4 · ieMR module (from the CITTA Apps and Functions Portfolios)
mw = f"Round((Parent.Width - {r(36)} - {r(10)}) / 2, 0)"
mod_rows = (len(MODULES) + 1) // 2
module = card('conModule_Cap', f'{74 + mod_rows * 50 + 12}', [cap('cap_Mod', '4  ·  ieMR AREA (OPTIONAL)'), ques('q_Mod', 'Which part of ieMR?')]
    + [choice(f'Mod{i}_Cap', 'varModule', m, f'{PADX} + {i % 2} * ({mw} + {r(10)})', r(74 + 50 * (i // 2)), mw, size=13) for i, m in enumerate(MODULES)])
for c in module.children:
    if c.name.startswith('conMod') and c.children:
        b = c.children[0]; b.props['OnSelect'] = b.props['OnSelect'].replace('Set(varModule, ', 'Set(varModule, If(varModule = ' + b.props['Text'].lstrip('=') + ', Blank(), ') + ')'

# ---- 5 · theme
OTH = '(varTheme = "Other")'
themes = card('conTheme_Cap', f'If({OTH}, 400, 336)', [cap('cap_Theme', '5  ·  THEME'), ques('q_Theme', 'What kind of uplift is it?')]
    + [choice(f'Th{i}_Cap', 'varTheme', t, PADX, r(74 + 50 * i), IW) for i, t in enumerate(THEMES)]
    + [tin('txtThemeOther_Cap', 'What kind of theme? (short)', PADX, r(330), IW, r(52), vis=OTH)])

# ---- 6 · priority
pw = f"Round((Parent.Width - {r(36)} - 2 * {r(10)}) / 3, 0)"
pri = card('conPri_Cap', '140', [cap('cap_Pri', '6  ·  PRIORITY'), ques('q_Pri', 'How much impact would it have?')]
    + [colorpill(f'Pri{p}_Cap', 'varPri', p, f'{PADX} + {i} * ({pw} + {r(10)})', r(74), pw, pcol(f'"{p}"')) for i, p in enumerate(PRIS)])

# ---- 7 · patient safety
SAFE = '(varSafety = "Yes")'
safety = card('conSafety_Cap', f'If({SAFE}, 262, 140)', [cap('cap_Safe', '7  ·  PATIENT SAFETY'), ques('q_Safe', 'Could this harm a patient?'),
    colorpill('SafeYes_Cap', 'varSafety', 'Yes', PADX, r(74), hw, RED),
    colorpill('SafeNo_Cap', 'varSafety', 'No', f'{PADX} + {hw} + {r(12)}', r(74), hw, GREEN),
    box('conSafeNote_Cap', x=PADX, y=r(136), w=IW, h=r(108), fill='C_AmberBg', border='RGBA(178, 105, 0, 0.35)', radius=r(14), visible=SAFE, children=[
        lbl('lblSafeCap_Cap', '"REPORT IT NOW"', x=r(14), y=r(10), w=f'Parent.Width - {r(28)}', h=r(20), size=13, color='C_Amber', bold=True),
        lbl('lblSafe_Cap', '"Log a RiskMan and call the ieMR Service Desk. The CITTA safety lead is emailed when you submit."', x=r(14), y=r(32), w=f'Parent.Width - {r(28)}', h=r(66), size=14, color='C_Ink', bold=True, wrap=True)])])

# ---- 9 · photo (optional) — same pattern as the DTV audit
nophoto = 'IsBlank(addPhoto_Cap.Media)'
photo = card('conPhoto_Cap', f'If({nophoto}, 140, 262)', [
    cap('cap_Photo', '9  ·  PHOTO (OPTIONAL)'),
    ques('q_Photo', 'No patient details in the photo'),
    box('conAddPhoto_Cap', x=PADX, y=r(74), w=IW, h=r(48), fill='C_White', border='C_Accent', radius=r(24), children=[
        lbl('lblAddPhoto_Cap', f'If({nophoto}, "Add Photo", "Change Photo")', w='Parent.Width', h=r(48), size=15, color='C_Accent', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})]),
    N('imgPhoto_Cap', 'Image@2.2.3', props={'Height': r(110), 'Image': 'addPhoto_Cap.Media', 'ImagePosition': 'ImagePosition.Fit', 'Visible': f'!{nophoto}', 'Width': r(110), 'X': PADX, 'Y': r(134)}),
    lbl('lblRemovePhoto_Cap', '"Remove Photo"', x=f"{PADX} + {r(126)}", y=r(176), w=f"Parent.Width - {r(36)} - {r(126)}", h=r(26), size=15, color=RED, bold=True, visible=f'!{nophoto}'),
    tbtn('btnRemovePhoto_Cap', 'Reset(addPhoto_Cap)', x=f"{PADX} + {r(116)}", y=r(166), w=f"Parent.Width - {r(36)} - {r(116)}", h=r(46)),
    N('addPhoto_Cap', 'AddMedia@2.2.1', props={'BorderColor': TR, 'BorderStyle': 'BorderStyle.None', 'BorderThickness': '0', 'Color': TR, 'DisabledColor': TR, 'DisabledFill': TR, 'Fill': TR, 'Font': 'AppFont', 'Height': r(48), 'HoverBorderColor': TR, 'HoverColor': TR, 'HoverFill': TR, 'PressedBorderColor': TR, 'PressedColor': TR, 'PressedFill': TR, 'Size': r(F(15)), 'Width': IW, 'X': PADX, 'Y': r(74)}),
])
offline = inflow('conOffline_Cap', r(64), fill='C_AmberBg', border='RGBA(178, 105, 0, 0.35)', radius=r(16), visible='!Connection.Connected', children=[
    lbl('lblOffline_Cap', '"No signal. You can still submit: it saves on this phone and uploads later."', x=r(16), w=f'Parent.Width - {r(32)}', h=r(64), size=14, color='C_Ink', bold=True, wrap=True, extra={'VerticalAlign': 'VerticalAlign.Middle'})])
endC = inflow('conEnd_Cap', r(16), extra={'DropShadow': 'DropShadow.None'})
bodyC = vbody('conBody_Cap', [offline, where, idea, similar, detail, module, themes, pri, safety, stake, photo, endC], gap=12, top=15, bottom=0, scroll=True)

# ---- what gets saved (same fields online and in the offline queue)
FIELDS = [
    ('Title', 'Trim(txtSummary_Cap.Text)'),
    ('Idea', 'Trim(txtIdea_Cap.Text)'),
    ('Service', 'varSvc.Service'),
    ('ServiceLine', 'varSvc.Line'),
    ('Stream', 'If(IsBlank(varSvc.Service), Blank(), Coalesce(varSvc.Stream, "Other"))'),
    ('Location', 'Trim(txtLoc_Cap.Text)'),
    ('Module', 'varModule'),
    ('StakeholderName', f'If({DIR}, varStake.Name, {MAN}, Trim(txtStakeName_Cap.Text), Blank())'),
    ('StakeholderEmail', f'If({DIR}, varStake.Email, Blank())'),
    ('StakeholderJobTitle', f'If({DIR}, varStake.Job, Blank())'),
    ('StakeholderDept', f'If({DIR}, varStake.Dept, Blank())'),
    ('FollowUp', f'If({HASSTAKE} && varFollow = "Yes", "Yes", "No")'),
    ('Theme', 'varTheme'),
    ('ThemeOther', f'If({OTH}, Trim(txtThemeOther_Cap.Text), Blank())'),
    ('Priority', 'varPri'),
    ('SafetyConcern', f'If({SAFE}, "Yes", "No")'),
    ('Status', '"New"'),
    ('Votes', '0'),
]
def rec(get, ind='                ', extra=()):
    return '{\n' + ',\n'.join(f'{ind}{k}: {get(k, v)}' for k, v in list(FIELDS) + list(extra)) + '\n' + ind[:-4] + '}'
def esc(x): return f'Substitute(Substitute(Coalesce({x}, ""), "<", "&lt;"), ">", "&gt;")'
def safety_email(g):
    """g(field) -> expression. Branded email to the CITTA safety lead."""
    rows = [('Summary', g('Title')), ('Detail', g('Idea')), ('Service', g('Service')), ('Location', g('Location')), ('ieMR area', g('Module')),
            ('Stakeholder', g('StakeholderName')), ('Priority', g('Priority')), ('Floorwalker', 'MeName')]
    trs = ' &\n                '.join(f'"<tr><td style=\'padding:6px 0;color:#8C9BAE;font-size:12px;font-weight:700;width:120px;vertical-align:top;\'>{k.upper()}</td><td style=\'padding:6px 0;color:#0E1C2A;\'>" & {esc(v)} & "</td></tr>"' for k, v in rows)
    return f'''If(
    !IsBlank(SafetyAlertTo),
    IfError(
        Office365Outlook.SendEmailV2(
            SafetyAlertTo,
            "Patient safety concern: " & {g('Title')},
            Substitute(Substitute(EmailHead, "{{{{TITLE}}}}", "Patient Safety Concern"), "{{{{SUB}}}}", Coalesce({g('Service')}, "No service recorded")) &
            "<tr><td style='padding:24px 32px 8px 32px;font-size:15px;line-height:22px;color:#3A5068;'>A floorwalker flagged an idea as a possible patient safety concern. Please check a RiskMan has been logged.</td></tr>" &
            "<tr><td style='padding:8px 32px 24px 32px;'><table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0' style='font-size:14px;'>" &
                {trs} &
            "</table></td></tr>" &
            Substitute(EmailFoot, "{{{{NOTE}}}}", "Raised in the Floorwalking Ideas app."),
            {{ Importance: "High" }}
        ),
        Notify("Saved, but the safety email could not be sent. Tell the CITTA lead directly.", NotificationType.Warning)
    )
)'''
SAFETY_EMAIL_CAP = safety_email(lambda k: dict(FIELDS)[k])

# ---- sticky submit
READY = f'!IsBlank(Trim(txtSummary_Cap.Text)) && !IsBlank(varTheme) && (!{OTH} || !IsBlank(Trim(txtThemeOther_Cap.Text))) && !IsBlank(varPri)'
ok = 'btnSubmit_Cap.DisplayMode = DisplayMode.Edit'
SAVE = f'''Set(varSaving, true);
If(
    !Connection.Connected,
    // OFFLINE: keep it on this phone; Home uploads it when there is signal
    IfError(LoadData(colQueue, "fwQueue", true), false);
    Collect(
        colQueue,
        {rec(lambda k, v: v, '            ', [('QID', 'Text(GUID())'), ('Photo', f'If({nophoto}, Blank(), imgPhoto_Cap.Image)')])}
    );
    IfError(SaveData(colQueue, "fwQueue"), Notify("Kept for now. Keep the app open until you have signal.", NotificationType.Warning));
    Set(varSaving, false);
    Set(varDoneMode, "Offline");
    Set(varShowDone, true),
    // ONLINE
    With(
        {{
            rec: Patch(
                {LIST},
                Defaults({LIST}),
                {rec(lambda k, v: v, '                    ')}
            )
        }},
        If(
            IsEmpty(Errors({LIST})),
            // record is saved; the photo goes on second, so a failed photo never loses the idea
            If(
                !{nophoto},
                Patch({LIST}, rec, {{ Photo: imgPhoto_Cap.Image }});
                If(!IsEmpty(Errors({LIST}, rec)), Notify("Idea saved, but the photo could not be attached.", NotificationType.Warning))
            );
            If({SAFE}, {SAFETY_EMAIL_CAP});
            // so the duplicate check sees it straight away
            Collect(colIdeas_Cap, {{ ID: rec.ID, Summary: rec.Title, Service: Coalesce(rec.Service, ""), Status: "New", Votes: 0, Voters: "", Creator: MeEmail, Hay: Lower(rec.Title & " " & rec.Idea & " " & rec.Service & " " & rec.Module) }});
            Set(varSaving, false);
            Set(varDoneMode, "Saved");
            Set(varShowDone, true),
            Set(varSaving, false);
            Notify("Could not save. Check your connection and try again.", NotificationType.Error)
        )
    )
)'''
submit = box('conSubmit_Cap', x=f"Gutter + {r(20)}", y=r(12), w=W, h=r(60), fill=f'If({ok}, C_Accent, RGBA(160, 174, 180, 1))', radius=r(28), children=[
    lbl('lblSubmit_Cap', f'If(varSaving, "Saving...", {ok}, If(Connection.Connected, "Submit Idea", "Save on This Phone"), "Add a summary, theme and priority")', w='Parent.Width', h=r(60), size=19, color='C_White', bold=True, align='Align.Center', extra={'Size': f'If({ok} || varSaving, {r(F(19))}, {r(F(15))})', 'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnSubmit_Cap', SAVE, display=f'If({READY} && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)')])
footC = inflow('conFoot_Cap', r(84), w='App.Width', fill='C_White', border='C_Line', radius='0', children=[submit])
hdrC = header('Cap', '"Capture an Idea"', '"Floorwalker: " & MeName', 'Navigate(Home, ScreenTransition.UnCoverRight)')
# ---- service picker sheet
SVC_ITEMS = '''SortByColumns(
    Filter(
        ServiceMap,
        IsBlank(Trim(txtSvcSearch_Cap.Text))
        || Lower(Trim(txtSvcSearch_Cap.Text)) in Lower(Service & " " & Line)
    ),
    "Line",
    SortOrder.Ascending,
    "Service",
    SortOrder.Ascending
)'''
RH = 64
selSv = 'ThisItem.Service = varSvc.Service'
galSvc = wrap(N('galSvc_Cap', 'Gallery@2.15.0', 'Vertical', {'Height': f'Parent.Height - {r(160)}', 'Items': SVC_ITEMS, 'TemplatePadding': '0', 'TemplateSize': r(RH), 'Width': f'Parent.Width - {r(24)}', 'X': r(12), 'Y': r(150)}, [
    box('conSvcSel_Cap', x='0', y=r(2), w='Parent.TemplateWidth', h=r(RH - 4), fill=f'If({selSv}, C_AccentSoft, RGBA(0, 0, 0, 0))', radius=r(12)),
    lbl('lblSvcRowT_Cap', 'ThisItem.Service', x=r(12), y=r(8), w=f'Parent.TemplateWidth - {r(24)}', h=r(26), size=16, color='C_Ink', bold=True),
    lbl('lblSvcRowS_Cap', 'ThisItem.Line', x=r(12), y=r(34), w=f'Parent.TemplateWidth - {r(24)}', h=r(22), size=14, color='C_Muted'),
    box('conSvcLn_Cap', x=r(12), y=f'Parent.TemplateHeight - 1', w=f'Parent.TemplateWidth - {r(24)}', h='1', fill='C_Line'),
    tbtn('btnSvcRow_Cap', 'Set(varSvc, ThisItem);\nSet(varShowSvc, false)')]), 'conSvcRow_Cap')
svcSheet = sheet('Cap', 'Svc', 'varShowSvc', 'Pick a Service', [
    box('conSvcSearch_Cap', x=r(20), y=r(64), w=f'Parent.Width - {r(40)}', h=r(52), fill='C_White', border=LINE, radius=r(14), children=[
        ico('icoSvcSearch_Cap', 'Search', r(14), r(14), 24, 'C_Muted'), search_input('txtSvcSearch_Cap', 'Search e.g. physio, 7B, cardiology')]),
    lbl('lblSvcCount_Cap', 'CountRows(galSvc_Cap.AllItems) & If(CountRows(galSvc_Cap.AllItems) = 1, " service", " services") & "  ·  search ward, unit or profession"', x=r(20), y=r(122), w=f'Parent.Width - {r(40)}', h=r(22), size=13, color='C_Muted', bold=True),
    lbl('lblSvcNone_Cap', '"No service matches. Close this and leave Service blank."', x=r(20), y=r(200), w=f'Parent.Width - {r(40)}', h=r(50), size=15, color='C_Muted', align='Align.Center', wrap=True, visible='CountRows(galSvc_Cap.AllItems) = 0'),
    galSvc])

# ---- stakeholder picker sheet (Office 365 Users). Searches once 3+ letters are typed.
STK_ITEMS = '''Filter(
    Office365Users.SearchUserV2(
        {
            searchTerm: If(Len(Trim(txtStakeSearch_Cap.Text)) >= 3, Trim(txtStakeSearch_Cap.Text), ""),
            top: 25,
            isSearchTermRequired: true
        }
    ).value,
    !IsBlank(Mail)
)'''
galStake = wrap(N('galStake_Cap', 'Gallery@2.15.0', 'Vertical', {'Height': f'Parent.Height - {r(160)} - {r(80)}', 'Items': STK_ITEMS, 'TemplatePadding': '0', 'TemplateSize': r(RH + 6), 'Width': f'Parent.Width - {r(24)}', 'X': r(12), 'Y': r(150)}, [
    lbl('lblStkRowT_Cap', 'ThisItem.DisplayName', x=r(12), y=r(6), w=f'Parent.TemplateWidth - {r(24)}', h=r(26), size=16, color='C_Ink', bold=True),
    lbl('lblStkRowJ_Cap', 'Coalesce(ThisItem.JobTitle, "No job title listed") & If(IsBlank(ThisItem.Department), "", "  ·  " & ThisItem.Department)', x=r(12), y=r(31), w=f'Parent.TemplateWidth - {r(24)}', h=r(20), size=14, color='C_Ink2'),
    lbl('lblStkRowM_Cap', 'Lower(ThisItem.Mail)', x=r(12), y=r(50), w=f'Parent.TemplateWidth - {r(24)}', h=r(18), size=13, color='C_Muted'),
    box('conStkLn_Cap', x=r(12), y=f'Parent.TemplateHeight - 1', w=f'Parent.TemplateWidth - {r(24)}', h='1', fill='C_Line'),
    tbtn('btnStkRow_Cap', 'Set(varStake, { Name: ThisItem.DisplayName, Email: Lower(ThisItem.Mail), Job: ThisItem.JobTitle, Dept: ThisItem.Department });\nSet(varStakeMode, "Dir");\nSet(varShowStake, false)')]), 'conStkRow_Cap')
short = '(Len(Trim(txtStakeSearch_Cap.Text)) < 3)'
stakeSheet = sheet('Cap', 'Stk', 'varShowStake', 'Find a Stakeholder', [
    box('conStkSearch_Cap', x=r(20), y=r(64), w=f'Parent.Width - {r(40)}', h=r(52), fill='C_White', border=LINE, radius=r(14), children=[
        ico('icoStkSearch_Cap', 'Search', r(14), r(14), 24, 'C_Muted'), search_input('txtStakeSearch_Cap', 'Type a name (3+ letters)')]),
    lbl('lblStkCount_Cap', f'If({short}, "Type at least 3 letters of their name", CountRows(galStake_Cap.AllItems) & If(CountRows(galStake_Cap.AllItems) = 1, " person", " people") & " found  ·  shows job title")', x=r(20), y=r(122), w=f'Parent.Width - {r(40)}', h=r(22), size=13, color='C_Muted', bold=True),
    lbl('lblStkNone_Cap', '"No one found. Try the surname, or type the name below."', x=r(20), y=r(200), w=f'Parent.Width - {r(40)}', h=r(50), size=15, color='C_Muted', align='Align.Center', wrap=True, visible=f'!{short} && CountRows(galStake_Cap.AllItems) = 0'),
    galStake,
    box('conStkType_Cap', x=r(20), y=f'Parent.Height - {r(68)}', w=f'Parent.Width - {r(40)}', h=r(52), fill='C_White', border='C_Accent', radius=r(26), children=[
        pillbtn('btnStkType_Cap', '"Not Listed? Type the Name"', 'Set(varStakeDefault, Trim(txtStakeSearch_Cap.Text));\nSet(varStakeMode, "Manual");\nSet(varShowStake, false);\nReset(txtStakeName_Cap)', 'C_Accent', size=15, radius=26)])])

# ---- saved / offline / vote: confirmation pop-up
DW = f'Min(App.Width - {r(40)}, {r(420)})'
OFF = 'varDoneMode = "Offline"'
done = box('conOverlayDone_Cap', x='0', y='0', w='App.Width', h='App.Height', fill='RGBA(14, 28, 42, 0.45)', visible='varShowDone', children=[
    box('conDone_Cap', x=f'(App.Width - {DW}) / 2', y=f'(App.Height - {r(360)}) / 2', w=DW, h=r(360), fill='C_White', radius=r(24), children=[
        box('conDoneIc_Cap', x=f'(Parent.Width - {r(72)}) / 2', y=r(28), w=r(72), h=r(72), fill=f'If({OFF}, C_AmberBg, C_GoodBg)', radius=r(36), children=[
            ico('icoDone_Cap', 'CheckmarkCircle', r(16), r(16), 40, f'If({OFF}, C_Amber, {GREEN})', True)]),
        lbl('lblDoneT_Cap', 'Switch(varDoneMode, "Offline", "Saved on This Phone", "Vote", "Vote Added", "Idea Saved")', x=r(20), y=r(112), w=f'Parent.Width - {r(40)}', h=r(36), size=24, color='C_Ink', bold=True, align='Align.Center'),
        lbl('lblDoneS_Cap', 'Switch(varDoneMode, "Offline", "No signal. It uploads next time you open Home with signal.", "Vote", "Thanks. That idea now counts your report too.", "Thanks. It is on the dashboard now.")', x=r(24), y=r(150), w=f'Parent.Width - {r(48)}', h=r(48), size=15, color='C_Ink2', align='Align.Center', wrap=True),
        box('conDoneAgain_Cap', x=r(24), y=r(214), w=f'Parent.Width - {r(48)}', h=r(56), fill='C_Accent', radius=r(28), children=[
            pillbtn('btnDoneAgain_Cap', '"Capture Another"', 'Select(btnReset_Cap)', 'C_White', size=17, radius=28)]),
        box('conDoneHome_Cap', x=r(24), y=r(280), w=f'Parent.Width - {r(48)}', h=r(56), fill='C_White', border='C_Accent', radius=r(28), children=[
            pillbtn('btnDoneHome_Cap', '"Back to Home"', 'Set(varShowDone, false);\nNavigate(Home, ScreenTransition.UnCoverRight)', 'C_Accent', size=17, radius=28)])])])

VOTE = f'''// ME TOO: add the user's vote to an idea already logged (re-read first, one vote per person)
Set(varSaving, true);
With(
    {{ fresh: LookUp({LIST}, ID = varVoteID) }},
    If(
        IsBlank(fresh),
        Notify("That idea could not be found.", NotificationType.Error),
        (";" & MeEmail & ";") in Lower(Coalesce(fresh.Voters, "")) || Lower(fresh.'Created By'.Email) = MeEmail,
        Notify("You have already added this one.", NotificationType.Information),
        With(
            {{ r: Patch({LIST}, fresh, {{ Votes: Coalesce(fresh.Votes, 0) + 1, Voters: Coalesce(fresh.Voters, ";") & MeEmail & ";" }}) }},
            If(
                IsEmpty(Errors({LIST})),
                Patch(colIdeas_Cap, LookUp(colIdeas_Cap, ID = r.ID), {{ Votes: r.Votes, Voters: Lower(r.Voters) }});
                Set(varDoneMode, "Vote");
                Set(varShowDone, true),
                Notify("Could not save. Check your connection and try again.", NotificationType.Error)
            )
        )
    )
);
Set(varSaving, false)'''

LOADIDEAS = f'''// ideas already logged, for the duplicate check (re-read at most every 5 minutes)
If(
    Connection.Connected && (IsBlank(varIdeasAt) || DateDiff(varIdeasAt, Now(), TimeUnit.Minutes) >= 5),
    ClearCollect(
        colIdeas_Cap,
        ForAll(
            Sort({LIST}, Created, SortOrder.Descending) As a,
            {{
                ID: a.ID,
                Summary: Coalesce(a.Title, ""),
                Service: Coalesce(a.Service, ""),
                Status: Coalesce(a.Status, "New"),
                Votes: Coalesce(a.Votes, 0),
                Voters: Lower(Coalesce(a.Voters, "")),
                Creator: Lower(a.'Created By'.Email),
                Hay: Lower(a.Title & " " & a.Idea & " " & a.Service & " " & a.Module)
            }}
        )
    );
    Set(varIdeasAt, Now())
);
Select(btnReset_Cap)'''

RESET = '''// RESET: clear every answer (screen opens, and "Capture Another")
Set(varSvc, Blank());
Set(varStake, Blank());
Set(varStakeMode, Blank());
Set(varStakeDefault, "");
Set(varFollow, Blank());
Set(varModule, Blank());
Set(varTheme, Blank());
Set(varPri, Blank());
Set(varSafety, Blank());
Set(varVoteID, Blank());
Set(varDoneMode, "");
Set(varSaving, false);
Set(varShowSvc, false);
Set(varShowStake, false);
Set(varShowDone, false);
Reset(txtLoc_Cap);
Reset(txtSummary_Cap);
Reset(txtStakeName_Cap);
Reset(txtThemeOther_Cap);
Reset(txtIdea_Cap);
Reset(addPhoto_Cap)'''
open(OUT + 'FW_Capture.pa.yaml', 'w').write(screen('Capture', {'Fill': 'C_Bg', 'OnVisible': LOADIDEAS},
    [vroot('conRoot_Cap', [hdrC, bodyC, footC]), svcSheet, stakeSheet, done, hidden('btnReset_Cap', RESET), hidden('btnVote_Cap', VOTE)]))


# ================================================================== HOME (after Capture: it reuses FIELDS + the safety email)
QN = 'CountRows(colQueue)'
queue = inflow('conQueue_Hm', r(150), fill='C_AmberBg', border='RGBA(178, 105, 0, 0.35)', radius=r(20), visible=f'{QN} > 0', children=[
    lbl('lblQueueCap_Hm', '"WAITING TO UPLOAD"', x=r(20), y=r(14), w=f'Parent.Width - {r(40)}', h=r(20), size=13, color='C_Amber', bold=True),
    lbl('lblQueueT_Hm', f'{QN} & If({QN} = 1, " idea", " ideas") & " saved on this phone"', x=r(20), y=r(36), w=f'Parent.Width - {r(40)}', h=r(30), size=19, color='C_Ink', bold=True),
    box('conQueueBtn_Hm', x=r(20), y=r(80), w=f'Parent.Width - {r(40)}', h=r(52), fill='If(Connection.Connected && !varSyncing, C_Accent, RGBA(160, 174, 180, 1))', radius=r(26), children=[
        pillbtn('btnQueue_Hm', 'If(varSyncing, "Uploading...", Connection.Connected, "Upload Now", "No Signal Yet")', 'Select(btnSync_Hm)', 'C_White', size=16, radius=26,
                display='If(Connection.Connected && !varSyncing, DisplayMode.Edit, DisplayMode.Disabled)')])])
bodyH = vbody('conBody_Hm', [queue, heroH, capH, t1, t2, endH], gap=15, top=20, bottom=30, scroll=True)
SYNC = f'''// UPLOAD: ideas saved on this phone while offline (one at a time; a failed one stays in the queue)
If(
    Connection.Connected && CountRows(colQueue) > 0,
    Set(varSyncing, true);
    ClearCollect(colSynced, {{ QID: "" }});
    Clear(colSynced);
    ForAll(
        colQueue As q,
        With(
            {{
                r: IfError(
                    Patch(
                        {LIST},
                        Defaults({LIST}),
                        {rec(lambda k, v: 'q.' + k, '                        ')}
                    ),
                    Blank()
                )
            }},
            If(
                !IsBlank(r.ID),
                If(!IsBlank(q.Photo), IfError(Patch({LIST}, r, {{ Photo: q.Photo }}), Notify("An idea uploaded without its photo.", NotificationType.Warning)));
                If(q.SafetyConcern = "Yes", {safety_email(lambda k: 'q.' + k)});
                Collect(colSynced, {{ QID: q.QID }})
            )
        )
    );
    RemoveIf(colQueue, QID in colSynced.QID);
    IfError(SaveData(colQueue, "fwQueue"), false);
    Set(varSyncing, false);
    If(
        CountRows(colQueue) = 0,
        Notify(CountRows(colSynced) & If(CountRows(colSynced) = 1, " idea", " ideas") & " uploaded.", NotificationType.Success),
        Notify(CountRows(colQueue) & " could not upload yet. Try again with better signal.", NotificationType.Warning)
    );
    Refresh({LIST});
    ClearCollect(colMine_Hm, Filter({LIST}, 'Created By'.Email = User().Email));
    Set(varHmMineAllN, CountRows(colMine_Hm))
)'''
ONV_H = f'''Set(varSyncing, false);
// ideas saved on this phone while offline (none = empty)
IfError(LoadData(colQueue, "fwQueue", true), false);
If(
    Connection.Connected,
    Refresh({LIST});
    // my ideas (for the My Ideas tile)
    ClearCollect(colMine_Hm, Filter({LIST}, 'Created By'.Email = User().Email));
    Set(varHmMineAllN, CountRows(colMine_Hm));
    // upload anything saved offline
    If(CountRows(colQueue) > 0, Select(btnSync_Hm))
)'''
open(OUT + 'FW_Home.pa.yaml', 'w').write(screen('Home', {'Fill': 'C_Bg', 'OnVisible': ONV_H}, [vroot('conRoot_Hm', [hdrH, bodyH]), hidden('btnSync_Hm', SYNC)]))

# ================================================================== DASHBOARD
WIDE = 'DashWide'; GAP = 'DashGap'
def panel(name, title, children, sub=None):
    ch = [lbl(f'cap{name}_Dsh', f'"{title}"', x=r(20), y=r(16), w=f'Parent.Width - {r(40)}', h=r(22), size=14, color='C_Muted', bold=True)]
    if sub: ch.append(lbl(f'sub{name}_Dsh', sub, x=r(20), y=r(38), w=f'Parent.Width - {r(40)}', h=r(20), size=13, color='C_Muted'))
    return box(f'con{name}_Dsh', fill='C_White', border='C_Line', radius=r(20), children=ch + children)
def row(name, specs):
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
def bar(name, x, y, w, h, frac, color):
    return box(f'conTrk{name}_Dsh', x=x, y=y, w=w, h=h, fill='C_Line', radius=r(6), children=[
        box(f'conBar{name}_Dsh', w=f'Parent.Width * Min(1, Max(0, {frac}))', h='Parent.Height', fill=color, radius=r(6))])

STREAMLBL = 'If(varDashStream = "ALL", "All streams", varDashStream)'
PERLBL = 'Switch(varDashPeriod, "Today", "Today", "7", "Last 7 days", "30", "Last 30 days", "All time")'
hdrD = inflow('conHdr_Dsh', r(95), w='App.Width', fill=HDR_FILL, radius='0', extra={'DropShadow': 'DropShadow.None'}, children=[
    N('imgHdr_Dsh', 'Image@2.2.3', props={'Height': 'Parent.Height', 'Image': 'HeaderImage', 'ImagePosition': 'ImagePosition.Fill', 'Width': 'Parent.Width'}),
    N('btnBack_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_White', 'FontWeight': '""', 'Height': r(60), 'Icon': '"ChevronLeft"', 'OnSelect': 'Navigate(Home, ScreenTransition.UnCoverRight)', 'Size': r(24), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': r(60), 'X': f'DashX - {r(10)}', 'Y': r(18)}, **SBOX)),
    lbl('lblHdrT_Dsh', 'If(varDashMine, "My Ideas", "Ideas Dashboard")', x=f'DashX + {r(55)}', y=r(12), w=f'DashW - {r(55)} - If({WIDE}, {r(190)}, {r(70)})', h=r(42), size=24, color='C_White', bold=True),
    lbl('lblHdrS_Dsh', f'{STREAMLBL} & "  ·  " & {PERLBL} & "  ·  " & varDashN & If(varDashN = 1, " idea", " ideas")', x=f'DashX + {r(55)}', y=r(53), w=f'DashW - {r(55)} - If({WIDE}, {r(190)}, {r(70)})', h=r(25), size=15, color='RGBA(255, 255, 255, 0.85)'),
    box('conRefresh_Dsh', x=f'DashX + DashW - If({WIDE}, {r(170)}, {r(56)})', y=r(22), w=f'If({WIDE}, {r(170)}, {r(56)})', h=r(50), fill='RGBA(255, 255, 255, 0.16)', border='RGBA(255, 255, 255, 0.45)', radius=r(25), children=[
        N('btnRefresh_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_White', 'DisplayMode': 'If(varDashLoading, DisplayMode.Disabled, DisplayMode.Edit)', 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'Icon': '"ArrowClockwise"', 'OnSelect': 'Select(btnLoad_Dsh)', 'Size': r(F(15)), 'Text': f'If({WIDE}, "Refresh", "")', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(25)), **NOSB))]),
])

# ---- filters: stream pills; period pills + Mine
def pillgal(name, items, selexpr, onsel, label, w, x, y):
    return N(f'gal{name}_Dsh', 'Gallery@2.15.0', 'Horizontal', {'Height': r(52), 'Items': items, 'ShowScrollbar': 'false', 'TemplatePadding': '0',
        'TemplateSize': f'({w}) / Max(1, CountRows({items}))', 'Width': w, 'X': x, 'Y': y}, [
        box(f'con{name}P_Dsh', x='3', y=r(2), w=f'Parent.TemplateWidth - {r(6)}', h=r(48), fill=f'If({selexpr}, C_Accent, C_White)', border=f'If({selexpr}, C_Accent, C_Line)', radius=r(24), children=[
            lbl(f'lbl{name}P_Dsh', label, x=r(4), w=f'Parent.Width - {r(8)}', h=r(48), size=14, color=f'If({selexpr}, C_White, C_Ink2)', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
            tbtn(f'btn{name}P_Dsh', onsel)])])
galStr = pillgal('Str', 'colDashPills', 'ThisItem.Key = varDashStream', 'Set(varDashStream, ThisItem.Key);\nSelect(btnCalc_Dsh)', f'If({WIDE}, ThisItem.Full, ThisItem.Label)', f'Parent.Width - {r(32)}', r(16), r(12))
galPer = pillgal('Per', 'colDashPer', 'ThisItem.Key = varDashPeriod', 'Set(varDashPeriod, ThisItem.Key);\nSelect(btnCalc_Dsh)', 'ThisItem.Label', f'Parent.Width - {r(32)} - {r(110)}', r(16), r(70))
mine = box('conMine_Dsh', x=f'Parent.Width - {r(16)} - {r(104)}', y=r(72), w=r(104), h=r(48), fill='If(varDashMine, C_Accent, C_White)', border='If(varDashMine, C_Accent, C_Line)', radius=r(24), children=[
    pillbtn('btnMine_Dsh', 'If(varDashMine, "✓  Mine", "Mine")', 'Set(varDashMine, !varDashMine);\nSelect(btnCalc_Dsh)', 'If(varDashMine, C_White, C_Ink2)', size=14, radius=24)])
filters = inflow('conFilters_Dsh', r(134), w='DashW', fill='C_White', border='C_Line', radius=r(20), children=[galStr, galPer, mine])

# ---- KPI tiles: tap to list those ideas
pc = lambda v: f'Round((If(varDashN > 0, {v} / varDashN, 0)) * 100, 0) & "% of " & varDashN'
KPIS = [('All', 'IDEAS', 'varDashN', PERLBL, 'C_Ink', '', ''),
        ('New', 'NEW', 'varDashNewN', '"Not yet reviewed"', 'C_Accent', 'Status', 'New'),
        ('High', 'HIGH PRIORITY', 'varDashHighN', pc('varDashHighN'), RED, 'Priority', 'High'),
        ('Fol', 'FOLLOW-UP', 'varDashFolN', '"Wants contact"', 'C_Amber', 'Follow', 'Yes'),
        ('Safe', 'SAFETY CONCERN', 'varDashSafeN', '"Could harm a patient"', RED, 'Safety', 'Yes'),
        ('Act', 'ACTIONED', 'varDashActN', pc('varDashActN'), GREEN, 'Status', 'Actioned')]
TH = 112
twW = f'(DashW - 5 * {GAP}) / 6'; twN = f'(DashW - {GAP}) / 2'
tiles = []
for i, (k, capt, val, sub, col, fk, fv_) in enumerate(KPIS):
    sel = f'varDashFKind = "{fk}" && varDashFVal = "{fv_}"' if fk else 'false'
    onsel = (f'If({sel}, Set(varDashFKind, ""); Set(varDashFVal, ""), Set(varDashFKind, "{fk}"); Set(varDashFVal, "{fv_}"))' if fk else 'Set(varDashFKind, "");\nSet(varDashFVal, "")')
    tiles.append(box(f'conK{k}_Dsh', x=f'If({WIDE}, {i} * ({twW} + {GAP}), {i % 2} * ({twN} + {GAP}))', y=f'If({WIDE}, 0, {i // 2} * ({r(TH)} + {GAP}))', w=f'If({WIDE}, {twW}, {twN})', h=r(TH),
        fill=f'If({sel}, C_AccentSoft, C_White)', border=f'If({sel}, C_Accent, C_Line)', radius=r(20), children=[
        lbl(f'lblK{k}C_Dsh', f'"{capt}"', x=r(18), y=r(14), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Muted', bold=True),
        lbl(f'lblK{k}V_Dsh', val, x=r(18), y=r(34), w=f'Parent.Width - {r(36)}', h=r(46), size=36, color=col, bold=True),
        lbl(f'lblK{k}S_Dsh', sub, x=r(18), y=r(80), w=f'Parent.Width - {r(36)}', h=r(20), size=13, color='C_Ink2'),
        tbtn(f'btnK{k}_Dsh', onsel)]))
kpi = inflow('conKpi_Dsh', f'If({WIDE}, {r(TH)}, 3 * {r(TH)} + 2 * {GAP})', w='DashW', children=tiles, extra={'DropShadow': 'DropShadow.None'})

# ---- bar panels
SH_ = 56
def listpanel(name, title, sub, items, label, value, frac, color, rows, onsel=None, selexpr=None, empty=None):
    ch = []
    if selexpr: ch.append(box(f'con{name}Sel_Dsh', x='0', y=r(2), w='Parent.TemplateWidth', h=r(SH_ - 4), fill=f'If({selexpr}, C_AccentSoft, RGBA(0, 0, 0, 0))', radius=r(12)))
    ch += [lbl(f'lbl{name}_Dsh', label, x=r(10), y=r(4), w=f'Parent.TemplateWidth - {r(120)}', h=r(24), size=14, color='C_Ink', bold=True),
           lbl(f'lbl{name}N_Dsh', value, x=f'Parent.TemplateWidth - {r(110)}', y=r(4), w=r(100), h=r(24), size=14, color='C_Ink2', bold=True, align='Align.Right'),
           bar(name, r(10), r(32), f'Parent.TemplateWidth - {r(20)}', r(12), frac, color)]
    if onsel: ch.append(tbtn(f'btn{name}_Dsh', onsel))
    g = wrap(N(f'gal{name}_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'{rows} * {r(SH_)}', 'Items': items, 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(SH_), 'Width': f'Parent.Width - {r(20)}', 'X': r(10), 'Y': r(62)}, ch), f'con{name}Row_Dsh')
    kids = [g]
    if empty: kids.append(lbl(f'lbl{name}None_Dsh', f'"{empty}"', x=r(20), y=r(150), w=f'Parent.Width - {r(40)}', h=r(30), size=15, color='C_Muted', align='Align.Center', visible=f'Sum(gal{name}_Dsh.AllItems, N) = 0'))
    return panel(name, title, kids, sub=sub)
def focus(kind, key='ThisItem.Key'):
    sel = f'varDashFKind = "{kind}" && varDashFVal = {key}'
    return (f'If({sel}, Set(varDashFKind, ""); Set(varDashFVal, ""), Set(varDashFKind, "{kind}"); Set(varDashFVal, {key}))', sel)
share = lambda tot: f'ThisItem.N & "  ·  " & Round((If({tot} > 0, ThisItem.N / {tot}, 0)) * 100, 0) & "%"'
pStr = listpanel('ByStr', 'BY BAU STREAM', '"Tap to show one stream"', 'colDashStr', 'ThisItem.Key', share('varDashBaseN'), 'If(varDashBaseN > 0, ThisItem.N / varDashBaseN, 0)', 'C_Accent', 6,
                 onsel='Set(varDashStream, If(varDashStream = ThisItem.Key, "ALL", ThisItem.Key));\nSelect(btnCalc_Dsh)', selexpr='varDashStream = ThisItem.Key', empty='No ideas yet')
o, s_ = focus('Theme'); pTh = listpanel('ByTheme', 'BY THEME', '"Tap a theme to list those ideas"', 'colDashTheme', 'ThisItem.Key', share('varDashN'), 'If(varDashN > 0, ThisItem.N / varDashN, 0)', 'C_Teal', 5, onsel=o, selexpr=s_, empty='No ideas yet')
o, s_ = focus('Status'); pSt = listpanel('ByStat', 'BY STATUS', '"Where each idea is up to"', 'colDashStat', 'ThisItem.Key', share('varDashN'), 'If(varDashN > 0, ThisItem.N / varDashN, 0)', scol('ThisItem.Key'), 4, onsel=o, selexpr=s_, empty='No ideas yet')
o, s_ = focus('Service'); pSv = listpanel('BySvc', 'TOP SERVICES', 'varDashNoSvcN & If(varDashNoSvcN = 1, " idea", " ideas") & " with no service recorded"', 'colDashSvc', 'ThisItem.Key', 'ThisItem.N', 'If(varDashMaxSvc > 0, ThisItem.N / varDashMaxSvc, 0)', 'C_Accent', 6, onsel=o, selexpr=s_, empty='No services recorded yet')
o, s_ = focus('Module'); pMod = listpanel('ByMod', 'ieMR AREAS', 'varDashNoModN & If(varDashNoModN = 1, " idea", " ideas") & " with no area recorded"', 'colDashMod', 'ThisItem.Key', 'ThisItem.N', 'If(varDashMaxMod > 0, ThisItem.N / varDashMaxMod, 0)', 'C_Amber', 6, onsel=o, selexpr=s_, empty='No areas recorded yet')
o, s_ = focus('Walker'); pWk = listpanel('ByWalk', 'FLOORWALKERS', '"Ideas captured by each person"', 'colDashWalk', 'ThisItem.Key', 'ThisItem.N', 'If(varDashMaxWalk > 0, ThisItem.N / varDashMaxWalk, 0)', 'C_Teal', 6, onsel=o, selexpr=s_, empty='No ideas yet')

# ---- idea list
nf = '!IsBlank(varDashFKind)'
FOCUSLBL = 'Switch(varDashFKind, "Follow", "Follow-up wanted", "Priority", varDashFVal & " priority", "Walker", "Captured by " & varDashFVal, "Safety", "Safety concerns", "Module", "ieMR: " & varDashFVal, varDashFVal)'
SEARCH = 'Lower(Trim(txtSearch_Dsh.Text))'
ITEMS = f'''SortByColumns(
    Filter(
        colDash,
        Switch(
            varDashFKind,
            "Status", Status = varDashFVal,
            "Theme", Theme = varDashFVal,
            "Priority", Priority = varDashFVal,
            "Follow", Follow,
            "Service", Service = varDashFVal,
            "Walker", Walker = varDashFVal,
            "Safety", Safety,
            "Module", Module = varDashFVal,
            true
        )
        && (IsBlank({SEARCH}) || {SEARCH} in Lower(Summary & " " & Idea & " " & Module & " " & Service & " " & Loc & " " & Stake & " " & Walker & " " & Theme & " " & ThemeOther))
    ),
    "When",
    SortOrder.Descending
)'''
LH = 142
lrow = box('conRow_Dsh', x='1', y=r(5), w=f'Parent.TemplateWidth - {r(12)}', h=r(LH - 10), fill='C_White', border='C_Line', radius=r(16), children=[
    box('conStripe_Dsh', w=r(8), h='Parent.Height', fill=pcol('ThisItem.Priority'), extra={'RadiusTopLeft': r(16), 'RadiusBottomLeft': r(16), 'RadiusTopRight': '0', 'RadiusBottomRight': '0'}),
    lbl('lblRowT_Dsh', 'ThisItem.Summary', x=r(22), y=r(10), w=f'Parent.Width - {r(66)}', h=r(44), size=15, color='C_Ink', bold=True, wrap=True),
    lbl('lblRowS_Dsh', 'ThisItem.Theme & "  ·  " & If(IsBlank(ThisItem.Service), "No service", ThisItem.Service) & "  ·  " & ThisItem.StreamShort', x=r(22), y=r(58), w=f'Parent.Width - {r(66)}', h=r(20), size=13, color='C_Ink2'),
    lbl('lblRowM_Dsh', 'ThisItem.Walker & "  ·  " & Text(ThisItem.When, "d mmm, h:mm AM/PM") & If(IsBlank(ThisItem.Loc), "", "  ·  " & ThisItem.Loc)', x=r(22), y=r(80), w=f'Parent.Width - {r(66)}', h=r(20), size=13, color='C_Muted'),
    box('conRowSt_Dsh', x=r(22), y=r(102), w=r(120), h=r(24), fill=ssoft('ThisItem.Status'), radius=r(12), children=[
        lbl('lblRowSt_Dsh', 'ThisItem.Status', w='Parent.Width', h=r(24), size=13, color=scol('ThisItem.Status'), bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})]),
    lbl('lblRowP_Dsh', 'ThisItem.Priority & If(ThisItem.Safety, "  ·  ⚠ Safety", "") & If(ThisItem.Votes > 0, "  ·  +" & ThisItem.Votes, "") & If(ThisItem.Follow, "  ·  Follow-up", "")', x=r(152), y=r(102), w=f'Parent.Width - {r(170)}', h=r(24), size=13, color=pcol('ThisItem.Priority'), bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    ico('icoRowGo_Dsh', 'ChevronRight', f'Parent.Width - {r(40)}', r(54), 24, 'C_Muted'),
    tbtn('btnRow_Dsh', 'Set(varDashSel, ThisItem);\nSet(varDetStatus, ThisItem.Status);\nSet(varDetPri, ThisItem.Priority);\nReset(txtRevNotes_Dsh);\nSet(varDashShowDet, true)'),
])
GY = f'If({WIDE}, {r(118)}, If({nf}, {r(170)}, {r(120)}))'
galList = N('galList_Dsh', 'Gallery@2.15.0', 'Vertical', {'Height': f'Parent.Height - {GY} - {r(10)}', 'Items': ITEMS, 'TemplatePadding': '0', 'TemplateSize': r(LH), 'Width': f'Parent.Width - {r(28)}', 'X': r(16), 'Y': GY}, [lrow])
wrap(galList, 'conRowWrap_Dsh')
cntL = 'CountRows(galList_Dsh.AllItems)'
pList = panel('List', 'IDEAS', [
    lbl('lblListN_Dsh', f'{cntL} & If({cntL} = 1, " idea", " ideas") & If({nf} || !IsBlank({SEARCH}), " match", "") & ", newest first. Tap one for detail."', x=r(20), y=r(38), w=f'If({WIDE}, Parent.Width - {r(400)}, Parent.Width - {r(40)})', h=r(22), size=14, color='C_Ink2', bold=True),
    box('conSearch_Dsh', x=f'If({WIDE}, Parent.Width - {r(360)}, {r(20)})', y=f'If({WIDE}, {r(14)}, {r(66)})', w=f'If({WIDE}, {r(340)}, Parent.Width - {r(40)})', h=r(44), fill='C_White', border=LINE, radius=r(14), children=[
        ico('icoSearch_Dsh', 'Search', r(12), r(11), 22, 'C_Muted'),
        N('txtSearch_Dsh', 'Classic/TextInput@2.3.2', props={'BorderStyle': 'BorderStyle.None', 'Color': 'C_Ink', 'Default': '""', 'DelayOutput': 'true', 'Fill': TR, 'Font': 'AppFont', 'Height': 'Parent.Height', 'HintText': '"Search idea, service, location, people"', 'Size': r(F(14)), 'Width': f'Parent.Width - {r(44)}', 'X': r(40)})]),
    box('conFocus_Dsh', x=r(20), y=f'If({WIDE}, {r(66)}, {r(118)})', w=f'If({WIDE}, Parent.Width - {r(400)}, Parent.Width - {r(40)})', h=r(40), fill='C_AccentSoft', border='C_Accent', radius=r(20), visible=nf, children=[
        lbl('lblFocus_Dsh', '"Showing: " & ' + FOCUSLBL, x=r(16), w=f'Parent.Width - {r(130)}', h=r(40), size=14, color='C_Accent', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        lbl('lblFocusX_Dsh', '"Clear  ✕"', x=f'Parent.Width - {r(110)}', w=r(96), h=r(40), size=14, color='C_Accent', bold=True, align='Align.Right', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn('btnFocusX_Dsh', 'Set(varDashFKind, "");\nSet(varDashFVal, "")')]),
    lbl('lblListNone_Dsh', 'If(varDashN = 0, "No ideas in this view yet", "No ideas match")', x=r(20), y=r(220), w=f'Parent.Width - {r(40)}', h=r(30), size=16, color='C_Muted', align='Align.Center', visible=f'{cntL} = 0'),
    galList])
pList.props.update({'Width': 'DashW', 'Height': r(780), 'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'LayoutMinHeight': r(780)})

loading = lbl('lblLoading_Dsh', '"Loading ideas..."', w='DashW', h=r(26), size=15, color='C_Muted', align='Align.Center', visible='varDashLoading', extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(26)})
endD = inflow('conEnd_Dsh', r(16), w='DashW', extra={'DropShadow': 'DropShadow.None'})
bodyP = {'AlignInContainer': 'AlignInContainer.SetByContainer', 'DropShadow': 'DropShadow.None', 'LayoutAlignItems': 'LayoutAlignItems.Start', 'LayoutDirection': 'LayoutDirection.Vertical', 'LayoutGap': GAP,
         'LayoutMinHeight': r(250), 'LayoutOverflowY': 'LayoutOverflow.Scroll', 'PaddingBottom': r(10), 'PaddingLeft': 'DashX', 'PaddingRight': 'DashX', 'PaddingTop': r(18), 'Width': 'App.Width'}
bodyP.update(rad('0'))
bodyD = N('conBody_Dsh', 'GroupContainer@1.5.0', 'AutoLayout', bodyP, [
    filters, loading, kpi,
    row('A', [(pStr, 1 / 3, 412), (pTh, 1 / 3, 356), (pSt, 1 / 3, 300)]),
    row('B', [(pSv, 1 / 3, 412), (pMod, 1 / 3, 412), (pWk, 1 / 3, 412)]),
    pList, endD])
# row A: all 412 high side by side (stream has 6 rows)
for p_ in (pTh, pSt):
    p_.props['Height'] = f'If({WIDE}, {r(412)}, {p_.props["Height"]})'

# ---- idea detail (pop-up) + review (status, priority, notes)
SEL = 'varDashSel'
DETW = f'Min(App.Width - {r(24)}, {r(900)})'
IW2 = f'{DETW} - {r(40)}'
def dl(name, text, h, size=15, color='C_Ink', bold=False, wrap=False, auto=False, visible=None):
    x = {'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'LayoutMinHeight': r(h)}
    if auto: x['AutoHeight'] = 'true'
    return lbl(name, text, w=IW2, h=r(h), size=size, color=color, bold=bold, wrap=wrap, visible=visible, extra=x)
def dcap(name, text, visible=None):
    return dl(name, f'"{text}"', 30, size=13, color='C_Muted', bold=True, visible=visible)
INFO = [('Svc', 'SERVICE', f'If(IsBlank({SEL}.Service), "Not recorded", {SEL}.Service)'), ('Mod', 'ieMR AREA', f'If(IsBlank({SEL}.Module), "Not recorded", {SEL}.Module)'),
        ('Str', 'BAU STREAM', f'{SEL}.Stream'), ('Loc', 'LOCATION', f'If(IsBlank({SEL}.Loc), "Not recorded", {SEL}.Loc)'),
        ('Thm', 'THEME', f'{SEL}.Theme & If(IsBlank({SEL}.ThemeOther), "", ": " & {SEL}.ThemeOther)'), ('Fol', 'FOLLOW-UP WANTED', f'If({SEL}.Follow, "Yes", "No")'),
        ('Safe', 'PATIENT SAFETY CONCERN', f'If({SEL}.Safety, "Yes", "No")'), ('Vote', 'ALSO SEEN BY', f'If({SEL}.Votes = 0, "No one else yet", {SEL}.Votes & If({SEL}.Votes = 1, " other person", " other people"))')]
IH = 56
ninfo = len(INFO)
# wide: two columns of 3; phone: one column of 6
cw = f'If({WIDE}, ({IW2}) / 2, {IW2})'
info_kids = []
for i, (k, c, v) in enumerate(INFO):
    xx = f'If({WIDE}, {i % 2} * ({IW2}) / 2, 0)'
    yy = f'If({WIDE}, {i // 2} * {r(IH)}, {i} * {r(IH)})'
    info_kids += [lbl(f'lblI{k}C_Dsh', f'"{c}"', x=f'{xx} + {r(16)}', y=f'{yy} + {r(8)}', w=f'{cw} - {r(32)}', h=r(20), size=13, color='C_Muted', bold=True),
                  lbl(f'lblI{k}V_Dsh', v, x=f'{xx} + {r(16)}', y=f'{yy} + {r(28)}', w=f'{cw} - {r(32)}', h=r(24), size=15, color='C_Ink', bold=True)]
info = inflow('conDetInfo_Dsh', f'If({WIDE}, {r(((ninfo + 1) // 2) * IH + 8)}, {r(ninfo * IH + 8)})', w=IW2, fill='C_Bg', radius=r(14), children=info_kids)
HASST = f'!IsBlank({SEL}.Stake)'
HASEM = f'!IsBlank({SEL}.StakeEmail)'
stk = inflow('conDetStake_Dsh', f'If({HASEM}, {r(150)}, {r(92)})', w=IW2, fill='C_White', border='C_Line', radius=r(14), visible=HASST, children=[
    lbl('lblDStkN_Dsh', f'{SEL}.Stake', x=r(16), y=r(10), w=f'Parent.Width - {r(32)}', h=r(26), size=17, color='C_Ink', bold=True),
    lbl('lblDStkJ_Dsh', f'If(IsBlank({SEL}.StakeJob), "Typed in (not from the directory)", {SEL}.StakeJob & If(IsBlank({SEL}.StakeDept), "", "  ·  " & {SEL}.StakeDept))', x=r(16), y=r(38), w=f'Parent.Width - {r(32)}', h=r(22), size=14, color='C_Ink2'),
    lbl('lblDStkM_Dsh', f'{SEL}.StakeEmail', x=r(16), y=r(60), w=f'Parent.Width - {r(32)}', h=r(22), size=14, color='C_Muted', visible=HASEM),
    box('conDStkMail_Dsh', x=r(16), y=r(92), w=f'Min(Parent.Width - {r(32)}, {r(260)})', h=r(44), fill='C_White', border='C_Accent', radius=r(22), visible=HASEM, children=[
        N('btnDStkMail_Dsh', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_Accent', 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'Icon': '"Mail"',
            'OnSelect': f'Launch("mailto:" & {SEL}.StakeEmail & "?subject=" & EncodeUrl("Your ieMR improvement idea") & "&body=" & EncodeUrl("Hi " & First(Split({SEL}.Stake, " ")).Value & "," & Char(10) & Char(10) & "Following up on your idea: " & {SEL}.Idea & Char(10) & Char(10)))',
            'Size': r(F(14)), 'Text': '"Email Stakeholder"', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(22)), **NOSB))])])
noStk = dl('lblDetNoStk_Dsh', '"No stakeholder recorded"', 30, size=15, color='C_Muted', visible=f'!{HASST}')
HASPH = f'!IsBlank(LookUp(colDashSrc, ID = {SEL}.ID).Photo)'
photoD = inflow('conDetPhoto_Dsh', r(380), w=IW2, fill='C_Bg', radius=r(14), visible=HASPH, children=[
    N('imgDetPhoto_Dsh', 'Image@2.2.3', props={'Height': f'Parent.Height - {r(16)}', 'Image': f'LookUp(colDashSrc, ID = {SEL}.ID).Photo', 'ImagePosition': 'ImagePosition.Fit', 'Width': f'Parent.Width - {r(16)}', 'X': r(8), 'Y': r(8)})])
# review pills: status 4 (row when wide, 2 x 2 on phones), priority 3
sw = f'If({WIDE}, (Parent.Width - 3 * {r(10)}) / 4, (Parent.Width - {r(10)}) / 2)'
st_kids = [colorpill(f'DSt{i}_Dsh', 'varDetStatus', s, f'If({WIDE}, {i} * ({sw} + {r(10)}), {i % 2} * ({sw} + {r(10)}))', f'If({WIDE}, 0, {i // 2} * {r(58)})', sw, scol(f'"{s}"'), size=14)
           for i, s in enumerate(STATUSES)]
stPills = inflow('conDetSt_Dsh', f'If({WIDE}, {r(48)}, {r(106)})', w=IW2, children=st_kids, extra={'DropShadow': 'DropShadow.None'})
pw2 = f'(Parent.Width - 2 * {r(10)}) / 3'
prPills = inflow('conDetPr_Dsh', r(48), w=IW2, extra={'DropShadow': 'DropShadow.None'}, children=[
    colorpill(f'DPr{p}_Dsh', 'varDetPri', p, f'{i} * ({pw2} + {r(10)})', '0', pw2, pcol(f'"{p}"'), size=14) for i, p in enumerate(PRIS)])
revNotes = tin('txtRevNotes_Dsh', 'What was decided, who owns it, next step', '0', '0', IW2, r(110), multi=True, default=f'{SEL}.ReviewNotes')
revNotes.props.update({'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'LayoutMinHeight': r(110)})
del revNotes.props['X']; del revNotes.props['Y']
CHANGED = f'(varDetStatus <> {SEL}.Status || varDetPri <> {SEL}.Priority || Trim(txtRevNotes_Dsh.Text) <> Coalesce({SEL}.ReviewNotes, ""))'
okD = 'btnDetSave_Dsh.DisplayMode = DisplayMode.Edit'
SAVE_D = f'''Set(varSaving, true);
With(
    {{ fresh: LookUp({LIST}, ID = {SEL}.ID) }},
    If(
        IsBlank(fresh),
        Set(varSaving, false);
        Notify("This idea could not be found. Tap Refresh.", NotificationType.Error),
        // someone else saved this idea after the dashboard loaded: don't overwrite their change
        fresh.Modified > {SEL}.Modified,
        Set(varSaving, false);
        Notify("Someone updated this idea a moment ago. Tap Refresh, then try again.", NotificationType.Warning),
        With(
            {{
                rec: Patch(
                    {LIST},
                    fresh,
                    {{
                        Status: varDetStatus,
                        Priority: varDetPri,
                        ReviewNotes: Trim(txtRevNotes_Dsh.Text),
                        StatusBy: MeName,
                        StatusOn: Now()
                    }}
                )
            }},
            If(
                IsEmpty(Errors({LIST})),
                Patch(
                    colDashRows,
                    LookUp(colDashRows, ID = rec.ID),
                    {{ Status: rec.Status, Priority: rec.Priority, ReviewNotes: Coalesce(rec.ReviewNotes, ""), StatusBy: rec.StatusBy, StatusOn: rec.StatusOn, Modified: rec.Modified }}
                );
                Set({SEL}, LookUp(colDashRows, ID = rec.ID));
                Select(btnCalc_Dsh);
                Set(varSaving, false);
                Notify("Saved.", NotificationType.Success),
                Set(varSaving, false);
                Notify("Could not save. Check your connection and try again.", NotificationType.Error)
            )
        )
    )
)'''
saveD = inflow('conDetSave_Dsh', r(56), w=IW2, fill=f'If({okD}, C_Accent, RGBA(160, 174, 180, 1))', radius=r(28), children=[
    lbl('lblDetSave_Dsh', f'If(varSaving, "Saving...", {okD}, "Save Changes", "No changes to save")', w='Parent.Width', h=r(56), size=17, color='C_White', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnDetSave_Dsh', SAVE_D, display=f'If({CHANGED} && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)')])
lastUp = dl('lblDetLast_Dsh', f'If(IsBlank({SEL}.StatusBy), "Not reviewed yet", "Last updated by " & {SEL}.StatusBy & " on " & Text({SEL}.StatusOn, "d mmm yyyy, h:mm AM/PM"))', 24, size=13, color='C_Muted')
endDet = inflow('conDetEnd_Dsh', r(16), w=IW2, extra={'DropShadow': 'DropShadow.None'})
detP = {'AlignInContainer': 'AlignInContainer.SetByContainer', 'DropShadow': 'DropShadow.None', 'Height': f'Parent.Height - {r(100)}', 'LayoutAlignItems': 'LayoutAlignItems.Start',
        'LayoutDirection': 'LayoutDirection.Vertical', 'LayoutGap': r(8), 'LayoutOverflowY': 'LayoutOverflow.Scroll', 'PaddingBottom': r(8), 'PaddingLeft': r(20), 'PaddingRight': r(20),
        'PaddingTop': r(10), 'Width': 'Parent.Width', 'X': '0', 'Y': r(100)}
detP.update(rad('0'))
VOTED_D = '((";" & MeEmail & ";") in varDashSel.Voters || varDashSel.WalkerEmail = MeEmail)'
meToo = inflow('conDetVote_Dsh', r(48), w=f'Min({IW2}, {r(300)})', fill=f'If({VOTED_D}, C_GoodBg, C_Accent)', radius=r(24), children=[
    pillbtn('btnDetVote_Dsh', f'If({VOTED_D}, "✓ You Reported This Too", "Me Too: I Have Seen This")', 'Select(btnVote_Dsh)', f'If({VOTED_D}, {GREEN}, C_White)', size=14, radius=24,
            display=f'If({VOTED_D} || varSaving, DisplayMode.Disabled, DisplayMode.Edit)')])
VOTE_D = f'''// ME TOO from the dashboard (re-read first, one vote per person)
Set(varSaving, true);
With(
    {{ fresh: LookUp({LIST}, ID = varDashSel.ID) }},
    If(
        IsBlank(fresh),
        Notify("This idea could not be found. Tap Refresh.", NotificationType.Error),
        (";" & MeEmail & ";") in Lower(Coalesce(fresh.Voters, "")) || Lower(fresh.'Created By'.Email) = MeEmail,
        Notify("You have already added this one.", NotificationType.Information),
        With(
            {{ r: Patch({LIST}, fresh, {{ Votes: Coalesce(fresh.Votes, 0) + 1, Voters: Coalesce(fresh.Voters, ";") & MeEmail & ";" }}) }},
            If(
                IsEmpty(Errors({LIST})),
                Patch(colDashRows, LookUp(colDashRows, ID = r.ID), {{ Votes: r.Votes, Voters: Lower(r.Voters), Modified: r.Modified }});
                Set(varDashSel, LookUp(colDashRows, ID = r.ID));
                Select(btnCalc_Dsh);
                Notify("Added. Thanks.", NotificationType.Success),
                Notify("Could not save. Check your connection and try again.", NotificationType.Error)
            )
        )
    )
);
Set(varSaving, false)'''
detBody = N('conDetBody_Dsh', 'GroupContainer@1.5.0', 'AutoLayout', detP, [
    dcap('capDetIdea_Dsh', 'THE IDEA'), dl('lblDetSum_Dsh', f'{SEL}.Summary', 30, size=19, color='C_Ink', bold=True, wrap=True, auto=True),
    dl('lblDetIdea_Dsh', f'{SEL}.Idea', 26, size=16, color='C_Ink2', wrap=True, auto=True, visible=f'!IsBlank({SEL}.Idea) && {SEL}.Idea <> {SEL}.Summary'),
    meToo,
    info,
    dcap('capDetStk_Dsh', 'STAKEHOLDER'), stk, noStk,
    dcap('capDetPh_Dsh', 'PHOTO', visible=HASPH), photoD,
    box('conDetLn2_Dsh', w=IW2, h='1', fill='C_Line', extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'LayoutMinHeight': '1'}),
    dcap('capDetSt_Dsh', 'REVIEW  ·  STATUS'), stPills,
    dcap('capDetPr_Dsh', 'PRIORITY'), prPills,
    dcap('capDetNote_Dsh', 'REVIEW NOTES'), revNotes,
    saveD, lastUp, endDet])
cardD = box('conDetCard_Dsh', x=f'(App.Width - {DETW}) / 2', y=r(24), w=DETW, h=f'App.Height - {r(48)}', fill='C_White', radius=r(22), extra={'DropShadow': 'DropShadow.Bold'}, children=[
    box('conDetStripe_Dsh', w=r(10), h=r(100), fill=pcol(f'{SEL}.Priority'), extra={'RadiusTopLeft': r(22), 'RadiusBottomLeft': '0', 'RadiusTopRight': '0', 'RadiusBottomRight': '0'}),
    lbl('lblDetT_Dsh', f'{SEL}.Theme', x=r(28), y=r(16), w=f'Parent.Width - {r(110)}', h=r(36), size=19, color='C_Ink', bold=True),
    lbl('lblDetS_Dsh', f'Text({SEL}.When, "d mmm, h:mm AM/PM") & "  ·  " & {SEL}.Walker', x=r(28), y=r(54), w=f'Parent.Width - {r(110)}', h=r(26), size=15, color='C_Ink2'),
    iconbtn('btnDetClose_Dsh', 'DismissCircle', 'Set(varDashShowDet, false)', f'Parent.Width - {r(72)}', r(20)),
    box('conDetLine_Dsh', x='0', y=r(99), w='Parent.Width', h='1', fill='C_Line'),
    detBody])
overlayD = box('conOverlayDet_Dsh', x='0', y='0', w='App.Width', h='App.Height', fill='RGBA(14, 28, 42, 0.45)', visible='varDashShowDet', children=[
    tbtn('btnDetVeil_Dsh', 'Set(varDashShowDet, false)'), cardD])

LOAD = f'''// LOAD: newest 2000 ideas, flattened to plain columns once (the screen then works on the device)
Set(varDashLoading, true);
Refresh({LIST});
ClearCollect(colDashSrc, Sort({LIST}, Created, SortOrder.Descending));
ClearCollect(
    colDashRows,
    ForAll(
        colDashSrc As a,
        {{
            ID: a.ID,
            When: a.Created,
            Modified: a.Modified,
            Walker: a.'Created By'.DisplayName,
            WalkerEmail: Lower(a.'Created By'.Email),
            Summary: Coalesce(a.Title, Left(a.Idea, 120)),
            Idea: a.Idea,
            Module: a.Module,
            Safety: a.SafetyConcern = "Yes",
            Votes: Coalesce(a.Votes, 0),
            Voters: Lower(Coalesce(a.Voters, "")),
            Service: a.Service,
            Line: a.ServiceLine,
            // blank stream: no service picked ("No service"), or a service with no stream ("Other")
            Stream: If(!IsBlank(a.Stream), a.Stream, IsBlank(a.Service), "No service", "Other"),
            StreamShort: If(!IsBlank(a.Stream), Coalesce(LookUp(StreamList, Key = a.Stream).Short, a.Stream), IsBlank(a.Service), "No service", "Other"),
            Loc: a.Location,
            Stake: a.StakeholderName,
            StakeEmail: a.StakeholderEmail,
            StakeJob: a.StakeholderJobTitle,
            StakeDept: a.StakeholderDept,
            Follow: a.FollowUp = "Yes",
            Theme: Coalesce(a.Theme, "Other"),
            ThemeOther: a.ThemeOther,
            Priority: Coalesce(a.Priority, "Medium"),
            Status: Coalesce(a.Status, "New"),
            ReviewNotes: Coalesce(a.ReviewNotes, ""),
            StatusBy: a.StatusBy,
            StatusOn: a.StatusOn
        }}
    )
);
Set(varDashLoading, false);
Select(btnCalc_Dsh)'''
CALC = '''// CALC: apply Mine + period + stream, then every number and bar on the screen
ClearCollect(
    colDashBase,
    Filter(
        colDashRows,
        (!varDashMine || WalkerEmail = MeEmail)
        && Switch(
            varDashPeriod,
            "Today", When >= Today(),
            "7", When >= DateAdd(Today(), -6, TimeUnit.Days),
            "30", When >= DateAdd(Today(), -29, TimeUnit.Days),
            true
        )
    )
);
ClearCollect(colDash, Filter(colDashBase, varDashStream = "ALL" || Stream = varDashStream));
Set(varDashBaseN, CountRows(colDashBase));
Set(varDashN, CountRows(colDash));
Set(varDashNewN, CountIf(colDash, Status = "New"));
Set(varDashHighN, CountIf(colDash, Priority = "High"));
Set(varDashFolN, CountIf(colDash, Follow));
Set(varDashActN, CountIf(colDash, Status = "Actioned"));
// by stream ignores the stream filter, so every stream stays visible
ClearCollect(colDashStr, ForAll(StreamList As s, { Key: s.Key, N: CountIf(colDashBase, Stream = s.Key) }));
ClearCollect(colDashTheme, ForAll(ThemeList As t, { Key: t.Value, N: CountIf(colDash, Theme = t.Value) }));
ClearCollect(colDashStat, ForAll(StatusList As t, { Key: t.Value, N: CountIf(colDash, Status = t.Value) }));
ClearCollect(
    colDashSvc,
    FirstN(
        SortByColumns(
            ForAll(Filter(Distinct(colDash, Service), !IsBlank(Value)) As s, { Key: s.Value, N: CountIf(colDash, Service = s.Value) }),
            "N",
            SortOrder.Descending
        ),
        6
    )
);
Set(varDashMaxSvc, Max(colDashSvc, N));
Set(varDashNoSvcN, CountIf(colDash, IsBlank(Service)));
ClearCollect(
    colDashWalk,
    FirstN(
        SortByColumns(
            ForAll(Filter(Distinct(colDash, Walker), !IsBlank(Value)) As s, { Key: s.Value, N: CountIf(colDash, Walker = s.Value) }),
            "N",
            SortOrder.Descending
        ),
        6
    )
);
Set(varDashMaxWalk, Max(colDashWalk, N));
Set(varDashSafeN, CountIf(colDash, Safety));
ClearCollect(
    colDashMod,
    FirstN(
        SortByColumns(
            ForAll(Filter(Distinct(colDash, Module), !IsBlank(Value)) As s, { Key: s.Value, N: CountIf(colDash, Module = s.Value) }),
            "N",
            SortOrder.Descending
        ),
        6
    )
);
Set(varDashMaxMod, Max(colDashMod, N));
Set(varDashNoModN, CountIf(colDash, IsBlank(Module)))'''
ONV_D = '''If(IsBlank(varDashStream), Set(varDashStream, "ALL"));
If(IsBlank(varDashPeriod), Set(varDashPeriod, "All"));
If(IsBlank(varDashMine), Set(varDashMine, false));
Set(varDashFKind, "");
Set(varDashFVal, "");
Set(varSaving, false);
Set(varDashShowDet, false);
Reset(txtSearch_Dsh);
ClearCollect(colDashPills, { Label: "All", Full: "All Streams", Key: "ALL" });
ForAll(FirstN(StreamList, 4) As s, Collect(colDashPills, { Label: s.Short, Full: s.Key, Key: s.Key }));
ClearCollect(colDashPer, { Label: "Today", Key: "Today" }, { Label: "7 Days", Key: "7" }, { Label: "30 Days", Key: "30" }, { Label: "All Time", Key: "All" });
Select(btnLoad_Dsh)'''
open(OUT + 'FW_Dashboard.pa.yaml', 'w').write(screen('Dashboard', {'Fill': 'C_Bg', 'OnVisible': ONV_D},
    [vroot('conRoot_Dsh', [hdrD, bodyD]), overlayD, hidden('btnLoad_Dsh', LOAD), hidden('btnCalc_Dsh', CALC), hidden('btnVote_Dsh', VOTE_D)]))
print('built App_Formulas.txt, FW_Home, FW_Capture, FW_Dashboard ->', os.path.normpath(OUT))
