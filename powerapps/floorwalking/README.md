# Floorwalking app

Only the pieces built here are in the repo. The rest of the app lives in Studio.

| File | What |
|---|---|
| `Discharge_Dash.pa.yaml` | Easter egg game, portrait (7 x 9 hallway). Opened from the avatar button (`Navigate(Discharge_Dash, ScreenTransition.Fade)`). Replaces the old Snake screen. |

Needs only `UI` and `Gutter` in App > Formulas (colours and font are written out in full).
Keys W A S D / number pad work on computers; on phones and tablets (`Host.OSType` iOS / Android) the hidden key box is never focused, so the on-screen keyboard never pops up.
Desktop dashboard version (landscape 14 x 7): `powerapps/desktop/Discharge_Dash.pa.yaml`.
