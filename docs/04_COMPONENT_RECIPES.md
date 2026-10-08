# 04 · Component Recipes

Copy-ready patterns. Each one is used in a real screen already — the "Real example" column points to it.
Fastest route: start from a template in `templates/` (Home, List, Form), which already contains every recipe below.

Sizes assume the phone system (`UI`, `PageW`, `Gutter`). For desktop swap to `SX/SY/SF/SR`.
In the YAML below, `r(n)` means `Round(n * UI, 0)`.

---

## Starters

| File | What's in it |
|---|---|
| `templates/App_Formulas_Starter.txt` | Colours, `AppFont`, `HeaderImage`, `UI/PageW/Gutter/SheetW`, `MeEmail/MeName/MeDirectory/IsManager`, `EmailHead/EmailFoot` |
| `templates/Template_Home.pa.yaml` | Screen `TemplateHome`: big header, hero action card, progress card, caption, two tiles |
| `templates/Template_List.pa.yaml` | Screen `TemplateList`: sub-header, search box, filter pill row, count, empty state, gallery rows with status stripe |
| `templates/Template_Form.pa.yaml` | Screen `TemplateForm`: amber note, Yes/No with "why not" choice pills + notes, multi-select chips, notes card, sticky submit with save + Errors check + double-tap guard |

To regenerate / change: edit `tools/templates/build_templates.py`, run it, validate. To use one: paste it, then rename screen + controls' suffix (`_Hom`, `_Lst`, `_Frm`) **before** pasting a second copy, or build a new screen with the generator.

---

## 1. Screen root + body (mobile)

Real example: every `powerapps/dtv/*.pa.yaml`.
```yaml
- conRoot_X:
    Control: GroupContainer@1.5.0
    Variant: AutoLayout
    Properties:
      DropShadow: =DropShadow.None
      Fill: =C_Bg
      Height: =Parent.Height
      LayoutAlignItems: =LayoutAlignItems.Stretch
      LayoutDirection: =LayoutDirection.Vertical
      Width: =Parent.Width
      (Radius… all =0)
    Children:
      - conHdr_X: ...        # header (recipe 2)
      - conBody_X:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            AlignInContainer: =AlignInContainer.SetByContainer
            LayoutAlignItems: =LayoutAlignItems.Stretch
            LayoutDirection: =LayoutDirection.Vertical
            LayoutGap: =r(12)
            LayoutMinHeight: =r(250)
            LayoutOverflowY: =LayoutOverflow.Scroll     # omit when the body holds a gallery that fills
            PaddingLeft: =Gutter + r(20)
            PaddingRight: =Gutter + r(20)
            PaddingTop: =r(15)
            Width: =App.Width
      - conFoot_X: ...       # optional sticky footer (recipe 9)
```
**Scroll body vs gallery body:** a body with cards uses `LayoutOverflowY: Scroll` and ends with a 16*UI spacer (`conEnd_X`). A body whose last child is a gallery does **not** scroll — the gallery (no `FillPortions`) fills the rest and scrolls itself.

---

## 2. Sub-screen header (95 high)

Real example: `DTV_Done.pa.yaml` → `conHdr_Dn`.
- Container: ManualLayout, `Fill RGBA(7,95,115,1)`, `FillPortions 0`, `Height = LayoutMinHeight = r(95)`, `Width App.Width`.
- `imgHdr_X`: Image, `Image: =HeaderImage`, `ImagePosition.Fill`, full size.
- `btnBack_X`: ModernButton, `Appearance Transparent`, `Icon: ="ChevronLeft"`, `Color C_White`, `Size r(24)`, 60×60, `X Gutter + r(5)`, `Y r(18)`, `OnSelect Navigate(Prev, ScreenTransition.UnCoverRight)`.
- `lblHdrT_X`: title, 19 pt bold white, `X Gutter + r(65)`, `Y r(12)`, `W PageW - r(85)`, `H r(42)`, `Wrap false`.
- `lblHdrS_X`: subtitle, 12 pt, `RGBA(255,255,255,0.85)`, `Y r(53)`, `H r(25)`.

Home header (165 high): see `Template_Home` → `conHdr_Hom` (kicker / title / "Hi <name> · <date>").

---

## 3. Card (fixed or growing)

