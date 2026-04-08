"""
Job 35 — Junior Research Associate, Impact & Policy
CV-Stage Rejection Emails — PILOT (2 candidates)

Candidates: Zainab Azhar (1537), Midhat Fatima (1634)
PILOT_MODE = True → sends to Ayesha only
Set PILOT_MODE = False → sends live with CC
"""

import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from scripts.utils.safe_send import safe_sendmail, allow_candidate_addresses
from scripts.utils.feedback_widget import feedback_widget

PILOT_MODE = True
SENDER     = "ayesha.khan@taleemabad.com"
PASSWORD   = os.getenv("EMAIL_PASSWORD")
PILOT_TO   = "ayesha.khan@taleemabad.com"
CC_LIVE    = ["hiring@taleemabad.com", "ayesha.khan@taleemabad.com"]
ROLE       = "Junior Research Associate, Impact & Policy"
LOGO_PATH  = os.path.join(os.path.dirname(__file__), "../../..", "assets", "logo_taleemabad.png")

# ── HTML HELPERS (v8 design) ──────────────────────────────────────────────────

H   = lambda t: f'<h2 style="color:#1565c0;font-size:17px;font-weight:bold;margin:36px 0 6px 0;letter-spacing:0.3px;">{t}</h2>'
P   = lambda t: f'<p style="margin:0 0 18px 0;text-align:justify;">{t}</p>'
PS  = lambda t: f'<p style="margin:32px 0 0 0;padding:20px 24px;background:#f1f8e9;border-left:4px solid #1b5e20;font-style:italic;color:#2a2a2a;font-size:14px;line-height:1.7;">{t}</p>'

FOOTER = """
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

def header_block():
    return f"""
<table width="100%" cellpadding="0" cellspacing="0"
       style="border-radius:8px 8px 0 0;overflow:hidden;border-bottom:2px solid #1565c0;">
  <tr>
    <td align="center" bgcolor="#ffffff"
        style="background-color:#ffffff;padding:28px 40px 22px 40px;">
      <img src="cid:taleemabad_logo" height="38" alt="Taleemabad"
           style="display:block;margin:0 auto 14px auto;">
      <p style="margin:0;font-family:Georgia,serif;font-size:11px;
                color:#1565c0;letter-spacing:2px;text-transform:uppercase;">
        People &amp; Culture &nbsp;&bull;&nbsp; Application Update
      </p>
      <p style="margin:10px 0 4px 0;font-family:Georgia,serif;font-size:17px;
                font-weight:bold;color:#1565c0;line-height:1.4;">
        Your Application for Junior Research Associate
      </p>
      <p style="margin:0;font-family:Georgia,serif;font-size:12px;color:#5c85c7;">
        {ROLE}
      </p>
    </td>
  </tr>
