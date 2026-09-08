# -*- coding: utf-8 -*-
"""
Verify every load-bearing claim in the five outcome letters against the ACTUAL submissions
downloaded from Drive. Nothing here trusts the evaluation record.

Text extraction covers docx (paragraphs AND text boxes), pptx (all shapes incl. tables and
notes), xlsx (cell values AND formulas), pdf (PyMuPDF).
"""
import io
import os
import re
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build as gbuild
from googleapiclient.http import MediaIoBaseDownload

OUT = r"C:\Users\Dell\AppData\Local\Temp\claude\c--Agent-Coco\fba5d52e-65f2-44a6-a576-5c1cb54b4837\scratchpad\subs"
os.makedirs(OUT, exist_ok=True)
TOK = r"c:\Agent Coco\.claude\config\token_sheets_broad.json"

creds = Credentials.from_authorized_user_file(TOK)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
    open(TOK, "w").write(creds.to_json())
drive = gbuild("drive", "v3", credentials=creds)

FOLDERS = {
    "Kanooz": "1AQy-QpAQDnkXuu7nPlGlcvY2BHNmSAaL",
    "Irfan": "10CM1Mvz7YgO8hS0dOOU4sx0LWhr69Y4B",
    "Wajdan": "1fKGJ3LtOXPy5N4EVXShdnDbdiQp3LyBA",
    "Basit": "1ENRRftnC4SLDykVG3nSeE2pacNUGEQMi",
    "Rimsha": "1cplnC8M84DO9Zia11tum6gdT3KXBje57",
}


def dl(fid, name):
    path = os.path.join(OUT, re.sub(r"[^\w.\- ]", "_", name))
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    req = drive.files().get_media(fileId=fid)
    buf = io.BytesIO()
    d = MediaIoBaseDownload(buf, req)
    done = False
    while not done:
        _, done = d.next_chunk()
    with open(path, "wb") as f:
        f.write(buf.getvalue())
    return path


def text_docx(p):
    from docx import Document
    from docx.oxml.ns import qn
    doc = Document(p)
    parts = [t.text for t in doc.element.body.iter(qn("w:t")) if t.text]
    for tb in doc.tables:
        for row in tb.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def text_pptx(p):
    from pptx import Presentation
    prs = Presentation(p)
    parts = []
    for i, slide in enumerate(prs.slides, 1):
        parts.append(f"[[SLIDE {i}]]")
        for sh in slide.shapes:
            if sh.has_text_frame:
                parts.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    parts.append(" | ".join(c.text for c in row.cells))
        try:
            if slide.has_notes_slide:
                parts.append("[notes] " + slide.notes_slide.notes_text_frame.text)
        except Exception:
            pass
    return "\n".join(parts)


def text_xlsx(p):
    import openpyxl
    parts = []
    for data_only in (True, False):          # values, then formulas
        try:
            wb = openpyxl.load_workbook(p, data_only=data_only, read_only=False)
        except Exception as e:
            parts.append(f"[xlsx open failed data_only={data_only}: {e}]")
            continue
        for ws in wb.worksheets:
            parts.append(f"[[SHEET {ws.title} data_only={data_only} "
                         f"dims={ws.max_row}x{ws.max_column}]]")
            for row in ws.iter_rows():
                vals = [str(c.value) for c in row if c.value is not None]
                if vals:
                    parts.append(" | ".join(vals))
        wb.close()
    return "\n".join(parts)


def text_pdf(p):
    import fitz
    doc = fitz.open(p)
    return "\n".join(pg.get_text() for pg in doc)


def extract(p):
    e = p.lower()
    try:
        if e.endswith(".docx"):
            return text_docx(p)
        if e.endswith(".pptx"):
            return text_pptx(p)
        if e.endswith(".xlsx"):
            return text_xlsx(p)
        if e.endswith(".pdf"):
            return text_pdf(p)
        if e.endswith(".txt"):
            return open(p, encoding="utf-8", errors="replace").read()
    except Exception as ex:
        return f"[EXTRACT FAILED {type(ex).__name__}: {ex}]"
    return ""


corpus = {}
for nm, fid in FOLDERS.items():
    res = drive.files().list(q=f"'{fid}' in parents and trashed=false",
                             fields="files(id,name,mimeType)",
                             supportsAllDrives=True, includeItemsFromAllDrives=True,
                             pageSize=100).execute()
    blobs = []
    for f in res.get("files", []):
        if f["mimeType"] == "application/vnd.google-apps.folder":
            continue
        try:
            p = dl(f["id"], f"{nm}__{f['name']}")
            t = extract(p)
            blobs.append(f"\n===== FILE: {f['name']} =====\n{t}")
            print(f"  {nm}: {f['name']} -> {len(t)} chars", flush=True)
        except Exception as ex:
            print(f"  {nm}: {f['name']} -> DOWNLOAD/EXTRACT ERROR {type(ex).__name__}: "
                  f"{str(ex)[:130]}", flush=True)
    corpus[nm] = "\n".join(blobs)

for nm, t in corpus.items():
    open(os.path.join(OUT, f"CORPUS_{nm}.txt"), "w", encoding="utf-8").write(t)
print("\ncorpus sizes:", {k: len(v) for k, v in corpus.items()})
