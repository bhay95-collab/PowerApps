# DTV Audit app: Kit Scan Test screen (trial). Scan form / kit barcodes and see exactly what each one contains.
#   cd tools/dtv_generator && python3 scantestbuild.py   -> powerapps/dtv/DTV_ScanTest.pa.yaml
from dtvgen import *
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'powerapps', 'dtv') + os.sep
W = f"PageW - {r(40)}"
LINE = "RGBA(14, 42, 70, 0.22)"
NOSB = {k: v for k, v in SBOX.items() if not k.startswith('Radius')}

# ---- optional label for the next scan (helps build the master list later)
note = inflow('conNote_Sct', r(108), fill='C_White', border='C_Line', radius=r(20), children=[
    lbl('capNote_Sct', '"WHAT ARE YOU SCANNING? (OPTIONAL)"', x=r(18), y=r(14), w=f'Parent.Width - {r(36)}', h=r(22), size=14, color='C_Muted', bold=True),
    N('txtNote_Sct', 'Classic/TextInput@2.3.2', props=dict({'BorderColor': LINE, 'BorderThickness': '1', 'Color': 'C_Ink', 'Default': '""', 'FocusedBorderColor': 'C_Accent', 'FocusedBorderThickness': '2', 'Font': 'AppFont',
        'Height': r(48), 'HintText': '"e.g. Fluid Balance Chart v2.00 / kit label"', 'Size': r(F(15)), 'Width': f'Parent.Width - {r(36)}', 'X': r(18), 'Y': r(44)}, **rad(r(12))))])

# ---- scan button: styled card with the scanner laid over it (same as the equipment app)
SCAN = '''// every barcode the camera read in this scan (some phones read more than one at once)
ForAll(
    scnTest_Sct.Barcodes As b,
    Collect(
        colScanTest,
        {
            Seq: CountRows(colScanTest) + 1,
            Value: b.Value,
            Kind: b.Type,
            InScan: CountRows(scnTest_Sct.Barcodes),
            When: Now(),
            Note: Trim(txtNote_Sct.Text)
        }
    )
);
Reset(txtNote_Sct);
If(
    IsEmpty(scnTest_Sct.Barcodes),
    Notify("Nothing was read. Try again, a bit further away and in good light.", NotificationType.Warning),
    Notify("Read: " & Concat(scnTest_Sct.Barcodes, Value, "  |  "), NotificationType.Success)
)'''
scan = inflow('conScan_Sct', r(110), fill='C_Accent', radius=r(25), children=[
    box('conScanIc_Sct', x=r(20), y=r(27), w=r(56), h=r(56), fill='RGBA(255, 255, 255, 0.16)', radius=r(28), children=[ico('icoScan_Sct', 'Camera', r(13), r(13), 30, 'C_White', True)]),
    lbl('lblScanT_Sct', '"Scan a Barcode"', x=r(92), y=r(28), w=f'Parent.Width - {r(108)}', h=r(32), size=24, color='C_White', bold=True),
    lbl('lblScanS_Sct', '"Form, kit label or anything else"', x=r(92), y=r(62), w=f'Parent.Width - {r(108)}', h=r(22), size=15, color='RGBA(255, 255, 255, 0.85)'),
    N('scnTest_Sct', 'BarcodeReader@1.0.25', props={'BorderStyle': 'BorderStyle.None', 'FillColor': 'RGBA(0, 0, 0, 0)', 'FontSize': '1', 'Height': 'Parent.Height', 'HoverFillColor': 'RGBA(255, 255, 255, 0.08)',
        'OnScan': SCAN, 'ScanningMode': "'BarcodeReader.ScanningMode'.SelectToScan", 'Text': '""', 'Width': 'Parent.Width'}),
])

count = lbl('lblCount_Sct', 'CountRows(colScanTest) & If(CountRows(colScanTest) = 1, " scan", " scans") & "  ·  " & CountRows(Distinct(colScanTest, Value)) & " different codes  ·  newest first"',
            w=W, h=r(22), size=14, color='C_Muted', bold=True, extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(22)})
