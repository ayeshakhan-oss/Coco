---
name: markaz-submissions-arrive-by-email-2026-08-17
description: "Every Markaz document submission is mirrored to email as an attachment ('New Case Study Received' notification) — check the mailbox FIRST; the /api/case-study-file 401 wall is not a blocker."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 673ef4b8-03ca-4de3-80bf-f4f15266cda4
  modified: 2026-08-17T06:45:33.257Z
---

**Ayesha, 2026-08-17:** "when someone submits the case study response on markaz in document, we
always receive it in the email."

Markaz sends a **"New Case Study Received"** notification (from Taleemabad Markaz — Talent
Acquisition) carrying **the submitted documents as real attachments**, named
`case-study-<appId>-<word|excel>-<ts>-<Original_Name>.<ext>`. It lands in Ayesha's mailbox /
hiring@, not the jawwad.ali mailbox the Gmail MCP is connected to.

**So the retrieval order is: email FIRST, Drive links second, Markaz UI never.**

I wasted a cycle reporting three candidates as unreadable because
`https://markaz.taleemabad.com/api/case-study-file/<appId>/<word|excel>` returns **401** to
automation (staff Google SSO only). That wall is real but **irrelevant** — the same files are
sitting in the mailbox. Blocked submissions are almost never actually blocked.

Working path (read-only IMAP, see [[reference_ayesha_mailbox_imap_2026_08_10]]):

```python
M = imaplib.IMAP4_SSL("imap.gmail.com"); M.login("ayesha.khan@taleemabad.com", os.environ["EMAIL_PASSWORD"])
M.select('"[Gmail]/All Mail"', readonly=True)
M.search(None, '(SUBJECT "Case Study" SINCE "01-Aug-2026")')   # then walk parts for get_filename()
M.fetch(i, "(BODY.PEEK[])")                                     # PEEK; log to logs/read_audit.log
```

Filter attachments by **application ID in the filename**, not by MIME type — the notification
carries both the Word/PDF and the Excel.

Cost of getting this wrong on Job 42: an entire evaluation report ranked 5 of 8 candidates, and
the 3 missing ones turned out to include **2 of the top 3** (Arshan Bilal 94, Yusra Amjad 89).
A ranking built on a partial pool is not a partial answer — it is a wrong one.

Related: [[comm_evidence_dual_source_rule_2026_06_20]] ·
[[case_study_folders_and_gm_lahore_eval_2026_08_10]]
