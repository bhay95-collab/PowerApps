# 02 · Power Fx Rules (learned the hard way)

Each rule exists because something broke. Follow them by default.

---

## 1. Saving data

### Always check `Errors()` after a Patch
```
Patch(List, rec, { Status: { Value: "Allocated" } });
If(
    !IsEmpty(Errors(List)),
    Notify("Could not save. Check your connection and try again.", NotificationType.Error),
    // only now: write log rows, show success, navigate
    Patch(Log, Defaults(Log), { ... });
    Notify("Saved.", NotificationType.Success)
)
```
Without it, log rows and "success" happen even when SharePoint refused the update.

### Re-read before checking status (stale records)
A record read earlier (gallery `ThisItem`, a variable) can be out of date. Another person — or a double tap — may have changed it.
```
With(
    { fresh: LookUp(Equipment_Inventory_SharePoint, ID = varItem.ID) },
    If(
        fresh.Status.Value <> "Available",
        Notify("Someone allocated this a moment ago.", NotificationType.Warning),
        Patch(Equipment_Inventory_SharePoint, fresh, { ... })
    )
)
```
**Swaps** (e.g. move bed): capture both values first, then patch both.

### Double-tap guard
```
// button DisplayMode
If(<form valid> && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)
// button OnSelect
Set(varSaving, true);
... save ...
// reset on EVERY path: success, failure — and in screen OnVisible
Set(varSaving, false)
```

### Optimistic lock (multi-user edit boards)
Keep `Modified` in the collection when loading (`Modified: Modified`). On save, refuse a row if SharePoint's copy is newer; after a good save, store the new `Modified`:
```
If(
    !IsBlank(w.ID) && !IsBlank(w.Modified) && LookUp(Ward_4A_Shared, ID = w.ID).Modified > w.Modified,
    // changed by someone else since load → collect for a message, don't save
    ...,
    With({ spRow: Patch(Ward_4A_Shared, ...) },
        Patch(colWard, w, { ID: spRow.ID, IsDirty: false, Modified: spRow.Modified }))
)
```
Show a message; Discard reloads. (Real code: `powerapps/desktop/Ward_All.pa.yaml`, Save.)

### Save record first, photo second
```
With(
    { rec: Patch(Audit_Results, Defaults(Audit_Results), { ...fields... }) },
    If(
        IsEmpty(Errors(Audit_Results)),
        If(!IsBlank(addPhoto.Media),
            Patch(Audit_Results, rec, { AuditPhoto: imgPhoto.Image });
            If(!IsEmpty(Errors(Audit_Results, rec)), Notify("Saved, but the photo could not be attached.", NotificationType.Warning))
        );
        Navigate(Done, ScreenTransition.Cover),
        Notify("Could not save.", NotificationType.Error)
    )
)
```
A failed photo never loses the record.

### SharePoint Image column
Patch the **Image control's `.Image`**, not the AddMedia `.Media` (`.Media` → "Record expected, Text found").

### Soft delete
Set `IsActive = false` instead of `Remove()`. History stays; filter `IsActive` everywhere.

---

## 2. Column types

| Type | Read | Write |
|---|---|---|
| Choice | `x.Status.Value` | `{ Value: "Allocated" }` |
| Multi-select choice | `Concat(x.EducationGiven, Value, ", ")` | `ForAll(colEdu As e, { Value: e.Value })` (values must match choices **exactly**) |
| Person | `x.'Created By'.DisplayName`, `.Email` | (claims record — avoid writing; store name/email as text) |
| Number | `Text(x.Bed)` | number |
| Image | `x.AuditPhoto` | `imgControl.Image` |

**Columns imported from Excel** have internal names `field_N`.
- `SortByColumns`, `ShowColumns` need the **internal** name: `SortByColumns(DTV_Register, "field_2", SortOrder.Ascending)`.
- Filters and formulas accept display names.
- `ShowColumns(DTV_Register, Title, Stream)` broke `Stream` → copy the whole list instead: `ClearCollect(col, DTV_Register)`.
- Find internal name: list settings → click column → end of URL `Field=field_2`.

**Who / when:** use SharePoint's own `Created` and `Created By`. Never `Modified` (changes on every edit).

---

## 3. Types and blanks

