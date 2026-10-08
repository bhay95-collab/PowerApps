# 00 · New Build Playbook

The workflow for any new screen, app, feature or fix. Follow it in order.

---

## 1. Before writing anything: questions to ask Ben

Ask only what you can't find in the repo. Use multiple-choice where possible.

**Purpose**
- Who uses it? (all physios / managers only / auditors / one person)
- What decision or task does it make faster? What do they do today instead?
- Phone, desktop, or both? (decides sizing system: `UI` vs `SX/SY`)

**Data**
- Which SharePoint site and list? Does the list exist yet? (check `05_SHAREPOINT_DATA.md`)
- New columns needed? Exact name + type + choices. (Ben creates them; give exact steps.)
- Is any column imported from Excel? (→ `field_N` internal names)
- Expected size of the list in 1 year? (>2000 rows → delegation matters; >4999 → cleanup flow)
- Who/when is recorded? (use SharePoint `Created` / `Created By`, never `Modified`)

**People**
- Who gets emails/alerts? Exact addresses or a role lookup in `ClinicianDirectory`?
- Who can see manager tools? (role list from `ClinicianDirectory.Access` or a permissions list)

**Behaviour**
- What happens on fail / error / no connection?
- Anything destructive? (needs a confirm step)
- Does it repeat logic already in another app? (reuse, don't copy a 6th time)

**Push back** if: the idea duplicates an existing screen, stores data that SharePoint already records, adds a dropdown where pills fit, puts patient data somewhere unnecessary, or adds a manual step a flow could do.

---

## 2. Design

1. Sketch the screen as the anatomy in `01_DESIGN_SYSTEM.md` §5: header → body cards → (gallery) → sticky footer.
2. Pick components from `04_COMPONENT_RECIPES.md`. Don't invent new patterns when a recipe fits.
3. Name controls `<type><Thing>_<ScreenSuffix>` (e.g. `btnSave_Aud`, `lblHdrT_Hm`, `conCard_Sel`, `galRows_Sel`). Suffix keeps names unique across the app.
4. Variables: `var` = global (`Set`), `loc` = context (`UpdateContext`), `col` = collection. Screen-specific prefixes are fine (`wd…` on Ward_All).
5. Write the state list: every variable the screen sets, and where each is reset (OnVisible).

---

## 3. Build

**Mobile/DTV-style screens:** prefer generating with the Python helpers (`tools/dtv_generator/dtvgen.py`) — see `09_TOOLS.md`. The helpers emit correct YAML (block scalars, `=` prefixes, padding/radius defaults).

**Desktop screens:** draw at 1366 × 768, then run `tools/make_responsive.py`.

**Hand-written YAML:** start from `templates/Template_Screen.pa.yaml` or a real screen. Set Width, Height, Size, Font explicitly on every control (Studio omits defaults).

**Logic rules** (all in `02_POWER_FX_RULES.md`):
- Save → `Set(varSaving, true)` → Patch → check `Errors()` → then log / notify / navigate → reset `varSaving` on every path.
- Re-read with `LookUp` before status checks.
- Shared logic in one hidden button, called with `Select()`.
- Form completeness in one place (submit button's `DisplayMode`).

---

## 4. Check before handing over

- [ ] `python3 tools/preview/validate.py <file>` → `dups []`, `dupkeys 0`, `unbalanced 0`.
- [ ] `python3 tools/preview/sim.py <file> 375 700 out.png` then `python3 tools/preview/shoot.py out.html` — look at it at 375 wide (and 360×640). Nothing clipped, no "…".
- [ ] Every card that grows: `Height` = `LayoutMinHeight`, every state's bottom edge + 18 px fits.
- [ ] Every text fits one line at 375 wide (or is made for two lines).
- [ ] Every Patch has an `Errors()` check. Every save button has `!varSaving`.
- [ ] Every variable the screen relies on is reset in OnVisible.
- [ ] No staff/patient data in files you commit.
- [ ] Re-read own diff adversarially: what would make Studio reject this?

---

## 5. Hand over to Ben

Give, in this order:
1. **SharePoint changes first** (if any): list → column name → type → choices. Then "Data → list → ⋯ → Refresh".
2. **App > Formulas** additions (only the missing lines, or "paste whole file").
3. **Screens**, one at a time, with the delete → blank → rename → Paste code steps.
4. **Flows**: Import Package (Legacy) steps + "re-pick each red list".
5. **Test list**: numbered, what to tap, what should happen.
6. Link each file on GitHub (Raw button).

Template for the screen step:
```
1. In Studio, Tree view: right-click <ScreenName> → Delete.
2. + New screen → Blank.
3. Right-click the new screen → Rename → type exactly: <ScreenName>
4. Open <GitHub link> → click Raw → Ctrl+A, Ctrl+C.
5. In Studio, right-click <ScreenName> → Paste code.
6. ⋯ next to the screen → Run OnVisible.
7. Ctrl+S.
```

---

## 6. After

- Update `08_APPS_INVENTORY.md` (new screen/purpose), `05_SHAREPOINT_DATA.md` (new list/columns), `OPEN_ITEMS.md`.
- New gotcha learned? Add it to `02_POWER_FX_RULES.md` or `03_STUDIO_AND_YAML.md`. **This is how the knowledge base stays useful.**
- Commit + push to the working branch.
