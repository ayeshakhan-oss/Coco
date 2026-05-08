# scripts/memory/memory_sync.py
"""One-time sync: copies files from historical memory location to curated location.
Skips files that already exist. Prints a report of what was copied vs skipped."""

from pathlib import Path
import shutil

HISTORICAL = Path.home() / ".claude" / "projects" / "C--Agent-Coco" / "memory"
CURATED = Path("C:/Agent Coco/memory")

def sync():
    if not HISTORICAL.exists():
        print(f"Historical path not found: {HISTORICAL}")
        return

    copied = []
    skipped = []

    for src in sorted(HISTORICAL.glob("*.md")):
        dst = CURATED / src.name
        if dst.exists():
            skipped.append(src.name)
        else:
            shutil.copy2(src, dst)
            copied.append(src.name)

    print(f"\nCopied ({len(copied)} files):")
    for f in copied:
        print(f"  + {f}")
    print(f"\nSkipped ({len(skipped)} files — already exist in curated):")
    for f in skipped:
        print(f"  ~ {f}")

if __name__ == "__main__":
    sync()
