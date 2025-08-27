#!/usr/bin/env python3
"""
find_words_batch.py

Scan a folder of transcript .txt files and produce one grouped-by-word (hits-only) report per file.

Usage:
  python find_words_batch.py -d transcripts/ words.txt
  # optional:
  #   --outdir OUT/       where to save results (default: <dir>/results/)
  #   --substring         use substring matches (default = whole word)
  #   --no-highlight      do not wrap matches with [[ ]]

Transcript format: each line "mm:ss text" or "hh:mm:ss text"
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Matches "mm:ss text" or "hh:mm:ss text"
TIMESTAMP_RE = re.compile(r'^\s*((?:\d{1,2}:){1,2}\d{2})\s+(.*\S)\s*$')

def parse_args():
    p = argparse.ArgumentParser(description="Batch: group transcript hits by word (only words with matches).")
    p.add_argument("-d", "--dir", type=Path, required=True,
                   help="Directory containing transcript .txt files")
    p.add_argument("words", type=Path, help="File with words, one per line")
    p.add_argument("--outdir", type=Path, default=None,
                   help="Directory to write results (default: <dir>/results/)")
    p.add_argument("--substring", action="store_true",
                   help="Use substring matches (default = whole-word)")
    p.add_argument("--no-highlight", action="store_true",
                   help="Disable [[match]] highlighting in output")
    return p.parse_args()

def load_words(path: Path) -> List[str]:
    raw = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return [w.strip() for w in raw if w.strip() and not w.strip().startswith("#")]

def parse_transcript(path: Path) -> List[Tuple[str, str]]:
    items: List[Tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = TIMESTAMP_RE.match(line)
        if m:
            items.append((m.group(1), m.group(2)))
    return items

def ts_to_seconds(ts: str) -> int:
    parts = [int(p) for p in ts.split(":")]
    if len(parts) == 2:
        h, m, s = 0, parts[0], parts[1]
    else:
        h, m, s = parts
    return h*3600 + m*60 + s

def build_matcher(word: str, substring: bool):
    if substring:
        return re.compile(re.escape(word), re.IGNORECASE)
    else:
        return re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE)

def highlight(text: str, rx: re.Pattern) -> str:
    return rx.sub(lambda m: f"[[{m.group(0)}]]", text)

def process_file(transcript_path: Path, words: List[str], substring: bool, no_highlight: bool) -> str:
    """Return the output text for a single transcript (grouped by word, hits only)."""
    transcript = parse_transcript(transcript_path)
    if not transcript:
        return f"Transcript Search (grouped by word, hits only)\nTranscript: {transcript_path}\n(Empty or no lines matched timestamp format)\n"

    # Prepare matchers
    matchers: Dict[str, re.Pattern] = {w: build_matcher(w, substring) for w in words}
    # word -> dict of (ts,text) -> (sec, ts, text) to dedupe within each word
    grouped: Dict[str, Dict[Tuple[str, str], Tuple[int, str, str]]] = {w: {} for w in words}

    for ts, text in transcript:
        sec = ts_to_seconds(ts)
        for w, rx in matchers.items():
            if rx.search(text):
                key = (ts, text)
                if key not in grouped[w]:
                    grouped[w][key] = (sec, ts, text)

    # Keep only words that actually had hits, preserving original order
    words_with_hits = [w for w in words if grouped[w]]

    out_lines: List[str] = []
    out_lines.append("Transcript Search (grouped by word, hits only)")
    out_lines.append(f"Transcript: {transcript_path.name}")
    out_lines.append(f"Mode: {'substring' if substring else 'whole-word'}")
    out_lines.append(f"Highlight: {'off' if no_highlight else '[[match]]'}")
    out_lines.append("-" * 72)

    if not words_with_hits:
        out_lines.append("\n(no matches)")
        return "\n".join(out_lines) + "\n"

    # Compact index only for words with hits
    out_lines.append("\nINDEX (hits per word):")
    for w in words_with_hits:
        out_lines.append(f"- {w}: {len(grouped[w])}")
    out_lines.append("\n" + "=" * 72)

    # Sections per word (hits sorted by time)
    for w in words_with_hits:
        out_lines.append(f'\nWORD: "{w}"  —  {len(grouped[w])} hit{"s" if len(grouped[w])!=1 else ""}')
        out_lines.append("-" * 72)
        rx = matchers[w]
        hits = sorted(grouped[w].values(), key=lambda t: t[0])
        for _, ts, txt in hits:
            shown = txt if no_highlight else highlight(txt, rx)
            out_lines.append(f"[{ts}] {shown}")

    return "\n".join(out_lines) + "\n"

def main():
    args = parse_args()
    in_dir: Path = args.dir
    if not in_dir.is_dir():
        raise SystemExit(f"Not a directory: {in_dir}")

    out_dir: Path = args.outdir or (in_dir / "results")
    out_dir.mkdir(parents=True, exist_ok=True)

    words = load_words(args.words)
    if not words:
        raise SystemExit("Words file is empty (or only comments).")

    txt_files = sorted([p for p in in_dir.iterdir() if p.is_file() and p.suffix.lower() == ".txt"])

    if not txt_files:
        raise SystemExit(f"No .txt files found in {in_dir}")

    print(f"📂 Processing {len(txt_files)} transcript file(s) from: {in_dir}")
    print(f"📝 Writing results to: {out_dir}")

    processed = 0
    with_hits = 0
    for p in txt_files:
        out_text = process_file(p, words, args.substring, args.no_highlight)
        # Name: "<original>.hits.txt"
        out_path = out_dir / f"{p.stem}.hits.txt"
        out_path.write_text(out_text, encoding="utf-8")
        processed += 1
        if "\n(no matches)\n" not in out_text:
            with_hits += 1
        print(f"  - {p.name} → {out_path.name}")

    print(f"\n✅ Done. Processed {processed} file(s); {with_hits} had matches.")

if __name__ == "__main__":
    main()