empty = lbl('lblEmpty_Sct', '"Scan a few forms and a kit label. Each one appears here with exactly what the barcode contains."', w=W, h=r(60), size=15, color='C_Muted', align='Align.Center', wrap=True,
            visible='IsEmpty(colScanTest)', extra={'AlignInContainer': 'AlignInContainer.SetByContainer', 'LayoutMinHeight': r(60)})
dup = 'CountIf(colScanTest, Value = ThisItem.Value)'
row = box('conRow_Sct', x='1', y=r(5), w=f'Parent.TemplateWidth - {r(10)}', h=r(100), fill='C_White', border='C_Line', radius=r(18), children=[
    lbl('lblSeq_Sct', '"#" & ThisItem.Seq', x=r(16), y=r(10), w=r(60), h=r(22), size=13, color='C_Muted', bold=True),
    lbl('lblTime_Sct', 'Text(ThisItem.When, "h:mm:ss AM/PM")', x=f'Parent.Width - {r(140)}', y=r(10), w=r(124), h=r(22), size=13, color='C_Muted', align='Align.Right'),
    lbl('lblVal_Sct', 'ThisItem.Value', x=r(16), y=r(32), w=f'Parent.Width - {r(32)}', h=r(28), size=19, color='C_Ink', bold=True),
    lbl('lblType_Sct', 'Text(ThisItem.Kind)', x=r(16), y=r(64), w=r(150), h=r(22), size=13, color='C_Accent', bold=True),
    lbl('lblInfo_Sct', f'Len(ThisItem.Value) & " characters" & If({dup} > 1, "  ·  scanned " & {dup} & " times", "") & If(ThisItem.InScan > 1, "  ·  " & ThisItem.InScan & " codes in one scan", "") & If(IsBlank(ThisItem.Note), "", "  ·  " & ThisItem.Note)',
        x=r(170), y=r(64), w=f'Parent.Width - {r(186)}', h=r(22), size=13, color='C_Ink2'),
])
gal = N('galScans_Sct', 'Gallery@2.15.0', 'Vertical', {'AlignInContainer': 'AlignInContainer.SetByContainer', 'Items': 'SortByColumns(colScanTest, "Seq", SortOrder.Descending)', 'LayoutMinHeight': r(150),
        'TemplatePadding': '0', 'TemplateSize': r(110), 'Width': W}, [row])
body = vbody('conBody_Sct', [note, scan, count, empty, gal], gap=12, top=15, bottom=10)

