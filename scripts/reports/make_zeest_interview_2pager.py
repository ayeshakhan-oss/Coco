# -*- coding: utf-8 -*-
"""Two-page version of "How Zeest Interviews".

Page 1 - the themes she builds every interview around.
Page 2 - the questions themselves.

Detailed backing reference (full quotes, timestamps, observations):
  docs/interviewing/zeest_interview_style.md
  scripts/reports/make_zeest_interview_style_doc.py

Sources: 3 Fathom case-study debrief transcripts, Growth Manager -
Salman Tariq (10 Aug, 72m), Muhammad Waqas (11 Aug, 61m), Ahmad Wajahat Sheikh
(12 Aug, 84m). All three truncated before the call ended; the Waqas transcript has
inverted speaker labels in places, so attribution is by content.
"""
import os, sys, re

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.docx_brand import build, upload_as_gdoc

OUTDIR = r"c:\Agent Coco\output\reports"
MD_PATH = r"c:\Agent Coco\docs\interviewing\zeest_interview_style_2pager.md"
GDOC_ID = "1jaKbLtzohqQvmN9Wis81yP7zPPgBM_9ic0BJqP37HoY"

WT = [1.85, 3.75, 0.9]

SPEC = [
    # ===================================================== PAGE 1 - THEMES
    ("title", "How Zeest Interviews"),
    ("subtitle", "The Themes She Asks Around"),
    ("meta", "**Evidence:** 3 Growth Manager case-study debriefs \u2014 Salman Tariq (10 Aug) \u00b7 Muhammad Waqas (11 Aug) \u00b7 Ahmad Wajahat Sheikh (12 Aug)"),
    ("spacer", 4),

    ("callout", [
        ("who", "The one thing every question serves"),
        ("plain", "Can this person **get into a room they have no right to be in, and change the mind of the person sitting in it** \u2014 without lying, without paying, and without needing a relationship they already had. Her words, in all three calls: *\u201cbuilding relationships and sustaining them and manipulating conversations for your organization\u2019s incentive is the heart of the role.\u201d*"),
    ], "2F4FA2"),
    ("spacer", 6),

    ("table", [
        ["Theme", "What she is testing", "Asked"],
        ["**1. Charm the room**",
         "Persuasion over diagnosis. Research is table stakes; she wants the move that changes a mind in the meeting. One candidate was told his answers were too diagnosis-heavy.",
         "**3/3**"],
        ["**2. Access, and the end-run**",
         "Not \u201cdo you have contacts\u201d but: who would you call \u2014 and if you know nobody, how do you manufacture a way in? She rewards a named mechanism, not willingness.",
         "**3/3**"],
        ["**3. Translating our incentive into their mandate**",
         "Selling the same product in the counterpart\u2019s vocabulary. Her example: they want teacher training, not AI \u2014 so sell it as teacher training.",
         "**3/3**"],
        ["**4. Are the relationships portable?**",
         "Whether the skill travels or is an artefact of one long tenure. Narrows to individuals, and to cold opens: would **all** of them pick up your call?",
         "**3/3**"],
        ["**5. Persistence under escalation**",
         "She closes each escape route until only a decision remains \u2014 no budget, no time, no explanation, 50 jobs at risk \u2014 then: *\u201creally, what would you do?\u201d*",
         "**3/3**"],
        ["**6. The ethics floor**",
         "A kickback demand, with hospitality separated from corruption so they cannot hide in the ambiguity. Asked before the company position is disclosed.",
         "**3/3**"],
        ["**7. Ownership, not narration**",
         "Did they carry it or watch it? One deal inside a headline CV number; unfunded\u2192funded; and defining their own jargon \u2014 which caught AI-written content once.",
         "2/3"],
        ["**8. Skill transfer across sectors**",
         "For candidates crossing from NGO or private into government. Non-work evidence explicitly counts \u2014 bureaucracy navigated in your own life.",
         "2/3"],
        ["**9. Appetite for the job as it is**",
         "Government-only, slow, rejection-heavy \u2014 asked of the candidate whose ambition pointed elsewhere.",
         "1/3"],
    ], WT, 9.0),

    ("sh2", "How she runs the hour"),
    ("sbullet", "**Discloses her method first**, and warns a thought experiment is coming \u2014 no ambush, no loss of difficulty."),
    ("sbullet", "**Reuses the same scenarios** on every candidate (PECTA blocked pilot, kickback, \u201ca day in this role\u201d). This is what makes candidates comparable \u2014 the most copyable part of her method."),
    ("sbullet", "**Supplies real context generously** \u2014 Rumi\u2019s mechanics, the Prevail-funded Rawalpindi pilot, the PECTA collapse. A thinking test, not a research test."),
    ("sbullet", "**Plays the counterpart herself**, irritated rather than neutral: \u201cthis is the entirety of the government we deal with. **This is the baseline.**\u201d"),
    ("sbullet", "**Protects the candidate\u2019s dignity** \u2014 \u201cit won\u2019t count against you\u201d on a power cut; \u201cI\u2019m not married to English\u201d; teaches rather than traps."),

    ("pagebreak",),

    # ================================================== PAGE 2 - QUESTIONS
    ("title", "The Questions She Asks"),
    ("subtitle", "Verbatim and generalised, grouped by purpose"),
    ("spacer", 2),

    ("sh2", "Opening \u2014 role comprehension  [3/3, always her first question]"),
    ("sbullet", "\u201cWhat do you think a day in this role looks like?\u201d \u2014 asked before any praise or correction, then let the silence run."),

    ("sh2", "Interrogating the case study"),
    ("sbullet", "Name one strength, then stress it: \u201cyou made sure the success indicators were very pointed \u2014 now how would you **secure** that indicator?\u201d"),
    ("sbullet", "\u201cWhy did you choose **this** arm of government, as opposed to [two named alternatives]?\u201d"),
    ("sbullet", "\u201cYou wrote [term]. What do **you** understand when you say [term]?\u201d \u2014 the cheapest AI-detection tool there is."),
    ("sbullet", "\u201cYou leaned into [company value] in your one-pager. How have you done that in your own work \u2014 and any example you can come up with?\u201d"),

    ("sh2", "Verifying the CV"),
    ("sbullet", "\u201cWalk me through **one deal inside that number** \u2014 what did they pay for, how did you convince them, what almost killed it?\u201d Unbluffable."),

    ("sh2", "Access and end-runs  [3/3, her most-pressed line]"),
    ("sbullet", "\u201cWho would you call? And if you know nobody \u2014 how do you get in the room?\u201d"),
    ("sbullet", "\u201cAssume this is the **first time** we are entering the province, with no existing relationship. How do you push yourself into the room?\u201d"),
    ("sbullet", "\u201cHow do you turn somebody you merely know into somebody who gives you access?\u201d"),
    ("sbullet", "Live cold call: \u201cI have the secretary\u2019s number and no relationship. **Call him.** How does that go?\u201d"),

    ("sh2", "Relationship durability \u2014 the portability trap"),
    ("sbullet", "\u201cCould you go back to any organisation from the last five or six years, pick up a contact, and convert that capital today?\u201d"),
    ("sbullet", "\u201cWould **all** of them pick up your call \u2014 or only some? Which ones, and why?\u201d"),
    ("sbullet", "\u201cGive me a **cold open** with someone influential, whom you sustained, and could comfortably call today.\u201d"),

    ("sh2", "Ownership and skill transfer"),
    ("sbullet", "\u201cHave you taken something from **unfunded to funded** \u2014 or were you supporting a team that did?\u201d / \u201cmoved a free pilot to a paid deal?\u201d"),
    ("sbullet", "\u201cYour experience is donor/NGO/private. How does that translate to government \u2014 **and it needn\u2019t be a work example**; bureaucracy in your own life counts.\u201d"),
    ("sbullet", "If the honest answer is no, widen the credit to any leverage they created \u2014 and note whether they invented an example instead."),

    ("sh2", "Escalating scenarios \u2014 always real Taleemabad situations"),
    ("sbullet", "**Blocked pilot (PECTA):** approval authority withdrawn mid-deal, the CEO ghosting, the minister unreachable. What now?"),
    ("sbullet", "**Renewal squeeze:** one month of payroll left, 50 jobs at risk, no-cost extension dead, and they won\u2019t say what changed. \u201cReally, what would you do?\u201d"),
    ("sbullet", "**Three-way partnership:** they want it, they have no money. Bring a funder in without losing their ownership of it."),
    ("sbullet", "**Category refusal:** \u201cwe don\u2019t want AI, we want teacher training \u2014 end of story.\u201d Sell the same product in their words."),
    ("sbullet", "**The convening:** 60 days, no budget line, fill the room with secretaries and partners. Who first \u2014 and why not the top?"),

    ("sh2", "Running the role-play the way she does"),
    ("sbullet", "Give the product and deal history in full first \u2014 if they don\u2019t know the product, **stop, teach them, restart**. Offer one to three minutes\u2019 prep."),
    ("sbullet", "Name the counterpart and their real constraint; constrain the scene \u2014 ten minutes, mid-meeting, others in the room."),
    ("sbullet", "Play them **irritated, not neutral**, escalating objections in order: accountability, then budget cannibalisation, then scale."),
    ("sbullet", "Correct third-person narration at once: \u201ctalk to me, not about them.\u201d Close explicitly and thank them."),

    ("sh2", "Ethics gate \u2014 ask, probe, then disclose"),
    ("sbullet", "\u201cYou have the green light, but they want 1\u20133% of the contract in someone\u2019s pocket. How do you manage that conversation?\u201d"),
    ("sbullet", "Remove the ambiguity yourself \u2014 \u201cI mean 3% of the entire project cost, high-level bribes\u201d, not chai-pani \u2014 then probe once: \u201cso if your organisation green-lit it, you\u2019d go ahead?\u201d"),
    ("sbullet", "**Only then** state the position: hospitality is fine; skimming is not, and we walk away from the money rather than pay."),

    ("sh2", "Close"),
    ("sbullet", "\u201cIs there anything I should know before I make this decision?\u201d \u00b7 Fit, not capability: \u201chow do you feel that we don\u2019t work with the private sector at all?\u201d \u00b7 Then take their questions, candidly."),

    ("footer", "Internal \u2014 Taleemabad People & Culture. Full version with quotes, timestamps and open questions: docs/interviewing/zeest_interview_style.md"),
]


