# 07 · Branded Email Template

Every email from every app and flow uses this look. Source: `powerapps/email/Email_Formulas.txt` (also at the end of `templates/App_Formulas_Starter.txt`).

## Look
- Pale page `#EBF2F8`; white 680-wide card, radius 18, border `#D6E0EA`.
- Gradient bar built from **32 solid table cells** (navy `#001F47` → teal) — Outlook desktop (Word engine) ignores CSS gradients.
- Teal title block `#075F73`: kicker "STARS PHYSIOTHERAPY" (11 px, letter-spacing 2, `#BFE3E8`), title 26 px bold white, subtitle 14 px `#DCEFF2`.
- Body rows: 15 px `#3A5068` text, padding `28px 32px`.
- Footer `#F4F9FC`: "Sent from the STARS Physiotherapy app by <name>." + note, 12 px `#8C9BAE`.

## Build an email in Power Fx
```
Set(
    varEmailBody,
    Substitute(Substitute(EmailHead, "{{TITLE}}", "Title here"), "{{SUB}}", "Subtitle here") &
    "<tr><td style='padding:28px 32px 8px 32px;font-size:15px;line-height:22px;color:#3A5068;'>" &
        "Hi " & First(Split(User().FullName, " ")).Value & ",<br><br>Body text." &
    "</td></tr>" &
    Substitute(EmailFoot, "{{NOTE}}", "Optional small print")
);
Office365Outlook.SendEmailV2(toAddress, "Subject", varEmailBody, { IsHtml: true });
Notify("Email sent to " & toAddress & ".", NotificationType.Success)
```
Check for nothing-to-send first (`If(IsEmpty(rows), Notify("Nothing to send."), ...)`).

## Building blocks (copy from the real buttons)
| Block | Copy from |
|---|---|
| Table with header row + one row per record (`Concat`) | `powerapps/email/Todays_Allocation_Mobile.txt` |
| Blue reminder box (`#E8F1FA` / `#1A5A99`) | same file |
| Sign-off ("Thanks, <name>") | same file |
| Fail / alert email to another person | `powerapps/email/Audit_Fail_Email_Mobile.txt` |
| Summary table by date | `powerapps/email/EDD_Summary_Button.txt` |
| Training emails | `powerapps/email/Training_Emails_*.txt` |

## Outlook-safe rules
- Tables only (`role='presentation'`), `bgcolor` attribute **and** inline `background-color`.
- Inline styles only. No `<style>` blocks, no flex/grid, no CSS gradients.
- `border-radius` may be ignored on Outlook desktop — design must still look fine square.
- Plain-text user input: replace line breaks `Substitute(txt, Char(10), "<br>")`.
- Patient info in an email → footer note: "This email contains patient information. Please handle it in line with your privacy policy."
