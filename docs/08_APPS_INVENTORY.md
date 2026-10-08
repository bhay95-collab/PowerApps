# 08 · Apps Inventory

Organisation: Queensland Health, STARS (Surgical, Treatment and Rehabilitation Service), physiotherapy team.

| App | Platform | Purpose | Screens | Folder | Sizing |
|---|---|---|---|---|---|
| **Physio Dashboard** | Desktop / browser | Ward boards, patient detail, equipment, discharge, team info, data, leave, training, manager tools | 20 | `powerapps/desktop/` | SX/SY/SF/SR |
| **STARS Equipment** | Phone / tablet | Scan, find, allocate, return, audit, service equipment; training | 11 (M1–M11) | `powerapps/mobile/` | UI/PageW |
| **Physiotherapy Training Register** | Any (stand-alone) | Book BLS and Manual Handling | 2 | `powerapps/training/` | Wide/UI |
| **DTV Audit** | Phone | Audit ieMR Downtime Viewers | 5 | `powerapps/dtv/` (generated) | UI/PageW |
| **Flows** | Cloud | Training emails, reminders, waitlist, cleanup, Team Brief | 8 | `powerapps/flows/` | — |

Linked web tools (GitHub Pages, opened from desktop buttons): equipment prescription support (`bhay95-collab.github.io/stars-wheelchair-prescription/`), basic outcome measures (`bhay95-collab.github.io/basic-outcome-measures/`). Staff Movement Tracker (`index.html` in `bhay95-collab/staff-movements`) is the original visual reference for the ward board.

---

## Physio Dashboard (desktop)

App.Formulas: `Desktop_App_Formulas.txt` (SX/SY/SF/SR, MeEmail, MeName, CanManageTraining, EmailHead/EmailFoot). App.OnStart: `App_OnStart.txt` (old-equipment warning, `varChartPalette`, `varSelectedPatient`, `colEmailRecipients`, `colStaffRatios`, `colDiagnosisMap`).

| Screen | Purpose |
|---|---|
| `Home_Main` | Ward tiles (beds, patients, acuity, EDD ≤ 3 days); bottom bar: Equipment · My Day · Discharge Planner · Team Info · Training · Manager tools (Usage Log, Servicing, Audit Coverage, Data Health for Director/Team Leader/CA4) |
| `My_Day` | My patients, my equipment out, who is away today/tomorrow |
| `Ward_All` | One board for 4A/4B/5A/6A (`varWard`). Read-only rows + edit panel: AFRM chips, physio picker pop-up, acuity −/+ (0–4), dates, flags, Move bed (swap), Discharge, Save/Discard (optimistic lock), EDD Summary email. 6A: no NDIS, no AROC (`wdShowNDIS`/`wdShowAROC`) |
| `Handover_All` | Ward handover |
| `Patient_Detail_Screen` | Patient record, allocate / return equipment (return location + confirm) |
| `Discharge_Planner` | By EDD: overdue, next 5 working days, no EDD |
| `Equipment_Main`, `All_Allocated_Equipment`, `All_Available_Equipment` | Equipment views; email today's allocation |
| `scrAuditOversight`, `Audit_Coverage` | Equipment audit results; coverage (re-audit after 30/60/90/180 days) |
| `Usage_Log` | Manager view of usage log (no patient names) |
| `Service_Dash` | Servicing (due > 100 days in use, at service, history) |
| `Physiotherapy_Screen` | Team Brief files (via flow), team notes (Save/Discard), Manage Staff, Data Dashboard, Leave |
| `Physio_Data_New` | Ward acuity, week vs week, diagnosis pies, staffing FTE (one calc button `btnCalc_Dd`) |
| `Directory_Admin_New` | Manage staff (Director/Team Leader) → `ClinicianDirectory` |
| `PT_Leave_New` | Week view of STARSPhysioLeave calendar (multi-day leave shows each day) |
| `Data_Health` | Data problems (patients, equipment, audits) |
| `Training_Hub`, `Training_Sessions` | Training inside the dashboard |

## STARS Equipment (mobile)

App.Formulas: `App_Formulas.txt`. Data row limit 2000. Settings: Scale to fit Off, Lock aspect Off, Portrait locked.

| Screen | Purpose |
|---|---|
| M1 `Home` | Scan card (BarcodeReader), tiles, 6-week reminder card, Servicing tile (managers), Training tile |
| M2 `Find` | Barcode search, category segments, Filters sheet (size chips), results |
| M3 `Item` | One item: Allocate or Return (fresh status check, Errors guard, return location) |
| M4 `Allocate` | Pick patient (My / All / Other), bottom-sheet confirm; patients cached 10 min (`varPatientsLoaded`) |
| M5 `MyEquipment` | All / Today / 6+ weeks; email today's list |
| M6 `Allocated` | Search + ward chips |
| M7 `Availability` | Bars by width per category/type; tap → Find pre-filtered |
| M8 `Audit` | Equipment audit; FAIL emails treating physio |
| M9 `Servicing` | Managers: send for service, take back, due list |
| M10 `Training`, M11 `TrainingDates` | Training hub and dates |

Roles: Director, Team Leader, CA4 → manager tools. Training managers from `TrainingAppPermissions` (Director, Team Leader, HP4).

## DTV Audit

Source = generators `tools/dtv_generator/dtvbuild.py` (Home, SelectDTV, ReAuditList, Audit, Done) and `dashbuild.py` (Dashboard) → `powerapps/dtv/*.pa.yaml`. Needs Office 365 Outlook connector and data row limit 2000. `varStream` set in App.OnStart.

| Screen | Purpose |
|---|---|
| `Home` | Start an Audit (your stream, or all if none), Your Stream progress, All DTVs tile, Re-audit tile, Dashboard tile. OnVisible builds `colRecentAudits`, `colAllTags`, counts/percentages |
| `SelectDTV` | Search; one row of pills (My Stream / other streams / All) from `colPills`; hides DTVs audited in last month |
| `ReAuditList` | Latest audit per DTV in last month (`colReaudit`); Needs Follow-up / All Audited; red/green stripe |
| `Audit` | Re-audit amber card; info; 1 Found · 2 Login + Patient list · 3 Print · 4 Kit + Folder · 5 Staff + Education · 6 Photo · Notes; sticky submit; writes `ReAudit` |
| `Done` | Thank you + result line; Audit Another; Home |
| `Dashboard` | Desktop-first (one column under 1000 wide). Filters: period (7 / 30 / 90 days / all) + stream. KPI tiles (audits, DTVs covered, all clear, need follow-up, not found), results by check, why it failed (print/login reasons), coverage by stream, education given, top auditors, audit list with search. Tapping a tile, check, reason, stream or auditor filters the list. **Email Me the Data**: branded summary + CSV of every audit in the period/stream. Counts **every audit** (Ben's choice), not latest per DTV. Source: `tools/dtv_generator/dashbuild.py` |

Rule: any audit in the last month (rolling) drops the DTV off the to-do list — including "not found" (decision pending).
Manual Studio edits already mirrored in repo: `lblRemovePhoto_Aud.Color = RGBA(176, 52, 40, 1)`; Home OnVisible `Set(varStreamPick, Blank())`; `lblProg_Hm` ends "audited".

## Training Register (stand-alone)

`Home` + `scrTrainingSessions`. Two columns ≥ 820 px. Re-checks capacity and clashes (later booking cancelled), waitlist, soft delete, branded emails. Needs `varCanManageTraining` set in OnStart. Same logic also in desktop `Training_Hub/Sessions` and mobile M10/M11 — **three copies**, change all three.
