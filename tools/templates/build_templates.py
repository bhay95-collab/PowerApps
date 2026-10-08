# Builds the starter screens in templates/ from the same proven helpers as the DTV app.
#   cd tools/templates && python3 build_templates.py
# Then: python3 ../preview/validate.py ../../templates/<file>
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dtv_generator'))
from dtvgen import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'templates') + os.sep
W = f"PageW - {r(40)}"
LINE = "RGBA(14, 42, 70, 0.22)"
GREEN = "RGBA(30, 122, 80, 1)"; RED = "RGBA(176, 52, 40, 1)"
PADX = r(18); IW = f"Parent.Width - {r(36)}"
NOSBOXR = {k: v for k, v in SBOX.items() if not k.startswith('Radius')}

def pillbtn(name, text, onsel, color, size=15, radius=24):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': color, 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'OnSelect': onsel, 'Size': r(F(size)), 'Text': text, 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(radius)), **NOSBOXR))

# ================================================================== HOME TEMPLATE
hello = 'With({ n: User().FullName }, If("," in n, Trim(Last(Split(n, ",")).Value), First(Split(n, " ")).Value))'
hdrH = inflow('conHdr_Hom', r(165), w='App.Width', fill=HDR_FILL, radius='0', children=[
    N('imgHdr_Hom', 'Image@2.2.3', props={'Height': 'Parent.Height', 'Image': 'HeaderImage', 'ImagePosition': 'ImagePosition.Fill', 'Width': 'Parent.Width'}),
    lbl('lblKicker_Hom', '"STARS PHYSIOTHERAPY"', x=f"Gutter + {r(25)}", y=r(33), w=f"PageW - {r(50)}", h=r(23), size=14, color='RGBA(255, 255, 255, 0.8)', bold=True),
    lbl('lblTitle_Hom', '"App Title"', x=f"Gutter + {r(25)}", y=r(45), w=f"PageW - {r(50)}", h=r(70), size=36, color='C_White', bold=True),
    lbl('lblHello_Hom', f'"Hi " & {hello} & "  ·  " & Text(Today(), "dddd d mmmm")', x=f"Gutter + {r(25)}", y=r(110), w=f"PageW - {r(50)}", h=r(28), size=16, color='RGBA(255, 255, 255, 0.9)'),
])
hero = inflow('conHero_Hom', r(120), fill='C_Accent', radius=r(25), children=[
    box('conHeroIc_Hom', x=r(20), y=r(32), w=r(56), h=r(56), fill='RGBA(255, 255, 255, 0.16)', radius=r(28), children=[ico('icoHero_Hom', 'CheckmarkCircle', r(11), r(11), 34, 'C_White', True)]),
    lbl('lblHeroT_Hom', '"Main Action"', x=r(92), y=r(32), w=f"Parent.Width - {r(108)}", h=r(32), size=24, color='C_White', bold=True),
    lbl('lblHeroS_Hom', '"One line saying what it does"', x=r(92), y=r(66), w=f"Parent.Width - {r(108)}", h=r(22), size=15, color='RGBA(255, 255, 255, 0.85)'),
    tbtn('btnHero_Hom', 'Navigate(TemplateList, ScreenTransition.Cover)'),
])
pct = 'Coalesce(varPct_Hom, 0)'
progress = inflow('conProg_Hom', r(112), fill='C_White', border='C_Line', radius=r(20), children=[
    lbl('lblProgCap_Hom', '"PROGRESS"', x=r(20), y=r(12), w=f"Parent.Width - {r(40)}", h=r(18), size=13, color='C_Muted', bold=True),
    lbl('lblProgT_Hom', '"Card Title"', x=r(20), y=r(32), w=f"Parent.Width - {r(40)}", h=r(28), size=19, color='C_Ink', bold=True),
    lbl('lblProgS_Hom', 'varDone_Hom & " of " & varTotal_Hom & " done"', x=r(20), y=r(62), w=f"Parent.Width - {r(40)}", h=r(20), size=14, color='C_Ink2'),
    box('conBarBg_Hom', x=r(20), y=r(88), w=f"Parent.Width - {r(40)}", h=r(8), fill='C_Line', radius=r(4), children=[
        box('conBarFg_Hom', w=f'Parent.Width * {pct}', h='Parent.Height', fill=f'If({pct} >= 1, {GREEN}, C_Accent)', radius=r(4))]),
])
capH = lbl('capOther_Hom', '"OTHER OPTIONS"', w=W, h=r(23), size=14, color='C_Muted', bold=True, extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(23)})
def tile(k, icon, title, subtitle, onsel, amber=False):
    return inflow(f'conTile{k}_Hom', r(90), fill='C_White', border='C_Line', radius=r(20), children=[
        box(f'conTileIc{k}_Hom', x=r(18), y=r(18), w=r(55), h=r(55), fill='C_AmberBg' if amber else 'C_AccentSoft', radius=r(28), children=[ico(f'icoTile{k}_Hom', icon, r(13), r(13), 30, 'C_Amber' if amber else 'C_Accent', True)]),
        lbl(f'lblTileT{k}_Hom', f'"{title}"', x=r(88), y=r(18), w=f"Parent.Width - {r(130)}", h=r(26), size=19, color='C_Ink', bold=True),
        lbl(f'lblTileS{k}_Hom', f'"{subtitle}"', x=r(88), y=r(46), w=f"Parent.Width - {r(130)}", h=r(22), size=15, color='C_Muted'),
        ico(f'icoTileGo{k}_Hom', 'ChevronRight', f"Parent.Width - {r(38)}", r(33), 24, 'C_Muted'),
        tbtn(f'btnTile{k}_Hom', onsel),
    ])
