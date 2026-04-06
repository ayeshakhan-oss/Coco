"""
Job 36 — Send rejection emails LIVE to candidates.
Processes 151 personalised drafts. Skips:
  - 10 flagged (no CV / unreadable) from generation log
  - LinkedIn .temp placeholder emails
  - Duplicate emails (first occurrence wins)
  - Faryal Afridi (1442) and Muhammad Omer Khan (1789) — already received
    values interview feedback today; CV rejection would be wrong
Applies: we-voice, no em dashes, no markdown bold, confirmed HTML design.
CC: hiring@taleemabad.com + ayesha.khan@taleemabad.com on every send.
"""

import os, re, json, smtplib, time, base64, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../..", ".env"))

SENDER    = "ayesha.khan@taleemabad.com"
PASSWORD  = os.getenv("EMAIL_PASSWORD")
CC_LIST   = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
SUBJECT   = "Your Application for Field Coordinator, Research & Impact Studies"
ROLE_HTML = "Field Coordinator, Research &amp; Impact Studies"
DRAFTS_DIR = "c:/Agent Coco/output/rejection_emails_job36/"
LOG_PATH   = os.path.join(DRAFTS_DIR, "_generation_log.json")
LOGO_PATH  = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")
SEND_LOG   = "c:/Agent Coco/output/job36_rejection_send_log.json"

# App IDs already emailed via a different (values feedback) script — exclude
ALREADY_EMAILED = {1442, 1789}

