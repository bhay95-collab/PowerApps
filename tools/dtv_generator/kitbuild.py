# DTV Audit app: Kit Audit (scan kit QR -> scan each form -> tick other items) and Kit Done screens.
#   cd tools/dtv_generator && python3 kitbuild.py   -> powerapps/dtv/DTV_KitAudit.pa.yaml, DTV_KitDone.pa.yaml
# Two routes in:  Home "Audit DTV + Kit" -> Audit -> Submit -> KitAudit (varKitMode = "DTV")
#                 Home "Audit Kit Only"                       -> KitAudit (varKitMode = "KIT")
# SharePoint lists: Kit_Register, Kit_Items, Kit_Contents (master), Kit_Audits, Kit_Audit_Items (results, exceptions only).
from dtvgen import *
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'powerapps', 'dtv') + os.sep
W = f"PageW - {r(40)}"
LINE = "RGBA(14, 42, 70, 0.22)"
GREEN = "RGBA(30, 122, 80, 1)"; RED = "RGBA(176, 52, 40, 1)"
PADX = r(18); IW = f"Parent.Width - {r(36)}"
NOSB = {k: v for k, v in SBOX.items() if not k.startswith('Radius')}
HASKIT = '!IsBlank(varKit)'
NOKIT = 'IsBlank(varKit)'
DTVMODE = 'varKitMode = "DTV"'

def pillbtn(name, text, onsel, color, size=15, radius=24):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': color, 'Font': 'AppFont', 'FontWeight': 'FontWeight.Bold', 'Height': 'Parent.Height', 'OnSelect': onsel, 'Size': r(F(size)), 'Text': text, 'VerticalAlign': 'VerticalAlign.Middle', 'Width': 'Parent.Width'}, **rad(r(radius)), **NOSB))
def yn(sfx, var, y):
    hw = f"Round((Parent.Width - {r(36)} - {r(12)}) / 2, 0)"
    def half(nm, val, col, x):
        return box(f'con{nm}_{sfx}', x=x, y=y, w=hw, h=r(48), fill=f'If({var} = "{val}", {col}, C_White)', border=f'If({var} = "{val}", {col}, C_Line)', radius=r(24), children=[
            pillbtn(f'btn{nm}_{sfx}', f'"{val}"', f'Set({var}, "{val}")', f'If({var} = "{val}", C_White, C_Muted)')])
    return [half('Yes', 'Yes', GREEN, PADX), half('No', 'No', RED, f"{PADX} + {hw} + {r(12)}")]
def cap(name, text, visible=None):
    return lbl(name, text, w=W, h=r(23), size=14, color='C_Muted', bold=True, visible=visible, extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(23)})
def scanner(name, onscan):
    return N(name, 'BarcodeReader@1.0.25', props={'BorderStyle': 'BorderStyle.None', 'FillColor': 'RGBA(0, 0, 0, 0)', 'FontSize': '1', 'Height': 'Parent.Height', 'HoverFillColor': 'RGBA(255, 255, 255, 0.08)',
        'OnScan': onscan, 'ScanningMode': "'BarcodeReader.ScanningMode'.SelectToScan", 'Text': '""', 'Width': 'Parent.Width'})
def hero(name, icon, title, sub, children, visible=None, h=110):
    return inflow(name, r(h), fill='C_Accent', radius=r(25), visible=visible, children=[
        box(f'{name}Ic', x=r(20), y=f'({r(h)} - {r(56)}) / 2', w=r(56), h=r(56), fill='RGBA(255, 255, 255, 0.16)', radius=r(28), children=[ico(f'ico{name}', icon, r(13), r(13), 30, 'C_White', True)]),
        lbl(f'lbl{name}T', title, x=r(92), y=f'({r(h)} - {r(56)}) / 2', w=f'Parent.Width - {r(108)}', h=r(32), size=24, color='C_White', bold=True),
        lbl(f'lbl{name}S', sub, x=r(92), y=f'({r(h)} - {r(56)}) / 2 + {r(34)}', w=f'Parent.Width - {r(108)}', h=r(22), size=15, color='RGBA(255, 255, 255, 0.85)')] + children)