t1 = tile('1', 'AppsList', 'List Screen', 'Search, filter pills, rows', 'Navigate(TemplateList, ScreenTransition.Cover)')
t2 = tile('2', 'Edit', 'Form Screen', 'Questions and sticky submit', 'Navigate(TemplateForm, ScreenTransition.Cover)', amber=True)
endH = inflow('conEnd_Hom', r(16), extra={'DropShadow': 'DropShadow.None'})
bodyH = vbody('conBody_Hom', [hero, progress, capH, t1, t2, endH], gap=15, top=20, bottom=30, scroll=True)
onvH = '''// demo numbers: replace with real counts (work ratios out once, never divide by a blank)
Set(varTotal_Hom, 10);
Set(varDone_Hom, 4);
Set(varPct_Hom, If(varTotal_Hom > 0, varDone_Hom / varTotal_Hom, 0))'''
open(OUT + 'Template_Home.pa.yaml', 'w').write(screen('TemplateHome', {'Fill': 'C_Bg', 'OnVisible': onvH}, [vroot('conRoot_Hom', [hdrH, bodyH])]))

# ================================================================== LIST TEMPLATE
cnt = 'CountRows(galRows_Lst.AllItems)'
search = inflow('conSearch_Lst', r(60), border=LINE, fill='C_White', radius=r(15), children=[
    ico('icoSearch_Lst', 'Search', r(16), r(18), 24, 'C_Muted'),
    N('txtSearch_Lst', 'Classic/TextInput@2.3.2', props={'BorderStyle': 'BorderStyle.None', 'Color': 'C_Ink', 'Default': '""', 'DelayOutput': 'true', 'Fill': 'RGBA(0, 0, 0, 0)', 'Font': 'AppFont', 'Height': 'Parent.Height', 'HintText': '"Search"', 'Size': r(F(16)), 'Width': f"Parent.Width - {r(54)}", 'X': r(46)}),
])
selP = 'ThisItem.Key = Coalesce(varPick_Lst, "ALL")'
pillRow = N('galPills_Lst', 'Gallery@2.15.0', 'Horizontal', {
    'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'Height': r(52), 'Items': 'colPills_Lst', 'LayoutMinHeight': r(52), 'ShowScrollbar': 'false', 'TemplatePadding': '0',
    'TemplateSize': f'({W}) / Max(1, CountRows(colPills_Lst))', 'Width': W}, [
    box('conPill_Lst', x='3', y=r(2), w=f'Parent.TemplateWidth - {r(6)}', h=r(48), fill=f'If({selP}, C_Accent, C_White)', border=f'If({selP}, C_Accent, C_Line)', radius=r(24), children=[
        lbl('lblPill_Lst', 'ThisItem.Label', x=r(4), w=f'Parent.Width - {r(8)}', h=r(48), size=14, color=f'If({selP}, C_White, C_Ink2)', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn('btnPill_Lst', 'Set(varPick_Lst, ThisItem.Key)'),
    ])])
countL = lbl('lblCount_Lst', f'{cnt} & If({cnt} = 1, " item", " items")', w=W, h=r(22), size=14, color='C_Muted', bold=True, extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(22)})
emptyL = lbl('lblEmpty_Lst', 'If(!IsBlank(Trim(txtSearch_Lst.Text)), "Nothing matches your search", "Nothing to show")', w=W, h=r(50), size=15, color='C_Muted', align='Align.Center', visible=f'{cnt} = 0', extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(50)})
itemsL = '''SortByColumns(
    Filter(
        colRows_Lst,
        (Coalesce(varPick_Lst, "ALL") = "ALL" || Group = varPick_Lst)
        && (
            IsBlank(Trim(txtSearch_Lst.Text))
            || Lower(Trim(txtSearch_Lst.Text)) in Lower(Title)
            || Lower(Trim(txtSearch_Lst.Text)) in Lower(Detail)
        )
    ),
    "Title",
    SortOrder.Ascending
)'''
row = box('conRow_Lst', x='1', y=r(5), w=f"Parent.TemplateWidth - {r(10)}", h=r(84), fill='C_White', border='C_Line', radius=r(18), children=[
    box('conBar_Lst', w=r(8), h='Parent.Height', fill=f'If(ThisItem.NeedsAction, {RED}, {GREEN})', extra={'RadiusTopLeft': r(18), 'RadiusBottomLeft': r(18), 'RadiusTopRight': '0', 'RadiusBottomRight': '0'}),
    lbl('lblRowT_Lst', 'ThisItem.Title', x=r(22), y=r(10), w=f"Parent.Width - {r(62)}", h=r(24), size=17, color='C_Ink', bold=True),
    lbl('lblRowS_Lst', 'ThisItem.Detail & "  ·  " & ThisItem.Group', x=r(22), y=r(35), w=f"Parent.Width - {r(62)}", h=r(20), size=14, color='C_Ink2'),
    lbl('lblRowM_Lst', 'If(ThisItem.NeedsAction, "Needs action", "All clear")', x=r(22), y=r(56), w=f"Parent.Width - {r(62)}", h=r(20), size=13, color=f'If(ThisItem.NeedsAction, {RED}, {GREEN})', bold=True),
    ico('icoGo_Lst', 'ChevronRight', f"Parent.Width - {r(36)}", r(30), 24, 'C_Muted'),
    tbtn('btnRow_Lst', 'Set(varRow, ThisItem);\nNavigate(TemplateForm, ScreenTransition.Cover)'),
])
gal = N('galRows_Lst', 'Gallery@2.15.0', 'Vertical', {'AlignInContainer': 'AlignInContainer.SetByContainer', 'Items': itemsL, 'LayoutMinHeight': r(150), 'TemplatePadding': '0', 'TemplateSize': r(94), 'Width': W}, [row])
bodyL = vbody('conBody_Lst', [search, pillRow, countL, emptyL, gal], gap=12, top=15, bottom=10)
hdrL = header('Lst', '"List Title"', '"Subtitle or step"', 'Navigate(TemplateHome, ScreenTransition.UnCoverRight)')
onvL = '''// demo rows: replace with ClearCollect(colRows_Lst, <your list / filter>)
ClearCollect(
    colRows_Lst,
    { Title: "First item", Detail: "Location", Group: "Alpha", NeedsAction: true },
    { Title: "Second item", Detail: "Location", Group: "Beta", NeedsAction: false },
    { Title: "Third item", Detail: "Location", Group: "Alpha", NeedsAction: false }
);
// pills: one per group + All (labels kept short so they fit one row)
ClearCollect(colPills_Lst, ForAll(Distinct(colRows_Lst, Group) As g, { Label: g.Value, Key: g.Value }));
Collect(colPills_Lst, { Label: "All", Key: "ALL" });
Set(varPick_Lst, "ALL");
Reset(txtSearch_Lst)'''
open(OUT + 'Template_List.pa.yaml', 'w').write(screen('TemplateList', {'Fill': 'C_Bg', 'OnVisible': onvL}, [vroot('conRoot_Lst', [hdrL, bodyL])]))