# ---- footer: email results / clear
q = lambda e: f'Char(34) & Substitute(Coalesce({e}, ""), Char(34), Char(34) & Char(34)) & Char(34)'
EMAIL = f'''If(
    IsEmpty(colScanTest),
    Notify("Scan something first.", NotificationType.Information),
    Set(varSaving, true);
    Set(
        varScanCsv,
        "Order,Barcode Value,Characters,Codes In Same Scan,Time,Label" & Char(13) & Char(10) &
        Concat(
            colScanTest,
            Seq & "," & {q('Value')} & "," & Len(Value) & "," & InScan & "," & Text(When, "yyyy-mm-dd hh:mm:ss") & "," & {q('Note')},
            Char(13) & Char(10)
        )
    );
    Set(
        varScanHtml,
        Substitute(Substitute(EmailHead, "{{{{TITLE}}}}", "Kit Scan Test"), "{{{{SUB}}}}", CountRows(colScanTest) & " scans  |  " & Text(Now(), "d mmm yyyy h:mm AM/PM")) &
        "<tr><td style='padding:24px 32px 8px 32px;'>" &
        "<table role='presentation' width='100%' cellpadding='0' cellspacing='0' border='0' style='border-collapse:separate;border-spacing:0;width:100%;font-size:14px;border:1px solid #E3EAF1;border-radius:14px;overflow:hidden;'>" &
            "<tr bgcolor='#F2F6FA' style='background-color:#F2F6FA;'>" &
                "<th align='left' style='padding:10px 12px;font-size:11px;letter-spacing:1px;color:#8C9BAE;border-bottom:2px solid #1A5A99;'>#</th>" &
                "<th align='left' style='padding:10px 12px;font-size:11px;letter-spacing:1px;color:#8C9BAE;border-bottom:2px solid #1A5A99;'>BARCODE VALUE</th>" &
                "<th align='left' style='padding:10px 12px;font-size:11px;letter-spacing:1px;color:#8C9BAE;border-bottom:2px solid #1A5A99;'>LABEL</th>" &
            "</tr>" &
            Concat(
                colScanTest,
                "<tr>" &
                    "<td style='padding:10px 12px;border-top:1px solid #E3EAF1;color:#8C9BAE;'>" & Seq & "</td>" &
                    "<td style='padding:10px 12px;border-top:1px solid #E3EAF1;font-weight:700;color:#0E1C2A;font-family:Consolas,monospace;'>" & Substitute(Substitute(Value, "&", "&amp;"), "<", "&lt;") & "</td>" &
                    "<td style='padding:10px 12px;border-top:1px solid #E3EAF1;color:#3A5068;'>" & Note & "</td>" &
                "</tr>"
            ) &
        "</table></td></tr>" &
        "<tr><td style='padding:16px 32px 28px 32px;font-size:15px;line-height:22px;color:#3A5068;'>The same list is attached as a CSV file.</td></tr>" &
        Substitute(EmailFoot, "{{{{NOTE}}}}", "Kit scan test from the DTV Audit app.")
    );
    If(
        IsError(DTVDashboardEmail.Run(User().Email, "DTV Kit Scan Test (" & CountRows(colScanTest) & " scans)", varScanHtml, "Kit_Scan_Test_" & Text(Now(), "yyyy-mm-dd_hhmm") & ".csv", varScanCsv)),
        Notify("Could not send the email.", NotificationType.Error),
        Notify("Email sent to " & User().Email & ".", NotificationType.Success)
    );
    Set(varSaving, false)
)'''
bw = f'(PageW - {r(40)} - {r(12)}) / 2'
def fbtn(name, x, text, onsel, fill, color, border=None, display=None):
    return box(f'con{name}_Sct', x=x, y=r(12), w=bw, h=r(60), fill=fill, border=border, radius=r(28), children=[
        lbl(f'lbl{name}_Sct', text, w='Parent.Width', h=r(60), size=17, color=color, bold=True, align='Align.Center', extra={'VerticalAlign': 'VerticalAlign.Middle'}),
        tbtn(f'btn{name}_Sct', onsel, display=display)])
foot = inflow('conFoot_Sct', r(84), w='App.Width', fill='C_White', border='C_Line', radius='0', children=[
    fbtn('Email', f'Gutter + {r(20)}', 'If(varSaving, "Sending...", "Email Me Results")', 'Select(btnSend_Sct)', 'C_Accent', 'C_White', display='If(varSaving || IsEmpty(colScanTest), DisplayMode.Disabled, DisplayMode.Edit)'),
    fbtn('Clear', f'Gutter + {r(20)} + {bw} + {r(12)}', 'If(varScanClearAsk, "Tap Again to Clear", "Clear List")',
         'If(varScanClearAsk, Clear(colScanTest); Set(varScanClearAsk, false), Set(varScanClearAsk, true))', 'If(varScanClearAsk, RGBA(176, 52, 40, 1), C_White)',
         'If(varScanClearAsk, C_White, C_Ink2)', border='C_Line'),
])
hdr = header('Sct', '"Kit Scan Test"', '"Trial: see what each barcode contains"', 'Navigate(Home, ScreenTransition.UnCoverRight)')
send = N('btnSend_Sct', 'ModernButton@1.0.0', props=dict({'Align': 'Align.Center', 'FontWeight': '""', 'Height': '1', 'OnSelect': EMAIL, 'Size': r(11), 'Text': '""', 'VerticalAlign': 'VerticalAlign.Middle', 'Visible': 'false', 'Width': '1'}, **SBOX))
ONV = '''Set(varSaving, false);
Set(varScanClearAsk, false)'''
open(OUT + 'DTV_ScanTest.pa.yaml', 'w').write(screen('ScanTest', {'Fill': 'C_Bg', 'OnVisible': ONV}, [vroot('conRoot_Sct', [hdr, body, foot]), send]))
print('built ScanTest')
