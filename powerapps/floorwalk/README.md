# Floorwalking Ideas app (RBWH post go-live optimisation)

Capture ideas while floorwalking; dashboard for everyone to see what is coming in. Phone and desktop (one app).
**Generated** by `tools/floorwalk_generator/fwbuild.py` (services in `services.py`). Edit the generator, re-run, validate. Don't hand-edit the YAML.

| File | Paste as |
|---|---|
| `App_Formulas.txt` | App > Formulas (whole file) |
| `FW_Home.pa.yaml` | screen `Home` |
| `FW_Capture.pa.yaml` | screen `Capture` |
| `FW_Dashboard.pa.yaml` | screen `Dashboard` |

Data: SharePoint list `Floorwalk_Ideas` on `https://healthqld.sharepoint.com/teams/CITTA` + **Office 365 Users** (stakeholder search) + **Office 365 Outlook** (patient safety alert email).

---

## 1. SharePoint list (CITTA site)

1. Open `https://healthqld.sharepoint.com/teams/CITTA` → **+ New → List → Blank list** → name exactly `Floorwalk_Ideas` → Create.
Faster: create the list **From CSV** with `Floorwalk_Ideas.csv` (headers + one fake row to delete). At import set every column to **Single line of text** except Idea + ReviewNotes (**Multiple lines of text**) and StatusOn (**Date and time**). Then add Photo (Image) by hand.

2. Or add each column below: **+ Add column** → type → name **exactly** (no spaces) → Save.

| Column | Type | Notes |
|---|---|---|
| Title | (already there) | The one-line summary (max 120) |
| Idea | Multiple lines of text | More options → **plain text** (turn off rich text). Append changes **Off** |
| Service | Single line of text | |
| ServiceLine | Single line of text | |
| Stream | Single line of text | Set automatically from the service (floorwalker never sees it): `Surgical & Critical Care`, `Women's, Cancer & Mental Health`, `Internal Medicine & Emergency`, `Operational Support Services`, or `Other` (service with no clear stream). Blank when no service was picked |
| Location | Single line of text | |
| StakeholderName | Single line of text | |
| StakeholderEmail | Single line of text | |
| StakeholderJobTitle | Single line of text | |
| StakeholderDept | Single line of text | |
| FollowUp | Single line of text | `Yes` / `No` |
| Theme | Single line of text | `Workflow/Business Rules`, `Functionality`, `Downtime`, `Resource Development`, `Other` |
| ThemeOther | Single line of text | Only when Theme = Other |
| Priority | Single line of text | `Low` / `Medium` / `High` |
| Status | Single line of text | `New` / `Under Review` / `Actioned` / `Not Progressing` |
| ReviewNotes | Multiple lines of text | plain text, Append changes Off |
| StatusBy | Single line of text | Who last changed the review |
| StatusOn | Date and time | Include time **Yes** |
| Photo | Image | |
| Module | Single line of text | ieMR area: ESM, OERR, Medicines, Maternity, FirstNet, SAA / SurgiNet, Powertrials, Radiology, Nursing Workflows, Medical Workflows, Pathology, AH Workflows, Community, Devices, Other / Not Sure |
| SafetyConcern | Single line of text | `Yes` / `No` |
| Votes | Number | 0 decimal places, default 0. "Me Too" count |
| Voters | Multiple lines of text | plain text. Emails of people who tapped Me Too (stops double votes) |

**No Choice columns** (writing text to a Choice column turns the whole save red). Who/when = SharePoint's own `Created By` / `Created`.

Size: one row per idea. The dashboard reads the newest **2000** (Settings → General → Data row limit = 2000). Past ~1500 rows, tell Claude: add a date window.

## 2. Access
1. CITTA site → ⚙ → **Site permissions** → **Share site** → add every floorwalker (the DTV staff allocation group) → permission **Edit** (Members).
2. After publishing: app → **Share** → add the same people (or the same Microsoft 365 group).
3. First open: each person accepts the SharePoint + Office 365 Users permission prompt.

