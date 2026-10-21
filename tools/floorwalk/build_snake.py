# Builds powerapps/floorwalk/Snake.pa.yaml (hidden easter egg screen of the Floorwalking Ideas app).
#   python3 tools/floorwalk/build_snake.py
# Power Apps runs the game (Timer + collection); the HTML viewer only draws the board.
# (The HTML viewer strips <script> and <iframe>, so game code cannot live inside the HTML.)
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'powerapps', 'floorwalk', 'Snake.pa.yaml')

C = "Round(21 * UI, 0)"          # cell size
BX = f"Gutter + (PageW - 14 * {C}) / 2"   # board left
BY = "Round(16 * UI, 0)"
BW = f"14 * {C}"
BH = f"15 * {C}"
BS = "Round(64 * UI, 0)"         # d-pad button size
G = "Round(8 * UI, 0)"           # d-pad gap
CX = "Gutter + PageW / 2"
Y0 = f"{BY} + {BH} + Round(16 * UI, 0)"

def props(d, ind):
    out = []
    for k in sorted(d):
        v = d[k]
        if '\n' in v or ': ' in v or ' #' in v:
            out.append(f"{ind}{k}: |-")
            for line in v.split('\n'):
                out.append(f"{ind}  {line}")
        else:
            out.append(f"{ind}{k}: {v}")
    return out

def ctl(ind, name, control, p, children=None, variant=None):
    out = [f"{ind}- {name}:", f"{ind}    Control: {control}"]
    if variant:
        out.append(f"{ind}    Variant: {variant}")
    out.append(f"{ind}    Properties:")
    out += props(p, ind + "      ")
    if children:
        out.append(f"{ind}    Children:")
        for c in children:
            out += c
    return out

def con(ind, name, p, children=None, variant='ManualLayout'):
    base = {'DropShadow': '=DropShadow.None', 'RadiusBottomLeft': '=0', 'RadiusBottomRight': '=0', 'RadiusTopLeft': '=0', 'RadiusTopRight': '=0'}
    base.update(p)
    return ctl(ind, name, 'GroupContainer@1.5.0', base, children, variant)

def rad(n):
    r = f"=Round({n} * UI, 0)"
    return {'RadiusBottomLeft': r, 'RadiusBottomRight': r, 'RadiusTopLeft': r, 'RadiusTopRight': r}

def lbl(ind, name, text, p):
    base = {'Font': '=AppFont', 'Text': text}
    base.update(p)
    return ctl(ind, name, 'Label@2.5.1', base)

def tbtn(ind, name, onselect, p=None):
    base = {'Align': '=Align.Center', 'Appearance': '=ButtonAppearance.Transparent', 'BorderStyle': '=BorderStyle.None', 'FontWeight': '=""',
            'Height': '=Parent.Height', 'OnSelect': onselect, 'PaddingBottom': '=5', 'PaddingLeft': '=12', 'PaddingRight': '=12', 'PaddingTop': '=5',
            'RadiusBottomLeft': '=4', 'RadiusBottomRight': '=4', 'RadiusTopLeft': '=4', 'RadiusTopRight': '=4', 'Text': '=""',
            'VerticalAlign': '=VerticalAlign.Middle', 'Width': '=Parent.Width'}
    if p: base.update(p)
    return ctl(ind, name, 'ModernButton@1.0.0', base)

def hidden_btn(ind, name, onselect):
    return ctl(ind, name, 'ModernButton@1.0.0', {
        'Align': '=Align.Center', 'FontWeight': '=""', 'Height': '=1', 'OnSelect': onselect, 'PaddingBottom': '=5', 'PaddingLeft': '=12', 'PaddingRight': '=12',
        'PaddingTop': '=5', 'RadiusBottomLeft': '=4', 'RadiusBottomRight': '=4', 'RadiusTopLeft': '=4', 'RadiusTopRight': '=4', 'Size': '=Round(11 * UI, 0)',
        'Text': '=""', 'VerticalAlign': '=VerticalAlign.Middle', 'Visible': '=false', 'Width': '=1'})