# DB email lookup — app_id → email (from Markaz, fetched 2026-03-25)
# Only real (non-.temp) emails are stored here
DB_EMAILS = {
    1401: "misbah.zafar@isb.nu.edu.pk",
    1403: "mkreply2005@gmail.com",
    1405: "qaziishfaqkhan45@gmail.com",
    1408: "laibaahmed938@gmail.com",
    1413: "saeedahmed4288@gmail.com",
    1415: "kaynatsyeda4@gmail.com",
    1422: "aqsagul3122@gmail.com",
    1426: "iqraparvez0105@gmail.com",
    1430: "noorscheherazade@gmail.com",
    1447: "Aleenafm1@gmail.com",
    1448: "tehreemaly90@gmail.com",
    1450: "naveenshariff73@gmail.com",
    1451: "usmanahmaddenin@gmail.com",
    1453: "abidqaisrani5@gmail.com",
    1454: "shahid.kaamal@gmail.com",
    1455: "atifrahim105@gmail.com",
    1465: "saadburney10@gmail.com",
    1477: "sadich61@gmail.com",
    1482: "kashiafridi87@gmail.com",
    1484: "raoasfandraheel@gmail.com",
    1485: "naeemmuhammad689@gmail.com",
    1489: "qasee.khundian@gmail.com",
    1491: "raza2001040616@gmail.com",
    1494: "m.awaishakim99@gmail.com",
    1495: "shabbir.dani@gmail.com",
    1496: "maimoona.malik83@gmail.com",
    1499: "muzurazee121@gmail.com",
    1501: "asifhayat21@gmail.com",
    1503: "nimrabaqir43@gmail.com",
    1507: "azraparveen0012@gmail.com",
    1508: "yasmeennisar27@gmail.com",
    1513: "alizia.hyder@outlook.com",
    1518: "zubair.hafiz8@gmail.com",
    1519: "imamatahir5@gmail.com",
    1521: "amjadfatima190@gmail.com",
    1527: "perniya_akram@hotmail.com",
    1528: "m.afzal36@yahoo.com",
    1533: "muqqadas2001@gmail.com",
    1536: "neno.farman@gmail.com",
    1538: "ambroali161@gmail.com",
    1540: "muhammadakmala287@gmail.com",
    1545: "pariyalfazal@gmail.com",
    1546: "pariyalfazal@gmail.com",
    1547: "aniladad786@gmail.com",
    1549: "alyhnz1140@gmail.com",
    1553: "shaheenshagufta73@yahoo.com",
    1556: "sanamehboob42@gmail.com",
    1561: "zhrehman603@gmail.com",
    1564: "mahroosha.sal@gmail.com",
    1570: "sartaj.daulat@gmail.com",
    1577: "balouchzohra@gmail.com",
    1579: "rida.zanib97@gmail.com",
    1583: "aliyafarooq321@gmail.com",
    1584: "Faiza.ghazal098@gmail.com",
    1585: "sultanaquresh94@gmail.com",
    1588: "hooria.khan773@gmail.com",
    1591: "junaidjadee912@gmail.com",
    1593: "zainabsajjad122@gmail.com",
    1594: "mamoona.safeer1997@gmail.com",
    1597: "saba.shahwani999@gmail.com",
    1600: "adiljaved371@gmail.com",
    1601: "periakharal@gmail.com",
    1602: "Asifmkhan771@gmail.com",
    1603: "sehrishumairgill@gmail.com",
    1604: "amanullahnaich3@gmail.com",
    1607: "fatimatuzaharaawais@gmail.com",
    1608: "afaqa4851@gmail.com",
    1611: "muhammadahmedkhan774@gmail.com",
    1614: "sumbalkhan6699@gmail.com",
    1617: "inayatsona4@gmail.com",
    1618: "salman.ahmedd.work@gmail.com",
    1624: "siddiquemuhammad100@gmail.com",
    1625: "naima.memoon55@gmail.com",
    1626: "mr.hassnain423@gmail.com",
    1630: "okashachangwani@gmail.com",
    1633: "midhatfatima22@gmail.com",
    1636: "daud.anissa@yahoo.com",
    1639: "wajiha.rehberali@gmail.com",
    1643: "mutiurrehman004@gmail.com",
    1644: "ahaleem7222@gmail.com",
    1647: "hareemmoinkhattak1@gmail.com",
    1648: "hasaanbhutta78@icloud.com",
    1653: "mahnoor.iqbal0009@gmail.com",
    1657: "zainhashmi183@gmail.com",
    1658: "fatima.razzaq92@gmail.com",
    1659: "zaynabhashmi740@gmail.com",
    1660: "zaynabhashmi740@gmail.com",
    1662: "ghanzala0@gmail.com",
    1664: "javeriazahra215@gmail.com",
    1669: "zarghuna.rahman06@gmail.com",
    1674: "aminajabin229@gmail.com",
    1677: "abdulsubhangormani@gmail.com",
    1678: "mssairaakram@gmail.com",
    1683: "afiraannis6@gmail.com",
    1687: "dr.muhammad.hakim@gmail.com",
    1688: "dr.muhammad.hakim@gmail.com",
    1690: "rmukhtar450@gmail.com",
    1694: "varishakhaan97@gmail.com",
    1698: "uzair.ahmad5519@gmail.com",
    1700: "masad.malik59@gmail.com",
    1704: "imtessals@gmail.com",
    1706: "basitalee77@gmail.com",
    1708: "hafsanijat08@gmail.com",
    1709: "saandqurban@gmail.com",
    1711: "rafeeqaakram@gmail.com",
    1714: "amankhan9618@gmail.com",
    1720: "jawadmarwat47@gmail.com",
    1721: "maryamrf832@gmail.com",
    1723: "fatima.shah444@gmail.com",
    1726: "amara.naqui4@gmail.com",
    1731: "abbasisanatariq@gmail.com",
    1738: "amirmehmoodm9@gmail.com",
    1740: "m.zulqarnain910@gmail.com",
    1750: "usmanshabbirchouhan@gmail.com",
    1755: "usmanumar646@gmail.com",
    1760: "talhaiftykhar458@gmail.com",
    1764: "muhammadmustafakhan549@gmail.com",
    1766: "fizza_faizan@yahoo.com",
    1767: "sidraishfaq@gmail.com",
    1775: "Barcha151214@gmail.com",
    1779: "shahzadakber66@gmail.com",
    1781: "complicatedtarar786@gmail.com",
    1783: "sohailkhattak1010@gmail.com",
    1786: "shaistaowais3@gmail.com",
    1788: "aliizaffaar@gmail.com",
    1791: "mwaleed@math.qau.edu.pk",
    1794: "kakarmalayeka@gmail.com",
    1795: "call2hamid@gmail.com",
    1797: "merabiatariq@gmail.com",
    1802: "farzanaali77@hotmail.com",
    1805: "Muhammad.ali.rajpoot12@gmail.com",
    1808: "aly_mehwish@yahoo.com",
    1812: "hafizaswairashahbaz@gmail.com",
    1817: "zaybeequreshi@gmail.com",
    1819: "rijazahid7@gmail.com",
    1825: "cyedhuxayn@gmail.com",
    1826: "ssc.eisha.191094@gmail.com",
    1827: "saifa8841@gmail.com",
    1833: "mkhaliluafbrw@gmail.com",
    1837: "hunzausman66@gmail.com",
    1839: "habibbest@gmail.com",
    1853: "usmankonosuba@gmail.com",
    1856: "sairashakoor3@gmail.com",
    1857: "aminabatool2000@gmail.com",
    1858: "jawerialateef87@gmail.com",
    1861: "hafsaqadri875@gmail.com",
    1864: "fatima_knz@yahoo.com",
    1869: "ayesharazakhan406@gmail.com",
    1871: "arifsadiq03@gmail.com",
    1879: "mzainmob@gmail.com",
    1887: "khanzadahayat7@gmail.com",
    1893: "tajhusssain.qau@gmail.com",
    1895: "farooqsociologist611@gmail.com",
    1896: "farooqsociologist611@gmail.com",
    1903: "muhammad.abubakr@niete.edu.pk",
    1905: "saadiaasad123@gmail.com",
    1906: "saadiaasad123@gmail.com",
    1907: "ssikandarmalik95@gmail.com",
    1915: "amirafatima5566@gmail.com",
    1916: "ansaarmaseed125@gmail.com",
    1917: "nasirshigri001@gmail.com",
    1921: "rosheen.naeem@gmail.com",
    1923: "maryammurtaza389@gmail.com",
    1924: "mubarahchaudhary271998@gmail.com",
    1926: "sobiam424@gmail.com",
    1927: "syedwajihbukhari@gmail.com",
    1930: "Javidjamal1970@gmail.com",
    1932: "tahseenun1988@gmail.com",
    1935: "sabamanzoor909@gmail.com",
    1936: "najamnisar@hotmail.com",
    1942: "fatima.razzaq92@gmail.com",
    1946: "mariamrehman681@gmail.com",
    1948: "daniyahnoor@gmail.com",
    1950: "jalalsaraikhan@gmail.com",
    1952: "aliyabukhari123@gmail.com",
    1955: "adnanaliaup2018@gmail.com",
    1956: "amna12arshad@gmail.com",
}


