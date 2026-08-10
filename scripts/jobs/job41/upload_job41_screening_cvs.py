# -*- coding: utf-8 -*-
"""Job 41 (Growth Manager - Karachi) screening: download shortlist+maybe CVs from
Markaz (Neon HTTPS SQL API) and upload to a shared Google Drive folder.
Prints app_id -> webViewLink for the screening report."""
import os, re, base64, json
import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild
from googleapiclient.http import MediaFileUpload

load_dotenv(r"c:\Agent Coco\.env")
URL = os.environ["DATABASE_URL"]
HOST = URL.split("@")[1].split("/")[0]

APP_IDS = [3811, 4063, 4065, 4075, 4083, 4113, 4121, 4132,   # shortlist
           3832, 4072, 4073, 4087, 4092, 4097, 4128]          # maybe

CV_DIR = r"c:\Agent Coco\output\job41\cvs"
os.makedirs(CV_DIR, exist_ok=True)


def q(sql, params=None):
    r = requests.post(f"https://{HOST}/sql",
                      headers={"Neon-Connection-String": URL, "Content-Type": "application/json"},
                      json={"query": sql, "params": params or []}, timeout=120)
    r.raise_for_status()
    return r.json()["rows"]


creds = Credentials.from_authorized_user_file(r"c:\Agent Coco\.claude\config\token_sheets_broad.json")
drive = gbuild("drive", "v3", credentials=creds)

folder = drive.files().create(body={
    "name": "Job 41 GM-Karachi — Screening CVs (10 Aug 2026)",
    "mimeType": "application/vnd.google-apps.folder",
}, fields="id, webViewLink").execute()
drive.permissions().create(fileId=folder["id"], body={"role": "reader", "type": "anyone"}).execute()
print("FOLDER:", folder["webViewLink"])

links = {}
for app_id in APP_IDS:
    rows = q("""SELECT TRIM(c.first_name || ' ' || COALESCE(c.last_name,'')) AS name,
                       c.resume_file_name, c.resume_data
                FROM applications a JOIN candidates c ON c.id = a.candidate_id
                WHERE a.id = $1""", [app_id])
    if not rows or not rows[0]["resume_data"]:
        print(f"[SKIP] app {app_id}: no resume")
        continue
    name = rows[0]["name"]
    ext = os.path.splitext(rows[0]["resume_file_name"] or "cv.pdf")[1].lower() or ".pdf"
    safe = re.sub(r"[^a-zA-Z0-9_\- ]", "", name).strip()
    path = os.path.join(CV_DIR, f"{safe}_CV{ext}")
    with open(path, "wb") as f:
        f.write(base64.b64decode(rows[0]["resume_data"]))

    mimetype = "application/pdf" if ext == ".pdf" else \
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    media = MediaFileUpload(path, mimetype=mimetype)
    f = drive.files().create(body={"name": f"{safe} — CV (Job 41)", "parents": [folder["id"]]},
                             media_body=media, fields="id, webViewLink").execute()
    links[app_id] = {"name": name, "link": f["webViewLink"]}
    print(f"[OK] app {app_id}  {name}: {f['webViewLink']}")

with open(r"c:\Agent Coco\output\job41\cv_drive_links.json", "w", encoding="utf-8") as fh:
    json.dump({"folder": folder["webViewLink"], "cvs": links}, fh, indent=2, ensure_ascii=False)
print("\nSaved links to output/job41/cv_drive_links.json")
