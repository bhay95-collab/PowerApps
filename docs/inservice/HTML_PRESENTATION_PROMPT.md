# Prompt: build the inservice HTML presentation tool

Copy everything below the line into a new chat.

---

## 1. Your job

Build **one self-contained HTML file** that I (Ben) will present from a Queensland Health laptop on a projector. It is a slide deck with interactive pages built in. It supports a 60-minute inservice called:

**"SharePoint, Lists and Power Apps: from problem to app"**

Give me the complete file in one code block (or as a downloadable file). I am new to coding: after the file, give me numbered steps to save it, open it, and present it.

## 2. Who I am, who the audience is

- Me: Ben, Clinical Informatics Officer, Digital Metro North (Queensland Health). Physiotherapist by background. I have built several Power Apps on SharePoint lists (details in §8).
- Audience: **Clinical Informatics Officers (CIOs), Digital Metro North.** Clinicians by background, digitally confident, use Teams and SharePoint files every day, **have never built a SharePoint list or a Power App.** They know ieMR, downtime viewers (DTVs) and **floorwalking** (supporting wards during go-lives).
- Their goal: leave knowing (1) where SharePoint and Lists live, (2) which column type to pick and why, (3) **how to think through a problem into lists and columns before building anything**, (4) that a basic Power App is 10 minutes away.
- Tone: practical, plain English, short sentences. No marketing language. Clinical examples, not business/sales examples.

## 3. Hard technical rules (the QH network blocks a lot)

1. **One `.html` file. Works fully offline.** No CDN scripts, no Google Fonts, no external images, no frameworks. Plain HTML + CSS + vanilla JavaScript, all inline. Icons = inline SVG.
2. Font: `"Segoe UI", system-ui, sans-serif`.
3. Must run in **Microsoft Edge** opened by double-clicking the file (`file://`). No server, no build step, no `fetch()` of local files, no ES module imports.
4. **16:9 stage** (design at 1920 × 1080) scaled to fit the window with letterboxing, so it looks the same on any projector.
5. Readable at the back of a room: body text ≥ 28 px at 1920 wide, titles ≥ 56 px, max ~6 bullets per slide, high contrast.
6. Light theme (projectors wash out dark themes). Palette — use only these:

| Token | Hex | Use |
|---|---|---|
| ink | `#0E1C2A` | main text |
| ink-2 | `#3A5068` | secondary text |
| muted | `#8C9BAE` | captions |
| bg | `#EBF2F8` | page background |
| bg-2 | `#F4F9FC` | soft panels, table headers |
| line | `rgba(14,42,70,0.12)` | borders |
| white | `#FFFFFF` | cards |
| accent | `#1A5A99` | buttons, links, highlights |
| accent-soft | `rgba(26,90,153,0.10)` | chips |
| good / good-bg | `#0C7A52` / `#E8F6F0` | pass, "do" |
| danger / danger-bg | `#B41A1A` / `#FEF2F2` | fail, "don't" |
| amber / amber-bg | `#B26900` / `#FFF6E5` | warning, gotcha |
| teal | `#009099` | secondary accent |
| header gradient | `#001D46 → #075F73 → #00838A` | title bars, section dividers |

7. **Neutral look.** No Queensland Health or Metro North logos, crests or official templates. Don't claim to be official material.
8. **No real data.** Every name, ward, URN, patient, staff member and ticket number must be obviously fictional (e.g. "Ward 7Z", "Alex Example", "INC0000123").
9. Keep code tidy and commented by section so I can edit slide text later. Put **all slide content in one clearly marked JavaScript array or in clearly separated `<section>` blocks** at the top so I can change wording without touching logic.
10. Must not break if `localStorage` is blocked: wrap every read/write in `try/catch`.

## 4. Presenter features

