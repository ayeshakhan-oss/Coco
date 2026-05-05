# Warm Bench Email SEND LOG

**Purpose:** Track every warm bench feedback email send (pilot + live) for self-diagnosis if errors occur.

**When to update:** Immediately after each send (pilot or live).

---

## Send Records

| Date/Time (PKT) | Recipient Email | Candidate Name | Subject Line | Body Preview (first 300 chars) | Status | Mode | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

---

## Entry Template

```
Date/Time: [YYYY-MM-DD HH:MM AM/PM PKT]
Recipient: [email@domain.com]
Candidate: [Full Name]
Subject: [exact subject line]
Body (first 300 chars): [copy-paste first 300 characters of body HTML]
Status: sent
Mode: [pilot / live]
Notes: [any issues/observations]
```

---

## Self-Diagnosis Protocol

When error reported:
1. Find the send record in this log
2. Compare recipient in log vs error report
3. Compare subject in log vs what user expected
4. Compare body preview in log vs what user expected
5. Identify discrepancy
6. Tell user: "I sent X instead of Y because [reason]" (don't ask user to explain)