```yaml
- conCard_X:
    Control: GroupContainer@1.5.0
    Variant: ManualLayout
    Properties:
      AlignInContainer: =AlignInContainer.SetByContainer
      BorderColor: =C_Line
      BorderThickness: =1
      DropShadow: =DropShadow.None
      Fill: =C_White
      FillPortions: =0
      Height: =Round(If(varQ = "No", 360, 140) * UI, 0)
      LayoutMinHeight: =Round(If(varQ = "No", 360, 140) * UI, 0)
      (Radius… all =r(20))
      Width: =PageW - r(40)
```
Inside: caption at `X r(18), Y r(14)` (11 pt bold muted CAPS), question at `Y r(38)` (13 pt bold ink), content from `Y r(74)`. Inner width `Parent.Width - r(36)`.
**Growing card check:** for each state, last child's `Y + Height + 18` ≤ card height.

---

## 4. Hero action card

Real: `DTV_Home` → `conStart_Hm`. Solid `C_Accent`, radius 25, height 120. Icon circle 56 at (20, 32) fill `RGBA(255,255,255,0.16)` with filled white `ModernIcon` 34. Title 19 pt bold white at X 92 Y 32; subtitle 12 pt white 85% at Y 66. Transparent button last, full size.

## 5. Tile (navigation row)

Real: `DTV_Home` → `conTileRe_Hm`. White card 90 high, radius 20. Icon circle 55 at (18, 18) `C_AccentSoft` (or `C_AmberBg` for amber actions) with filled icon 30. Title 15 pt bold at X 88 Y 18; subtitle 12 pt muted at Y 46; width `Parent.Width - r(130)`. Chevron `ModernIcon ChevronRight` 24 at `X Parent.Width - r(38)`. Transparent button last.

## 6. Progress bar

```
track: X r(20), Y r(88), W Parent.Width - r(40), H r(8), Fill C_Line, radius r(4)
  fill: W Parent.Width * Coalesce(varPct, 0), H Parent.Height, radius r(4),
        Fill If(Coalesce(varPct, 0) >= 1, RGBA(30, 122, 80, 1), C_Accent)
```
Work `varPct` out once: `Set(varPct, If(varTotal > 0, varDone / varTotal, 0))`.

---

## 7. Pills

**Filter pill row (one row, equal widths, built from data)** — Real: `DTV_SelectDTV` → `galPills_Sel`.
- Horizontal Gallery, `Items colPills` (`{Label, Key}`), `ShowScrollbar false`, `TemplatePadding 0`, `TemplateSize (PageW - r(40)) / Max(1, CountRows(colPills))`, height 52.
- Inside: container 48 high, `Width Parent.TemplateWidth - r(6)`, `X 3`, radius 24; label centred; transparent button.
- Selected: `C_Accent` fill + border, white text. Unselected: white, `C_Line` border, `C_Ink2` text.
- Short labels: `Trim(First(Split(Substitute(s.Value, ",", "&"), "&")).Value)`.

**Two fixed segments** — Real: `DTV_ReAuditList` → `conSeg_Re`. Width each `(PageW - r(40) - r(10)) / 2`, second at `X segw + r(10)`.

**Yes / No pair** — Real: `DTV_Audit` → `conYes_Found` / `conNo_Found`.
- Half width `Round((Parent.Width - r(36) - r(12)) / 2, 0)`, 48 high, radius 24.
- Fill/border `If(var = "Yes", RGBA(30,122,80,1), C_White)` / `If(var = "No", RGBA(176,52,40,1), C_White)`; text white when selected, `C_Muted` otherwise.
- `OnSelect: Set(varQ, "Yes")`.

**Single-select choice pills** (stacked, "why not?") — full width, 44 high, radius 22, 50 apart. Selected `C_AccentSoft` fill, `C_Accent` border + text.

**Multi-select chips** — as choice pills, collection-backed:
```
Text:     If("Option A" in colTicks.Value, "✓  ", "") & "Option A"
OnSelect: If("Option A" in colTicks.Value,
             Remove(colTicks, LookUp(colTicks, Value = "Option A")),
             Collect(colTicks, { Value: "Option A" }))
Save:     Covered: ForAll(colTicks As e, { Value: e.Value })
OnVisible: ClearCollect(colTicks, { Value: "" }); Clear(colTicks)
```

---

## 8. Search + gallery list

