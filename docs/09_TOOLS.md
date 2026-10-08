# 09 · Tools

All Python 3. Run from the repo root unless stated. Needs `pyyaml`; screenshots need `playwright` (`pip install playwright`; Chromium is at `/opt/pw-browsers/chromium` in cloud sessions — never run `playwright install`).

---

## YAML validator — run on every screen before handing over
```
python3 tools/preview/validate.py powerapps/dtv/DTV_Audit.pa.yaml
```
Prints `controls N dups [...]`, `dupkeys N`, `unbalanced N`. All must be empty / 0. Checks: YAML parses, no duplicate control names, no duplicate property keys, balanced brackets in block formulas.

## Layout simulator — see a screen at phone size without Studio
```
python3 tools/preview/sim.py <screen.pa.yaml> 375 700 /path/out.png   # writes out.html
python3 tools/preview/shoot.py /path/out.html                           # writes out.png
```
Evaluates X/Y/Width/Height/Size formulas (UI, PageW, Gutter, SX/SY…), converts pt → px so truncation shows. Prints width mismatches.
Limits: can't evaluate `If()` heights or formula TemplateSizes (pill rows look clipped); ignores `Visible` (state blocks overlap); formula text shows "Sample text"; transparent button text not drawn. `TRAIN=1` env → training wide/narrow maths.
Try sizes: 375×700, 360×640 (small phone), 768×1024 (tablet).

## Screen generator (phone screens)
`tools/dtv_generator/dtvgen.py` = helper library. Key functions:

| Function | Makes |
|---|---|
| `r(n)` | `"Round(n * UI, 0)"` |
| `F(px)` | px → pt font size |
| `N(name, control, variant, props, children)` | any control |
| `lbl(name, text, x, y, w, h, size, color, bold, wrap, align, visible, extra)` | Label (size in **px design**, converted) |
| `ico(name, icon, x, y, size, color, filled)` | ModernIcon |
| `tbtn(name, onselect, …, display)` | transparent full-size tap button |
| `box(name, x, y, w, h, fill, border, radius, visible, extra, children)` | ManualLayout container |
| `inflow(name, h, w, …)` | container as an auto-layout child (FillPortions 0, LayoutMinHeight) |
| `vroot(name, children)` | screen root (vertical auto-layout) |
| `vbody(name, children, gap, top, bottom, scroll)` | body column with Gutter padding |
| `header(sfx, title, sub, back)` | 95-high sub-screen header with back chevron |
| `screen(name, props, children)` | whole file text |

Formulas with newlines / `: ` / ` #` are written as block scalars automatically.

- DTV app: `cd tools/dtv_generator && python3 dtvbuild.py` → rewrites `powerapps/dtv/*.pa.yaml`.
- Templates: `cd tools/templates && python3 build_templates.py` → rewrites `templates/Template_*.pa.yaml`. Copy this file as the start of a new app's builder.

## Desktop responsive converter
```
python3 tools/make_responsive.py <input folder of .pa.yaml> <output folder>
```
Rewrites fixed 1366×768 numbers to `* SX` / `* SY` / `Round(size * SF, 0)` / `* SR`. Writes Studio's omitted defaults back first.

## Archive
`tools/archive/` — retired one-off patch scripts (history; useful as examples of editing exported YAML in place with Python).