</table>"""

def wrap(body_html):
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
            {body_html}
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


# ── EMAIL 1: ZAINAB AZHAR ─────────────────────────────────────────────────────
# CV: COMSATS Psychology thesis (interparental conflict, attachment styles, emotional dysregulation)
# Experience: DE Risc Group (communications, CRM, client outreach) — no research/M&E background
# Tier: No-Hire — tools present (SPSS) but no research methods, no RA work

ZAINAB_SUBJECT = "Your Application for Junior Research Associate, Impact & Policy"

ZAINAB_BODY = (
    P("Dear Zainab,") +
    P("Thank you for taking the time to apply for the Junior Research Associate role at Taleemabad. We have reviewed your application carefully and want to let you know that we will not be moving forward with your candidacy at this stage. We appreciate your interest in the work we do, and we want to be honest with you about what we found rather than offering a generic reply.") +

    H("What We Noticed in Your Application") +
    P("Your thesis on the role of interparental conflict and attachment styles on emotional dysregulation in young adults showed genuine engagement with research design. A literature review, survey-based data collection, and statistical analysis on a nuanced psychological question is not a light undertaking, and the fact that you saw it through is worth acknowledging. The methodological instinct was there, even if the domain is different from where this role sits.") +
    P("The communications and outreach work at DE Risc Group also showed real range: CRM management using HubSpot and LeadSquared, client correspondence across email and virtual meetings, business proposal writing, NDA and contract coordination, social media strategy, and targeted email campaigns across multiple functions. That breadth of exposure in an early role is not common, and it tells us you can move between tasks and hold multiple responsibilities at once without losing your footing. Managing end-to-end client communication while simultaneously running outreach campaigns and maintaining internal documentation requires a kind of operational steadiness that is genuinely useful, just not in the direction this particular role is pointing.") +

    H("Where the Fit Did Not Quite Come Together") +
    P("The Junior Research Associate role sits firmly in the impact and policy research space: education data, school-level field monitoring, quantitative analysis of programme outcomes, and evidence-based reporting for decision-makers within Pakistan's public education system. What we were looking for, and did not yet see in your profile, was direct experience in that space: research assistant work in an education or development organisation, field data collection on learning outcomes or school quality, applied methods work such as regression analysis, difference-in-differences, or survey design for impact evaluation, or any substantive engagement with education policy questions.") +
    P("Your research experience to date has been grounded in psychology, and your professional experience has been in client communications and business development. Both are legitimate and coherent paths. Neither, at this point, maps closely enough to the research methods and domain knowledge this role requires from day one. We did not see enough demonstrated experience in impact research or educational data work to move you forward in this particular pool, and we would rather be honest about that than leave you guessing.") +
    P("This is not a comment on your capability or your potential. The research instinct that produced your thesis is real, and the operational fluency you have built at DE Risc Group is genuinely useful. The gap is about domain fit and methods specificity, not about the quality of what you have built so far.") +

    H("What We Think Could Serve You Well") +
    P("If impact and policy research is a direction you want to move toward, the most direct path is to build the methods foundation deliberately. A course in econometrics or impact evaluation, even a self-directed one through J-PAL's free online offerings, would give you the vocabulary and technical grounding that this kind of role expects. Hands-on RA work with a research organisation, or a project that puts you in the field collecting and cleaning data in an education or development context, would build the applied experience that makes a profile like yours much harder to pass over in a pool like this one.") +
    P("Organisations like CERP, J-PAL South Asia, the Institute of Development and Economic Alternatives (IDEAS), or development-focused NGOs working in education often take on research interns who are early in this transition. Starting there, even on a part-time or voluntary basis, would close the domain gap meaningfully and give you a body of work that speaks directly to what roles like this require.") +
    P("Your communication skills and your ability to manage multiple workstreams simultaneously are real assets. In a research environment, those qualities matter a great deal, particularly when it comes to coordinating field teams, writing up findings for non-specialist audiences, and keeping complex projects on schedule. The gap to close is on the technical and domain side, and it is closable with the right next move.") +
    P("We would encourage you to keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>. Roles that sit closer to communications, coordination, or programme support may be a stronger fit at this stage, and we would welcome your application when the match is tighter.") +

    PS("<strong>P.S.</strong> The thesis topic, how parental conflict shapes emotional regulation in young adults, is a more consequential question than it might appear in a CV summary. The fact that you chose to investigate it suggests a genuine curiosity about human behaviour and its roots. That is not nothing. Bring that same curiosity to whatever domain you build in next.") +

    FOOTER +
    feedback_widget("Zainab Azhar", ROLE, 1537, "Application Feedback")
)

ZAINAB_HTML = wrap(ZAINAB_BODY)


# ── EMAIL 2: MIDHAT FATIMA ────────────────────────────────────────────────────
# CV: MSPH (3.78 CGPA), public health background, EMPHNET internship (Jordan HQ),
# PPHI/Benazir Nashonuma SBC work, De Risc Group research assistant (2026)
# Tier: Tier C — some methods but wrong domain (public health, not education/policy)

MIDHAT_SUBJECT = "Your Application for Junior Research Associate, Impact & Policy"

MIDHAT_BODY = (
    P("Dear Midhat,") +
    P("Thank you for applying for the Junior Research Associate role at Taleemabad. We have reviewed your application carefully and want to let you know that we will not be moving forward at this stage. We want to be honest with you about our reasoning rather than offering a standard reply.") +

    H("What We Noticed in Your Application") +
    P("Your public health training is substantive. An MSPH with a 3.78 CGPA from Health Services Academy, a BSPH from PUMHS, and research experience spanning both qualitative and quantitative methods, including an in-depth interview study on paternal postpartum depression and a cross-sectional study on anaemia in pregnant women, tells us you know how to design and carry a study from question to conclusion. That is a meaningful foundation.") +
    P("The EMPHNET internship at the Jordan headquarters, working within the Disease Control and Prevention team, contributing to the MenMap Annual Report, and attending monthly technical and biweekly progress meetings, showed you can operate in a structured international research environment, navigate institutional hierarchies, and contribute to real outputs under supervision. That is a meaningful credential at this stage, and it is not one many candidates in Pakistan can point to.") +
    P("The PPHI work under the Benazir Nashonuma project, conducting health awareness sessions on maternal and infant nutrition at the community level across villages, also demonstrated sustained field presence and the ability to engage directly with beneficiaries across different geographic and social settings. Running MIYCAN sessions, cooking demonstrations, and breastfeeding awareness in the field requires adaptability and a tolerance for the messiness of community work. Those are qualities that transfer across sectors.") +
    P("Your most recent role as a Research and Investigation Assistant at De Risc Group added primary and secondary data collection, investigation report compilation, and data subject rights handling to your profile. Taken together, you have built a genuinely varied research portfolio at an early career stage, and the consistency of your academic performance across both degrees, 3.32 and 3.78, tells us the quality of your work has been steady throughout.") +

    H("Where the Fit Did Not Quite Come Together") +
    P("The Junior Research Associate role at Taleemabad sits in the education impact and policy space: learning outcomes data, school monitoring, education programme evaluation, and evidence generation for decision-makers in the public education system. The research methods we were looking for, applied econometrics, difference-in-differences, RCT design, or quantitative analysis of education data, and the domain experience we needed, school-level fieldwork, education sector familiarity, or policy research in an education context, were not yet visible in your profile.") +
    P("Your research experience is strong, but it is anchored firmly in public health: disease surveillance, maternal nutrition, community health behaviour change. The overlap with education research at the methods level exists, but the domain gap is material. In a role that requires someone to hit the ground running on education data and school-level monitoring from day one, we could not yet see enough alignment to move you forward in this particular pool.") +
    P("We want to be clear that this is not a comment on the quality of your work. It is an honest read of where your profile currently sits relative to what this specific role requires right now.") +

    H("What We Think Could Serve You Well") +
    P("If education policy or impact research is a direction you want to move toward, your methods foundation gives you a genuine head start. The translation from health research to education research is less of a leap than it might appear: sampling, survey design, field coordination, and quantitative analysis transfer directly. What you would need to add is the domain layer, familiarity with how schools are structured, how education data is collected and reported, and what the key questions in Pakistan's education policy landscape look like right now.") +
    P("Reading the evidence base around programmes like those run by Taleemabad, CERP, or J-PAL South Asia, or seeking out a short project or consultancy that puts you in contact with education data, would close that gap meaningfully. Your communication skills and your ability to work across communities and institutional settings are assets that a research organisation in this space would value. The gap is domain, not capability.") +
    P("We would encourage you to keep an eye on our careers page at <a href='http://www.taleemabad.com' style='color:#1565c0;'>www.taleemabad.com</a>. Should a role emerge that aligns more closely with your public health and community research background, we would genuinely welcome your application.") +

    PS("<strong>P.S.</strong> The combination of a 3.78 MSPH, an international research internship, and community-level fieldwork at your stage is not ordinary. The direction you are building in is clear and it is coherent. Keep going.") +

    FOOTER +
    feedback_widget("Midhat Fatima", ROLE, 1634, "Application Feedback")
)

MIDHAT_HTML = wrap(MIDHAT_BODY)


# ── SEND ──────────────────────────────────────────────────────────────────────

EMAILS = [
    {"name": "Zainab Azhar",  "email": "zainabazhar361@gmail.com", "app_id": 1537,
     "subject": ZAINAB_SUBJECT, "html": ZAINAB_HTML},
    {"name": "Midhat Fatima", "email": "midhatfatima22@gmail.com",  "app_id": 1634,
     "subject": MIDHAT_SUBJECT, "html": MIDHAT_HTML},
]

def send_email(to_email, to_name, subject, html, cc_list=None):
    msg = MIMEMultipart("related")
    msg["From"]    = SENDER
    msg["To"]      = to_email
    msg["Subject"] = subject
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html, "html", "utf-8"))
    msg.attach(alt)

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            img = MIMEImage(f.read())
        img.add_header("Content-ID", "<taleemabad_logo>")
        img.add_header("Content-Disposition", "inline", filename="logo_taleemabad.png")
        msg.attach(img)

    recipients = [to_email] + (cc_list or [])
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(SENDER, PASSWORD)
        allow_candidate_addresses(recipients)
        safe_sendmail(server, SENDER, recipients, msg.as_string(),
                      context=f"job35_cv_rejection_{'pilot' if PILOT_MODE else 'live'}_{to_name.replace(' ','_')}")
    cc_str = f" (CC: {', '.join(cc_list)})" if cc_list else ""
    print(f"  Sent: {to_name} -> {to_email}{cc_str}")


def main():
    print("=" * 60)
    print(f"Job 35 — Junior Research Associate | CV Rejection Pilot")
    print(f"Mode: {'PILOT (Ayesha only)' if PILOT_MODE else 'LIVE'}")
    print("=" * 60)

    for e in EMAILS:
        if PILOT_MODE:
            send_email(PILOT_TO, e["name"],
                       f"[PILOT — {e['name']}] {e['subject']}", e["html"])
        else:
            send_email(e["email"], e["name"], e["subject"], e["html"], cc_list=CC_LIVE)

    print(f"\nDone. {len(EMAILS)} emails {'piloted' if PILOT_MODE else 'sent live'}.")
    print("=" * 60)


if __name__ == "__main__":
    main()
