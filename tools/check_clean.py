"""Guard for the content policy: fails if the repository contains anything environment-specific.

Checks (all text files except .git): URLs, e-mail addresses, domain names, GUIDs, long opaque identifiers,
credential assignments, and one environment-specific word. Keep any private deny-list of real names OUTSIDE this repository
and pass it with --deny-file <path> (one term per line, case-insensitive).

Usage:  python tools/check_clean.py [--deny-file path]
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
TLDS = "com|net|org|io|dev|cloud|microsoft|ms|de|at|eu|info|app|ai|co|uk|us"

PATTERNS = {
    "url": re.compile(r"(?i)\b(?:https?://|www\.)\S+"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "domain": re.compile(rf"(?i)\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:{TLDS})\b"),
    "guid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "opaque-id": re.compile(r"\b[A-Za-z0-9_-]{32,}\b"),
    "credential": re.compile(r"(?i)\b(?:password|passwd|secret|token|api[_-]?key)\b\s*[:=]\s*[\"']?[^\s\"'<>$(){}\[\]]{4,}"),
    "env-word": re.compile(r"(?i)" + "ten" + "ants?" + r""),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deny-file", help="private list of forbidden terms (kept outside the repo)")
    args = ap.parse_args()
    deny = []
    if args.deny_file:
        deny = [t.strip().lower() for t in Path(args.deny_file).read_text(encoding="utf-8").splitlines() if t.strip()]

    findings = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT)
        for lineno, line in enumerate(text.splitlines(), start=1):
            for name, rx in PATTERNS.items():
                if path.name == "check_clean.py" and name in {"env-word", "credential"}:
                    continue
                for m in rx.finditer(line):
                    print(f"{rel}:{lineno}: {name}: {m.group(0)[:80]}")
                    findings += 1
            low = line.lower()
            for term in deny:
                if term in low:
                    print(f"{rel}:{lineno}: deny-list term found")
                    findings += 1
    print(f"\n{findings} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
