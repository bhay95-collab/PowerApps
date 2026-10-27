# Floorwalking Ideas app (phone)

CITTA floorwalkers capture ieMR improvement ideas on the ward (Capture), see them (Dashboard), **find a Quick Reference Guide (QRG)** (QRG + QrgView) and read the **RBWH Business Rules** (Rules + RuleView).

Studio export is the source of truth (all five screens + App.Formulas were copied in on 20 Oct 2026). The app's original generator (`tools/floorwalk_generator/fwbuild.py`, named in the old App.Formulas header) is **not in any repo**: edit these files and Studio directly. Never re-run an old generator over them.

## What is in this folder

| File | What it is |
|---|---|
| `App_Formulas.txt` | Whole App > Formulas. **`SafetyAlertTo` is a placeholder** (real addresses are staff data, not kept in this public repo): type them in Studio after pasting |
| `Home.pa.yaml` | Home: Capture an Idea, Find a Guide, Ideas Dashboard, My Ideas |
| `Capture.pa.yaml` | Capture an idea (offline queue, similar-idea check, safety email) |
| `Dashboard.pa.yaml` | Dashboard, detail sheet, review |
| `QRG.pa.yaml` | Search + application chips + list of ieMR QRGs |
| `QrgView.pa.yaml` | One QRG in the PDF viewer (`pdfQrg_Qv`, `PDFViewer@2.5.0`) + Open in Browser |
| `Snake.pa.yaml` | Hidden Snake game. Tap the round avatar (`Avatar1`, `ModernAvatar@1.1.0`, shows the user's Teams/Microsoft 365 profile picture by default) in front of "Hi <name>" on Home to open it. Built by `tools/floorwalk/build_snake.py` (edit the script, not the YAML). Power Apps runs the game (Timer + `colSnake`); the HTML viewer only draws the board, because it strips `<script>` and `<iframe>` (tested Oct 2026) |
| `../flows/Get_QRG_PDF.zip` | Flow `GetQrgPdf` (built by `tools/flows/build_qrg_pdf_flow.py`) |
| `Rules.pa.yaml` | RBWH Business Rules: search + list grouped under the DMN RBWH Go-Live page headings |
| `RuleView.pa.yaml` | One Business Rules PDF in the PDF viewer (`pdfRule_Rv`) + Open in Browser |
| `../flows/Get_Rule_PDF.zip` | Flow `GetRulePdf` (built by `tools/flows/build_rule_pdf_flow.py`) |

## How the QRG feature works

- Data: the ieMR Applications site library `Resources library` (`https://healthqld.sharepoint.com/teams/MNHHS-DMN-APP`). It is **read only for us**. About 1,330 files; 704 are ieMR QRGs; all are PDFs in the library root.
- Columns used: `Resource title`, `Description` (Power Apps name `'Description (Description0)'`), `Resource type` (lookup), `Systems` (lookup), `Applications` (multi-choice), `Profession` (multi-choice), `Modified`, file name.
- A guide is shown when **Systems contains ieMR** and **Resource type contains Quick reference guide** and the file ends `.pdf`.
- `btnLoad_Qrg` copies those rows into `colQrg` (plain columns) once per hour and saves them on the phone (`SaveData` `fwQrg`), so the **list and search work offline**. Opening a PDF needs signal.
- Search: every word typed must appear in the title, description, application or profession.
- Chips: All, **Recent** (your last 10 guides, newest first), **Starred** (tap the ☆ on a row; stars live on that phone only, so a new phone starts empty), then the 12 applications with the most guides (built from the data, so new applications appear on their own).
- Opening a PDF: `QrgView` runs flow `GetQrgPdf` (file name in, PDF as `data:application/pdf;base64,...` out). The PDF viewer cannot open a SharePoint link itself (sign-in), which is why the flow is needed. If it fails, **Open in Browser** opens the file in the phone browser.
- Nothing is written to SharePoint.
- Library growth: the app reads the library in one go, so it must stay **under the 2000 row limit**. At about 1,900 files, change `btnLoad_Qrg` to a delegable filter.

## Install steps (Ben)

Do them in this order.

### A. Studio settings
1. Studio → open Floorwalking Ideas → **Settings** (top) → **General** → **Data row limit** → type `2000`.
2. Left rail → **Data**. `Resources library` must be listed. If not: **Add data** → SharePoint → pick the DMN-APP site → tick **Resources library** → **Connect**.

### A2. Open log list
1. Open the SharePoint site that holds `Floorwalk_Ideas` → **+ New** → **List** → **Blank list**.
2. Name it exactly `QRG_Open_Log` → **Create**. No columns to add (it uses Title, Created, Created By).
3. Studio → left rail **Data** → **Add data** → **SharePoint** → pick the same site as `Floorwalk_Ideas` → tick `QRG_Open_Log` → **Connect**.

Each tap on a guide adds one row (Title = file name). The QRG screen counts rows per file: most-opened first, the rest A to Z.

### B. Flow
1. Open the zip on GitHub: `powerapps/flows/Get_QRG_PDF.zip` → **Download raw file**.
2. make.powerautomate.com → **My flows** → **Import** → **Import Package (Legacy)** → **Upload** → pick the zip.
3. Flow row: **Import setup** → *Create as new* → Save. SharePoint row: **Select during import** → pick your SharePoint connection → Save. **Import**.
4. Open the flow → **Edit**. Click **Get file content using path**. Check **Site Address** is the DMN-APP site and **File Path** reads `/Resources library/` + **FileName**. If a step is red, re-pick the Site Address from the drop-down. **Save**.
5. **Test** → Manually → **Test**. FileName: `Ordering a medication.pdf` → **Run flow**. Open **Respond to a PowerApp or flow** in the result: output `pdf` must start `data:application/pdf;base64,`.
6. Studio → left rail **Power Automate** → **Add flow** → pick `GetQrgPdf`.

If the zip will not import, build it by hand: **Create** → **Instant cloud flow** → trigger **PowerApps (V2)** → **Add an input** → Text → name `FileName` → **+** → **SharePoint** → **Get file content using path** → Site Address: DMN-APP site → File Path: type `/Resources library/` then pick **FileName** → **+** → **Respond to a PowerApp or flow** → **Add an output** → Text → name `pdf` → value: Expression tab → `concat('data:application/pdf;base64,', body('Get_file_content_using_path')?['$content'])` → name the flow `GetQrgPdf` → Save.

### C. App > Formulas
1. Tree view → click **App** → property drop-down → **Formulas**.
2. Click at the very end, new line, add:
```
QrgLibUrl = "https://healthqld.sharepoint.com/teams/MNHHS-DMN-APP/Resources%20library/";
```
(It is already in `App_Formulas.txt`. Do **not** paste that whole file over the live one: it has a placeholder for `SafetyAlertTo`.)

### D. Screens
For each of `QRG`, then `QrgView`, then `Home`: follow `docs/03_STUDIO_AND_YAML.md` §1 (delete old screen if there is one → **+ New screen → Blank** → rename exactly → **Raw** copy → right-click screen → **Paste code**).
For `Home` also: after pasting, drag **Home** to the top of Tree view so it is still the first screen.
Red errors naming a screen that is not pasted yet clear once all three are in.

### E. PDF viewer
Already inside `QrgView.pa.yaml` (`pdfQrg_Qv`, `PDFViewer@2.5.0`). Nothing to add by hand.

### F. Check, publish, test on a phone
1. Tree view → **QRG** → ⋯ → **Run OnVisible**. Wait. `Home` → **Find a Guide** should list guides.
2. App checker (stethoscope): no red.
3. **File → Save → Publish this version**.
4. On a phone, open the app in Power Apps mobile (first open after publishing: close and reopen).
   1. Home → **Find a Guide**. First open takes a few seconds. Header shows `704 ieMR guides` (about).
   2. Type `pca`. Only PCA guides stay.
   3. Clear the search. Tap chip **PowerChart**. List shortens. Tap **All**.
   4. Tap a guide. `Loading guide...`, then the PDF.
   5. Back. Turn on airplane mode. Close and reopen the app. Find a Guide still lists guides. Tap one: amber card says no signal.
   6. Airplane mode off. Open a guide, tap **Open in Browser**: PDF opens in the browser.

### If something is red or blank
- Red names inside `btnLoad_Qrg` (`File name with extension`, `Resource title`, `Systems`…): the column names differ in your copy. Screenshot the red text and send it.
- List empty after load: tell Claude the count shown in the header.
- PDF viewer blank but no amber card: try **Open in Browser**; tell Claude the phone type (iPhone / Android).


---

# RBWH Business Rules (Rules + RuleView)

Same headings as the DMN "RBWH ieMR Go-Live resources" page. Home tile **Business Rules** → `Rules` (search + grouped list) → tap a document → `RuleView` (PDF in the app, Open in Browser backup).

## How it works

- Data: CITTA site (`https://healthqld.sharepoint.com/teams/CITTA`), library **Documents** (= Shared Documents). Files sit loose in `RBWH Clinical Informatics/RBWH Business Rules`.
- Choice column **`Section`** on that library. A PDF shows in the app only when Section is picked. Heading order in the app = order of the choices in the column. Rename or reorder a choice in SharePoint, the app follows after refresh. No app change needed to add a document: upload PDF, pick its Section.
- Name in the app = file name without `.pdf`. Keep file names tidy (`Allied Health.pdf`, not `RBWH_BR_AH_v3_final.pdf`).
- Search: every word typed must appear in the name or the heading.
- `btnLoad_Rl` reads the library once an hour, saves it on the phone (`SaveData` `fwRules`): list works offline. Opening a PDF needs signal.
- Opening: flow `GetRulePdf` (whole path in, PDF out as `data:application/pdf;base64,...`). Path = `/` + `Folder path` + file name, so a file in a subfolder works too.
- Whole Documents library (all folders) must stay under 2000 files. Under 1,500 in Oct 2026.
- Nothing is written to SharePoint.

## Install steps (Ben)

Do them in this order.

### R1. Section column (CITTA site)
1. Open `https://healthqld.sharepoint.com/teams/CITTA` → **Documents** → open folder `RBWH Clinical Informatics` → `RBWH Business Rules`.
2. Top right of the file list: **+ Add column** → **Choice** → **Next**.
3. Name: `Section` (exact, capital S).
4. Choices: delete the 3 sample choices, then type these 7, one per box, **in this order**:
   1. `General Business Rules`
   2. `Service Business Rules`
   3. `Mental Health Business Rules`
   4. `Perioperative Services (SurgiNet and SAA) Business Rules`
   5. `Women's and Newborn Services Business Rules`
   6. `RBWH ieMR Go-Live Resources`
   7. `Inpatient Conversion Resources`
5. Default value: **None**. Leave "Allow multiple selections" **off**. **Save**.
6. Tag the files fast: top of list → **Edit in grid view**. Click the Section cell of each PDF → pick the heading (table below). Done → **Exit grid view**.

| Section | Files (as on the DMN page) |
|---|---|
| General Business Rules | General Business Rules, Chart Management, Medications Management |
| Service Business Rules | Aboriginal and Torres Strait Islander Health Service, Allied Health, Cancer Care, Cardiology, Emergency and Trauma Centre, Intensive Care Unit, Kidney Health Service, Management for Care of the Dying, Medical Imaging, Nuclear Medicine, Outpatients (OPD), PowerTrials, Transfer to Hospital in the Home |
| Mental Health Business Rules | Mental Health Inpatient Services, Mental Health Inpatient Services Medication Management, SurgiNet and SAA Mental Health ECT |
| Perioperative Services (SurgiNet and SAA) Business Rules | Anaesthetics, Bookings, Endoscopy, Off Floor Areas, Postoperative, Preadmission and Preoperative, Surgical Day Care Unit (SDCU), Theatre |
| Women's and Newborn Services Business Rules | Grantley Stable Neonatal Unit, Gynaecology, Maternity and Obstetrics |
| RBWH ieMR Go-Live Resources | Administration Message Pool Guide, Administration Workflow Change Overview, Admission Workflow, CHARM and ieMR for Medical Oncology and Haematology, CHARM Placeholder, Digital Cardiac Orders within ieMR, Documenting Food Allergies, EDIS to ieMR Consult Orders Placemat, Encounter Management, Grantley Stable Neonatal Unit Clinical Information Directory, Inpatient Referral Placemat, Medical Imaging Ordering Guide - Digital, Medical Imaging Ordering Guide - Paper, Medical Officers – cross-departmental ieMR essentials, Pathology Labelling, Pathology Ordering Guide, Printing for ieMR, RBWH Go-Live Support |
| Inpatient Conversion Resources | Day of Ward Go-Live and Conversion Sequence, Identifying patients converted to the ieMR, Paper and Digital Workflow Map - Team-Specific Scenarios, Sequenced Implementation Support Guide - Surgical and..., What is Inpatient Ward Conversion? |

### R2. Flow
1. GitHub: `powerapps/flows/Get_Rule_PDF.zip` → **Download raw file**.
2. make.powerautomate.com → **My flows** → **Import** → **Import Package (Legacy)** → **Upload** → pick the zip.
3. Flow row: **Import setup** → *Create as new* → Save. SharePoint row: **Select during import** → pick your SharePoint connection → Save. **Import**.
4. Open flow `GetRulePdf` → **Edit**. Click **Get file content using path**. **Site Address** must be the CITTA site. **File Path** must be just **FilePath** (the trigger input). If red: re-pick Site Address from the drop-down. **Save**.
5. **Test** → Manually → **Test**. FilePath: `/Shared Documents/RBWH Clinical Informatics/RBWH Business Rules/Allied Health.pdf` (use a real file name from the folder) → **Run flow**. Output `pdf` must start `data:application/pdf;base64,`.
6. Studio → left rail **Power Automate** → **Add flow** → pick `GetRulePdf`.

By hand if the zip will not import: **Create** → **Instant cloud flow** → trigger **PowerApps (V2)** → **Add an input** → Text → name `FilePath` → **+** → **SharePoint** → **Get file content using path** → Site Address: CITTA → File Path: pick **FilePath** → **+** → **Respond to a PowerApp or flow** → **Add an output** → Text → name `pdf` → value: Expression tab → `concat('data:application/pdf;base64,', body('Get_file_content_using_path')?['$content'])` → name the flow `GetRulePdf` → Save.

### R3. Data source
1. Studio → open Floorwalking Ideas → left rail **Data** → **Add data** → **SharePoint** → pick the CITTA site → tick **Documents** → **Connect**.
2. Check the name it shows in the Data list. Must be exactly `Documents`. If it shows `Documents_1` or another name: stop, tell Claude the name.
3. If Section was added after connecting: Data → **Documents** → **⋯** → **Refresh**.

### R4. App > Formulas
Tree view → **App** → property drop-down → **Formulas** → click at the very end → new line → paste:
```
RuleSiteUrl = "https://healthqld.sharepoint.com/teams/CITTA";
```

### R5. Screens
Paste order: `RuleView`, then `Rules`. Each: **+ New screen → Blank** → rename exactly → open the file on GitHub → **Raw** → copy all → right-click the screen in Tree view → **Paste code**.
Red on `Rules` naming `RuleView` clears once both are in.

### R6. Home tile
Live Home may differ from the repo (avatar → Discharge Dash), so do not paste the whole Home. Copy the Find a Guide tile instead:
1. Home → Tree view → click `conTileQrg_Hm` → **Ctrl+C** → **Ctrl+V**. A copy appears under it (names end `_1`).
2. In the copy set:
   - `lblTileTQrg_Hm_1` → **Text** → `"Business Rules"`
   - `lblTileSQrg_Hm_1` → **Text** → `"RBWH ieMR rules and go-live"`
   - `icoTileQrg_Hm_1` → **Icon** → `"AppsList"`
   - `btnTileQrg_Hm_1` → **OnSelect** → `Navigate(Rules, ScreenTransition.Cover)`
3. Wrong place? Drag the copy in Tree view to sit right under `conTileQrg_Hm`.

(Repo `Home.pa.yaml` has the same tile as `conTileRule_Hm`.)

### R7. Check, publish, test
1. Tree view → **Rules** → ⋯ → **Run OnVisible**. Wait. Headings + documents should list.
2. App checker (stethoscope): no red. Yellow delegation warning on `Documents` inside `btnLoad_Rl` is expected (library under 2000).
3. **File → Save → Publish this version**.
4. Phone: Home → **Business Rules**.
   1. Headings in the order of R1 step 4. Header shows document count.
   2. Type `theatre`. Only Perioperative heading + Theatre left.
   3. Tap a document: `Loading document...`, then PDF.
   4. **Open in Browser**: PDF opens in browser.
   5. Airplane mode → close + reopen app → Business Rules still lists.

### If something is red or blank
- Red names in `btnLoad_Rl` (`Section`, `'Folder path'`, `'File name with extension'`): column name differs. Screenshot red text, send it.
- List empty: Section not picked on files, or Documents not refreshed (R3 step 3).
- PDF fails but Open in Browser works: run the flow test (R2 step 5) with that file's path. Send the error.
