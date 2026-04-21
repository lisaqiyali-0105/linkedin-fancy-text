#!/usr/bin/env python3
"""
LinkedIn Unicode Text Formatter
Converts **bold**, _italic_, ***bold italic*** markers to Unicode characters
that display as formatted text on LinkedIn.

Usage:
    python3 formatter.py [filename]
    echo "**Hello** world" | python3 formatter.py
"""

import sys
import re

# ── Unicode character maps ──────────────────────────────────────────────────────

# Bold Serif (Mathematical Bold) — uppercase U+1D400, lowercase U+1D41A, digits U+1D7CE
BOLD = {
    **{chr(ord('A') + i): chr(0x1D400 + i) for i in range(26)},
    **{chr(ord('a') + i): chr(0x1D41A + i) for i in range(26)},
    **{chr(ord('0') + i): chr(0x1D7CE + i) for i in range(10)},
}

# Italic Serif (Mathematical Italic) — uppercase U+1D434, lowercase U+1D44E
# Exception: 'h' → ℎ (U+210E) because U+1D455 is unassigned in Unicode
ITALIC = {
    **{chr(ord('A') + i): chr(0x1D434 + i) for i in range(26)},
    **{chr(ord('a') + i): chr(0x1D44E + i) for i in range(26)},
    'h': '\u210E',  # override: ℎ
}

# Bold Italic Serif (Mathematical Bold Italic) — uppercase U+1D468, lowercase U+1D482
BOLD_ITALIC = {
    **{chr(ord('A') + i): chr(0x1D468 + i) for i in range(26)},
    **{chr(ord('a') + i): chr(0x1D482 + i) for i in range(26)},
}

# Sans-Serif Bold — uppercase U+1D5D4, lowercase U+1D5EE, digits U+1D7EC
SANS_BOLD = {
    **{chr(ord('A') + i): chr(0x1D5D4 + i) for i in range(26)},
    **{chr(ord('a') + i): chr(0x1D5EE + i) for i in range(26)},
    **{chr(ord('0') + i): chr(0x1D7EC + i) for i in range(10)},
}

STYLE_MAP = {
    'bold': BOLD,
    'italic': ITALIC,
    'bold_italic': BOLD_ITALIC,
    'sans_bold': SANS_BOLD,
}

# ── Conversion helpers ──────────────────────────────────────────────────────────

def convert(text, mapping):
    """Apply a character mapping, passing through unmapped characters unchanged."""
    return ''.join(mapping.get(c, c) for c in text)


def format_linkedin(raw: str) -> str:
    """
    Convert markdown-style markers to Unicode formatting.

    Markers:
        ***text***  →  bold italic
        **text**    →  bold
        _text_      →  italic

    Order matters: ***...*** must be processed before **...** to avoid partial matches.
    """
    result = raw

    result = re.sub(
        r'\*\*\*(.+?)\*\*\*',
        lambda m: convert(m.group(1), BOLD_ITALIC),
        result,
        flags=re.DOTALL,
    )
    result = re.sub(
        r'\*\*(.+?)\*\*',
        lambda m: convert(m.group(1), BOLD),
        result,
        flags=re.DOTALL,
    )
    result = re.sub(
        r'_(.+?)_',
        lambda m: convert(m.group(1), ITALIC),
        result,
        flags=re.DOTALL,
    )

    return result


def whole_style(raw: str, style: str) -> str:
    """Convert every letter in the entire text to a given style."""
    mapping = STYLE_MAP.get(style, BOLD)
    return convert(raw, mapping)


# ── Entry point ─────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # Optional --style flag for whole-post conversion
    style = None
    if '--style' in args:
        idx = args.index('--style')
        style = args[idx + 1]
        args = [a for i, a in enumerate(args) if i != idx and i != idx + 1]

    if args:
        with open(args[0], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if style:
        result = whole_style(text, style)
    else:
        result = format_linkedin(text)

    print(result, end='')


if __name__ == '__main__':
    main()
