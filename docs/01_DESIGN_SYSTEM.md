# 01 · Design System

One look across every STARS app. Values are identical in all apps.

---

## 1. Colours

Named formulas in **App > Formulas** (full starter: `templates/App_Formulas_Starter.txt`).

| Name | Value | Use |
|---|---|---|
| `C_Ink` | `RGBA(14, 28, 42, 1)` | Main text |
| `C_Ink2` | `RGBA(58, 80, 104, 1)` | Secondary text, unselected pill text |
| `C_Muted` | `RGBA(140, 155, 174, 1)` | Captions, hints, chevrons |
| `C_Bg` | `RGBA(235, 242, 248, 1)` | Screen background |
| `C_Bg2` | `RGBA(244, 249, 252, 1)` | Table headers, soft panels |
| `C_Line` | `RGBA(14, 42, 70, 0.12)` | Card borders, dividers, progress track |
| *(input border)* | `RGBA(14, 42, 70, 0.22)` | Search boxes / inputs |
| `C_White` | `RGBA(255, 255, 255, 1)` | Cards |
| `C_Accent` | `RGBA(26, 90, 153, 1)` | Primary buttons, selected pills, links |
| `C_AccentDark` | `RGBA(18, 64, 112, 1)` | Pressed / dark accent |
| `C_AccentSoft` | `RGBA(26, 90, 153, 0.10)` | Selected chips, icon circles |
| `C_Good` / `C_GoodBg` | `RGBA(12, 122, 82, 1)` / `RGBA(232, 246, 240, 1)` | Pass / success |
| `C_Danger` / `C_DangerBg` | `RGBA(180, 26, 26, 1)` / `RGBA(254, 242, 242, 1)` | Fail / error |
| `C_Amber` / `C_AmberBg` | `RGBA(178, 105, 0, 1)` / `RGBA(255, 246, 229, 1)` | Warning, re-audit, not allocated |
| `C_Teal` | `RGBA(0, 144, 153, 1)` | Training app accent |
| *Header teal* | `RGBA(7, 95, 115, 1)` | Header container fill (under the gradient image) |
| *Yes / No pills* | `RGBA(30, 122, 80, 1)` / `RGBA(176, 52, 40, 1)` | Selected Yes (green) / No (red) |
| *Disabled button* | `RGBA(160, 174, 180, 1)` | Sticky submit before form is complete |

Notes:
- **DTV app has no `C_Danger`** → use `RGBA(176, 52, 40, 1)` there (or add `C_Danger` to its Formulas first).
- **Desktop app** uses the same values as literal `RGBA(...)` (no `C_` names).
- Desktop chart palette `varChartPalette`: `RGBA(166,199,130)`, `RGBA(35,100,153)`, `RGBA(0,144,153)`, `RGBA(0,200,210)`, `RGBA(112,188,166)`.
- Web (HTML/CSS) equivalents: ink `#0E1C2A`, ink-2 `#3A5068`, muted `#8C9BAE`, bg `#EBF2F8`, bg-2 `#F4F9FC`, accent `#1A5A99`, header teal `#075F73`.

---

## 2. Font, header art, icon

- `AppFont = Font.'Segoe UI'` on **every** control.
- `HeaderImage` = SVG data URI, horizontal gradient `#001D46 → #075F73 → #00838A`. Placed as an `Image` filling the header container (`ImagePosition.Fill`) on top of fill `RGBA(7, 95, 115, 1)`. Exact formula in `templates/App_Formulas_Starter.txt`.
- **App icon:** white flat line symbol on diagonal gradient `#001D46 → #075F73 → #00A3A8`, faint top-right glow, no text. Symbol inside the middle 70% so round masks never clip it. Upload the 512 px PNG: Settings → General → App icon → Upload. Files: `powerapps/icon/`.

---

## 3. Sizing systems

### Mobile / DTV / phone-first apps
```
UI     = Max(0.9, Min(1.25, Min(App.Width, App.Height * 0.55) / 390));  // scale factor
PageW  = Min(App.Width, 720);                                           // content column width
Gutter = (App.Width - PageW) / 2;                                       // side space on tablets
SheetW = Min(App.Width, 600);                                           // pop-up sheet width
```
- Every size: `Round(n * UI, 0)`.
- Content width: `PageW - Round(40 * UI, 0)`.
- Body padding left/right: `Gutter + Round(20 * UI, 0)`.
- Headers and footers: `Width: =App.Width` (full bleed); their contents start at `Gutter + …`.
- Settings → Display: Scale to fit **Off**, Lock aspect ratio **Off**, Orientation **Portrait**, Lock orientation **On**.
- Too big/small everywhere? Change the two numbers in `UI` (0.9 and 1.25).

### Desktop (Physio Dashboard)
Drawn at 1366 × 768, stretched:
```
SX = App.Width / 1366;  SY = App.Height / 768;
SF = Max(0.75, Min(1.4, Min(SX, SY)));   // text
SR = Min(SX, SY);                        // radii, gaps
```
X/Width `* SX`, Y/Height `* SY`, text `Round(size * SF, 0)`, radii `* SR`. Convert a fixed screen with `tools/make_responsive.py`.

### Training stand-alone (wide/narrow)
`Wide = App.Width >= 820` → two columns (list + detail). `PageW = Min(App.Width, 1280)`, plus `GapPx`, `ListW`, `DetailX`, `DetailW`. Narrow = one column with back arrow.

### Why widths are written from `App.Width`
Inside an auto-layout container, Power Apps sizes the child, but the child's own `Width` property still returns its formula. Children using `Parent.Width` get the wrong number. So write every auto-layout child's real width out (e.g. `PageW - Round(40 * UI, 0)`, or `(App.Width - 48) / 3` for three tabs).

