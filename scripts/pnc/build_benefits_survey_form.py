"""
Build the Benefits Pulse Check Google Form (P&C, 2026-09-03).

Owner: created with token_sheets_broad.json = Ayesha's own OAuth token,
so the form is owned by ayesha.khan@ and lands in her Drive root.

Requires the Google Forms API to be ENABLED on GCP project 954828175525.
The `drive` scope on token_sheets_broad.json is already accepted by the Forms API
(probe returned SERVICE_DISABLED, not a scope error).

Usage:  python scripts/pnc/build_benefits_survey_form.py
"""
import pathlib
import sys

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

TOKEN = pathlib.Path(__file__).resolve().parents[2] / ".claude" / "config" / "token_sheets_broad.json"
API = "https://forms.googleapis.com/v1/forms"

TITLE = "Benefits Pulse Check"
DOC_TITLE = "Benefits Pulse Check - P&C 2026"

DESCRIPTION = (
    "The People & Culture team is reviewing how our benefits are designed, and we want to "
    "start by understanding what actually matters to you.\n\n"
    "This is a research exercise, not an announcement. No change has been proposed, approved "
    "or budgeted. Some questions below describe hypothetical approaches purely so we can "
    "understand your preferences. Your answers do not create an entitlement, and a question "
    "being asked does not mean that benefit is being introduced.\n\n"
    "A few questions ask about having more choice in how benefits are allocated. To make that "
    "concrete, here is a hypothetical example only: suppose a pool of PKR 200,000 per year was "
    "set aside for each individual, and instead of fixed budgets per benefit you could draw "
    "from that pool through a wallet or a similar mechanism, spending it on the benefits that "
    "mattered most to you. The amount and the mechanism in this example are purely "
    "illustrative. Nothing has been fixed, costed or approved.\n\n"
    "Responses are reviewed in aggregate. This takes about 5 minutes."
)


# ---------------------------------------------------------------- item helpers


def _choice(kind, title, options, description, required, other):
    opts = [{"value": o} for o in options]
    if other:
        opts.append({"isOther": True})
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "choiceQuestion": {"type": kind, "options": opts, "shuffle": False},
            }
        },
    }
    if description:
        item["description"] = description
    return item


def radio(title, options, description=None, required=True, other=False):
    return _choice("RADIO", title, options, description, required, other)


def checkbox(title, options, description=None, required=True, other=False):
    return _choice("CHECKBOX", title, options, description, required, other)


def scale(title, low_label, high_label, description=None, required=True):
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "scaleQuestion": {
                    "low": 1,
                    "high": 5,
                    "lowLabel": low_label,
                    "highLabel": high_label,
                },
            }
        },
    }
    if description:
        item["description"] = description
    return item


def paragraph(title, description=None, required=False):
    item = {
        "title": title,
        "questionItem": {
            "question": {"required": required, "textQuestion": {"paragraph": True}}
        },
    }
    if description:
        item["description"] = description
    return item


# ---------------------------------------------------------------- questions