# ------------------------------------------------------------------ step 1: identify the kit
scanKit = hero('conScanKit_Kit', 'Camera', '"Scan Kit QR Code"', '"On the label on the kit box"', [scanner('scnKit_Kit', 'Set(varKitCode, Upper(Trim(First(scnKit_Kit.Barcodes).Value)));\nSelect(btnLoadKit_Kit)')], visible=NOKIT)
typeKit = inflow('conTypeKit_Kit', r(118), fill='C_White', border='C_Line', radius=r(20), visible=NOKIT, children=[
    lbl('capTypeKit_Kit', '"OR TYPE THE KIT ID"', x=PADX, y=r(14), w=IW, h=r(22), size=14, color='C_Muted', bold=True),
    N('txtKitID_Kit', 'Classic/TextInput@2.3.2', props=dict({'BorderColor': LINE, 'BorderThickness': '1', 'Color': 'C_Ink', 'Default': '""', 'FocusedBorderColor': 'C_Accent', 'FocusedBorderThickness': '2', 'Font': 'AppFont',
        'Height': r(52), 'HintText': '"e.g. DTK-014"', 'Size': r(F(16)), 'Width': f'Parent.Width - {r(36)} - {r(110)}', 'X': PADX, 'Y': r(48)}, **rad(r(12)))),
    box('conGo_Kit', x=f'Parent.Width - {r(18)} - {r(98)}', y=r(48), w=r(98), h=r(52), fill='C_Accent', radius=r(26), children=[
        pillbtn('btnGo_Kit', '"Open"', 'Set(varKitCode, Upper(Trim(txtKitID_Kit.Text)));\nSelect(btnLoadKit_Kit)', 'C_White', radius=26)])])
noKit = inflow('conNoKit_Kit', r(90), fill='C_AmberBg', border='RGBA(178, 105, 0, 0.35)', radius=r(20), visible=f'{NOKIT} && {DTVMODE}', children=[
    lbl('lblNoKitT_Kit', '"No Kit at This DTV"', x=PADX, y=r(16), w=f'Parent.Width - {r(80)}', h=r(28), size=19, color='C_Amber', bold=True),
    lbl('lblNoKitS_Kit', '"Records the kit as not found"', x=PADX, y=r(48), w=f'Parent.Width - {r(80)}', h=r(22), size=15, color='C_Amber'),
    ico('icoNoKit_Kit', 'ChevronRight', f'Parent.Width - {r(40)}', r(33), 24, 'C_Amber'),
    tbtn('btnNoKit_Kit', 'If(varKitNoKitAsk, Select(btnSaveNoKit_Kit), Set(varKitNoKitAsk, true); Notify("Tap again to confirm there is no kit here.", NotificationType.Warning))', display='If(varSaving, DisplayMode.Disabled, DisplayMode.Edit)')])

# ------------------------------------------------------------------ step 2: kit card + questions
kitInfo = inflow('conKitInfo_Kit', r(150), fill='C_White', border='C_Line', radius=r(20), visible=HASKIT, children=[
    lbl('capKitInfo_Kit', '"KIT  ·  " & varKit.Title', x=PADX, y=r(14), w=f'Parent.Width - {r(140)}', h=r(22), size=14, color='C_Muted', bold=True),
    lbl('lblChange_Kit', '"Change Kit"', x=f'Parent.Width - {r(130)}', y=r(10), w=r(112), h=r(30), size=14, color='C_Accent', bold=True, align='Align.Right'),
    tbtn('btnChange_Kit', 'Set(varKit, Blank());\nClear(colKitExp);\nClear(colKitExtra);\nReset(txtKitID_Kit)', x=f'Parent.Width - {r(140)}', y=r(4), w=r(136), h=r(40)),
    lbl('lblKitUnit_Kit', 'varKit.Unit', x=PADX, y=r(38), w=IW, h=r(30), size=19, color='C_Ink', bold=True),
    lbl('lblKitLoc_Kit', 'varKit.Location', x=PADX, y=r(68), w=IW, h=r(22), size=15, color='C_Ink2'),
    lbl('lblKitType_Kit', 'varKit.KitType', x=PADX, y=r(92), w=IW, h=r(22), size=14, color='C_Accent', bold=True),
    lbl('lblKitDTV_Kit', '"Auditing with DTV: " & varDTV.Department & " · " & varDTV.DTVLocation', x=PADX, y=r(116), w=IW, h=r(22), size=14, color='C_Muted', visible=DTVMODE)])
