# 05 · SharePoint Data

Never commit exports of these lists (staff/patient data).

---

## Sites

| Site | URL | Used by |
|---|---|---|
| PhysioDreamTeam | `https://healthqld.sharepoint.com/teams/PhysioDreamTeam` | Desktop dashboard, mobile equipment, training |
| DTVAuditing | `https://healthqld.sharepoint.com/teams/DTVAuditing` | DTV Audit app |

---

## PhysioDreamTeam lists

| List | Used by | Key columns / notes |
|---|---|---|
| `Ward_4A_Shared`, `Ward_4B_Shared`, `Ward_5A_Shared`, `Ward_6A_Shared` | Desktop ward board, patient detail, mobile allocate/audit | Patient name internal `field_11` (display `Patient`); `Bed` is a **number**; `URN`, `DOB`; `PT_Users`/`OT_Users`/`SP_Users`, `PTKeys`; `EDD`, `AROC EDD` (not 6A), `NDIS` (not 6A); falls/contact/maintenance flags; AFRM diagnosis; acuity 0–4 |
| `ClinicianDirectory` | All apps | `Person` (Person; read `.Email`), `Discipline` (Choice), `Access` (Choice: Director, Team Leader, HP4, HP3, CA4…) |
| `Equipment_Inventory_SharePoint` | Equipment | `Title` = barcode; `Status` (Choice: Available, Allocated, In Service, Out of Service); `'Patient Name'`, `Physiotherapist`, `'Date Signed Out'`, `TotalDaysSignedOut`, `LastServiceDate`, `Location` (Choice), `IsActive`, `OutOfService`, `Category`, `Brand`, `Model`, `Width`/`Depth`/`Height`, `'Wheelchair Type'`, `Ward` (Choice), `URN`, `DOB` |
| `Equipment_Usage_Log` | Usage log, allocate/return | One row per sign-out / return. `EpisodeKey`, `EquipmentItemID`, `EventDateTime`. Cleaned at 4999 |
| `Equipment_Audits` | Mobile audit, audit oversight/coverage | Pass/fail, escalation fields (`EscalationSent` only true after the email actually goes) |
| `Service_Log` | Servicing | Full schema below |
| `Acuity_Longitudinal` | Data dashboard | `EntryDate`, `WardCode`, `AcuityScore`, `WeekStart` (calculated) |
| `TrainingSessions` | Training (3 apps) | `SessionDate`, `TrainingType`, `Capacity` (blank → 6 BLS / 8 Manual Handling), `Location`, `IsActive` (soft delete) |
| `TrainingBookings` | Training | `Title`, `SessionID`, `TrainingType`, `SessionDate`, `SlotNumber`, `BookedUserName`, `BookedUserEmail`, `BookingStatus` (Booked / Cancelled), `BookedOn` |
| `TrainingWaitlist` | Training | `Title`, `SessionID`, `WaitlistUserName`, `WaitlistUserEmail`, `WaitlistStatus` (Waiting / Removed), `AddedOn` |
| `TrainingAppPermissions` | Training | `Person`, `Access` (Director, Team Leader, HP4 = managers) |
| `Home_Colors_Shared` | Desktop home | |
| `Discipline_Team_Notes` | Team info | Save/Discard (no save on every keystroke) |
| Outlook calendar `STARSPhysioLeave` | Leave screen, My Day | Read only |
| Team Brief document library | Physiotherapy_Screen | Read via flow `GetTeamBriefFiles` |

### `Service_Log` schema
| Column | Type | Notes |
|---|---|---|
| Title | Text | barcode |
| EquipmentItemID | Number | |
| Category, Brand, Model, Width, Depth, Height, WheelchairType | Text | snapshot of the item |
| ServiceType | Choice | Full service, Repair, Safety check, Other |
| ServiceStatus | Choice | In Service, Completed (**index**) |
| SentDateTime | Date+time | (**index**) |
| SentByName, SentByEmail | Text | |
| DaysInUseAtSend | Number | |
| SendNotes | Multi-line plain | |
| ReturnedDateTime | Date+time | |
| ReturnedByName, ReturnedByEmail | Text | |
| Outcome | Choice | Serviced and returned to stock, Repaired and returned to stock, Condemned - out of service (plain hyphen) |
| ReturnNotes | Multi-line plain | |
| DaysAtService | Number | |
| SourceApp | Choice | Mobile, Web |

Servicing rules: send → item `Status = In Service` + new log row (hidden from Find). Return → `Available` (or condemned: `Out of Service`, `OutOfService = Yes`, `IsActive = No`), `LastServiceDate = today`, Full service resets `TotalDaysSignedOut` to 0, location recorded.

---

## DTVAuditing lists

| List | Notes |
|---|---|
| `DTV_Register` | **Imported from Excel → `field_N` internal names** (sort by `"field_2"`). Columns: `Title` (asset tag e.g. QH12745661), `DisplayName`, `Department`, `DTVLocation`, `Building`, `Floor`, `Stream`, `LoginAccount`. Stream values: **Internal Medicine & Emergency**, **Women's, Cancer & Mental Health**, **Surgical & Critical Care**, **All** (shared, shows under every filter). Small list (<500) → device filtering OK |
| `Audit_Results` | One row per audit. `Title`, `DisplayName`, `Stream`, `DTVFound`, `LoginWorked`, `LoginFailReason`, `LoginNotes`, `PatientListWorked`, `PrintWorked`, `PrintFailReason`, `PrintNotes`, `FolderFound`, `ContentsListInFolder`, `KitMatched`, `MissingItems`, `ExtraItems`, `SpokeTo`, `EducationGiven` (multi-choice: Downtime Escalation Pathway, Downtime Process, Downtime Coordinator, Key's Location, DMN Resourcing Page), `IssuesRaised`, `Notes`, `AuditPhoto` (Image), `ReAudit` (text: blank / "Yes"). Who/when = `Created By` / `Created` |

---

## Growth and cleanup

SharePoint list view threshold = 5000. Flow **`Data_Cleanup_All_Lists`** runs daily 02:30:
- `Acuity_Longitudinal`, `Equipment_Audits`, `Service_Log` (Completed only), `Equipment_Usage_Log`: at **4999** rows, archive oldest **1000** to CSV in `Shared Documents/Usage Log Archive`, then recycle bin (93 days).
- `TrainingBookings`, `TrainingSessions`: remove sessions older than **12 months**.
- Tested on the usage log only → verify others (see `OPEN_ITEMS.md`).

**Recommended indexes:** `ServiceStatus`, `SessionDate`, `EpisodeKey`, `EquipmentItemID`, `EventDateTime`, `SessionID`, `BookingStatus`, `WaitlistStatus`, `SentDateTime`. (`ID` and `Created` are always indexed.)
How: list → ⚙ Settings → List settings → Indexed columns → Create a new index → pick column → Create.

---

## Adding a column (steps for Ben)

1. Open the list in SharePoint → **+ Add column** → pick type.
2. Name it **exactly** as given (no spaces unless stated; names are case-sensitive in formulas).
3. Choice columns: type each choice on its own line, exact spelling.
4. **Save**.
5. In Studio: **Data** (cylinder) → the list → **⋯ → Refresh**.
6. Image column: same steps, type **Image**.

New list: **+ New → List → Blank list**, name exactly, then add columns. Then Studio: Data → Add data → SharePoint → site → tick list.