def dpad(ind, key, icon, x, y, onselect):
    I = ind + "      "   # children indent of the container
    return con(ind, f"con{key}_Sn", {
        'BorderColor': '=C_Line', 'BorderThickness': '=1', 'Fill': '=C_White', 'Height': f'={BS}', 'Width': f'={BS}', 'X': f'={x}', 'Y': f'={y}', **rad(16)},
        [ctl(I, f"ico{key}_Sn", 'ModernIcon@1.1.1', {'Height': '=Round(30 * UI, 0)', 'Icon': f'="{icon}"', 'IconColor': '=C_Accent', 'Width': '=Round(30 * UI, 0)',
                                                    'X': f'=({BS} - Round(30 * UI, 0)) / 2', 'Y': f'=({BS} - Round(30 * UI, 0)) / 2'}),
         tbtn(I, f"btn{key}_Sn", onselect)])

# ---- board HTML (Power Apps writes one string from the snake and the food; no script needed)
HTML = f'''=With(
    {{ c: {C}, hs: Max(colSnake, Seq) }},
    "<div style='position:absolute;left:0;top:0;width:" & (14 * c) & "px;height:" & (15 * c) & "px;background:#F4F9FC;border-radius:12px;overflow:hidden;box-shadow:0 0 0 1px #D6E0EA'>" &
    "<div style='position:absolute;left:" & (varSnFood.X * c) & "px;top:" & (varSnFood.Y * c) & "px;width:" & (c - 2) & "px;height:" & (c - 2) & "px;margin:1px;border-radius:50%;background:#B41A1A'></div>" &
    Concat(
        colSnake,
        "<div style='position:absolute;left:" & (X * c) & "px;top:" & (Y * c) & "px;width:" & (c - 2) & "px;height:" & (c - 2) & "px;margin:1px;border-radius:" & Round(c / 3, 0) & "px;background:" & If(Seq = hs, "#124070", "#1A5A99") & "'></div>"
    ) &
    "</div>"
)'''

RESET = '''=// RESET: a short snake in the middle, moving right, score 0, waiting for Start
ClearCollect(colSnake, { X: 6, Y: 7, Seq: 1 }, { X: 7, Y: 7, Seq: 2 }, { X: 8, Y: 7, Seq: 3 });
Set(varSnDir, { X: 1, Y: 0 });
Set(varSnNext, { X: 1, Y: 0 });
Set(varSnScore, 0);
Set(varSnDead, false);
Set(varSnWon, false);
Set(varSnRun, false);
Select(btnFood_Sn)'''

FOOD = '''=// FOOD: pick a random empty cell (14 x 15 board). No empty cell left = the player wins.
With(
    {
        free: Filter(
            ForAll(Sequence(14 * 15, 0) As s, { X: Mod(s.Value, 14), Y: RoundDown(s.Value / 14, 0) }) As c,
            IsBlank(LookUp(colSnake, X = c.X && Y = c.Y))
        )
    },
    If(
        CountRows(free) = 0,
        Set(varSnWon, true);
        Set(varSnDead, true);
        Set(varSnRun, false);
        Set(varSnBest, Max(Coalesce(varSnBest, 0), varSnScore)),
        Set(varSnFood, Index(free, RandBetween(1, CountRows(free))))
    )
)'''

TICK = '''=// TICK (every timer beat): move one cell. Head = highest Seq, tail = lowest Seq.
If(
    varSnRun && !varSnDead,
    With(
        {
            head: First(Sort(colSnake, Seq, SortOrder.Descending)),
            tailSeq: Min(colSnake, Seq),
            d: varSnNext
        },
        With(
            { nx: head.X + d.X, ny: head.Y + d.Y },
            Set(varSnDir, d);
            If(
                nx < 0 || nx >= 14 || ny < 0 || ny >= 15 || !IsBlank(LookUp(colSnake, X = nx && Y = ny && Seq > tailSeq)),
                // hit a wall or itself (the tail cell is free because the tail moves away)
                Set(varSnDead, true);
                Set(varSnRun, false);
                Set(varSnBest, Max(Coalesce(varSnBest, 0), varSnScore)),
                Collect(colSnake, { X: nx, Y: ny, Seq: head.Seq + 1 });
                If(
                    nx = varSnFood.X && ny = varSnFood.Y,
                    Set(varSnScore, varSnScore + 1);
                    Select(btnFood_Sn),
                    RemoveIf(colSnake, Seq = tailSeq)
                )
            )
        )
    )
)'''

I0 = "      "          # screen children indent
ROOT = "          "   # inside conRoot
HDR = "              "  # inside conHdr / conBody children