QS = [('Loc', 'varKitLoc', '1  ·  LOCATION', 'Is the kit at the location above?'),
      ('Seal', 'varKitSeal', '2  ·  SEAL', 'Was the tamper seal intact?'),
      ('Staff', 'varKitStaff', '3  ·  STAFF', 'Did staff know where the kit is kept?')]
qkids = []
for i, (k, v, c, q) in enumerate(QS):
    y0 = 14 + i * 124
    qkids += [lbl(f'capQ{k}_Kit', f'"{c}"', x=PADX, y=r(y0), w=IW, h=r(22), size=14, color='C_Muted', bold=True),
              lbl(f'lblQ{k}_Kit', f'"{q}"', x=PADX, y=r(y0 + 24), w=IW, h=r(28), size=16, color='C_Ink', bold=True)] + yn(f'Q{k}', v, r(y0 + 60))
qs = inflow('conQs_Kit', r(14 + 3 * 124), fill='C_White', border='C_Line', radius=r(20), visible=HASKIT, children=qkids)

# ------------------------------------------------------------------ step 3: scan forms
NSCAN = 'CountRows(Filter(colKitExp, Scan))'
NDONE = 'CountRows(Filter(colKitExp, Scan && Present))'
SCANFORM = '''With(
    { code: Upper(Trim(First(scnForm_Kit.Barcodes).Value)) },
    With(
        { hit: LookUp(colKitExp, Scan && Barcode = code) },
        If(
            IsBlank(code),
            Notify("Nothing was read. Try again.", NotificationType.Warning),
            !IsBlank(hit) && hit.Present,
            Notify("Already scanned: " & hit.Name, NotificationType.Information),
            !IsBlank(hit),
            Patch(colKitExp, hit, { Present: true });
            Notify("✓  " & hit.Name, NotificationType.Success),
            !IsBlank(LookUp(colKitExtra, Value = code)),
            Notify("Already noted as not on this kit's list", NotificationType.Information),
            With(
                { known: LookUp(colKitItems, Upper(BarcodeValue) = code) },
                Collect(colKitExtra, { Value: code, Name: Coalesce(known.ItemName, "Unknown barcode") });
                Notify(If(IsBlank(known), "Unknown barcode " & code, known.ItemName & " is not on this kit's list"), NotificationType.Warning)
            )
        )
    )
)'''
pct = f'If({NSCAN} > 0, {NDONE} / {NSCAN}, 0)'
scanForm = hero('conScanForm_Kit', 'Camera', '"Scan Each Form"', f'{NDONE} & " of " & {NSCAN} & " forms scanned"', [
    box('conFormBar_Kit', x=r(92), y=r(96), w=f'Parent.Width - {r(112)}', h=r(8), fill='RGBA(255, 255, 255, 0.25)', radius=r(4), children=[
        box('conFormBarFg_Kit', w=f'Parent.Width * {pct}', h='Parent.Height', fill='C_White', radius=r(4))]),
    scanner('scnForm_Kit', SCANFORM)], visible=HASKIT, h=120)
RH = 70
toScanItems = 'Filter(colKitExp, Scan)'
leftItems = 'Filter(colKitExp, Scan && !Present)'
toScanRow = box('conTsRow_Kit', x='0', y='0', w='Parent.TemplateWidth', h='Parent.TemplateHeight', children=[
    box('conTs_Kit', x='1', y=r(4), w=f'Parent.Width - {r(2)}', h=r(RH - 8), fill='If(ThisItem.Present, C_GoodBg, RGBA(176, 52, 40, 0.07))', border=f'If(ThisItem.Present, {GREEN}, RGBA(176, 52, 40, 0.45))', radius=r(16), children=[
        box('conTsDot_Kit', x=r(14), y=f'(Parent.Height - {r(28)}) / 2', w=r(28), h=r(28), fill=f'If(ThisItem.Present, {GREEN}, {RED})', radius=r(14), children=[
            lbl('lblTsDot_Kit', 'If(ThisItem.Present, "✓", "!")', w='Parent.Width', h='Parent.Height', size=14, color='C_White', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})]),
        lbl('lblTsName_Kit', 'ThisItem.Name', x=r(54), y=r(8), w=f'Parent.Width - {r(66)}', h=r(24), size=15, color='C_Ink', bold=True),
        lbl('lblTsSub_Kit', 'If(ThisItem.Present, "Scanned", "Not scanned yet") & "  ·  " & ThisItem.Barcode & "  ·  " & ThisItem.Sections', x=r(54), y=r(32), w=f'Parent.Width - {r(66)}', h=r(22), size=13,
            color=f'If(ThisItem.Present, {GREEN}, {RED})', bold=True)])])
