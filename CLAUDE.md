# CLAUDE.md — STARS Physiotherapy Power Apps

Read this first, every session. Then open the doc in `docs/` that matches the task.

## Who you work with
Ben (STARS physiotherapy, Queensland Health). New to coding.
- Short and direct. No filler. Code when asked; explain only if asked.
- **Every instruction = exact numbered steps**: which app, which screen, which control, which property, what to paste, what to click.
- **Ask, don't guess.** Use the multiple-choice question tool for decisions.
- **Push back** when an idea can be improved — only when it matters to the task's purpose.
- Deliver code as a GitHub link to the file (Ben clicks **Raw**, copies all) or full code in chat if asked. Small fixes: give only `Control → Property → formula`.
- Before Ben pastes a replacement screen: delete old screen → add blank screen → rename exactly → right-click → **Paste code**. (See `docs/03_STUDIO_AND_YAML.md` §1.)
- After a SharePoint column is added: tell Ben to refresh the data source (Data → list → ⋯ → Refresh).
- Commit and push to the working branch. **Never** put staff or patient data (exports, names, URNs) in the repo.

## Docs (read the one you need)
| File | Use it when |
|---|---|
| `docs/00_NEW_BUILD_PLAYBOOK.md` | Starting any new screen, app, feature or fix. The workflow + checklists. |
| `docs/01_DESIGN_SYSTEM.md` | Colours, fonts, sizing maths, screen anatomy, look of every component. |
| `docs/02_POWER_FX_RULES.md` | Power Fx gotchas: data, delegation, Patch, errors, dates, choice columns. |
| `docs/03_STUDIO_AND_YAML.md` | Paste mechanics, YAML rules, control versions, icon names, Studio steps. |
| `docs/04_COMPONENT_RECIPES.md` | Copy-ready patterns (header, card, tile, pills, Yes/No, gallery row, sticky submit, photo, save). |
| `docs/05_SHAREPOINT_DATA.md` | Every list and column, internal names, growth/cleanup rules. |
| `docs/06_POWER_AUTOMATE.md` | Flow packaging, triggers, HTTP actions, existing flows. |
| `docs/07_EMAIL_TEMPLATE.md` | Branded HTML email (Outlook-safe). |
| `docs/08_APPS_INVENTORY.md` | What each app and screen does today. |
| `docs/09_TOOLS.md` | Generator, layout simulator, YAML validator. |
| `docs/OPEN_ITEMS.md` | Work still to do + decisions waiting on Ben. |
| `docs/HANDOVER_2026-10-08.md` | Original handover (history). |

## Repo map
```
CLAUDE.md                this file
docs/                    knowledge base (above)
templates/               starters for new apps/screens (App_Formulas_Starter.txt, Template_Screen.pa.yaml)
powerapps/desktop/       Physio Dashboard (Studio export = source of truth)
powerapps/mobile/        STARS Equipment mobile (Studio export = source of truth)
powerapps/dtv/           DTV Audit (generated from tools/dtv_generator — edit the generator, not the YAML)
powerapps/training/      stand-alone Training Register
powerapps/email/         email formulas and button OnSelects
powerapps/flows/         Power Automate Import Package (Legacy) zips
powerapps/icon/          app icons
powerapps/archive/       history only — do not edit
tools/                   generator, preview/sim, validator, make_responsive.py
```

## Non-negotiables (quick list — details in docs)
1. Use the named colours / `AppFont` / `UI` sizing. Never invent new colours.
2. Font `Size` is **points**: px design → pt (36→28, 24→19, 19→15, 16→13, 14→11). Min 11 pt.
3. Every Patch → check `Errors()` before logging or showing success.
4. Re-read a record with `LookUp` right before checking its status.
5. Double-tap guard (`varSaving`) on every save button.
6. Confirm before remove / delete / return.
7. No Classic ComboBox for people/patients — search box + gallery.
8. Run `python3 tools/preview/validate.py <file>` on every YAML you write before giving it to Ben.
9. Title Case on buttons/titles/labels. CAPS for section captions.
10. Never `Exit()`. Never `DateValue(DatePicker.SelectedDate)`. Use `TimeUnit.Days`, not `"Days"`.

## Source code origin
Copied 8 Oct 2026 from `bhay95-collab/staff-movements`, branch `claude/upbeat-faraday-jktxlf` (`powerapps/` + `tools/`). This repo is now the home for all Power Apps work.
