---
name: linkedin-fancy-text
description: Converts LinkedIn post text to Unicode bold/italic for copy-paste into LinkedIn. Triggered by /linkedin-fancy-text, "format this for LinkedIn", or "format my LinkedIn post". Handles raw text, .md files, and .docx files.
---

# LinkedIn Fancy Text

## What This Does
LinkedIn doesn't support native formatting — but Unicode mathematical characters look like bold/italic text and paste correctly. This skill takes a post and returns Unicode-formatted text ready to copy into LinkedIn.

## Trigger
`/linkedin-fancy-text` — or "format this for LinkedIn", "make this LinkedIn-ready", "format my post"

---

## Step 1 — Detect the input type

### Path A — Raw text pasted (no file path)

User pastes their post directly. Check if it contains `**markers**` or `_markers_`:

- **Markers present** → skip to Step 2A, convert silently
- **No markers** → ask: *"What do you want to bold, italic, or bold italic? Describe it in plain English — e.g. 'bold the first line, bold italic AT ALL'."*
  - Once the user responds, add the markers to the text yourself, then go to Step 2A

### Path B — Markdown or Obsidian file (`.md`)

User provides a file path ending in `.md`. Read the file with the Read tool. Convert any `**markers**` found. Go to Step 2A.

### Path C — Word document (`.docx`)

User provides a `.docx` file path. Go straight to Step 2B — the script reads formatting metadata directly from the file.

---

## Step 2A — Run the formatter (text with markers)

Write the marked-up text to `/tmp/linkedin_input.txt`, then run:

```bash
python3 ~/.claude/skills/linkedin-fancy-text/formatter.py /tmp/linkedin_input.txt
```

Capture the output and go to Step 3.

## Step 2B — Run the formatter (Word doc)

Run directly on the `.docx` file — no temp file needed:

```bash
python3 ~/.claude/skills/linkedin-fancy-text/formatter.py /path/to/file.docx
```

Capture the output and go to Step 3.

---

## Step 3 — Present the result

Show the output as plain text — NOT in a code block:

---

✅ **Copy this into LinkedIn:**

[formatted text here]

---

Then ask: "Want to adjust anything?"

---

## Whole-Post Style (Optional)

If the user wants the entire post in one consistent style, use `--style`:

```bash
python3 ~/.claude/skills/linkedin-fancy-text/formatter.py --style sans_bold /tmp/linkedin_input.txt
```

Available styles: `bold`, `italic`, `bold_italic`, `sans_bold`

Offer this if the user asks "make the whole thing bold" or "try a different font."

---

## Rules
- Never put output in a triple-backtick code block — it makes it hard to copy
- Never modify post content — only apply formatting
- Never do Unicode conversion manually — always use the script
- For .docx files, always use the script directly on the file path — do not extract text first