header = con(ROOT + "  ", "conHdr_Sn", {'AlignInContainer': '=AlignInContainer.SetByContainer', 'Fill': '=RGBA(7, 95, 115, 1)', 'FillPortions': '=0',
        'Height': '=Round(95 * UI, 0)', 'LayoutMinHeight': '=Round(95 * UI, 0)', 'Width': '=App.Width'}, [
    ctl(HDR + "  ", "imgHdr_Sn", 'Image@2.2.3', {'Height': '=Parent.Height', 'Image': '=HeaderImage', 'ImagePosition': '=ImagePosition.Fill', 'Width': '=Parent.Width'}),
    ctl(HDR + "  ", "btnBack_Sn", 'ModernButton@1.0.0', {
        'Align': '=Align.Center', 'Appearance': '=ButtonAppearance.Transparent', 'Color': '=C_White', 'FontWeight': '=""', 'Height': '=Round(60 * UI, 0)', 'Icon': '="ChevronLeft"',
        'OnSelect': '=Navigate(Home, ScreenTransition.UnCoverRight)', 'PaddingBottom': '=5', 'PaddingLeft': '=12', 'PaddingRight': '=12', 'PaddingTop': '=5',
        'RadiusBottomLeft': '=4', 'RadiusBottomRight': '=4', 'RadiusTopLeft': '=4', 'RadiusTopRight': '=4', 'Size': '=Round(24 * UI, 0)', 'Text': '=""',
        'VerticalAlign': '=VerticalAlign.Middle', 'Width': '=Round(60 * UI, 0)', 'X': '=Gutter + Round(5 * UI, 0)', 'Y': '=Round(18 * UI, 0)'}),
    lbl(HDR + "  ", "lblHdrT_Sn", '="Snake"', {'Color': '=C_White', 'FontWeight': '=FontWeight.Bold', 'Height': '=Round(42 * UI, 0)', 'Size': '=Round(19 * UI, 0)',
        'Width': '=PageW - Round(85 * UI, 0)', 'Wrap': '=false', 'X': '=Gutter + Round(65 * UI, 0)', 'Y': '=Round(12 * UI, 0)'}),
    lbl(HDR + "  ", "lblHdrS_Sn", '="Score " & Coalesce(varSnScore, 0) & "  ·  Best " & Coalesce(varSnBest, 0)', {'Color': '=RGBA(255, 255, 255, 0.85)', 'Height': '=Round(25 * UI, 0)',
        'Size': '=Round(12 * UI, 0)', 'Width': '=PageW - Round(85 * UI, 0)', 'Wrap': '=false', 'X': '=Gutter + Round(65 * UI, 0)', 'Y': '=Round(53 * UI, 0)'}),
])

B = ROOT + "      "   # children of conBody
board = ctl(B, "htmBoard_Sn", 'HtmlViewer@2.1.0', {
    'DisabledBorderColor': '=RGBA(161, 159, 157, 1)', 'Font': '=AppFont', 'Height': f'={BH} + 4', 'HtmlText': HTML, 'Width': f'={BW} + 4', 'X': f'={BX}', 'Y': f'={BY}'})

OV = B + "      "
over = con(B, "conOver_Sn", {
    'BorderColor': '=C_Line', 'BorderThickness': '=1', 'Fill': '=RGBA(255, 255, 255, 0.94)', 'Height': '=Round(190 * UI, 0)', 'Visible': '=!varSnRun',
    'Width': f'=Min({BW} - Round(40 * UI, 0), Round(260 * UI, 0))', 'X': f'={BX} + ({BW} - Min({BW} - Round(40 * UI, 0), Round(260 * UI, 0))) / 2',
    'Y': f'={BY} + ({BH} - Round(190 * UI, 0)) / 2', **rad(22)}, [
    lbl(OV, "lblOverT_Sn", '=If(varSnWon, "You Win!", varSnDead, "Game Over", "Snake")', {'Align': '=Align.Center', 'Color': '=C_Ink', 'FontWeight': '=FontWeight.Bold',
        'Height': '=Round(34 * UI, 0)', 'Size': '=Round(19 * UI, 0)', 'Width': '=Parent.Width', 'Wrap': '=false', 'Y': '=Round(16 * UI, 0)'}),
    lbl(OV, "lblOverS_Sn", '=If(varSnDead, "Score " & varSnScore, "Eat the dots. Avoid the walls and your tail.")', {'Align': '=Align.Center', 'Color': '=C_Ink2',
        'Height': '=Round(44 * UI, 0)', 'Size': '=Round(12 * UI, 0)', 'Width': '=Parent.Width - Round(32 * UI, 0)', 'X': '=Round(16 * UI, 0)', 'Y': '=Round(54 * UI, 0)'}),
    con(OV, "conGo_Sn", {'Fill': '=C_Accent', 'Height': '=Round(52 * UI, 0)', 'Width': '=Parent.Width - Round(48 * UI, 0)', 'X': '=Round(24 * UI, 0)', 'Y': '=Round(114 * UI, 0)', **rad(26)}, [
        lbl(OV + "      ", "lblGo_Sn", '=If(varSnDead, "Play Again", "Start")', {'Align': '=Align.Center', 'Color': '=C_White', 'FontWeight': '=FontWeight.Bold', 'Height': '=Parent.Height',
            'Size': '=Round(14 * UI, 0)', 'VerticalAlign': '=VerticalAlign.Middle', 'Width': '=Parent.Width', 'Wrap': '=false'}),
        tbtn(OV + "      ", "btnGo_Sn", '|\n=If(varSnDead, Select(btnReset_Sn));\nSet(varSnRun, true)'.replace('|\n', ''))]),
])