| Key / control | Action |
|---|---|
| → / Space / PageDown / click right half | next slide (or next build step if the slide reveals bullets one by one) |
| ← / PageUp / click left half | previous |
| Home / End | first / last |
| `F` | fullscreen toggle |
| `N` | speaker notes panel toggle (bottom overlay, my eyes only — I'll mirror screens, so notes must be hideable instantly) |
| `O` | overview grid of all slides, click to jump |
| `T` | show / hide session timer (counts up from when I press it, shows section target time, turns amber when over) |
| `P` | print the cheat sheet (§7) |
| `Esc` | close any overlay |

- Progress bar along the bottom, coloured by section (SharePoint / Lists / Thinking / Build / Wrap).
- Slide number + section name in a small footer.
- URL hash per slide (`#12`) so refresh keeps my place.
- Keyboard nav must **not** fire while typing in an input on an interactive slide.
- Every slide has speaker notes (2–6 lines: what to say, what to click, timing).

## 5. Run sheet (60 min) and slide content

Target timings per section. Write the slides below; you may split a slide into two if it is crowded, but keep the timings.

### A. Opening (3 min)
1. **Title slide.** "SharePoint, Lists and Power Apps: from problem to app". Subtitle: "Digital Metro North · CIO inservice · January 2027". Presenter: Ben (placeholder I can edit).
2. **The hook.** "Every one of us has a spreadsheet, a paper sheet, or a Teams chat doing a job a small app could do better." Three icons: paper floorwalking sheet → Excel on a shared drive → app on a phone. Notes: ask the room "Who has a spreadsheet that more than 3 people edit?"
3. **Today's map.** 4 blocks with times: SharePoint basics (10) · Lists (15) · Thinking before building (15) · Build it live (12) · wrap (5).

### B. SharePoint basics (10 min)
4. **Every Team has a SharePoint site behind it.** Diagram: a Teams team → its SharePoint site → Documents library (= the Files tab) + Lists + Pages. Channels = folders in Documents. Private and shared channels get their own separate site. Notes: open a Team → Files → "Open in SharePoint" to show it live.
5. **Site contents = where everything lives.** Show path: ⚙ (Settings) → **Site contents**. Explain: lists, document libraries, pages, recycle bin all live here. Tip box: shortcut — add `/_layouts/15/viewlsts.aspx` to the site URL.
6. **Library vs List.** Two-column compare. Library = files (Word, PDF, images), versions, co-authoring. List = rows and columns of data, like a smart table: every row has an ID, who made it, when. "If you'd put it in a spreadsheet row, it belongs in a List."
7. **SharePoint tips that save you** (one per card, 6 cards):
   - Recycle bin keeps deleted items for **93 days** (site bin, then second-stage bin).
   - **Version history** on files and list items: restore an older version.
   - **Share a link vs give access**: sharing a file ≠ access to the site. Check "Manage access".
   - **Follow** a site (☆) so it shows on the SharePoint start page.
   - Add a list or library as a **tab in Teams**.
   - **Edit in grid view** on a list = edit like Excel; **Export to Excel** for a quick report.
8. **Quick check (interactive).** 3 multiple-choice questions, click to reveal answer + one-line explanation (green/red). E.g. "Where do you find a list you can't see in the menu?" → Site contents.

### C. Lists (15 min)
9. **What a list gives you for free.** ID, Title, **Created**, **Created By**, Modified, Modified By, version history, views, filters, permissions, mobile access, works with Power Apps and Power Automate. Key point: **never make your own "Date entered" or "Entered by" column — SharePoint already records Created and Created By.** Use Created, not Modified (Modified changes on every edit).
10. **Column types (interactive explorer).** Left: a grid of type tiles. Click one → right panel shows: what it stores, a clinical example, ✅ good for, ⚠ watch out (Power Apps gotcha). Cover:

| Type | Example | Good for | Watch out |
|---|---|---|---|
| Single line of text | Ward, asset tag, ticket number | Most things. Fast, simple, easy for Power Apps to read and write | 255 character limit |
| Multiple lines of text | Issue description, notes | Free text | Use **plain text**, not rich text, if an app writes it. Can't sort/filter on it well |
| Choice | Severity: Low / Medium / High | Fixed short lists people pick in SharePoint | In Power Apps you read `.Value` and must write `{ Value: "High" }`. Writing plain text to a Choice column breaks the whole save. If an app writes the value, a Single line of text is often simpler |
| Number | Bed number, minutes spent, count | Maths, sorting, totals | Blank is not 0 |
| Yes/No | Resolved on the spot? | One clear yes/no question | Default value matters — decide it |
| Date and time | Go-live date, follow-up due | Filtering by date ranges, overdue | Time zones; "date only" vs "date and time" — pick on purpose |
| Person or Group | Escalated to | Picking a staff member in SharePoint | Hard for apps to write. Apps often store name + email as text instead |
| Lookup | Issue → Location from a Locations list | Linking two lists | More than 12 lookup/person columns in a view causes errors; keep few |
| Hyperlink | Link to a KB article | Links | — |
| Image | Photo of the error screen | Evidence | Power Apps can write it from the camera control |
| Calculated | Days open | Display only | Read-only; filtering on it in Power Apps doesn't scale |

11. **Name columns like a developer.** Name a column `EscalatedTo` first (no spaces, no symbols), save, then rename the display name to "Escalated To" if you want. The **internal name is set forever when you create it**. Example of the trap: lists imported from Excel get internal names like `field_2`. Show how to find the internal name: List settings → click the column → end of the URL `Field=...`.
12. **List settings worth knowing.** Path: ⚙ → **List settings**. Cards:
    - **Required** fields and **default values** (set per column).
    - **Column validation** (e.g. follow-up date must be after today).
    - **Versioning settings** (keep history of edits).
    - **Indexed columns** (see next slide).
    - **Views**: saved filters/sorts/groups, e.g. "Open issues by ward".
    - **Permissions** for this list (who can see/edit).
    - **Rules** ("Automate → Create a rule") for simple email notifications when something changes — no Power Automate needed.
    - **Conditional formatting** ("Format this column") to colour severity or status.
13. **The 5,000 rule (interactive).** Slider: number of rows in a list (0 → 50,000). Show what happens: under 2,000 = fine everywhere; over 2,000 = Power Apps can silently miss rows unless filters "delegate" to SharePoint; over 5,000 = SharePoint views can fail unless the filter/sort column is **indexed**. Text: "Index the columns you filter or sort by (status, date, location). Max 20 indexes per list. Add indexes **before** the list gets big." Path: List settings → Indexed columns → Create a new index.
14. **Big list habits.** Archive old rows (a scheduled flow can move rows older than X to a CSV), soft delete (`IsActive = No`) instead of deleting, keep history in a separate log list.

### D. Thinking before building (15 min) — the heart of the session
15. **Section divider:** "Don't open Power Apps first. Open a notepad."
16. **The 4 steps.** Problem → Data → Lists & columns → Screens. One line each:
    1. **Problem**: what decision or task does this make faster? What happens today instead?
    2. **Data**: what must we know to make that decision? Who enters it, who reads it?
    3. **Lists & columns**: "One row = one ___." Then each column: name, type, required, who fills it.
    4. **Screens**: what does each person need to see first? Enter → list → detail → dashboard.
17. **The design questions (interactive checklist).** A clickable checklist I walk through. These are the exact questions I use when designing a list:

**Purpose**
- Who uses it: everyone, managers only, auditors, one person?
- What decision or task does it make faster? What do they do today instead?
- Phone, desktop, or both?

**The record**
- Finish the sentence: **"One row = one ___"** (one issue, one audit, one device, one booking). If you can't finish it, you probably need two lists.
- Does something **stay the same** (a device, a ward, a kit) while **events happen to it** (audits, issues, loans)? → two lists: a **register** (one row per thing) and a **log** (one row per event).
- What does the register need to show **right now** (current status) vs what does the log keep **forever** (history)?

**Each column**
- Exact name (no spaces), type, required?, who fills it (person or app)?
- Is the list of options fixed and short? Who picks it — a person in SharePoint, or an app?
- Is it already recorded by SharePoint (Created, Created By)? → don't add it.
- Do we need it to make the decision? If not, **don't collect it** (especially patient details).

**Size and speed**
- How many rows in 1 year? (>2,000 → design filters carefully; >5,000 → index + archive plan)
- What will we filter or sort by? → index those columns.

**People and alerts**
- Who gets told when something happens? Fixed email address, or a role looked up from a staff list?
- Who can see the manager/oversight views?

**What can go wrong**
- No signal on the ward? Double tap on Save? Two people editing the same row?
- Anything destructive (delete, close, return)? → confirm step.

18. **Patterns I keep reusing.** 6 cards, each with a tiny diagram:
    - **Register + Log**: thing list + event list (device register + audit results).
    - **Current state on the item, history in a log**: item has `Status`; every change adds a log row.
    - **Snapshot for trends**: save a daily/weekly value (e.g. acuity score per ward) so you can chart change over time.
    - **Store exceptions only**: record only missing/extra items, not every item that was fine.
    - **Soft delete**: `IsActive = No` instead of deleting.
    - **A people/roles list**: one list of staff with their role → app shows manager tools only to the right people.
19. **Case study 1 — DTV audit (they know this).** Problem: prove every downtime viewer works and is ready. Show:
    - `DTV_Register` — one row = one DTV. Columns: Title (asset tag), DisplayName, Department, Location, Building, Floor, Stream.
    - `Audit_Results` — one row = one audit. Columns: Title (asset tag), Stream, DTVFound, LoginWorked, LoginFailReason, PatientListWorked, PrintWorked, PrintFailReason, KitMatched, MissingItems, EducationGiven (multi-choice), Notes, AuditPhoto, ReAudit. Auditor and time = Created By / Created (not columns).
    - Screens that came from it: pick a DTV (hides ones audited in the last month) → audit form in 6 steps → done → dashboard (latest audit per DTV, failures by reason, coverage by stream, follow-up: fixed / still failing).
    - Lesson boxes: "Imported from Excel → `field_2` internal names." "Reason columns only filled when a check fails."
20. **Case study 2 — Downtime kit check (next round).** Shows the "register + contents + exceptions" pattern: `Kit_Register` (one row per kit, QR code), `Kit_Items` (one row per item type), `Kit_Contents` (which items belong in which kit), `KitAudits` (one row per kit check), `Kit_Audit_Items` (**only** missing or extra items). Lesson: "Every kit list column is text, not Choice, because the app writes the values. A Choice column turned the save red."
21. **Case study 3 — Physiotherapy dashboard (broader functionality).** One app, many lists. Show as a diagram (mock boxes, **no screenshots, no patient data**):
    - Ward lists (one row = one bed/patient) → ward board, discharge planner (by expected discharge date), handover.
    - `ClinicianDirectory` (staff + role) → who sees manager tools.
    - `Equipment_Inventory` (current state: Available / Allocated / In Service) + `Equipment_Usage_Log` (every sign-out/return) + `Service_Log` (every service trip) → allocate/return on phone, servicing due list, usage reports.
    - `Acuity_Longitudinal` (daily snapshot) → week-vs-week charts.
    - `TrainingSessions` + `TrainingBookings` + `TrainingWaitlist` → booking with capacity, waitlist, reminder emails via Power Automate.
    - Cleanup flow: when a log reaches 4,999 rows, archive oldest 1,000 to CSV.
    - Notes: "The point is not the app, it is that every screen maps to a list with a clear 'one row = one ___'."
22. **Group task (5 min, interactive).** "Design the lists for this problem" — the room picks one card (click to choose): (a) device loan tracker for go-live (b) go-live readiness checklist per ward (c) training attendance for a new ieMR module (d) ieMR access request tracking. Then the **List Designer** (see §6) is filled in live by me while the room calls out answers. A timer (5:00) shows on screen.

### E. Build it live — Floorwalking issue log (12 min)
23. **The problem.** During a go-live, CIOs floorwalk wards and fix or escalate issues. Today: paper sheets or a Teams chat → no totals, hard to see repeat problems, hard to hand over between shifts.
24. **Design it first (use the 4 steps).** One row = **one issue raised on the floor**. List `FW_Issues`:

| Column (internal name) | Display name | Type | Required | Notes |
|---|---|---|---|---|
| Title | Summary | Single line of text | Yes | Short, e.g. "Label printer offline" |
| Facility | Facility | Choice | Yes | Fictional: Hospital A, Hospital B, Hospital C |
| Location | Ward / Unit | Single line of text | Yes | Free text (or a Locations list later) |
| System | System | Choice | Yes | ieMR, Printing, Device / Hardware, Login / Access, Network, Other |
| Severity | Severity | Choice | Yes | Low, Medium, High (patient safety) |
| Description | Description | Multiple lines of text (plain) | No | |
| Status | Status | Choice | Yes | Open, Resolved, Escalated. Default: Open |
| ResolvedOnSpot | Resolved On The Spot | Yes/No | — | Default No |
| TicketNumber | Ticket Number | Single line of text | No | Fill when escalated |
| Photo | Photo | Image | No | Screen photo — **never** a photo showing patient details |
| *(free)* | Created / Created By | — | — | Who logged it and when |

Notes: point out what is NOT a column (logged by, logged at). Index `Status` and `Facility` if it will grow. "Choice is fine here because we'll start with the auto-generated form, which handles Choice for us."

25. **Live build steps (checklist slide I tick as I go — clicking a step ticks it).**
    1. Open the demo Team → SharePoint → **+ New → List → Blank list** → name `FW_Issues`.
    2. Add the columns from the table (I'll have it pre-built as backup).
    3. Add 3 fake rows in **Edit in grid view**.
    4. **Integrate → Power Apps → Create an app** → name it "Floorwalking Log". Power Apps builds 3 screens: browse, detail, edit.
    5. Browse screen: show Summary, Ward and Status in the gallery; colour Status (Open = amber, Resolved = green, Escalated = red).
    6. Add a filter: Open only.
    7. Edit screen: remove fields we don't need, reorder (Summary, Facility, Ward, System, Severity, Status…).
    8. Save → Publish → **Share** with the room.
    9. Room scans the QR code (next slide) and logs a fake issue → I refresh the list → it appears.
26. **Join the demo (interactive).** A text box where I paste the app link, and a big QR code generated from it **in the page (write a small QR encoder inline — no library)**. If that's not possible reliably, show the link very large instead. Save the last link with try/catch'd localStorage.
27. **Mock of the finished app.** A phone-shaped frame (CSS) showing the browse screen with 5 fictional issues, status colours, a "+ New" button. Clicking "+ New" shows the form mock; clicking an issue shows the detail mock. Purpose: backup if the live build fails, and a picture of where we're heading.
28. **Where next.** Short list: a Locations list (Lookup) instead of free text; a dashboard screen (counts by system and severity); a rule or flow that emails the shift lead on "High"; an end-of-shift handover view; Power BI later.

### F. Wrap (5 min)
29. **Five things to remember.**
    1. Every Team has a SharePoint site; find lists in Site contents.
    2. One row = one ___. If you can't say it, you need two lists.
    3. Pick column types on purpose; let SharePoint record who and when.
    4. Index what you filter by; plan for 2,000 and 5,000.
    5. Design on paper first; the app is the easy part.
30. **Questions + cheat sheet.** "Press P to print the cheat sheet" (note for me). Contact placeholder I can edit.

## 6. Interactive pieces (build all of these)

1. **Quick check quiz** (slide 8): multiple choice, instant feedback, no scoring needed.
2. **Column type explorer** (slide 10): tile grid → detail panel. Data from the table in slide 10.
3. **Row-count slider** (slide 13): 0 → 50,000 with thresholds at 2,000 and 5,000; message and colour change (good / amber / danger).
4. **Design checklist** (slide 17): click to tick questions; "Reset" button.
5. **List Designer** (slide 22, also reusable): the most important widget.
   - Fields: problem (text), "One row = one ___" (text), list name.
   - Table of columns: add / remove row; each row has Name, Type (dropdown of the types in slide 10), Required (checkbox), Filled by (Person / App / SharePoint), Index (checkbox), Notes.
   - **Live warnings** under the table (amber), e.g.:
     - Column name contains spaces or symbols → "Internal name will be messy — name it without spaces first."
     - Column called "Date", "Created", "Entered by", "Author" or similar → "SharePoint already records Created / Created By."
     - Type = Choice and Filled by = App → "Apps must write `{ Value: … }` — consider Single line of text."
     - Type = Person and Filled by = App → "Hard for apps to write — consider name + email as text."
     - More than 12 Lookup + Person columns → "Lookup threshold — views will fail."
     - More than 20 indexed → "Max 20 indexes per list."
     - "One row = one ___" empty → "Finish the sentence first."
     - A column name that looks like patient identifiers (URN, DOB, patient name) → "Do you need this to make the decision? Collect the minimum."
   - "Load example" button fills it with the `FW_Issues` design.
   - "Print spec" prints just the designed list as a clean table.
   - Save state with try/catch'd localStorage; "Clear" button.
6. **Group task card picker + 5-min countdown** (slide 22).
7. **Live build checklist** (slide 25): click to tick.
8. **QR join slide** (slide 26).
9. **Phone mock** (slide 27): 3 states (browse / detail / new form), fictional data.

## 7. Printable cheat sheet (press P)

`@media print` produces a **2-page A4** cheat sheet (not the slides), hidden on screen. Clean, black-on-white friendly, palette accents only. Content:
- Page 1: Where things live (Team → SharePoint → Site contents; Library vs List; 6 SharePoint tips). Column type table (type · use it for · watch out). List settings paths (Required, Validation, Versioning, Indexed columns, Views, Rules, Formatting).
- Page 2: The 4 steps. The design questions (§5 slide 17, compact). The 6 patterns. The 2,000 / 5,000 rule + "index what you filter". "Five things to remember".
- Footer: "Fictional examples only. Not official QH guidance."

## 8. Background: how my real apps are structured (use for case studies, do not invent extra detail)

- **DTV Audit** (phone): `DTV_Register` (reference, imported from Excel, small) + `Audit_Results` (one row per audit). Dashboard shows the latest audit per DTV. Created By = auditor.
- **Kit audit** (next round): `Kit_Register`, `Kit_Items`, `Kit_Contents`, `KitAudits`, `Kit_Audit_Items` (exceptions only). All text columns because the app writes them.
- **Physiotherapy Dashboard** (desktop, 20 screens) + **STARS Equipment** (phone, 11 screens) + **Training Register**: ward lists, `ClinicianDirectory` (Person, Discipline, Access role), `Equipment_Inventory` (current state) + `Equipment_Usage_Log` (history) + `Service_Log`, `Equipment_Audits`, `Acuity_Longitudinal` (snapshot), `TrainingSessions` / `TrainingBookings` / `TrainingWaitlist` / `TrainingAppPermissions`, Power Automate flows for emails, reminders, waitlist and a nightly cleanup at 4,999 rows.
- Lessons learned the hard way: writing text to a Choice column breaks the save; Excel imports give `field_N` internal names; use Created not Modified; blank ≠ 0; Power Apps data row limit is 2,000 max (default 500 — set it to 2,000 in Settings); `DateDiff` / `in` / `Lower()` filters don't delegate on big lists.

## 9. Quality checks before you give me the file

- [ ] Opens from `file://` in Edge with **no console errors** and **no network requests**.
- [ ] All 30 slides present, each with speaker notes.
- [ ] Every interactive piece works with mouse; arrow keys don't fire while typing.
- [ ] Looks right at 1920×1080, 1366×768 and 1280×720 (letterboxed, nothing clipped).
- [ ] Print preview (P) gives exactly 2 A4 pages of cheat sheet, no slides.
- [ ] No real names, patients, URNs or official logos anywhere.
- [ ] Slide content is easy to find and edit at the top of the file.

## 10. After the file, tell me (numbered steps, I'm new to this)

1. How to save it (Notepad → Save as → `Inservice.html`, encoding UTF-8, "All files").
2. How to open it in Edge and go fullscreen.
3. The keyboard shortcuts (one short table).
4. How to change a slide's text.
5. How to print the cheat sheet.
6. A 5-minute pre-session test list (open on the QH laptop on the projector the day before, test QR with my phone, check the live-build backup list exists).

Ask me questions first if anything here is unclear or conflicts. Don't guess.
