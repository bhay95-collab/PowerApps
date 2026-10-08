# 03 · Studio and YAML

How screen code moves between this repo and Power Apps Studio.

---

## 1. Pasting a screen (give Ben these steps)

Control names are **global** across the app. If the old screen still exists, Studio adds `_1` to every pasted control name, or Ben ends up looking at the old screen.

1. (Optional) Save old screen code: right-click old screen → **Copy code** → paste into a text file.
2. Right-click the old screen → **Delete**. (If it's the only screen, add a blank one first.)
3. **+ New screen → Blank**.
4. Right-click it → **Rename** → type the exact name (e.g. `Audit`).
5. Open the file on GitHub → **Raw** → Ctrl+A, Ctrl+C.
6. Right-click the new screen → **Paste code**.
7. ⋯ next to the screen → **Run OnVisible**.
8. **Ctrl+S**. Open **App checker** (stethoscope) — should be clean.

Red errors naming a screen that isn't pasted yet clear once all screens are in. Paste order matters when screens reference each other: paste targets first, Home last.

**Brand-new app:** File → Save as (copy of an existing app keeps connections) → Settings → Display (Scale to fit Off, Lock aspect Off) → App > Formulas paste → paste screens → drag Home to top of Tree view.

---

## 2. YAML format rules

```yaml
Screens:
  ScreenName:
    Properties:
      Fill: =C_Bg
      OnVisible: |-
        =Set(varSaving, false);
        Refresh(MyList)
    Children:
      - conRoot_X:
          Control: GroupContainer@1.5.0
          Variant: AutoLayout
          Properties:
            Height: =Parent.Height
          Children:
            - ...
```
- Every property value starts with `=`.
- A formula containing `: ` or ` #`, or spanning lines → **block scalar** `Prop: |-` then indented `=formula`.
- A formula starting with a `//` comment exports as a quoted string. Fine.
- Text literals: `Text: ="Hello"`. Empty text: `Text: =""`.
- **Studio omits default values when exporting.** When writing by hand, set `Width`, `Height`, `Size`, `Font` explicitly on every control.
- Children order = z-order. Last child is on top (put transparent tap buttons last).
- Property keys sorted alphabetically (the generator does this; keeps diffs clean).

---

## 3. Control versions that paste

| Control | Version | Notes |
|---|---|---|
| `GroupContainer` | `@1.5.0` | `Variant: AutoLayout` or `ManualLayout` |
| `Label` | `@2.5.1` | |
| `ModernButton` | `@1.0.0` | Transparent tap layer; icon buttons (`Icon: ="ChevronLeft"`) |
| `ModernIcon` | `@1.1.1` | `Icon`, `IconColor`, `IconStyle: =IconStyle.Filled` |
| `ModernText` | `@1.0.0` | |
| `Classic/TextInput` | `@2.3.2` | Search boxes, notes (`Mode: =TextMode.MultiLine`) |
| `Classic/DropDown` | `@2.3.1` | Desktop only; prefer pills |
| `Classic/DatePicker` | `@2.6.0` | |
| `Classic/CheckBox` | `@2.1.0` | |
| `Gallery` | `@2.15.0` | `Variant: Vertical` / `Horizontal` |
| `Image` | `@2.2.3` | |
| `AddMedia` | `@2.2.1` | Photo picker (make it transparent, overlay on styled button) |
| `BarcodeReader` | `@1.0.25` | Device only |
| `Button` | `@0.0.45` | Older desktop screens |
| `Timer` | `@2.1.0` | |
| `PieChart` / `LineChart` | `@2.3.0` | `BarChart@2.4.0`, `Legend@2.1.0` |
| `Rectangle` | `@2.3.0` | |

Avoid: `Classic/ComboBox` for people/patients (blank until typing).

## 4. ModernIcon / ModernButton icon names known to work

`ChevronLeft` · `ChevronRight` · `ChevronDown` · `ArrowClockwise` · `ArrowRight` · `CheckmarkCircle` · `Checkmark` · `DismissCircle` · `Search` · `Filter` · `Save` · `Edit` · `People` · `PeopleAdd` · `Person` · `BookContacts` · `Mail` · `Heart` · `Open` · `Calendar` · `Database` · `Camera` · `AppsList` · `Settings` · `Eye` · `Cart` · `Attach`

New icon name? It's Fluent UI naming. If it shows blank in Studio, pick from the list above.

## 5. Standard props blocks

**ModernButton** always carries (Studio exports these):
```
PaddingBottom: =5   PaddingLeft: =12   PaddingRight: =12   PaddingTop: =5
RadiusBottomLeft: =4  RadiusBottomRight: =4  RadiusTopLeft: =4  RadiusTopRight: =4
FontWeight: =""   Align: =Align.Center   VerticalAlign: =VerticalAlign.Middle
```

**GroupContainer** always: `DropShadow: =DropShadow.None` and all four `Radius…` set.

**Auto-layout child**: `AlignInContainer: =AlignInContainer.SetByContainer`, `FillPortions: =0` (fixed height) and `LayoutMinHeight` = `Height`.

---

## 6. Studio tips for Ben

- **Property drop-down** = top left, next to the formula bar. Pick the property (OnSelect, Items, Visible…) then edit the formula.
- **App > Formulas**: Tree view → click **App** → property drop-down → **Formulas**.
- **Refresh a data source**: Data (cylinder icon) → list → ⋯ → **Refresh**.
- **Add data**: Data → Add data → SharePoint → site → tick list.
- **Add a flow**: Power Automate icon (left rail) → Add flow.
- **Find a name everywhere**: Ctrl+F in Studio (search box in Tree view).
- **App checker**: stethoscope icon, top right.
- **Barcode scanner / camera**: only works on a device (Power Apps mobile app), not in the browser preview.
- **Publish**: File → Save → Publish this version. Users get it on next open.

---

## 7. Renaming / `_1` cleanup

If `_1` names appear: the screen was pasted next to an old copy. Fix: delete the pasted screen, delete the old one, re-paste per §1. Don't rename by hand (references break).