def to_markdown(spec):
    out = []
    for item in spec:
        k = item[0]
        t = item[1] if len(item) > 1 else ""
        if k == "title":
            out.append(f"\n# {t}\n")
        elif k == "subtitle":
            out.append(f"## {t}\n")
        elif k == "meta":
            out.append(f"{t}\n")
        elif k in ("sh2", "h2"):
            out.append(f"\n### {t}\n")
        elif k in ("para", "spara"):
            out.append(f"{t}\n")
        elif k in ("bullet", "sbullet"):
            out.append(f"- {t}")
        elif k == "footer":
            out.append(f"\n*{t}*")
        elif k == "pagebreak":
            out.append("\n---\n")
        elif k == "callout":
            for kind, text in item[1]:
                out.append(f"> **{text}**" if kind == "who" else f"> {text}")
                out.append(">")
            out.append("")
        elif k == "table":
            rows = item[1]
            out.append("")
            out.append("| " + " | ".join(rows[0]) + " |")
            out.append("|" + "---|" * len(rows[0]))
            for r in rows[1:]:
                out.append("| " + " | ".join(c.replace("\n", " ") for c in r) + " |")
            out.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(os.path.dirname(MD_PATH), exist_ok=True)

docx_path = os.path.join(OUTDIR, "How_Zeest_Interviews_2pager.docx")
build(SPEC, docx_path, footer_note="Internal \u2014 Taleemabad People & Culture")

with open(MD_PATH, "w", encoding="utf-8") as fh:
    fh.write(to_markdown(SPEC))
print("built", MD_PATH)

if os.environ.get("UPLOAD") == "1":
    upload_as_gdoc(docx_path,
                   "How Zeest Interviews \u2014 Themes & Questions (2-pager)",
                   file_id=GDOC_ID)
