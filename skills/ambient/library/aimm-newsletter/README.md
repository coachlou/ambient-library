# group-newsletter

A Claude skill that sends a formatted HTML newsletter to a Google Contacts group in one prompt. You write the subject and body in markdown; the skill handles member lookup, HTML conversion, branded template injection, preview, confirmation, and individual sends.

---

## What it does

1. Collects a subject line and markdown body (asks if not provided)
2. Fetches the recipient list from a named Google Contacts group via `get_contact_group`
3. Converts markdown to HTML (paragraphs, bold, italic, lists, headings, links, rules)
4. Injects the HTML into a branded email template (`assets/template.html`)
5. Renders a preview and waits for confirmation before sending
6. Sends individually to each member — not BCC — so each recipient gets a personal send

Trigger phrases: *"send this to [your group name]"*, *"send the newsletter"*, *"email the group"*.

---

## Prerequisites

This skill requires the **advanced-gmail-mcp** server to be set up and wired into Claude Desktop. That covers:

- Cloning and configuring [coreyepstein/advanced-gmail-mcp](https://github.com/coreyepstein/advanced-gmail-mcp)
- Creating a Google Cloud OAuth Desktop app credential
- Configuring `accounts.json` with your sending account(s)
- Running the OAuth auth flow for each account
- Adding the MCP entry to `claude_desktop_config.json`
- Enabling the **People API** in Google Cloud Console (required for contact group lookup)
- Adding `contacts.readonly` to the OAuth scopes in `src/gmail/auth.ts` and re-running auth

**Full setup guide:** [`look-over-my-shoulder/gmail-mcp-multi-account-setup/`](https://github.com/coachlou/aimm-shared-repo/tree/main/look-over-my-shoulder/gmail-mcp-multi-account-setup) — includes step-by-step instructions, gotchas, and all required code patches.

Your Google Contacts must have a contact group containing the recipient email addresses. The skill looks up this group by name at send time.

---

## Install

```bash
cp -r skills/aimm-newsletter ~/.claude/skills/group-newsletter
```

Then restart Claude Desktop (or reload the skills index).

---

## Customize for your own use

Open `~/.claude/skills/group-newsletter/SKILL.md` and update two lines in **Step 2**:

```
group_name: "YOUR_GROUP_NAME"     ← the name of your Google Contacts group
account: "YOUR_ACCOUNT_ALIAS"     ← the alias from your accounts.json
```

And in **Step 5**, update the subject prefix:

```
subject: "[YOUR PREFIX] " + the subject
```

**To swap the email template:**
Edit `assets/template.html`. The only required element is the `{{BODY_HTML}}` placeholder — the skill replaces it at runtime with the converted HTML body. Replace "Your Organization Name" in the header and footer, then adjust colours and fonts to match your brand.

---

## Files

```
group-newsletter/
├── README.md           ← this file
├── SKILL.md            ← skill instructions (edit account alias + group name here)
└── assets/
    └── template.html   ← HTML email shell with {{BODY_HTML}} placeholder (customize branding here)
```

---

## Notes

- **Individual sends, not BCC.** Each recipient receives the email addressed to them directly. BCC arrives as bulk mail and signals spam filters.
- **Subject prefix is always applied.** Even if the user includes a prefix in their input, the skill prepends the configured prefix to ensure consistency.
- **Preview is mandatory.** The skill will not send without an explicit confirmation — this is by design, not skippable.
- **Scope changes require re-auth.** If you add `contacts.readonly` to an existing setup, delete the affected token file and re-run `npx tsx src/auth.ts your_alias`.
