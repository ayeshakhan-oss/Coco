"""
Download resumes from DB, upload to Google Drive, get shareable links
"""

import os, sys, base64, re
sys.path.insert(0, r'c:\Agent Coco')
import psycopg2
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build as gdrive_build
from googleapiclient.http import MediaFileUpload

DB_CONN = "postgresql://neondb_owner:npg_kBQ10OASHEmd@ep-gentle-glitter-adkkn981.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
CV_DIR = r"c:\Agent Coco\output\cvs_job26"
os.makedirs(CV_DIR, exist_ok=True)

# Candidate IDs for shortlist + maybe (12 total)
CANDIDATE_IDS = [
    1064, 1090, 1096, 1048, 1078,  # Shortlist (5)
    1051, 817, 823, 1085, 1058, 1071, 1103  # Maybe (7)
]

def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\- ]', '', name)

def fetch_and_upload_cvs():
    print("Step 1: Fetching resumes from DB...")
    conn = psycopg2.connect(DB_CONN)
    cur = conn.cursor()

    # Fetch candidates with their resume data
    cur.execute("""
        SELECT c.id, c.first_name || ' ' || c.last_name as name, c.resume_data
        FROM candidates c
        WHERE c.id = ANY(%s) AND c.resume_data IS NOT NULL
    """, (CANDIDATE_IDS,))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"Found {len(rows)} candidates with resume data\n")

    # Save PDFs locally
    cv_paths = {}
    for cand_id, name, b64_data in rows:
        try:
            pdf_data = base64.b64decode(b64_data)
            filename = f"{safe_filename(name)}_CV.pdf"
            filepath = os.path.join(CV_DIR, filename)

            with open(filepath, 'wb') as f:
                f.write(pdf_data)

            cv_paths[name] = filepath
            print(f"[OK] Downloaded: {name}")
        except Exception as e:
            print(f"[FAIL] Failed {name}: {e}")

    print(f"\nStep 2: Uploading {len(cv_paths)} resumes to Google Drive...")

    # Load or create Google Drive credentials
    token_file = r'c:\Agent Coco\token_drive.json'
    creds = None

    try:
        creds = Credentials.from_authorized_user_file(
            token_file,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
    except:
        pass

    if not creds:
        from google_auth_oauthlib.flow import InstalledAppFlow
        flow = InstalledAppFlow.from_client_secrets_file(
            r'c:\Agent Coco\data\credentials.json',
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        creds = flow.run_local_server(port=0)
        with open(token_file, 'w') as f:
            f.write(creds.to_json())
        print("[OK] Generated new Drive token")

    service = gdrive_build('drive', 'v3', credentials=creds)

    # Upload to Drive and get links
    drive_links = {}
    for name, filepath in cv_paths.items():
        try:
            file_metadata = {
                'name': f"{name} — CV (Job 26 Soul Architect).pdf"
            }
            media = MediaFileUpload(filepath, mimetype='application/pdf')

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            file_id = file.get('id')

            # Make shareable
            service.permissions().create(
                fileId=file_id,
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()

            link = f"https://drive.google.com/file/d/{file_id}/view"
            drive_links[name] = link
            print(f"[OK] Uploaded: {name}")
        except Exception as e:
            print(f"[FAIL] Upload failed {name}: {e}")

    print(f"\nStep 3: Saving links to file...")

    # Save links to JSON for report generation
    import json
    with open(r'c:\Agent Coco\job26_cv_links.json', 'w') as f:
        json.dump(drive_links, f, indent=2)

    print(f"[OK] Links saved to job26_cv_links.json")
    print(f"\nTotal uploaded: {len(drive_links)}")
    return drive_links

if __name__ == '__main__':
    drive_links = fetch_and_upload_cvs()
    print("\nLinks:")
    for name, link in drive_links.items():
        print(f"  {name}: {link}")
