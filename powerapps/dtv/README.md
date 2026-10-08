# DTV Audit app (mobile)

Four screens drawn in the same style as the equipment app: `DTV_Home`, `DTV_SelectDTV`, `DTV_Audit`, `DTV_Done`.
Control names, variables and the Audit_Results fields are unchanged except where listed below.

## What changed
- Teal gradient header (HeaderImage) on every screen. Sub-screens use the compact 95-high header.
- **SelectDTV**: the list started at Y = 193, so it sat on top of the search box and count. It now sits in the same vertical layout as the other lists, so it always fills the space under the search. The big "tap to switch" bar became a two-button switch (My Stream / All DTVs). Search now also looks at department, location and asset (the hint already said so). "No DTVs" message when the list is empty. Chevron on each row.
- **Audit**: each question is now a white card (same as the Item screen). Spacing is the same everywhere. Submit is a fixed bar at the bottom, always visible, and says "Answer every question to submit" until the form is complete. The long "is the form complete" test was copied three times; it is now in one place (btnSubmit_Aud.DisplayMode). A double tap can no longer save two audits (varSaving).
- **Photo (optional)**: a new card on the Audit screen. Add Photo opens the camera / photo library, a small preview shows with Remove Photo. The photo is saved into the `AuditPhoto` Image column AFTER the audit row is saved (same method as the Exercise app: patch the Image control's `.Image`, not the Add picture `.Media`), so a failed photo never loses the audit.
- **Home**: "Your stream" and the amber warning are one card. Start an Audit opens All DTVs straight away if you have no stream.
- **Done**: shows what was saved (login / print / kit result).

## One-time step for photos
In `Audit_Results` add a column: **+ Add column → Image**, name it exactly `AuditPhoto`. Then in Studio: Data → Audit_Results → ⋯ → Refresh. Do this BEFORE pasting the Audit screen.

## Questions added from the other team's form (Oct 2026)
- **1 · DTV**: Could you find the DTV? (No skips Login, Patient List and Print) → `DTVFound`
- **2 · Login and Patient List**: after Login = Yes, "Could you open the patient list?" → `PatientListWorked`
- **4 · Kit and Folder**: starts with "Yellow folder and kit found?" (No skips the contents questions) → `FolderFound`
- **5 · Staff and Education**: Who did you speak to → `SpokeTo`; Education given, tick any of Downtime Escalation Pathway / Downtime Process / Downtime Coordinator / Key's Location / DMN Resourcing Page → `EducationGiven` (multi-select Choice, values must match exactly); Issues raised by staff → `IssuesRaised`

## Progress and list refresh
- **Home**: Your Stream card shows "x of y audited in the last month" with a bar (green when complete). All DTVs tile shows the site-wide count.
- Scan / type tag was tried and removed.
- The list of audited DTVs is re-read from SharePoint (`Refresh(Audit_Results)`) each time Home or Choose a DTV opens, and a submitted DTV is taken off the list straight away (added to `colRecentAudits` on save).

## Stream filter (one row of pills)
Choose a DTV has one row of equal-width pills under the search box: **My Stream** (only if you belong to a stream), one pill per other stream (short name = text before the first "&" or ","), and **All**. No sideways scrolling, nothing cut off. The streams are read from the `Stream` column of `DTV_Register`, so a new stream appears automatically. DTVs with Stream = "All" show under every filter. `varShowAll` + `varStreamPick` drive the filter; both reset when you go back to Home.

## Re-audit
- SharePoint: `Audit_Results` gets a Single line of text column `ReAudit`. Blank = normal audit, "Yes" = re-audit.
- Home: **Re-audit** tile → `ReAuditList` (`DTV_ReAuditList.pa.yaml`): the latest audit of every DTV in the last month, any stream. **Needs Follow-up** (default) shows only DTVs whose latest audit had a failure; **All Audited** shows all. Red bar = needs follow-up, green = all clear.
- Picking a DTV opens the normal **Audit** screen in re-audit mode (`varReaudit`): header says Re-audit, an amber card shows what failed last time, Back returns to the re-audit list, and the save writes `ReAudit = "Yes"`. Done screen offers "Re-audit Another DTV".

## Text sizes
Power Apps text Size is in points (1 pt = 1.33 px), so every font is now about 25% smaller than the first version, and long wording was shortened, so nothing is cut off with "..." on a phone.

## Paste order
Control names are shared by the whole app, so delete the old screen first or Studio adds `_1` to every name.
1. Add `App_Formulas_additions.txt` lines that are missing.
2. For each screen: copy the old screen's code somewhere safe, delete the screen, add a blank screen, rename it exactly `Home` / `SelectDTV` / `Audit` / `Done`, paste the new file with Paste code.
3. Run the app: Home → Start → pick a DTV → fill in → Submit.

## Dashboard (Oct 2026)
- New screen `Dashboard` (`DTV_Dashboard.pa.yaml`, built by `tools/dtv_generator/dashbuild.py`). Home has a new **Dashboard** tile.
- Built for a desktop browser; under 1000 wide everything stacks in one column.
- Needs: App > Formulas lines `C_Teal`, `DashW`, `DashX`, `DashWide`, `DashGap` (end of `App_Formulas_additions.txt`); the **Office 365 Outlook** connector; Settings → General → Data row limit **2000** ("All Time" reads up to that many audits).
- Final state only: each DTV counted once, using its latest audit in the period. Default period: All Time.
- Email button: branded summary (KPI tiles, results by check, why it failed, coverage by stream, newest 30 follow-ups) + `DTV_Audits_<date>.csv` with one row per DTV (latest audit, plus how many audits it has had) in the chosen period and stream. Sent to the signed-in user only.
