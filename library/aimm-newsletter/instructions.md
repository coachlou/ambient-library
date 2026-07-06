# group-newsletter v1.0

## What this skill does

1. Collect subject + markdown body (ask if not provided)
2. Fetch `aimm_member` contact group via `get_contact_group`
3. Convert markdown → HTML and inject into the AIMM template
4. Show preview — wait for confirmation
5. Send via BCC (single call) when 2+ members; direct send when only 1

---

## Step 1 — Collect inputs

If the user hasn't provided both, ask for:
- **Subject line**
- **Body** (markdown — supports `**bold**`, `*italic*`, bullet lists with `-`, headers with `##`, links `[text](url)`)

---

## Step 2 — Fetch members

Call `get_contact_group` with `group_name: "YOUR_GROUP_NAME"`, `account: "YOUR_ACCOUNT_ALIAS"`.

<!-- Customize: set group_name to your Google Contacts group and account to your accounts.json alias -->

---

## Step 3 — Convert markdown to HTML

Convert the markdown body to HTML using these rules:

- Double newline (blank line between paragraphs) → wrap each paragraph in `<p style="margin:0 0 20px 0;">...</p>`
- `**text**` → `<strong>text</strong>`
- `*text*` → `<em>text</em>`
- Lines starting with `- ` → collect into `<ul style="padding-left:20px; margin:0 0 25px 0;">` with each item as `<li style="margin-bottom:12px;">...</li>`
- `## heading` → `<p style="margin:0 0 8px 0;"><strong>heading</strong></p>`
- `[text](url)` → `<a href="url" style="color:#2c4d6e;">text</a>`
- Horizontal rule `---` → `<hr style="border:none; border-top:1px solid #cccccc; margin:30px 0;">`

Then read `${CLAUDE_PLUGIN_ROOT}/library/aimm-newsletter/assets/template.html` and replace `{{BODY_HTML}}` with the converted HTML.

---

## Step 4 — Preview HTML in Claude

Write the full HTML string to `/tmp/aimm-email-preview.html` using the Write tool. This automatically renders the email in the preview panel.

Show in text:
```
Subject:    <subject>
Recipients: <N> members — <comma-separated names>
```

Ask: **"Looks good? Send to all N members? (yes / no)"**

Do not proceed until confirmed.

---

## Step 5 — Send

**If 2 or more members** (default), send a single BCC call:
- `account`: `"YOUR_ACCOUNT_ALIAS"`
- `to`: `"YOUR_FROM_ADDRESS"` (the sending account's own From address)
- `bcc`: all member emails joined with `, `
- `subject`: `[YOUR PREFIX] ` + the subject (always prefix — add it even if the user already wrote it)
- `body`: the full HTML string
- `is_html`: `true`

<!-- Customize: YOUR_ACCOUNT_ALIAS → your accounts.json alias, YOUR_FROM_ADDRESS → the From address for that account, [YOUR PREFIX] → your subject prefix (e.g. [ACME]) or remove entirely -->

**If exactly 1 member**, send directly:
- `account`: `"YOUR_ACCOUNT_ALIAS"`
- `to`: that member's email address
- `subject`: `[YOUR PREFIX] ` + the subject
- `body`: the full HTML string
- `is_html`: `true`

Override: if the user explicitly requests individual sends, loop through members one call each.

After the send(s) complete, report:
```
✓ Sent to N members.
Failed (if any): list names + errors
```

---

## Gotchas

- The `get_contact_group` tool returns `[{name, email}]` — use `email` for the BCC list, `name` for the report.
- BCC mode: `to` must be a real address — use the sender's own From address (`YOUR_FROM_ADDRESS`), not blank.
- The template file path is absolute: `${CLAUDE_PLUGIN_ROOT}/library/aimm-newsletter/assets/template.html` — use the Read tool to load it.
- Do not skip the preview/confirmation step even if the user seems certain.
- If a send fails for one member, continue with the rest and report the failure at the end.