## 3. Build the app
1. make.powerapps.com → **+ Create → Blank app → Blank canvas app** → name `Floorwalking Ideas` → Format **Tablet** → Create.
2. **Settings → Display**: Scale to fit **Off**, Lock aspect ratio **Off**, Lock orientation **Off**.
3. **Settings → General**: Data row limit **2000**.
4. **Data** (cylinder) → Add data → **SharePoint** → `https://healthqld.sharepoint.com/teams/CITTA` → tick `Floorwalk_Ideas` → Connect.
5. Data → Add data → search **Office 365 Users** → add. Then **Office 365 Outlook** → add.
5b. App > Formulas: put the safety lead's email in `SafetyAlertTo = "...";` (empty = no alert email).
6. Tree view → **App** → property drop-down → **Formulas** → paste all of `App_Formulas.txt`.
7. Screens, in this order: **Capture**, **Dashboard**, **Home** (steps in `docs/03_STUDIO_AND_YAML.md` §1: + New screen → Blank → rename exactly → right-click → Paste code).
8. Drag `Home` to the top of Tree view. Delete the empty `Screen1`.
9. Each screen: ⋯ → **Run OnVisible**. Ctrl+S. App checker should be clean.
10. App icon: Settings → General → App icon (use any `powerapps/icon/` PNG or ask for a new one).
11. File → Save → **Publish**.

## 4. Test
1. Home: "Hi <name>", Capture hero, Dashboard + My Ideas tiles (no Today card).
2. Capture an Idea → Submit is grey ("Add a theme, idea and priority").
3. Tap Service → type `cath` → pick Cardiology - Cardiac Cath Lab. No stream shown on the form. After saving, SharePoint Stream = **Internal Medicine & Emergency**. An idea saved with no service has Stream blank.
4. Stakeholder → type 3+ letters of a colleague's surname → rows show name + job title + department → pick → follow-up Yes/No appears.
5. Clear (✕) → "Not in the Directory? Type a Name" → type → follow-up Yes → amber "No email" note.
6. Theme Other → text box appears. Type idea, pick High → Submit → "Idea Saved". Check the row in SharePoint (Created By = you).
7. Capture Another → form empty. Back to Home → Today = 1.
8. Dashboard on desktop: tiles + 5 panels side by side; on phone: one column. Tap stream / theme / status / tile → list filters, "Showing: … Clear ✕".
9. Tap an idea → detail. Email Stakeholder opens Outlook. Change status to Under Review + note → Save Changes → Saved, tile counts change.
10. Open the same idea on two devices, save on one, then save on the other → "Someone updated this idea…" warning.

## Oct 2026 additions
- **One-line summary** (Title) is required; detail is optional.
- **Duplicate check**: as the summary is typed, up to 3 similar ideas show (2+ matching words of 4+ letters, common words ignored). **Me Too** adds a vote (`Votes`, `Voters`) instead of a duplicate; one vote per person; the dashboard detail has the same button.
- **ieMR area** pills (CITTA Apps and Functions Portfolios). Dashboard panel "ieMR AREAS".
- **Patient safety**: Yes shows "Report it now" (RiskMan + Service Desk) and emails `SafetyAlertTo` on save. Dashboard tile "SAFETY CONCERN".
- **Offline**: no signal → Submit says "Save on This Phone"; the idea (and photo) is kept with SaveData and uploaded from Home (auto when Home opens with signal, or Upload Now). Created date = upload time. Works in the Power Apps phone app; the browser can't store offline.

## Service map
`tools/floorwalk_generator/services.py`: 262 services at sub-service level (e.g. `Cardiology - Cardiac Cath Lab`, `Pharmacy Services - Oncology Pharmacy`) from the **Service Allocations** sheet of the RBWH Stakeholder Directory & Allocations workbook (Oct 2026). Spelling fixed, duplicates removed. Each row carries its **RBWH CITTA Stream** from that sheet:
Surgical & Critical Care 83 (incl. all Allied Health) · Women's, Cancer & Mental Health 86 (incl. A&TSI Health) · Internal Medicine & Emergency 62 · Operational Support Services 31.
The stream is saved behind the scenes; the Capture form doesn't show it. No service → stream blank (dashboard shows "No service"). Dashboard pills: the 4 streams; the By Stream panel also lists Other and No service.
