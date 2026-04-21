---
name: linkedin-fancy-text
description: Formats LinkedIn post text with Unicode bold/italic so it stands out visually. Triggered when Lisa says /linkedin-fancy-text, "format this for LinkedIn", or "format my LinkedIn post". Takes a post with **bold** and _italic_ markers and converts to copy-paste ready Unicode.
---

# LinkedIn Text Formatter

## What This Does
LinkedIn doesn't support native text formatting — but Unicode mathematical characters *look* like bold/italic text. This skill converts a plain post with markdown-style markers into Unicode that you can paste directly into LinkedIn.

## Trigger
`/linkedin-format` — or any request like "format this for LinkedIn", "make this LinkedIn-ready", "convert my post formatting"

---

## Format Markers

Tell Lisa to mark up her post using:

| Marker | Style | Example |
|--------|-------|---------|
| `**text**` | 𝐁𝐨𝐥𝐝 (serif) | `**Key insight**` → 𝐊𝐞𝐲 𝐢𝐧𝐬𝐢𝐠𝐡𝐭 |
| `_text_` | 𝐼𝑡𝑎𝑙𝑖𝑐 (serif) | `_note:_` → 𝑛𝑜𝑡𝑒: |
| `***text***` | 𝑩𝒐𝒍𝒅 𝒊𝒕𝒂𝒍𝒊𝒄 | `***big idea***` → 𝒃𝒊𝒈 𝒊𝒅𝒆𝒂 |

---

## Workflow

### Step 1 — Get the text

If Lisa hasn't pasted text yet, prompt:

> Paste your LinkedIn post below. Wrap what you want formatted:
> - `**text**` → 𝐛𝐨𝐥𝐝
> - `_text_` → 𝑖𝑡𝑎𝑙𝑖𝑐
> - `***text***` → 𝒃𝒐𝒍𝒅 𝒊𝒕𝒂𝒍𝒊𝒄
>
> Everything else passes through unchanged — punctuation, emoji, numbers, line breaks all stay as-is.

If Lisa pastes her text with the command in one message, skip the prompt and go straight to Step 2.

### Step 2 — Run the formatter

Write the input text to `/tmp/linkedin_input.txt` using the Write tool, then run:

```bash
python3 ~/.claude/skills/linkedin-format/formatter.py /tmp/linkedin_input.txt
```

Capture the output.

### Step 3 — Present the result

Show the formatted output like this — NOT in a code block (LinkedIn paste needs clean text):

---

✅ **Copy this into LinkedIn:**

[formatted text, presented as plain output]

---

Then ask: "Want to adjust any of the formatting?"

---

## Whole-Post Style (Optional)

If Lisa wants her *entire post* in a consistent font style (not just specific words), run with `--style`:

```bash
python3 ~/.claude/skills/linkedin-format/formatter.py --style sans_bold /tmp/linkedin_input.txt
```

Available styles: `bold`, `italic`, `bold_italic`, `sans_bold`

Offer this if Lisa asks "can you make the whole thing bold?" or "try a different font."

---

## Common Mistakes to Avoid
- Do NOT put the output in a triple-backtick code block — it adds noise and makes it harder to copy cleanly
- Do NOT modify the post content — only convert the markers, leave everything else exactly as written
- Do NOT skip the formatter script and try to do the Unicode conversion manually — use the script for accuracy
