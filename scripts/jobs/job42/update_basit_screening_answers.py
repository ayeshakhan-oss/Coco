# -*- coding: utf-8 -*-
"""Add Syed Basit Hussain's screening answers to his Job-42 application (app 4142, cand 3350).
Data provided by Ayesha in chat 2026-08-14: city, relocation, current/expected salary, notice period.
Guards: exact app+candidate+email match, custom_answers currently empty, row-count assert.
Email + phone in the data match what's already on record - no candidate changes needed."""
import os, json
import requests
from dotenv import load_dotenv

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

APP_ID, CAND_ID = 4142, 3350

def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=60)
    r.raise_for_status()
    return r.json()["rows"]

answers = {
    "screening_current_city":        {"question": "Current City", "answer": "Islamabad"},
    "screening_willing_to_relocate": {"question": "Willingness to Relocate", "answer": "Already based in Islamabad"},
    "screening_current_salary":      {"question": "Current Monthly Salary", "answer": "Last drawn salary was 217,000 PKR"},
    "screening_expected_salary":     {"question": "Expected Monthly Salary", "answer": "At least above 250,000 PKR/month"},
    "screening_notice_period":       {"question": "Notice Period", "answer": "10 Days"},
}

note_line = ("\n[2026-08-14, via Ayesha] Screening answers: Current city Islamabad (no relocation needed). "
             "Current salary: last drawn 217,000 PKR/month. Expected: at least above 250,000 PKR/month. "
             "Notice period: 10 days.")

pre = q("""SELECT a.id, a.custom_answers, c.email FROM applications a
           JOIN candidates c ON c.id = a.candidate_id
           WHERE a.id = $1 AND a.candidate_id = $2 AND a.job_id = 42""", [APP_ID, CAND_ID])
assert len(pre) == 1 and pre[0]["email"] == "syed.basit89@gmail.com", f"Guard failed: {pre} - ABORTING"
assert pre[0]["custom_answers"] in ({}, None), f"Guard failed: custom_answers not empty: {pre[0]['custom_answers']} - ABORTING"

rows = q("""UPDATE applications
            SET custom_answers = $1::jsonb,
                notes = COALESCE(notes,'') || $2,
                updated_at = NOW()
            WHERE id = $3 AND candidate_id = $4 AND job_id = 42
            RETURNING id""", [json.dumps(answers), note_line, APP_ID, CAND_ID])
assert len(rows) == 1, f"Expected 1 row, got {len(rows)} - INVESTIGATE"

verify = q("SELECT custom_answers, notes FROM applications WHERE id = $1", [APP_ID])
print("custom_answers keys:", list(verify[0]["custom_answers"].keys()))
print("notes tail:", verify[0]["notes"][-260:])