- `Coalesce` needs one type: `If(IsBlank(x.Bed), "—", Text(x.Bed))` (Bed is a number).
- **Blank is not 0.** `If(var = 0, …)` is false when `var` is blank → `x / var` divides by zero. Work ratios out once:
  ```
  Set(varPct, If(varTotal > 0, varDone / varTotal, 0));
  // read with
  Coalesce(varPct, 0)
  ```
- Define a collection's shape before filling it:
  ```
  ClearCollect(colEdu, { Value: "" }); Clear(colEdu)
  ```

---

## 4. Dates

- `DateValue(DatePicker.SelectedDate)` depends on PC language → use the date directly.
- `TimeUnit.Days`, not `"Days"`.
- "Last month" rolling: `Created >= DateAdd(Now(), -1, TimeUnit.Months)` (delegable).
- `DateDiff` on a column is **not** delegable — filter by date range first, then DateDiff on the device.
- Format: `Text(Today(), "dddd d mmmm")`, short `Text(d, "d mmm yyyy")`.
- Blank date pickers show 31/12/2001 → display "Not set" when blank.

---

## 5. Delegation (SharePoint)

Data row limit: set **2000** (Settings → General). Above that, non-delegable filters silently miss rows.

| Delegable ✅ | Not delegable ❌ |
|---|---|
| `=`, `<>`, `<`, `>` on text/number/date | `Lower(column)`, `Upper(column)` |
| `StartsWith(column, "x")` | `"x" in column` (search inside text) |
| `Created >= DateAdd(...)` | `DateDiff(column, …)` |
| `IsBlank(column)` (mostly) | `Len`, `Trim`, `Left` on a column |
| `And` / `Or` / `!` of the above | `in` against a collection (`Title in colX.Value`) |

- SharePoint `=` is **case-insensitive** → `Email = MeEmail` works without `Lower`.
- Small lists (< 500, e.g. `DTV_Register`, `ClinicianDirectory`) are fine to filter on the device — but say so in a comment.
- Large lists: delegable filter first (date window, status), then `ClearCollect` and do the rest on the collection.

---

## 6. Caching

- Power Apps reuses its copy of a list. After saving, `Refresh(List)` before re-reading.
- Also update the local collection straight away so the UI changes instantly: `Collect(colRecentAudits, { Value: tag })`.
- Expensive lists: cache with a timestamp (`varPatientsLoaded`), rebuild only if older than 10 minutes.
- Per-user lookups (`varMeDirectory`): only look up when blank.
- Don't run a SharePoint query inside every gallery row. Read once per screen open into a collection, compute on the device.

---

## 7. Logic patterns

- **`Exit()` closes the whole app on a phone.** Never use for flow control. Use `If`.
- `Select(btnX)` works on hidden buttons on the **same screen**.
- `With({ a: …, b: … }, …)` to name intermediate values instead of repeating formulas.
- `Switch(key, "A", …, "B", …, default)` for pill handlers.
- `Navigate(Screen, ScreenTransition.Cover)` forward, `ScreenTransition.UnCoverRight` back, `Fade` for tab-like switches.
- `Notify` text: short, says what to do next.
- Never set "sent"/"done" flags unless the action actually happened (old bug: `EscalationSent = true` with no email).

---

## 7b. Percentages

`Text(0.52, "0%")` gives **"1%"** in Power Apps (it does NOT multiply by 100). Write `Round(x * 100, 0) & "%"`.

## 8. Email attachments

`Office365Outlook.SendEmailV2(..., { Attachments: Table({ Name, ContentBytes: <text> }) })` is **rejected** in Studio: ContentBytes must be a file/blob, not text. To attach a CSV or text file, pass the text to a flow (Power Apps V2 trigger) and attach it there (see `DTVDashboardEmail`).

## 9. User identity

```
MeEmail = Lower(User().Email);
MeName  = User().FullName;
// first name, works for "Smith, Ben" and "Ben Smith"
With({ n: User().FullName }, If("," in n, Trim(Last(Split(n, ",")).Value), First(Split(n, " ")).Value))
```
Roles come from `ClinicianDirectory.Access` (Director, Team Leader, HP4, HP3, CA4…) or `TrainingAppPermissions`.

---

## 10. After editing Formulas / OnVisible

Run **Run OnVisible** (⋯ on the screen) in Studio to clear stale red errors. Save, close, reopen if errors persist.
