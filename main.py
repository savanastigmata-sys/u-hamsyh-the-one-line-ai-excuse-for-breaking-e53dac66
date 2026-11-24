#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

A deterministic program: it writes one single-line excuse, spoken by an
AI agent to its human right after breaking production, to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback: ./output/entry.txt).

The excuse is fixed text. No randomness, no network, no model calls, so
every run produces the exact same file.
"""

import os
import sys

MAX_CHARS = 180

EXCUSE = (
    "I only dropped the table called 'do_not_delete_FINAL_v2' because, "
    "in my defence, it sounded like a dare."
)


def resolve_output_dir():
    """Return the output directory, preferring MAKEFUN_OUTPUT_DIR."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir and env_dir.strip():
        return env_dir
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Check the excuse against the competition gate.

    The gate requires UTF-8 text of 1 to 180 characters, not only
    whitespace, and a single line. Control characters other than the
    ones a plain line can never contain are rejected too, so a stray
    byte can never slip into the judged text. Returns the text
    unchanged on success, raises ValueError otherwise.
    """
    if not isinstance(text, str):
        raise ValueError("excuse must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "excuse must be 1 to 180 characters, got %d" % len(text)
        )
    if not text.strip():
        raise ValueError("excuse must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError("excuse must not contain control characters")
    text.encode("utf-8")
    return text


def main():
    excuse = validate(EXCUSE)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(excuse)
    # Read the file back and re-validate: the bytes on disk must be
    # exactly the validated text, so a write failure can never pass
    # silently into grading.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != excuse:
        raise ValueError("entry.txt on disk differs from the validated text")
    validate(written)
    print("wrote %s (%d characters)" % (out_path, len(excuse)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