pads = [
    dpad(B, "Up", "ChevronUp", f"{CX} - {BS} / 2", Y0, "=If(varSnDir.Y <> 1, Set(varSnNext, { X: 0, Y: -1 }))"),
    dpad(B, "Left", "ChevronLeft", f"{CX} - {BS} / 2 - {G} - {BS}", f"{Y0} + {BS} + {G}", "=If(varSnDir.X <> 1, Set(varSnNext, { X: -1, Y: 0 }))"),
    dpad(B, "Down", "ChevronDown", f"{CX} - {BS} / 2", f"{Y0} + {BS} + {G}", "=If(varSnDir.Y <> -1, Set(varSnNext, { X: 0, Y: 1 }))"),
    dpad(B, "Right", "ChevronRight", f"{CX} + {BS} / 2 + {G}", f"{Y0} + {BS} + {G}", "=If(varSnDir.X <> -1, Set(varSnNext, { X: 1, Y: 0 }))"),
]

body = con(ROOT + "  ", "conBody_Sn", {'AlignInContainer': '=AlignInContainer.SetByContainer', 'Fill': '=C_Bg', 'LayoutMinHeight': '=Round(250 * UI, 0)', 'Width': '=App.Width'},
           [board, over] + pads)

root = con(I0, "conRoot_Sn", {'Fill': '=C_Bg', 'Height': '=Parent.Height', 'LayoutAlignItems': '=LayoutAlignItems.Stretch', 'LayoutDirection': '=LayoutDirection.Vertical',
                              'Width': '=Parent.Width'}, [header, body], variant='AutoLayout')

timer = ctl(I0, "tmr_Sn", 'Timer@2.1.0', {
    'AutoStart': '=false', 'Duration': '=Max(90, 180 - Coalesce(varSnScore, 0) * 4)', 'Height': '=1', 'OnTimerEnd': '=Select(btnTick_Sn)', 'Repeat': '=true',
    'Start': '=Coalesce(varSnRun, false)', 'Visible': '=true', 'Width': '=1', 'X': '=0', 'Y': '=0'})

lines = ["Screens:", "  Snake:", "    Properties:", "      Fill: =C_Bg", "      OnVisible: |-"]
lines += ["        " + l for l in RESET.split('\n')]
lines.append("    Children:")
for blk in (root, timer, hidden_btn(I0, "btnReset_Sn", "|-\n" + RESET), ):
    pass
def hb(name, formula):
    return hidden_btn(I0, name, "=PLACEHOLDER")
def fix(block, formula):
    out = []
    for l in block:
        if l.strip() == "OnSelect: =PLACEHOLDER":
            ind = l[:len(l) - len(l.lstrip())]
            out.append(f"{ind}OnSelect: |-")
            out += [f"{ind}  {x}" for x in formula.split('\n')]
        else:
            out.append(l)
    return out
parts = [root, timer, fix(hb("btnReset_Sn", ""), RESET), fix(hb("btnFood_Sn", ""), FOOD), fix(hb("btnTick_Sn", ""), TICK)]
for p_ in parts:
    lines += p_
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('wrote', OUT)