# ================================================================== FORM TEMPLATE
def yn(sfx, var, y):
    hw = f"Round((Parent.Width - {r(36)} - {r(12)}) / 2, 0)"
    def half(nm, val, col, x):
        return box(f'con{nm}_{sfx}', x=x, y=y, w=hw, h=r(48), fill=f'If({var} = "{val}", {col}, C_White)', border=f'If({var} = "{val}", {col}, C_Line)', radius=r(24), children=[
            pillbtn(f'btn{nm}_{sfx}', f'"{val}"', f'Set({var}, "{val}")', f'If({var} = "{val}", C_White, C_Muted)')])
    return [half('Yes', 'Yes', GREEN, PADX), half('No', 'No', RED, f"{PADX} + {hw} + {r(12)}")]
def choice(sfx, k, var, val, y, vis=None):
    sel = f'{var} = "{val}"'
    return box(f'conR{k}_{sfx}', x=PADX, y=y, w=IW, h=r(44), fill=f'If({sel}, C_AccentSoft, C_White)', border=f'If({sel}, C_Accent, C_Line)', radius=r(22), visible=vis, children=[
        pillbtn(f'btnR{k}_{sfx}', f'"{val}"', f'Set({var}, "{val}")', f'If({sel}, C_Accent, C_Muted)', size=14, radius=22)])
