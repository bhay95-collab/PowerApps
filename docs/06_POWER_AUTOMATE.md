# 06 · Power Automate

---

## 1. Packaging (how flows travel)

Distribute as **Import Package (Legacy)** zips. Structure:
```
manifest.json                                   package name, resources, dependsOn
Microsoft.Flow/flows/manifest.json
Microsoft.Flow/flows/<guid>/definition.json     the flow (triggers + actions)
Microsoft.Flow/flows/<guid>/apisMap.json
Microsoft.Flow/flows/<guid>/connectionsMap.json
```
Easiest way to make a new one: unzip an existing package from `powerapps/flows/`, new GUID folder, edit `definition.json`, update both manifests, re-zip (zip the **contents**, not the folder).

### Import steps (for Ben)
1. make.powerautomate.com → **My flows** → **Import** → **Import Package (Legacy)**.
2. **Upload** → pick the zip → wait.
3. Each resource: **Import setup** → *Create as new* (or *Update* to replace) → Save.
4. Each connection: **Select during import** → pick your SharePoint / Outlook connection → Save.
5. **Import**.
6. Open the flow → **Edit**. Any red step: click it, re-pick the **Site address** and **List name** from the drop-downs (the connector stores list **GUIDs**, not names).
7. **Personal details are blanked in this public repo.** Search each step for `REPLACE_WITH_` and type the real value:
   - `REPLACE_WITH_BLS_COORDINATOR_EMAILS` → BLS coordinators, separated by `;`
   - `REPLACE_WITH_MANUAL_HANDLING_COORDINATOR_EMAILS` → Manual Handling coordinators, separated by `;`
   - `REPLACE_WITH_YOUR_EMAIL` → sender address (the "From" field)
   Never commit the filled-in version back to the repo.
8. **Save** → **Test** → Manually.
9. In Power Apps Studio: Power Automate icon → **Add flow** → pick it. (If the trigger inputs changed: remove and re-add the flow.)

---

## 2. Triggers

- **Power Apps (V2)**: `kind: PowerAppV2`. Inputs auto-named `text`, `text_1`, `text_2`, `number`, `file` (`{ name, contentBytes }`). In Power Apps call positionally: `MyFlow.Run(a, b, c)`.
- **Return to Power Apps**: "Respond to a PowerApp or flow" → e.g. text output `filesjson`; read in app with `Set(varJson, GetTeamBriefFiles.Run().filesjson)` then `ParseJSON(varJson)` (real: `Physiotherapy_Screen`).
- **Recurrence**: set `timeZone: "E. Australia Standard Time"` and a `startTime`.

## 3. Rules learned

- SharePoint **"Send an HTTP request"** (operationId `HttpRequest`, `parameters/method`, `parameters/uri`) with `_api/web/lists/getbytitle('<exact list title>')/items?...`. Title must be exact: `Equipment_Usage_Log`, not "Equipment Usage Log".
- Expressions inside action fields must start with `@` (e.g. `@{concat('...', variables('x'))}`). Plain text "concat(" is not evaluated.
- Use variables at the top (`Site_address`, `Archive_folder`, `Threshold`, `Batch_size`) so Ben can change one place.
- Emails: Outlook "Send an email (V2)" with the branded HTML (see `07_EMAIL_TEMPLATE.md`). Build body in a **Compose** first.
- Don't hard-code people where a list lookup works (current weekly reminders have hard-coded names — left by Ben's choice).
- *Recommended (not yet in the existing flows):* scheduled flows fail silently. Add a last step "Send an email" with **Configure run after → has failed** so someone hears about it.

---

## 4. Existing flows (`powerapps/flows/`)

| Flow (zip) | Trigger | What it does |
|---|---|---|
| `TrainingBookingConfirmationEmail` (`Training_Booking_Confirmation_branded.zip`) | Power Apps: ActionType, UserName, UserEmail, SessionID, TrainingType, BookingID | Booked / Cancelled / Waitlisted emails (branded, with location) |
| `TrainingWaitlistNotification` (`Training_Waitlist_Notification_branded.zip`) | Power Apps | Emails first person waiting when a place opens |
| Waitlist escalation 48 h (`Training_Waitlist_Escalation_branded.zip`) | Schedule | Moves down the waitlist; capacity read from session |
| Weekly reminder – booked users (`Weekly_Reminder_Booked_Users_branded.zip`) | Schedule | Branded reminder (hard-coded names kept) |
| Weekly session reminder – general (`Weekly_Session_Reminder_General_branded.zip`) | Schedule | Branded reminder |
| `GetTeamBriefFiles` | Power Apps | Returns Team Brief files JSON (`filesjson`). Not in repo as zip |
| `Data Cleanup (all lists)` (`Data_Cleanup_All_Lists.zip`) | Daily 02:30 AEST | Archive/recycle per `05_SHAREPOINT_DATA.md`. Variables: Site_address, Archive_folder, Trigger_count 4999, Batch_size 1000, Training_months_to_keep 12 |
| `Usage Log Cleanup` (`Usage_Log_Cleanup.zip`) | Daily | **Superseded** by Data Cleanup — turn it off |

Known behaviour: waitlist notification re-notifies the first waiting person on each later cancellation; the 48 h escalation then moves on. Accepted.