galToScan = N('galToScan_Kit', 'Gallery@2.15.0', 'Vertical', {'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'Height': f'Max(1, CountRows({toScanItems})) * {r(RH)}',
    'Items': toScanItems, 'LayoutMinHeight': f'Max(1, CountRows({toScanItems})) * {r(RH)}', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(RH), 'Visible': f'{HASKIT} && !IsEmpty({toScanItems})', 'Width': W}, [toScanRow])
allScanned = inflow('conAllScanned_Kit', r(56), fill='C_GoodBg', border='RGBA(30, 122, 80, 0.35)', radius=r(16), visible=f'{HASKIT} && !IsEmpty({toScanItems}) && IsEmpty({leftItems})', children=[
    lbl('lblAllScanned_Kit', '"✓  All forms on the list scanned"', x=r(16), w=f'Parent.Width - {r(32)}', h=r(56), size=15, color=GREEN, bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'})])

# extras
EH = 64
exRow = box('conExRow_Kit', x='0', y='0', w='Parent.TemplateWidth', h='Parent.TemplateHeight', children=[
    lbl('lblExName_Kit', 'ThisItem.Name', x=r(16), y=r(8), w=f'Parent.Width - {r(80)}', h=r(24), size=15, color='C_Ink', bold=True),
    lbl('lblExCode_Kit', 'ThisItem.Value', x=r(16), y=r(32), w=f'Parent.Width - {r(80)}', h=r(22), size=13, color='C_Amber'),
    N('btnExDel_Kit', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'Appearance': 'ButtonAppearance.Transparent', 'Color': 'C_Muted', 'FontWeight': '""', 'Height': r(48), 'Icon': '"DismissCircle"',
        'OnSelect': 'Remove(colKitExtra, ThisItem)', 'Size': r(20), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Width': r(48), 'X': f'Parent.Width - {r(56)}', 'Y': r(8)}, **SBOX))])
extras = inflow('conExtras_Kit', f'{r(56)} + Max(1, CountRows(colKitExtra)) * {r(EH)}', fill='C_AmberBg', border='RGBA(178, 105, 0, 0.35)', radius=r(20), visible=f'{HASKIT} && !IsEmpty(colKitExtra)', children=[
    lbl('capExtras_Kit', '"NOT ON THIS KIT\'S LIST  ·  " & CountRows(colKitExtra)', x=PADX, y=r(16), w=IW, h=r(24), size=14, color='C_Amber', bold=True),
    N('galExtras_Kit', 'Gallery@2.15.0', 'Vertical', {'Height': f'Max(1, CountRows(colKitExtra)) * {r(EH)}', 'Items': 'colKitExtra', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(EH),
        'Width': 'Parent.Width', 'X': '0', 'Y': r(48)}, [exRow])])

# ------------------------------------------------------------------ step 4: tick everything without a barcode
tickItems = 'Filter(colKitExp, !Scan)'
TH = 64
tRow = box('conTkRow_Kit', x='0', y='0', w='Parent.TemplateWidth', h='Parent.TemplateHeight', children=[
    box('conTk_Kit', x='1', y=r(4), w=f'Parent.Width - {r(2)}', h=r(TH - 8), fill='If(ThisItem.Present, C_GoodBg, RGBA(176, 52, 40, 0.07))', border=f'If(ThisItem.Present, {GREEN}, RGBA(176, 52, 40, 0.45))', radius=r(16), children=[
        box('conTkDot_Kit', x=r(14), y=f'(Parent.Height - {r(26)}) / 2', w=r(26), h=r(26), fill=f'If(ThisItem.Present, {GREEN}, C_White)', border=f'If(ThisItem.Present, {GREEN}, {RED})', radius=r(13), children=[
            lbl('lblTkDot_Kit', 'If(ThisItem.Present, "✓", "")', w='Parent.Width', h='Parent.Height', size=13, color='C_White', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})]),
        lbl('lblTkName_Kit', 'ThisItem.Name', x=r(52), y=r(6), w=f'Parent.Width - {r(64)}', h=r(24), size=14, color='C_Ink', bold=True),
        lbl('lblTkSub_Kit', 'If(ThisItem.Present, "Present", "Tap if present") & "  ·  " & ThisItem.Sections', x=r(52), y=r(30), w=f'Parent.Width - {r(64)}', h=r(20), size=13, color=f'If(ThisItem.Present, {GREEN}, {RED})'),
        tbtn('btnTk_Kit', 'Patch(colKitExp, ThisItem, { Present: !ThisItem.Present })')])])
galTick = N('galTick_Kit', 'Gallery@2.15.0', 'Vertical', {'AlignInContainer': 'AlignInContainer.SetByContainer', 'FillPortions': '0', 'Height': f'Max(1, CountRows({tickItems})) * {r(TH)}',
    'Items': tickItems, 'LayoutMinHeight': f'Max(1, CountRows({tickItems})) * {r(TH)}', 'ShowScrollbar': 'false', 'TemplatePadding': '0', 'TemplateSize': r(TH), 'Visible': f'{HASKIT} && !IsEmpty({tickItems})', 'Width': W}, [tRow])

# ------------------------------------------------------------------ step 5: photo + notes
TR = "RGBA(0, 0, 0, 0)"
nophoto = 'IsBlank(addPhoto_Kit.Media)'
def tin(name, hint, y, h):
    p = {'BorderColor': 'C_Line', 'BorderThickness': '1', 'Color': 'C_Ink', 'Default': '""', 'FocusedBorderColor': 'C_Accent', 'FocusedBorderThickness': '2', 'Font': 'AppFont', 'Height': r(h), 'HintText': f'"{hint}"',
         'Mode': 'TextMode.MultiLine', 'Size': r(F(15)), 'Width': IW, 'X': PADX, 'Y': y}
    p.update(rad(r(12))); return N(name, 'Classic/TextInput@2.3.2', props=p)
photo = inflow('conPhoto_Kit', f'Round(If({nophoto}, 268, 390) * UI, 0)', fill='C_White', border='C_Line', radius=r(20), visible=HASKIT, children=[
    lbl('capPhoto_Kit', '"PHOTO AND NOTES (OPTIONAL)"', x=PADX, y=r(14), w=IW, h=r(22), size=14, color='C_Muted', bold=True),
    box('conAddPhoto_Kit', x=PADX, y=r(44), w=IW, h=r(48), fill='C_White', border='C_Accent', radius=r(24), children=[
        lbl('lblAddPhoto_Kit', f'If({nophoto}, "Add Photo", "Change Photo")', w='Parent.Width', h=r(48), size=15, color='C_Accent', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'})]),
    N('addPhoto_Kit', 'AddMedia@2.2.1', props={'BorderColor': TR, 'BorderStyle': 'BorderStyle.None', 'BorderThickness': '0', 'Color': TR, 'DisabledColor': TR, 'DisabledFill': TR, 'Fill': TR, 'Font': "Font.'Segoe UI'", 'Height': r(48),
        'HoverBorderColor': TR, 'HoverColor': TR, 'HoverFill': TR, 'PressedBorderColor': TR, 'PressedColor': TR, 'PressedFill': TR, 'Size': r(F(15)), 'Width': IW, 'X': PADX, 'Y': r(44)}),
    N('imgPhoto_Kit', 'Image@2.2.3', props={'Height': r(110), 'Image': 'addPhoto_Kit.Media', 'ImagePosition': 'ImagePosition.Fit', 'Visible': f'!{nophoto}', 'Width': r(110), 'X': PADX, 'Y': r(104)}),
    lbl('lblRemovePhoto_Kit', '"Remove Photo"', x=f'{PADX} + {r(126)}', y=r(146), w=f'Parent.Width - {r(36)} - {r(126)}', h=r(26), size=15, color=RED, bold=True, visible=f'!{nophoto}'),
    tbtn('btnRemovePhoto_Kit', 'Reset(addPhoto_Kit)', x=f'{PADX} + {r(116)}', y=r(136), w=f'Parent.Width - {r(36)} - {r(116)}', h=r(46)),
    tin('txtNotes_Kit', 'Anything else about this kit (optional)', f'Round(If({nophoto}, 104, 226) * UI, 0)', 140)])
end = inflow('conEnd_Kit', r(16), extra={'DropShadow': 'DropShadow.None'})
body = vbody('conBody_Kit', [scanKit, typeKit, noKit, kitInfo, qs, scanForm,
                             cap('capToScan_Kit', '"FORMS  ·  " & ' + NDONE + ' & " OF " & ' + NSCAN + ' & " SCANNED"', visible=f'{HASKIT} && !IsEmpty({toScanItems})'), galToScan, allScanned, extras,
                             cap('capTick_Kit', '"OTHER ITEMS  ·  TAP IF IN THE BOX"', visible=f'{HASKIT} && !IsEmpty({tickItems})'), galTick,
                             photo, end], gap=12, top=15, bottom=0, scroll=True)

# ------------------------------------------------------------------ save
READY = '!IsBlank(varKit) && !IsBlank(varKitLoc) && !IsBlank(varKitSeal) && !IsBlank(varKitStaff)'
ok = 'btnSubmit_Kit.DisplayMode = DisplayMode.Edit'
NMISS = 'CountRows(Filter(colKitExp, !Present))'
SAVE = '''Set(varSaving, true);
With(
    {
        miss: Filter(colKitExp, !Present),
        nMiss: CountRows(Filter(colKitExp, !Present)),
        nExtra: CountRows(colKitExtra)
    },
    With(
        {
            clear: nMiss + nExtra = 0 && varKitLoc = "Yes" && varKitSeal = "Yes" && varKitStaff = "Yes",
            rec: Patch(
                Kit_Audits,
                Defaults(Kit_Audits),
                {
                    Title: varKit.Title,
                    Unit: varKit.Unit,
                    KitLocation: varKit.Location,
                    KitType: varKit.KitType,
                    AuditType: If(varKitMode = "DTV", "DTV + Kit", "Kit Only"),
                    DTVTitle: If(varKitMode = "DTV", varDTV.Title, ""),
                    AuditResultID: If(varKitMode = "DTV", varLastAudit.ID, Blank()),
                    RightLocation: varKitLoc,
                    SealIntact: varKitSeal,
                    StaffAware: varKitStaff,
                    ExpectedN: CountRows(colKitExp),
                    MissingN: nMiss,
                    ExtraN: nExtra,
                    MissingItems: Concat(miss, Name, "; "),
                    ExtraItems: Concat(colKitExtra, Name & " (" & Value & ")", "; "),
                    Notes: Trim(txtNotes_Kit.Text)
                }
            )
        },
        If(
            IsEmpty(Errors(Kit_Audits)),
            Patch(Kit_Audits, rec, { Result: If(clear, "All Clear", "Needs Follow-up") });
            // exceptions only: one row per missing item and per extra barcode
            ForAll(
                miss As m,
                Patch(Kit_Audit_Items, Defaults(Kit_Audit_Items), { Title: varKit.Title, KitAuditID: rec.ID, ItemKey: m.ItemKey, ItemName: m.Name, Status: "Missing", ScannedValue: "" })
            );
            ForAll(
                colKitExtra As x,
                Patch(Kit_Audit_Items, Defaults(Kit_Audit_Items), { Title: varKit.Title, KitAuditID: rec.ID, ItemKey: "", ItemName: x.Name, Status: "Extra", ScannedValue: x.Value })
            );
            If(!IsBlank(addPhoto_Kit.Media), Patch(Kit_Audits, rec, { KitPhoto: imgPhoto_Kit.Image }));
            // DTV + Kit: write the kit result onto the DTV audit so the Dashboard keeps working
            If(
                varKitMode = "DTV" && !IsBlank(varLastAudit),
                Set(
                    varLastAudit,
                    Patch(
                        Audit_Results,
                        LookUp(Audit_Results, ID = varLastAudit.ID),
                        {
                            FolderFound: { Value: "Yes" },
                            ContentsListInFolder: { Value: "Yes" },
                            KitMatched: { Value: If(nMiss + nExtra = 0, "Yes", "No") },
                            MissingItems: Concat(miss, Name, "; "),
                            ExtraItems: Concat(colKitExtra, Name & " (" & Value & ")", "; ")
                        }
                    )
                )
            );
            If(
                !IsEmpty(Errors(Kit_Audit_Items)),
                Notify("Kit audit saved, but some item rows could not be saved.", NotificationType.Warning)
            );
            Set(varKitLast, { KitID: varKit.Title, Unit: varKit.Unit, Missing: nMiss, Extra: nExtra, Clear: clear });
            Set(varSaving, false);
            If(varKitMode = "DTV", Navigate(Done, ScreenTransition.Cover), Navigate(KitDone, ScreenTransition.Cover)),
            Set(varSaving, false);
            Notify("Could not save the kit audit. Check your connection and try again.", NotificationType.Error)
        )
    )
)'''
NOKIT_SAVE = '''Set(varSaving, true);
Set(varKitNoKitAsk, false);
Patch(
    Kit_Audits,
    Defaults(Kit_Audits),
    {
        Title: "NO KIT",
        AuditType: "DTV + Kit",
        DTVTitle: varDTV.Title,
        AuditResultID: varLastAudit.ID,
        Result: "Kit not found",
        Notes: "No kit found at this DTV"
    }
);
If(
    !IsBlank(varLastAudit),
    Set(varLastAudit, Patch(Audit_Results, LookUp(Audit_Results, ID = varLastAudit.ID), { FolderFound: { Value: "No" } }))
);
Set(varSaving, false);
Navigate(Done, ScreenTransition.Cover)'''
LOADKIT = '''If(IsEmpty(colKitItems), ClearCollect(colKitItems, Kit_Items));
Set(varKit, LookUp(Kit_Register, Title = varKitCode));
If(
    IsBlank(varKit),
    Notify("Kit " & varKitCode & " is not in the kit register. Check the label or type the kit ID.", NotificationType.Error),
    ClearCollect(
        colKitExp,
        ForAll(
            Filter(Kit_Contents, Title = varKit.Title) As c,
            With(
                { i: LookUp(colKitItems, Title = c.ItemKey) },
                {
                    ItemKey: c.ItemKey,
                    Name: Coalesce(i.ItemName, c.ItemKey),
                    Barcode: Upper(Coalesce(i.BarcodeValue, "")),
                    Scan: i.ScanMethod = "Scan barcode" && !IsBlank(i.BarcodeValue),
                    Present: false,
                    Sections: c.Sections
                }
            )
        )
    );
    Clear(colKitExtra);
    Set(varKitLoc, Blank());
    Set(varKitSeal, Blank());
    Set(varKitStaff, Blank())
)'''
def hidden(name, onselect):
    return N(name, 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'FontWeight': '""', 'Height': '1', 'OnSelect': onselect, 'Size': r(11), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Visible': 'false', 'Width': '1'}, **SBOX))
submit = box('conSubmit_Kit', x=f"Gutter + {r(20)}", y=r(12), w=W, h=r(60), fill=f'If({ok}, C_Accent, RGBA(160, 174, 180, 1))', radius=r(28), children=[
    lbl('lblSubmit_Kit', f'If({ok}, "Complete Kit" & If({NMISS} + CountRows(colKitExtra) > 0, "  ·  " & {NMISS} & " missing, " & CountRows(colKitExtra) & " extra", ""), If(IsBlank(varKit), "Scan the kit first", "Answer questions 1 to 3 to submit"))',
        w='Parent.Width', h=r(60), size=17, color='C_White', bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    tbtn('btnSubmit_Kit', SAVE, display=f'If({READY} && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)')])
foot = inflow('conFoot_Kit', r(84), w='App.Width', fill='C_White', border='C_Line', radius='0', children=[submit])
hdr = header('Kit', 'If(varKitMode = "DTV", "Kit Audit", "Kit Only Audit")', 'If(varKitMode = "DTV", "Step 2 of 2  ·  " & varDTV.Department, If(IsBlank(varKit), "Scan the kit to start", varKit.Title))',
             'If(varKitMode = "DTV", Notify("The DTV audit is saved. Finish the kit, or tap No Kit at This DTV.", NotificationType.Information), Navigate(Home, ScreenTransition.UnCoverRight))')
ONV = '''Set(varSaving, false);
Set(varKitNoKitAsk, false);
Set(varKit, Blank());
Set(varKitLoc, Blank());
Set(varKitSeal, Blank());
Set(varKitStaff, Blank());
Clear(colKitExp);
Clear(colKitExtra);
Reset(txtKitID_Kit);
Reset(txtNotes_Kit);
Reset(addPhoto_Kit);
// the item catalogue (81 rows) is loaded once
If(IsEmpty(colKitItems), ClearCollect(colKitItems, Kit_Items))'''
open(OUT + 'DTV_KitAudit.pa.yaml', 'w').write(screen('KitAudit', {'Fill': 'C_Bg', 'OnVisible': ONV},
    [vroot('conRoot_Kit', [hdr, body, foot]), hidden('btnLoadKit_Kit', LOADKIT), hidden('btnSaveNoKit_Kit', NOKIT_SAVE)]))

# ------------------------------------------------------------------ KIT DONE (kit only audits)
res = 'If(varKitLast.Clear, "All clear", varKitLast.Missing & " missing  ·  " & varKitLast.Extra & " not on the list")'
okc = inflow('conOk_Kd', r(150), fill='C_White', border='C_Line', radius=r(20), children=[
    box('conOkIc_Kd', x=r(25), y=r(20), w=r(70), h=r(70), fill='C_AccentSoft', radius=r(35), children=[ico('icoOk_Kd', 'CheckmarkCircle', r(12), r(12), 45, 'C_Accent', True)]),
    lbl('lblOkT_Kd', '"Kit Audit Saved"', x=r(115), y=r(21), w=f"Parent.Width - {r(135)}", h=r(35), size=22, color='C_Ink', bold=True),
    lbl('lblOkS_Kd', 'varKitLast.KitID & "  ·  " & varKitLast.Unit', x=r(115), y=r(56), w=f"Parent.Width - {r(135)}", h=r(40), size=14, color='C_Muted', wrap=True),
    box('lnOk_Kd', x=r(25), y=r(104), w=f"Parent.Width - {r(50)}", h=1, fill='C_Line'),
    lbl('lblOkR_Kd', res, x=r(25), y=r(114), w=f"Parent.Width - {r(50)}", h=r(24), size=14, color=f'If(varKitLast.Clear, {GREEN}, {RED})', bold=True)])
nxt = inflow('conNext_Kd', r(100), fill='C_Accent', radius=r(25), children=[
    lbl('lblNextT_Kd', '"Audit Another Kit"', x=r(25), y=r(22), w=f"Parent.Width - {r(40)}", h=r(35), size=22, color='C_White', bold=True),
    lbl('lblNextS_Kd', '"Scan the next kit"', x=r(25), y=r(60), w=f"Parent.Width - {r(40)}", h=r(25), size=15, color='RGBA(255, 255, 255, 0.85)'),
    tbtn('btnNext_Kd', 'Set(varKitMode, "KIT");\nNavigate(KitAudit, ScreenTransition.UnCoverRight)')])
home = inflow('conHome_Kd', r(80), fill='C_White', border='C_Line', radius=r(20), children=[
    lbl('lblHomeT_Kd', '"Home"', x=r(25), w=f"Parent.Width - {r(80)}", h=r(80), size=19, color='C_Ink', bold=True, extra={'VerticalAlign': 'VerticalAlign.Middle'}),
    ico('icoHomeGo_Kd', 'ChevronRight', f"Parent.Width - {r(45)}", r(25), 30, 'C_Muted'),
    tbtn('btnHome_Kd', 'Navigate(Home, ScreenTransition.UnCoverRight)')])
bodyD = vbody('conBody_Kd', [okc, nxt, home], gap=12, top=18, bottom=30, scroll=True)
hdrD = header('Kd', '"Kit Audit Saved"', 'varKitLast.KitID', 'Navigate(Home, ScreenTransition.UnCoverRight)')
open(OUT + 'DTV_KitDone.pa.yaml', 'w').write(screen('KitDone', {'Fill': 'C_Bg'}, [vroot('conRoot_Kd', [hdrD, bodyD])]))
print('built KitAudit, KitDone')