Real: `DTV_SelectDTV`, `DTV_ReAuditList`.
- Search box: container 60 high, white, border `RGBA(14,42,70,0.22)`, radius 15; `ModernIcon Search` at (16, 18); `Classic/TextInput` borderless, transparent fill, `DelayOutput true`, X 46, width `Parent.Width - r(54)`.
- Count label: `CountRows(gal.AllItems) & If(... = 1, " item", " items")`, 11 pt bold muted.
- Empty label: `Visible: CountRows(gal.AllItems) = 0`, different text for "no match" vs "nothing to do".
- Gallery: Vertical, `TemplatePadding 0`, `TemplateSize r(94)`, `LayoutMinHeight r(150)`, no FillPortions.
- Row: container `X 1, Y r(5)`, `W Parent.TemplateWidth - r(10)`, `H r(84)`, radius 18. Text X 16–22, width `Parent.Width - r(56..62)`. Chevron at `Parent.Width - r(36)`, Y 30. Transparent button last.
- Status stripe: container `W r(8)`, `H Parent.Height`, only left radii set (`RadiusTopLeft/BottomLeft r(18)`, right = 0).

---

## 9. Sticky submit footer

Real: `DTV_Audit` → `conFoot_Aud`.
- Footer: inflow container, `W App.Width`, `H r(84)`, white, `C_Line` border.
- Button box: `X Gutter + r(20)`, `Y r(12)`, `W PageW - r(40)`, `H r(60)`, radius 28, fill `If(btnSubmit.DisplayMode = DisplayMode.Edit, C_Accent, RGBA(160,174,180,1))`.
- Label: `If(ok, "Submit Audit", "Answer every question to submit")`, smaller size when not ok.
- Transparent button: `DisplayMode: If(<READY> && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)`; `OnSelect: Set(varSaving, true); <save>`.

## 10. Save with Errors check

See `02_POWER_FX_RULES.md` §1 and `Template_Form` → `btnSubmit_Frm`. Pattern: `With({ rec: Patch(...) }, If(IsEmpty(Errors(List)), <success path>, <failure path>))`, reset `varSaving` on both.

## 11. Photo (optional) card

Real: `DTV_Audit` → `conPhoto_Aud`.
- Styled outline pill "Add Photo" / "Change Photo"; **AddMedia control laid over it** with every colour/fill = `RGBA(0,0,0,0)` (invisible but tappable).
- `imgPhoto` (110×110) shows `addPhoto.Media` when present; "Remove Photo" label + transparent button `Reset(addPhoto)`.
- Card height `If(IsBlank(addPhoto.Media), 140, 262)`.
- Save the record first, then `Patch(List, rec, { AuditPhoto: imgPhoto.Image })`.

## 12. Warning / amber note card

`C_AmberBg` fill, border `RGBA(178,105,0,0.35)`, caption `C_Amber` 11 pt bold, body 13 pt bold ink. Real: `DTV_Audit` → `conPrev_Aud`.

## 13. Hidden shared-logic button

Real: `M10_Training` (`OnVisible: =Select(btnLoad_Tm)`), `M11_TrainingDates` (`btnLoad_Tds`, `btnSlots_Tds`, `btnDoBook_Tds`…).
- Direct child of the screen (not inside a container), `Visible: false`, 1×1.
- Holds the logic once; screen OnVisible, refresh button and after-save all call `Select(btnLoad_X)`.

## 14. Bottom sheet / pop-up

Real: `M4_Allocate` (confirm sheet), `M2_Find` (Filters sheet).
- Overlay container (direct child of the screen, after `conRoot`), `Visible: alShowForm`, full screen, dark translucent fill.
- Transparent button over the veil: `OnSelect: Set(alShowForm, false)` (tap outside closes).
- Sheet: white, `Width Min(Parent.Width, SheetW)`, `X (Parent.Width - Min(Parent.Width, SheetW)) / 2`, `Height Min(Parent.Height - r(50), r(<content>))`, `Y If(App.Width >= 720, centred, Parent.Height - Self.Height)` (bottom sheet on phones, centred dialog on tablets). Small grey handle bar at top.

## 15. Barcode scan

Real: `M1_Home`, `M8_Audit`, `M9_Servicing`. `BarcodeReader@1.0.25` overlay; `OnScan` → `Set(varScan, First(Self.Barcodes).Value)` then LookUp by `Title`. Device only.

---

## Desktop recipes

Desktop screens are larger and older; don't regenerate them. Reuse from:
- Ward board read-only rows + single edit panel: `Ward_All.pa.yaml`.
- Tiles with KPIs: `Home_Main.pa.yaml`, `Audit_Coverage.pa.yaml`.
- Charts (pie/line/bar with `varChartPalette`): `Physio_Data_New.pa.yaml`.
- Week calendar view: `PT_Leave_New.pa.yaml`.
- People admin (writes `ClinicianDirectory`): `Directory_Admin_New.pa.yaml`.