# ── Text fix helpers ──────────────────────────────────────────────────────────

def fix_i_to_we(text):
    text = re.sub(r"\bI've\b",  "we've",  text)
    text = re.sub(r"\bI'd\b",   "we'd",   text)
    text = re.sub(r"\bI'll\b",  "we'll",  text)
    text = re.sub(r"\bI'm\b",   "we're",  text)
    text = re.sub(r"\bI can\b", "we can", text)
    text = re.sub(r"\bI do\b",  "we do",  text)
    text = re.sub(r"(?m)^I\b",         "We",  text)
    text = re.sub(r"(?<=[.!?] )I\b",   "We",  text)
    text = re.sub(r"\bI\b",            "we",  text)
    return text

def fix_em_dashes(text):
    text = text.replace(" — ", ", ")
    text = text.replace("—", ",")
    return text

def escape_html(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline_bold(text):
    """Convert **bold** to <strong>bold</strong>, escaping surrounding text."""
    parts = re.split(r'\*\*(.+?)\*\*', text)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            out.append(escape_html(part))
        else:
            out.append(f"<strong>{escape_html(part)}</strong>")
    return "".join(out)

def text_to_html(body_text):
    """Convert plain text body to HTML using confirmed design helpers."""
    P      = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;">{t}</p>'
    H2     = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
    SUB    = lambda t: f'<p style="color:#1b5e20;font-weight:bold;margin:0 0 14px 0;font-size:14px;">{t}</p>'

    blocks = re.split(r'\n{2,}', body_text.strip())
    html_parts = []

    for block in blocks:
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue

        # Detect standalone bold heading: only **...** on its own line
        if len(lines) == 1 and re.match(r'^\*\*[^*]+\*\*:?\s*$', lines[0]):
            heading = re.sub(r'\*\*(.+?)\*\*:?', r'\1', lines[0]).rstrip(':').strip()
            html_parts.append(SUB(escape_html(heading)))
            continue

        # Detect bullet list block
        if all(l.startswith('- ') or l.startswith('• ') for l in lines):
            items = []
            for l in lines:
                item_text = l[2:].strip()
                items.append(f'<li style="margin-bottom:6px;">{inline_bold(item_text)}</li>')
            html_parts.append(
                f'<ul style="margin:0 0 18px 0;padding-left:22px;line-height:1.8;">'
                + "".join(items) + "</ul>"
            )
            continue

        # Mixed block — join lines into one paragraph, handle inline bold
        combined = " ".join(lines)
        html_parts.append(P(inline_bold(combined)))

    return "\n".join(html_parts)


def strip_pilot_header(content):
    lines = content.splitlines()
    clean = []
    skip_next_blank = False
    for line in lines:
        if (line.startswith("*** PILOT") or line.startswith("[CATEGORY")
                or line.startswith("=" * 10)):
            skip_next_blank = True
            continue
        if skip_next_blank and line.strip() == "":
            skip_next_blank = False
            continue
        skip_next_blank = False
        clean.append(line)
    return "\n".join(clean).strip()


def parse_email_file(raw):
    """Returns (subject, body_without_signoff)."""
    content = strip_pilot_header(raw)
    lines = content.splitlines()
    subject = SUBJECT
    body_start = 0
    for i, line in enumerate(lines):
        if line.lower().startswith("subject:"):
            # We override subject with our confirmed format anyway
            body_start = i + 1
            while body_start < len(lines) and not lines[body_start].strip():
                body_start += 1
            break

    body = "\n".join(lines[body_start:]).strip()

    # Apply text fixes
    body = fix_i_to_we(body)
    body = fix_em_dashes(body)

    # Remove sign-off block (from "Warm regards" onwards)
    idx = body.rfind("Warm regards")
    if idx != -1:
        body = body[:idx].rstrip()

    return body


# ── HTML template (confirmed design) ─────────────────────────────────────────

def header_block():
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;
              border-bottom:2px solid #1565c0;">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; Application Update
      </p>
      <p style="margin:0 8px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:#1565c0;line-height:1.4;">
        {ROLE_HTML}
      </p>
    </td>
  </tr>
</table>"""


FOOTER_HTML = """
<table width="100%" cellpadding="0" cellspacing="0"
       style="margin-top:40px;border-top:1px solid #e0e0e0;padding-top:20px;">
  <tr>
    <td style="font-family:Georgia,serif;font-size:13px;color:#555;line-height:1.9;">
      Warm regards,<br>
      <strong style="color:#1a1a1a;">People and Culture Team</strong><br>
      <strong style="color:#1565c0;">Taleemabad</strong><br>
      <a href="mailto:hiring@taleemabad.com"
         style="color:#1565c0;text-decoration:none;">hiring@taleemabad.com</a>
      &nbsp;|&nbsp;
      <a href="http://www.taleemabad.com"
         style="color:#1565c0;text-decoration:none;">www.taleemabad.com</a><br>
      <span style="font-size:12px;color:#aaa;margin-top:4px;display:block;">
        Sent on behalf of Talent Acquisition Team by Coco
      </span>
    </td>
  </tr>
</table>"""


def build_html(body_text_html):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background-color:#f0f4f0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#f0f4f0;padding:32px 0;">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="max-width:620px;border-radius:8px;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
        <tr><td>{header_block()}</td></tr>
        <tr>
          <td style="background:#ffffff;padding:40px 52px 48px 52px;
                     border-radius:0 0 8px 8px;
                     font-family:Georgia,serif;font-size:15px;
                     line-height:1.8;color:#1a1a1a;">
            {body_text_html}
            {FOOTER_HTML}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


# ── Send ──────────────────────────────────────────────────────────────────────

def send_email(server, to_email, html):
    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Cc"]      = ", ".join(CC_LIST)
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(html, "html"))

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)

    all_recipients = [to_email] + CC_LIST
    allow_candidate_addresses([to_email])
    safe_sendmail(server, SENDER, all_recipients, msg.as_string(),
                  context=f"job36_rejection_{to_email}")


def main():
    log = json.load(open(LOG_PATH, encoding="utf-8"))
    flagged_ids = {f["app_id"] for f in log.get("generic_flag", [])}

    txt_files = sorted(f for f in os.listdir(DRAFTS_DIR) if f.endswith(".txt"))

    # Track sent emails to deduplicate
    sent_emails = set()
    results = {"sent": [], "skipped": [], "failed": []}

    to_send = []
    for fname in txt_files:
        m = re.match(r"(\d+)_(.+)\.txt", fname)
        if not m:
            continue
        app_id = int(m.group(1))
        name   = m.group(2).replace("_", " ")

        # Skip flagged (no CV)
        if app_id in flagged_ids:
            results["skipped"].append({"app_id": app_id, "name": name, "reason": "flagged-no-cv"})
            continue

        # Skip already-emailed via values feedback
        if app_id in ALREADY_EMAILED:
            results["skipped"].append({"app_id": app_id, "name": name, "reason": "already-received-values-feedback-email"})
            continue

        # Look up email
        email = DB_EMAILS.get(app_id)
        if not email or ".temp" in email:
            results["skipped"].append({"app_id": app_id, "name": name, "reason": "no-real-email"})
            continue

        email_lower = email.lower()

        # Deduplicate
        if email_lower in sent_emails:
            results["skipped"].append({"app_id": app_id, "name": name,
                                        "reason": f"duplicate-email:{email}"})
            continue

        to_send.append((app_id, name, email, fname))
        sent_emails.add(email_lower)

    print(f"Ready to send: {len(to_send)} emails")
    print(f"Skipping:      {len(results['skipped'])} (flagged, temp, duplicate, already-emailed)")
    print()

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, PASSWORD)

        for i, (app_id, name, email, fname) in enumerate(to_send, 1):
            fpath = os.path.join(DRAFTS_DIR, fname)
            raw   = open(fpath, encoding="utf-8").read()

            try:
                body_text = parse_email_file(raw)
                body_html = text_to_html(body_text)
                body_html += feedback_widget(name, ROLE_HTML, app_id, 'Application Feedback')
                html      = build_html(body_html)
                send_email(server, email, html)
                results["sent"].append({"app_id": app_id, "name": name, "email": email})
                print(f"  [{i}/{len(to_send)}] OK   {name} -> {email}")
            except Exception as e:
                results["failed"].append({"app_id": app_id, "name": name,
                                           "email": email, "error": str(e)})
                print(f"  [{i}/{len(to_send)}] FAIL {name} -> {email}: {e}")

            time.sleep(0.8)   # avoid SMTP rate limits

    # Save send log
    with open(SEND_LOG, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print(f"Done.")
    print(f"  Sent:    {len(results['sent'])}")
    print(f"  Skipped: {len(results['skipped'])}")
    print(f"  Failed:  {len(results['failed'])}")
    print(f"  Log:     {SEND_LOG}")

    if results["failed"]:
        print("\nFailed:")
        for f in results["failed"]:
            print(f"  App {f['app_id']} {f['name']} — {f['error']}")


if __name__ == "__main__":
    main()