---

## 4. Font sizes are POINTS

`Size` is in points (1 pt = 1.33 px). Designs drawn in px must be converted or text gets "…" on phones.

| px design | 36 | 24 | 22 | 19 | 18 | 17 | 16 | 15 | 14 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|
| **pt Size** | 28 | 19 | 18 | 15 | 14 | 14 | 13 | 12 | 11 | 11 |

Minimum readable: **11 pt**. Label height ≈ `size_px * 1.7`.

Typical mobile scale (pt): home title 28 · page title 19 (sub-header) / 15 · card title 14–15 · body 12–13 · caption 11 bold.

---

## 5. Screen anatomy (mobile / DTV)

```
Screen (Fill C_Bg, OnVisible resets state)
└ conRoot_X        GroupContainer AutoLayout, vertical, LayoutAlignItems Stretch, Height Parent.Height
  ├ conHdr_X       ManualLayout, FillPortions 0, Width App.Width, header teal + imgHdr_X (HeaderImage)
  ├ conBody_X      AutoLayout vertical, gap 12–15*UI, padding Gutter+20*UI, LayoutOverflowY Scroll
  │  ├ cards…      FillPortions 0, Height = LayoutMinHeight = Round(n*UI,0), Width PageW-40*UI
  │  ├ gallery     (no FillPortions → fills remaining height, scrolls itself)
  │  └ conEnd_X    16*UI spacer as LAST child (a scrolling container ignores bottom padding)
  └ conFoot_X      optional sticky bottom bar (white, 84*UI, C_Line border) holding the main action
```

| Part | Spec |
|---|---|
| **Home header** | 165 high. Kicker CAPS (11 pt bold, white 80%) · title 28 pt bold white · "Hi <first name> · <day date>" 13 pt white 90% |
| **Sub-screen header** | 95 high. Back = ModernButton `Icon: "ChevronLeft"` 60×60, Size 24, X `Gutter+5*UI`, Y 18. Title 19 pt bold at X `Gutter+65*UI`, Y 12. Subtitle 12 pt white 85% at Y 53 |
| **Card** | White, `C_Line` border 1, radius 18–25*UI, inner padding 18–22*UI |
| **Section caption** | UPPERCASE, 11 pt bold, `C_Muted` ("YOUR STREAM", "1 · LOGIN") |
| **Hero action card** | Solid `C_Accent`, radius 25, icon in translucent white circle (16%), white title + subtitle, transparent button over whole card |
| **Tile** | White card, 90–100 high, icon circle 55 (`C_AccentSoft` / `C_AmberBg`), title 15 pt bold, subtitle 12 pt muted, chevron at `Parent.Width - 38*UI` |
| **Gallery row** | Card width `Parent.TemplateWidth - 10*UI`, X 1, Y 5. Text width `Parent.Width - 56*UI`. Chevron at `Parent.Width - 36*UI`. TemplateSize = row height + 10 |
| **Status stripe** | 8 px bar on left of a row (red = needs follow-up, green = clear) |
| **Pills / segments** | Height 48–50, radius = height/2. Selected `C_Accent` + white text; unselected white + `C_Line` border + `C_Ink2` text |
| **Choice pills** (single select) | Stacked full-width, 44 high. Selected `C_AccentSoft` fill, `C_Accent` border + text |
| **Yes/No pair** | Two half-width pills, 12*UI gap. Selected Yes green, selected No red, white text |
| **Multi-select chips** | As choice pills, text prefixed "✓  " when selected. Stored in a collection |
| **Warning** | Amber card: `C_AmberBg`, border `RGBA(178,105,0,0.35)`, `C_Amber` text |
| **Progress bar** | Track `C_Line` 8 high radius 4; fill `C_Accent`, green at 100% |
| **Empty state** | Centred muted label, `Visible: CountRows(gal.AllItems) = 0` |
| **Sticky submit** | 60 high, radius 28, `C_Accent` when valid, grey + "Answer every question to submit" when not |

---

## 6. Text rules

- **Title Case** on buttons, titles, labels ("Start an Audit", "Audit Another DTV").
- **CAPS** for section captions and kickers.
- One line on a 375-wide phone. Too long → shorten wording, don't wrap. Labels `Wrap: false` unless designed for 2 lines.
- Blank dates show "Not set" / "Optional", never a fake date (31/12/2001).
- Numbers: `If(n = 1, " item", " items")`.
- Middle dot separator with two spaces: `"  ·  "`.

---

## 7. Interaction patterns (use these, not alternatives)

| Need | Use | Not |
|---|---|---|
| Tap a styled area | Transparent `ModernButton` (Appearance Transparent, Text "") as **last child** over the container | Styled button with complex visuals |
| Pick a person/patient | Search box + gallery, or pop-up list | Classic ComboBox (shows blank until you type) |
| Short option list | One row of equal-width pills | Dropdown, horizontally scrolling chips |
| Long names in pills | Derive a short label in a formula (text before first "&" or ",") | Tiny font |
| Logic used in several places | One hidden button (`Visible: false`, 1×1), call `Select(btnX)` | Copy-paste |
| Card that grows | `Height` and `LayoutMinHeight` same formula, e.g. `Round(If(varLogin = "No", 422, 140) * UI, 0)` | Fixed height + overflow |
| Form valid? | Written once in submit button `DisplayMode`; others read `btnSubmit.DisplayMode = DisplayMode.Edit` | Repeating the test |
| Destructive action | Confirm step (sheet or second tap) | Instant |
| Reminder/notice | Tappable card on Home | Long `Notify` on start |