def chip(sfx, k, col, val, y):
    sel = f'"{val}" in {col}.Value'
    return box(f'conC{k}_{sfx}', x=PADX, y=y, w=IW, h=r(44), fill=f'If({sel}, C_AccentSoft, C_White)', border=f'If({sel}, C_Accent, C_Line)', radius=r(22), children=[
        pillbtn(f'btnC{k}_{sfx}', f'If({sel}, "✓  ", "") & "{val}"', f'If({sel}, Remove({col}, LookUp({col}, Value = "{val}")), Collect({col}, {{ Value: "{val}" }}))', f'If({sel}, C_Accent, C_Muted)', size=14, radius=22)])
def tin(name, hint, y, h, vis=None):
    p = {'BorderColor': 'C_Line', 'BorderThickness': '1', 'Color': 'C_Ink', 'Default': '""', 'FocusedBorderColor': 'C_Accent', 'FocusedBorderThickness': '2', 'Font': 'AppFont', 'Height': r(h), 'HintText': f'"{hint}"', 'Mode': 'TextMode.MultiLine', 'Size': r(F(15)), 'Width': IW, 'X': PADX, 'Y': y}
    p.update(rad(r(12)))
    if vis: p['Visible'] = vis
    return N(name, 'Classic/TextInput@2.3.2', props=p)
def head(cap, q, sfx):
    return [lbl(f'cap_{sfx}', f'"{cap}"', x=PADX, y=r(14), w=IW, h=r(22), size=14, color='C_Muted', bold=True),
            lbl(f'q_{sfx}', f'"{q}"', x=PADX, y=r(38), w=IW, h=r(28), size=16, color='C_Ink', bold=True)]
def card(name, h, children, vis=None):
    return inflow(name, f'Round(({h}) * UI, 0)', fill='C_White', border='C_Line', radius=r(20), children=children, visible=vis)

