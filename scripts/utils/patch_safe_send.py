"""
patch_safe_send.py
Automatically patches all send scripts to use safe_sendmail() instead of raw sendmail().
Run once. Safe to re-run — skips already-patched files.
"""

import os, re, sys

ROOT    = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SCRIPTS = os.path.join(ROOT, "scripts")

# Files to skip (already patched or is the bouncer itself)
SKIP = {
    "safe_send.py",
    "patch_safe_send.py",
    "send_job36_rejection_live.py",
    "send_job36_debrief_invite_live.py",
}

IMPORT_INJECT = '''\nimport sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "{rel_to_root}"))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
'''

# Match: server.sendmail(X, Y, Z) or smtp.sendmail(X, Y, Z)
# Capture: (server_var, sender_var, recipients_var, msg_expr)
SENDMAIL_RE = re.compile(
    r'(\w+)\.sendmail\(([^,]+),\s*([^,]+),\s*([^)]+)\)'
)

def rel_to_root(filepath):
    """Return '../..' style relative path from file to project root."""
    depth = filepath.replace(SCRIPTS, "").count(os.sep) - 1
    return "/".join([".."] * depth)

def patch_file(filepath):
    filename = os.path.basename(filepath)
    if filename in SKIP:
        return False

    with open(filepath, encoding="utf-8", errors="ignore") as f:
        src = f.read()

    # Skip if already patched
    if "safe_sendmail" in src:
        return False

    # Skip if no sendmail call
    if ".sendmail(" not in src:
        return False

    original = src

    # 1. Inject import after the last "from dotenv" or "import" block
    inject = IMPORT_INJECT.format(rel_to_root=rel_to_root(filepath))

    # Find insertion point: after load_dotenv line, or after last import block
    insert_after = None
    for pattern in [r'load_dotenv\([^)]*\)', r'from dotenv import[^\n]+', r'import smtplib[^\n]*']:
        m = re.search(pattern, src)
        if m:
            insert_after = m.end()
            break

    if insert_after is None:
        print(f"  SKIP (no insertion point found): {filename}")
        return False

    src = src[:insert_after] + inject + src[insert_after:]

    # 2. Replace .sendmail( calls
    script_label = filename.replace(".py", "")

    def replace_sendmail(m):
        server_var   = m.group(1)
        sender_var   = m.group(2).strip()
        recip_var    = m.group(3).strip()
        msg_expr     = m.group(4).strip()
        return (
            f"allow_candidate_addresses({recip_var} if isinstance({recip_var}, list) "
            f"else [{recip_var}])\n        "
            f"safe_sendmail({server_var}, {sender_var}, "
            f"{recip_var}, {msg_expr}, context='{script_label}')"
        )

    src = SENDMAIL_RE.sub(replace_sendmail, src)

    if src == original:
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(src)

    return True


patched = []
skipped = []

for dirpath, _, files in os.walk(SCRIPTS):
    for fname in files:
        if not fname.endswith(".py"):
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            result = patch_file(fpath)
            if result:
                patched.append(fpath.replace(ROOT + os.sep, ""))
            else:
                skipped.append(fname)
        except Exception as e:
            print(f"ERROR patching {fname}: {e}")

print(f"\nPatched {len(patched)} files:")
for f in patched:
    print(f"  + {f}")

print(f"\nSkipped {len(skipped)} files (already patched or no sendmail).")
