"""
OAuth + CV Upload in one script with local callback server
"""

import os, sys, base64, json, threading, webbrowser
sys.path.insert(0, r'c:\Agent Coco')

from flask import Flask, request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build as gdrive_build
from googleapiclient.http import MediaFileUpload
import psycopg2
import re

app = Flask(__name__)
auth_code_storage = {'code': None}

@app.route('/callback')
def callback():
    auth_code_storage['code'] = request.args.get('code')
    return "Authorization successful! You can close this window."

def fetch_cvs():
    """Download CVs from database"""
    DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
    CV_DIR = r'c:\Agent Coco\output\cvs_job26'
    os.makedirs(CV_DIR, exist_ok=True)

    CANDIDATE_IDS = [1064, 1090, 1096, 1048, 1078, 1051, 817, 823, 1085, 1058, 1071, 1103]

    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name || ' ' || c.last_name, c.resume_data
        FROM candidates c WHERE c.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (CANDIDATE_IDS,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    cv_paths = {}
    for cand_id, name, b64_data in rows:
        try:
            pdf_data = base64.b64decode(b64_data)
            filename = f"{re.sub(r'[^a-zA-Z0-9_\- ]', '', name)}_CV.pdf"
            filepath = os.path.join(CV_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(pdf_data)
            cv_paths[name] = filepath
            print(f"[OK] Downloaded: {name}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")

    return cv_paths

def upload_cvs_to_drive(creds):
    """Upload CVs and return links"""
    service = gdrive_build('drive', 'v3', credentials=creds)
    cv_paths = fetch_cvs()

    drive_links = {}
    for name, filepath in cv_paths.items():
        try:
            file_metadata = {'name': f"{name} — CV (Job 26).pdf"}
            media = MediaFileUpload(filepath, mimetype='application/pdf')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            file_id = file.get('id')
            service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
            drive_links[name] = f"https://drive.google.com/file/d/{file_id}/view"
            print(f"[OK] Uploaded: {name}")
        except Exception as e:
            print(f"[FAIL] Upload {name}: {e}")

    return drive_links

def main():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    flow = InstalledAppFlow.from_client_secrets_file(
        r'c:\Agent Coco\data\credentials.json',
        scopes=SCOPES,
        redirect_uri='http://localhost:8080/callback'
    )

    print("[INFO] Starting OAuth flow...")
    creds = flow.run_local_server(port=8080, open_browser=True)

    print("[INFO] Starting CV upload...")
    drive_links = upload_cvs_to_drive(creds)

    # Save links
    with open(r'c:\Agent Coco\job26_cv_links.json', 'w') as f:
        json.dump(drive_links, f, indent=2)

    print(f"\n[OK] Upload complete! {len(drive_links)} CVs uploaded.")
    print("Links saved to job26_cv_links.json")

if __name__ == '__main__':
    main()
