#!/usr/bin/env python3
"""
OmA Behavioral Validator: scripts/check_sources.py
Verifies:
1. Each declared source file in research/sources/ exists and is non-empty.
2. Contains the recorded command and comment count/metadata.
3. research/discoveries/reading_notes.md exists and is non-empty.
4. Every quote under [QUOTED] is under 25 words and appears literally in its source file.
"""

import sys
import re
from pathlib import Path

def fail(msg: str):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(1)

def info(msg: str):
    print(f"[PASS] {msg}")

def main():
    root = Path.cwd()
    notes_path = root / "research" / "discoveries" / "reading_notes.md"
    sources_dir = root / "research" / "sources"

    if not notes_path.exists():
        fail(f"Reading notes file missing: {notes_path}")
    if notes_path.stat().st_size == 0:
        fail(f"Reading notes file is empty: {notes_path}")

    notes_text = notes_path.read_text(encoding="utf-8")
    info("reading_notes.md exists and is non-empty")

    # Source files to check
    source_files = list(sources_dir.glob("*.md"))
    if not source_files:
        fail(f"No source markdown files found in {sources_dir}")

    for src in source_files:
        if src.stat().st_size == 0:
            fail(f"Source file {src.name} is empty")
        
        content = src.read_text(encoding="utf-8")
        
        # Check command record
        if "Command:" not in content and "command:" not in content and "Exact Command:" not in content:
            fail(f"Source {src.name} missing recorded retrieval command")

        # Check comment count or status record
        if "Comment Count:" not in content and "Comments:" not in content and "Status:" not in content:
            fail(f"Source {src.name} missing recorded comment count or status")

        info(f"Verified source integrity: {src.name}")

    # Check quotes in reading_notes.md
    # Looking for lines or blocks containing [QUOTED] "..." from <file> or similar
    # Regex pattern matching quotes: e.g. [QUOTED] "..." or `...`
    quote_matches = re.findall(r'\[QUOTED\]\s*(?:source:\s*([^\n\r]+?)\s*)?["“](.*?)["”]', notes_text, re.DOTALL)
    
    if not quote_matches:
        # Check alternate format: lines starting with - [QUOTED]
        quote_blocks = [line for line in notes_text.splitlines() if "[QUOTED]" in line]
        if not quote_blocks:
            fail("No [QUOTED] entries found in reading_notes.md")

    quote_count = 0
    # Match: [QUOTED] ... "quote text"
    for match in re.finditer(r'\[QUOTED\](?:\s+source:\s*([^\s"]+))?[^"“”]*["“]([^"”]+)["”]', notes_text):
        ref_source, quote_text = match.groups()
        quote_text = quote_text.strip()
        word_count = len(quote_text.split())
        if word_count > 25:
            fail(f"Quote exceeds 25 words ({word_count} words): '{quote_text[:50]}...'")

        # Verify literal presence
        found = False
        if ref_source and (sources_dir / ref_source).exists():
            src_content = (sources_dir / ref_source).read_text(encoding="utf-8")
            if quote_text in src_content:
                found = True
        
        if not found:
            # Search across all sources
            for src in source_files:
                if quote_text in src.read_text(encoding="utf-8"):
                    found = True
                    break

        if not found:
            fail(f"Literal quote not found in source files: '{quote_text}'")

        info(f"Verified literal quote ({word_count} words): \"{quote_text[:40]}...\"")
        quote_count += 1

    if quote_count == 0:
        fail("No valid [QUOTED] entries could be verified.")

    info(f"Verified {quote_count} literal quote(s) (all under 25 words)")
    print("\nAll OmA source and quote verification criteria passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
