# Floorwalking Ideas app (phone)

CITTA floorwalkers capture ieMR improvement ideas on the ward (Capture), see them (Dashboard), and now **find a Quick Reference Guide (QRG)** (QRG + QrgView).

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
| `../flows/Get_QRG_PDF.zip` | Flow `GetQrgPdf` (built by `tools/flows/build_qrg_pdf_flow.py`) |

## How the QRG feature works

- Data: the ieMR Applications site library `Resources library` (`https://healthqld.sharepoint.com/teams/MNHHS-DMN-APP`). It is **read only for us**. About 1,330 files; 704 are ieMR QRGs; all are PDFs in the library root.
- Columns used: `Resource title`, `Description` (Power Apps name `'Description (Description0)'`), `Resource type` (lookup), `Systems` (lookup), `Applications` (multi-choice), `Profession` (multi-choice), `Modified`, file name.
- A guide is shown when **Systems contains ieMR** and **Resource type contains Quick reference guide** and the file ends `.pdf`.
- `btnLoad_Qrg` copies those rows into `colQrg` (plain columns) once per hour and saves them on the phone (`SaveData` `fwQrg`), so the **list and search work offline**. Opening a PDF needs signal.
- Search: every word typed must appear in the title, description, application or profession.
- Chips: All + the 12 applications with the most guides (built from the data, so new applications appear on their own).
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