ITEMS = [
    # Q1
    scale(
        "Overall, how well do our current benefits meet your needs?",
        "Not very well",
        "Extremely well",
    ),
    # Q2
    checkbox(
        "Which benefits are most valuable to you personally?",
        [
            "IPD / hospitalization",
            "Maternity coverage",
            "Parents' healthcare",
            "OPD (doctor visits, medicines, diagnostics, etc.)",
            "Physiotherapy",
            "Dental",
            "Cosmetics",
            "Mental wellbeing / personal development",
            "Professional development (courses, certifications, etc.)",
            "Travel / commute support",
            "Team lunches / workplace experiences",
        ],
        description="Please select up to 3.",
        other=True,
    ),
    # Q3
    checkbox(
        "Which benefits available to you do you currently use the least or not at all?",
        [
            "IPD / hospitalization",
            "Maternity coverage",
            "Parents' healthcare",
            "Mental wellbeing / personal development",
            "Professional development",
            "Travel / commute support",
            "Team lunches / workplace experiences",
            "I use most of the benefits available to me",
        ],
        other=True,
    ),
    # Q4
    radio(
        "Approximately how much have you spent on OPD for yourself and/or your immediate "
        "family so far this year?",
        [
            "PKR 0",
            "Less than PKR 10,000",
            "PKR 10,000 to 25,000",
            "PKR 25,001 to 50,000",
            "PKR 50,001 to 100,000",
            "More than PKR 100,000",
            "Prefer not to say",
        ],
    ),
    # Q5
    checkbox(
        "What types of OPD expenses do you most commonly incur?",
        [
            "Doctor consultations",
            "Medicines",
            "Diagnostic / lab tests",
            "Specialist consultations",
            "Dental care",
            "Vision / eye care",
            "Physiotherapy",
            "I generally do not have OPD expenses",
        ],
        other=True,
    ),
    # Q6
    radio(
        "Approximately how much have you personally spent on mental wellbeing or personal "
        "development so far this year, whether reimbursed or paid out of pocket?",
        [
            "PKR 0",
            "Less than PKR 10,000",
            "PKR 10,000 to 20,000",
            "PKR 20,001 to 30,000",
            "More than PKR 30,000",
            "Prefer not to say",
        ],
    ),
    # Q7
    radio(
        "Approximately how much have you personally spent on professional learning this year, "
        "including courses, certifications, workshops, or similar learning opportunities?",
        [
            "PKR 0",
            "Less than PKR 10,000",
            "PKR 10,000 to 25,000",
            "PKR 25,001 to 40,000",
            "PKR 40,001 to 75,000",
            "More than PKR 75,000",
            "Prefer not to say",
        ],
    ),
    # Q8
    scale(
        "If you had more choice in how some of your benefits were allocated, how appealing "
        "would that be to you?",
        "I would prefer the current or fixed approach",
        "I would strongly prefer more choice",
    ),
    # Q9
    checkbox(
        "If you could choose where additional benefits support went, which areas would you "
        "prioritize?",
        [
            "IPD / hospitalization",
            "Maternity",
            "Parents' healthcare",
            "OPD",
            "Mental wellbeing / personal development",
            "Professional development",
            "Travel / commute",
        ],
        description="Please select up to 3.",
        other=True,
    ),
    # Q10
    radio(
        "Which approach would you personally prefer?",
        [
            "Mostly fixed benefits",
            "Core benefits remain fixed, with some choice around other benefits",
            "More flexibility to choose how benefits are allocated",
            "I'm not sure",
        ],
    ),
    # Q11
    paragraph(
        "Are there any benefits or expenses you needed this year but were not covered, or "
        "where the available support did not fully meet your needs?",
        description="Optional.",
    ),
    # Q12
    paragraph(
        "If you could change, add, or improve one thing about the benefits currently available "
        "to you, what would it be and why?",
        description="Optional.",
    ),
]


def main():
    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if not creds.valid:
        creds.refresh(Request())
    hdrs = {"Authorization": "Bearer " + creds.token}

    r = requests.post(
        API, headers=hdrs, json={"info": {"title": TITLE, "documentTitle": DOC_TITLE}}
    )
    if r.status_code != 200:
        print("CREATE FAILED", r.status_code)
        print(r.text)
        sys.exit(1)
    fid = r.json()["formId"]
    print("created formId:", fid)

    reqs = [
        {
            "updateFormInfo": {
                "info": {"description": DESCRIPTION},
                "updateMask": "description",
            }
        }
    ]
    for i, item in enumerate(ITEMS):
        reqs.append({"createItem": {"item": item, "location": {"index": i}}})

    r = requests.post(f"{API}/{fid}:batchUpdate", headers=hdrs, json={"requests": reqs})
    if r.status_code != 200:
        print("BATCHUPDATE FAILED", r.status_code)
        print(r.text)
        sys.exit(1)

    final = requests.get(f"{API}/{fid}", headers=hdrs).json()
    print("questions:", len(final.get("items", [])))
    print("EDIT :", "https://docs.google.com/forms/d/%s/edit" % fid)
    print("LIVE :", final.get("responderUri"))


if __name__ == "__main__":
    main()
