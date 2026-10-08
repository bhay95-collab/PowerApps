# Open Items

Update this file whenever something is finished, decided or added.

| # | Item | Status | Waiting on |
|---|---|---|---|
| 1 | **DTV Day 1 findings workbook** (Excel for team leads) | Rebuild from `DTV_Audit_Export_D1.xlsx`. Never commit the export or the workbook (staff names) | Ben: upload export; total DTVs per stream |
| 2 | **DTV "not found" rule** — should a "DTV not found" audit keep the DTV on the to-do list? Currently drops off for a month | Decision | Ben |
| 3 | **DTV fail alerts** — email IT / downtime coordinator / NUM when Login, Patient List, Print or Kit fails, or DTV not found | Offered, not built | Ben: who receives each alert |
| 4 | **DTV ideas** — "Report wrong DTV details" link → register-fix list; coordinator overview (coverage by stream, open failures, repeat failures, education) | Ideas | Ben: priority |
| 5 | **Desktop Leave: "Request Leave" button** → Teams Shifts time-off (ADO, Annual Leave, Sick/Carers, PDL, Other). Plan: real Shifts request via flow; fallback SharePoint list + approver email | Waiting | Ben: (1) Shifts "Create a time off request" action / Graph available in Power Automate? (2) who approves? (3) part-day times? (4) time off only? (5) how approved leave reaches STARSPhysioLeave calendar? (6) placement (suggest Leave header) |
| 6 | **Code review leftovers** — allocate/return logic in 5 places → one flow or user-defined function; SharePoint indexes; `"Days"` → `TimeUnit.Days` (8 places) | Recommended | — |
| 7 | **Verify Data Cleanup flow** on the other lists; turn off old Usage Log Cleanup | To do | Ben (in Power Automate) |
| 8 | **Desktop App.OnStart** old-equipment filter matches `Physiotherapist = User().FullName` — if Physiotherapist is a Person column, match email instead | Question | Ben: column type |
| 10 | **DTV Dashboard** — built, not yet pasted in Studio. Verify: CSV attachment arrives and opens in Excel (if Studio rejects `ContentBytes` as text, move the send to a flow); numbers match a manual count | To verify | Ben: paste + test |
| 9 | **Templates** (`templates/Template_*.pa.yaml`) generated from proven helpers but **not yet pasted in Studio** — first real use: confirm they paste clean, then remove this line | To verify | First new build |

## Day 1 DTV results (7 Oct 2026, 21 DTVs, 6 auditors) — context for item 1
- 6 all clear.
- Print failed at 8: 5 printer faults (8BN, 9BN, Gastro OPD, 6C no printer mapped, 6A North), 3 couldn't log in.
- KVM switching fault at 3 (DTC, Cardiology OPD, Cancer Care OPD).
- Kit: Palliative Care kit never delivered (asset 12604538); Cardiology OPD has Cath Lab kit, missing Folder 2; 6B Maternity missing wristbands/labels; Vaccination Service PBS script pad missing; kits stored away from DTV at DTC, Thoracic OPD, HiTH VASE.
- 1 not found: NLHP HiTH.
- Rechecks due 08/10: Maternity OPD, 6B Maternity (print); NLHP HiTH (full).
- Decisions made: print "recheck" = pending, not fail; keep all names; PBS pad missing = real kit error; coverage per stream wanted.