warn = inflow('conWarn_Frm', r(76), fill='C_AmberBg', border='RGBA(178, 105, 0, 0.35)', radius=r(20), visible='!IsBlank(varRow)', children=[
    lbl('lblWarnCap_Frm', '"NOTE"', x=PADX, y=r(12), w=IW, h=r(20), size=13, color='C_Amber', bold=True),
    lbl('lblWarn_Frm', '"Editing: " & varRow.Title', x=PADX, y=r(36), w=IW, h=r(28), size=16, color='C_Ink', bold=True),
])
NO = 'varQ1_Frm = "No"'
q1 = card('conQ1_Frm', f'If({NO}, 360, 140)', head('1  ·  YES / NO', 'Did it work?', 'Q1') + yn('Q1', 'varQ1_Frm', r(74)) + [
    lbl('lblWhy_Q1', '"Why not?"', x=PADX, y=r(136), w=IW, h=r(24), size=14, color='C_Muted', bold=True, visible=NO),
    choice('Q1', '1', 'varWhy_Frm', 'Reason one', r(164), NO),
    choice('Q1', '2', 'varWhy_Frm', 'Reason two', r(214), NO),
    tin('txtWhy_Q1', 'Details (optional)', r(266), 76, NO),
])
q2 = card('conQ2_Frm', '256', head('2  ·  TICK ANY', 'What was covered?', 'Q2') + [
    chip('Q2', '1', 'colTicks_Frm', 'Option A', r(74)),
    chip('Q2', '2', 'colTicks_Frm', 'Option B', r(126)),
    chip('Q2', '3', 'colTicks_Frm', 'Option C', r(178)),
])
notes = card('conNotes_Frm', '148', [
    lbl('capNotes_Frm', '"NOTES (OPTIONAL)"', x=PADX, y=r(14), w=IW, h=r(22), size=14, color='C_Muted', bold=True),
    tin('txtNotes_Frm', 'Anything else', r(40), 90)])
endF = inflow('conEnd_Frm', r(16), extra={'DropShadow': 'DropShadow.None'})
bodyF = vbody('conBody_Frm', [warn, q1, q2, notes, endF], gap=12, top=15, bottom=0, scroll=True)
READY = f'!IsBlank(varQ1_Frm) && (varQ1_Frm = "Yes" || !IsBlank(varWhy_Frm))'
ok = 'btnSubmit_Frm.DisplayMode = DisplayMode.Edit'
save = '''// replace MyList and the fields with your list's real columns
With(
    {
        rec: Patch(
            MyList,
            Defaults(MyList),
            {
                Title: Coalesce(varRow.Title, "New"),
                Worked: { Value: varQ1_Frm },
                FailReason: If(varQ1_Frm = "No", { Value: varWhy_Frm }, Blank()),
                FailNotes: If(varQ1_Frm = "No", Trim(txtWhy_Q1.Text), Blank()),
                Covered: ForAll(colTicks_Frm As e, { Value: e.Value }),
                Notes: Trim(txtNotes_Frm.Text)
            }
        )
    },
    If(
        IsEmpty(Errors(MyList)),
        Set(varSaving, false);
        Notify("Saved.", NotificationType.Success);
        Navigate(TemplateHome, ScreenTransition.UnCoverRight),
        Set(varSaving, false);
        Notify("Could not save. Check your connection and try again.", NotificationType.Error)
    )
)'''
submit = box('conSubmit_Frm', x=f"Gutter + {r(20)}", y=r(12), w=W, h=r(60), fill=f'If({ok}, C_Accent, RGBA(160, 174, 180, 1))', radius=r(28), children=[
    lbl('lblSubmit_Frm', f'If({ok}, "Submit", "Answer every question to submit")', w='Parent.Width', h=r(60), size=19, color='C_White', bold=True, align='Align.Center', extra={'Size': f'If({ok}, {r(F(19))}, {r(F(15))})', 'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnSubmit_Frm', 'Set(varSaving, true);\n' + save, display=f'If({READY} && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)'),
])
foot = inflow('conFoot_Frm', r(84), w='App.Width', fill='C_White', border='C_Line', radius='0', children=[submit])
hdrF = header('Frm', '"Form Title"', '"Step 2 of 2"', 'Navigate(TemplateList, ScreenTransition.UnCoverRight)')
onvF = '''Set(varQ1_Frm, Blank());
Set(varWhy_Frm, Blank());
Set(varSaving, false);
Reset(txtWhy_Q1);
Reset(txtNotes_Frm);
// give the collection its shape, then empty it
ClearCollect(colTicks_Frm, { Value: "" });
Clear(colTicks_Frm)'''
open(OUT + 'Template_Form.pa.yaml', 'w').write(screen('TemplateForm', {'Fill': 'C_Bg', 'OnVisible': onvF}, [vroot('conRoot_Frm', [hdrF, bodyF, foot])]))
print('wrote Template_Home, Template_List, Template_Form')
