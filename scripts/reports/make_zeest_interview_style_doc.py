# -*- coding: utf-8 -*-
"""Build the "How Zeest Interviews" internal reference document.

Sources (Fathom transcripts, supplied by Ayesha 2026-08-20/21):
  A. Growth Manager Lahore - Salman Tariq - 10 Aug 2026, 72 min
     https://fathom.video/share/8JwNhZDz5eohhVNoiy6FF4RajezmUWsM
  B. Growth Manager Lahore - Muhammad Waqas - 11 Aug 2026, 61 min
     https://fathom.video/share/zdcsjPfpcrgjyWPtdVhsdDFM7kjWg-h1
  C. Growth Manager - Ahmad Wajahat Sheikh - 12 Aug 2026, 84 min
     https://fathom.video/share/zkDXPXfb4Ds3eMAEGU2oUfp96cioiY8_

Two transcription caveats, both stated in the document itself:
  1. All three transcripts were truncated at 50,000 characters on delivery -
     Salman at ~1:00 of 72 min, Waqas at ~52:00 of 61 min, Ahmad at 1:19:39 of 84 min.
  2. Fathom's speaker labels are INVERTED across long stretches of the Waqas
     transcript (the opening role-comprehension question is labelled "Muhammad
     Waqas" but is plainly Zeest). All attribution in this document is by content,
     not by label.

Emits a branded DOCX + markdown copy, and updates the existing Google Doc in place
so the shared link stays valid.
"""
import os, sys, re

sys.path.insert(0, r"c:\Agent Coco")
from scripts.utils.docx_brand import build, upload_as_gdoc

OUTDIR = r"c:\Agent Coco\output\reports"
MD_PATH = r"c:\Agent Coco\docs\interviewing\zeest_interview_style.md"
GDOC_ID = "1jaKbLtzohqQvmN9Wis81yP7zPPgBM_9ic0BJqP37HoY"

W3 = [1.45, 2.5, 2.55]
W3b = [2.9, 1.2, 2.4]
W2b = [2.6, 3.9]

SPEC = [
    ("title", "How Zeest Interviews"),
    ("subtitle", "Question Patterns & Emphases \u2014 Growth Manager Case-Study Debriefs"),
    ("meta", "**Prepared for:** Ayesha Khan, People & Culture"),
    ("meta", "**Interviewer analysed:** Zeest Hassan Qureshi"),
    ("meta", "**Evidence base:** 3 case-study debrief transcripts \u2014 Salman Tariq (10 Aug, 72 min) \u00b7 Muhammad Waqas (11 Aug, 61 min) \u00b7 Ahmad Wajahat Sheikh (12 Aug, 84 min)"),
    ("meta", "**Purpose:** Internal reference \u2014 how Zeest runs a Growth interview, what she is testing for, and a reusable question bank"),
    ("rule",),

    ("callout", [
        ("who", "Read this first \u2014 the limits of this document"),
        ("plain", "Three transcripts, all the same role family (Growth Manager, government-facing) and all the same stage (post-case-study debrief). This describes how Zeest interviews **for this role**; it is not her method for engineering, ops or junior hires. Two transcription problems affect the evidence. First, **all three transcripts were cut off before the call ended** \u2014 Salman at roughly 1:00 of 72 minutes, Waqas at roughly 52:00 of 61, Ahmad at 1:19:39 of 84 \u2014 so her closing minutes are never captured. Second, **Fathom inverted the speaker labels across long stretches of the Waqas transcript**; every quote here is attributed by content rather than by label, and Fathom also garbles Urdu and cross-talk, so quotes are lightly cleaned with square brackets marking a repaired word."),
    ], "2F4FA2"),
    ("spacer", 10),

    ("h1", "The one-paragraph summary"),
    ("para", "Zeest runs a **conversational stress test, not a q-and-a**. She discloses her method at the top, checks the candidate understands the job, then spends the bulk of the hour pushing a small number of **real, current Taleemabad situations \u2014 the same ones, reused across all three candidates** \u2014 progressively harder until the candidate either produces a concrete move or runs out of road. She is not testing knowledge of education, government or AI; she supplies all of that herself, generously. She is testing **whether this person can get into a room they have no right to be in, and change the mind of the person sitting in it.** She says so out loud in all three calls. Everything else \u2014 access, contacts, translation of incentives, persistence, ethics \u2014 is a component of that one thing."),

    ("h1", "What repeats across all three calls"),
    ("para", "The frequency column is the most useful thing in this document: it separates her fixed method from her improvisation. Anything marked 3/3 should be written into the Growth interview standard."),
    ("table", [
        ["Move", "Frequency", "Evidence"],
        ["\u201cWhat does a day in this role look like?\u201d as the first substantive question",
         "**3 / 3**", "Asked before any praise or correction, so the answer is uncoached"],
        ["Discloses her own interview style before using it",
         "**3 / 3**", "\u201cdynamic\u201d, \u201cthings I\u2019ll throw at you in the moment\u201d, warns a thought experiment is coming"],
        ["Access question: who would you call \u2014 and if nobody, how do you get in?",
         "**3 / 3**", "Her single most-pressed line of questioning"],
        ["The PECTA blocked-pilot scenario (SED ruling, minister unreachable, Kashmir)",
         "**3 / 3**", "Verbatim reuse \u2014 role-play for Waqas and Ahmad, pressure test for Salman"],
        ["Live role-play in which she plays the counterpart",
         "**3 / 3**", "PECTA CEO (\u00d72) and Sindh Education Minister Sardar Shah (\u00d71)"],
        ["Bribe / kickback question",
         "**3 / 3**", "1% (Salman), 3% of project cost (Waqas), 2% (Ahmad)"],
        ["Relationship portability \u2014 would those contacts still take your call?",
         "**3 / 3**", "Narrowed to individuals and to cold opens in each call"],
        ["Names \u201ccharm the room\u201d as the heart of the role",
         "**3 / 3**", "Stated explicitly to each candidate, in near-identical words"],
        ["Escalation ladder \u2014 closes each escape route until only a decision remains",
         "**3 / 3**", "Sharpest in the Waqas renewal sequence (19:13\u201322:10)"],
        ["Hands over real product / deal context unprompted",
         "**3 / 3**", "Rumi mechanics, Prevail-funded Rawalpindi pilot, PECTA, Beth/PEF"],
        ["Offers prep time before a hard ask",
         "**3 / 3**", "\u201ctake a minute\u201d, \u201cyou can take three minutes\u201d"],
        ["Anchors a question to a named Taleemabad value",
         "1 / 3", "\u201cyou really leaned into the one for all and all for one value\u201d (Waqas)"],
        ["Picks one deal inside a headline CV number",
         "1 / 3", "\u201cwalk me through one deal inside that [8.7 million]\u201d (Waqas)"],
        ["Asks the candidate to define their own jargon",
         "1 / 3", "\u201cregularization\u201d \u2014 exposed AI-written case-study content (Waqas)"],
        ["States the company\u2019s ethics position after the bribe answer",
         "1 / 3", "Done for Ahmad; **not** done for Waqas or Salman \u2014 see Part 4"],
    ], W3b, 9.5),

    ("pagebreak",),

    # ============================================================ EMPHASES
    ("part", "PART 1 \u2014 What Zeest Is Actually Emphasising"),
    ("para", "Ranked by airtime, by pressure applied, and by what she says explicitly."),

    ("banner", "1. Change the mind in the room", "3 / 3 \u00b7 her stated core"),
    ("para", "This is the emphasis everything else serves, and she names it in every call in almost the same words. It is also the axis on which she pushed back hardest on a candidate."),
    ("callout", [
        ("who", "To Ahmad, closing the role-play (1:11:19):"),
        ("quote", "\u201cThis is probably the gist of the role itself, because building relationships and sustaining them and manipulating conversations for your organization\u2019s incentive is the heart of the role.\u201d"),
        ("who", "To Waqas, explaining why the Lahore hire exists (35:50):"),
        ("quote", "\u201cThere will be obstacles\u2026 but there has to be somebody who is able to go in the room and **charm these government stakeholders** to make sure that they\u2019re able to deliver.\u201d"),
        ("who", "To Salman, challenging his answers to his face (30:43):"),
        ("quote", "\u201cA lot of your answers\u2026 are based about diagnosing the problem, figuring out what went wrong\u2026 In growth, a lot of that is already being done by AI for us. And what we end up doing actually in the room is making sure that\u2026 that person is fully charmed and really excited to work with us\u2026 What I\u2019m just trying to do is change their mind in the room. And that\u2019s where the key is within this role.\u201d"),
    ]),
    ("spacer", 8),
    ("para", "**What this means for scoring:** research, frameworks and diagnosis are table stakes and she treats them as such. A candidate who answers a blocked-deal scenario with \u201cfirst I would understand why\u201d is answering the wrong question, and she will say so."),

    ("banner", "2. Access \u2014 and the end-run when the door is shut", "3 / 3 \u00b7 most pressure"),
    ("para", "Her signature question is never \u201cdo you have contacts\u201d. It is the two-part version: **who would you call, and if you know nobody, how do you manufacture a way in.** She asks it in all three calls and escalates until she gets a name or a mechanism."),
    ("bullet", "To Waqas (9:30): \u201cyou picked PITB as the entry point. I\u2019m assuming you don\u2019t have an existing relationship with someone in PITB. So how would you approach that? And how would you try to **get in the room**?\u201d \u2014 then, when he drifted into pipeline theory, she re-framed it harder: \u201cregardless of all of that, I\u2019m wondering how you would push to get yourself in the room. Let\u2019s say\u2026 this is the first time Taleemabad is entering Punjab.\u201d"),
    ("bullet", "To Ahmad (41:54): \u201c**A**, who would you call if you know someone there? And if you don\u2019t, how would you approach them? And then how would you try to make an end[-]r[un] to get to know someone there? And **B**, how would you have that conversation?\u201d"),
    ("bullet", "To Salman (12:33): \u201cHow would you\u2026 [make] a relationship go from just somebody you know to somebody who gives you access? **A**, that, and **B**, how would you get access when you\u2019re outside of these structures, not inside?\u201d"),
    ("para", "She rewards a **named mechanism**, not willingness \u2014 and in the Waqas call she went as far as supplying her own answer, which is the clearest statement of the standard she holds candidates to:"),
    ("callout", [
        ("who", "Zeest to Waqas, endorsing his instinct to camp outside the office (15:43):"),
        ("quote", "\u201cYou are correct in terms of assuming that spending time in front of government offices is absolutely key. You have to just **leave your self-respect and pride at home** sometimes and just go there and be there and sit with them and have 15 cups of tea if that\u2019s what it takes. But that\u2019s how you push the paper forward.\u201d"),
    ]),
    ("spacer", 8),
    ("para", "Ahmad named two Muslim Hands executives and the Director Programs seat at PEF; Salman named Khurram Zafar and generalised it into pressure groups; Waqas described physically going to the deputy director\u2019s office because it was on his way home. All three landed, and she praised each explicitly \u2014 \u201cthe idea about approaching a side channel and not giving up is very important\u201d (Ahmad, 1:00:38); \u201cthe idea behind pressure groups\u2026 is very important\u201d (Salman, 19:28)."),

    ("banner", "3. Translate our incentive into their mandate", "3 / 3 \u00b7 most rewarded"),
    ("para", "The candidates\u2019 strongest moments were all versions of this move, and she supplies her own worked example unprompted \u2014 which tells you it is a live problem for the team, not a hypothetical."),
    ("callout", [
        ("who", "Zeest\u2019s own example, given to Salman (30:43):"),
        ("quote", "\u201cI go to Balochistan and they say, we\u2019re not focused on AI right now, we\u2019re only focused on teacher training. I say, okay. And now I have to figure out how to market my product in a way that to them, it\u2019s teacher training \u2014 even though technically it\u2019s still AI \u2014 and change the conversation in that way. And all of that is happening without diagnosing why they don\u2019t want AI, because that\u2019s irrelevant, frankly.\u201d"),
    ]),
    ("spacer", 8),
    ("para", "Salman had independently framed his own job the same way \u2014 \u201ctranslate what you are doing\u2026 to their vocabulary\u201d (2:00) \u2014 and she thanked him for the answer and the example. Waqas produced the equivalent inside the role-play, pitching Rumi on WhatsApp ubiquity rather than on AI (\u201ceven if you go into the remote areas, they know what WhatsApp is\u201d). Ahmad got credit for the hierarchy version of it \u2014 knowing not to go over the secretary\u2019s head."),

    ("banner", "4. Are the relationships portable, or venue-specific?", "3 / 3 \u00b7 the trap"),
    ("para", "Having accepted that a candidate has contacts, she immediately tests whether the *skill* travels or whether it is an artefact of one long tenure. The Waqas version is the sharpest of the three because it asks the uncomfortable half out loud."),
    ("callout", [
        ("who", "To Waqas (48:51):"),
        ("quote", "\u201cIf tomorrow you have to call someone up in any of those \u2014 experiences, fellowships, grants, all the people you met, the network you\u2019ve built \u2014 how would those conversations go? And **would all of them pick up your call?** Or do you think some organizations or some experiences were where people would pick up your call, but other people won\u2019t?\u201d"),
        ("who", "To Salman (27:21):"),
        ("quote", "\u201cDo you think that\u2019s true of any organization you\u2019ve worked with in the past? Not even just worked at, but worked with or collaborated with or volunteered with\u2026 or do you think that PIT[B] is special because you spent so much time there?\u201d"),
        ("who", "To Ahmad (48:48):"),
        ("quote", "\u201cCould you go back to any organization\u2026 in the last maybe five, six years\u2026 and be able to pick up any contact and leverage that political capital or social capital and convert it for today? I\u2019m just wondering how you sustain relationships.\u201d"),
    ]),
    ("spacer", 8),
    ("para", "She then narrows from organisational to **individual**, and from warm to **cold** \u2014 to Salman (51:20): \u201cgive me an example of a **cold open** with any particular person who turned out to be influential, who you then sustained a relationship with, who you could ask very comfortably.\u201d This is the question that separates a well-connected incumbent from a genuine relationship-builder. It produced the single best answer in any of the three calls (Salman\u2019s LinkedIn campaign that brought DigitalOcean, Notion and Miro startup credits into Pakistan)."),

    ("banner", "5. Persistence, and the refusal of abstraction", "3 / 3"),
    ("para", "Her escalation pattern is consistent: she removes each escape route until only a decision remains. This is the clearest scoring instrument she has, and the Waqas renewal sequence is the textbook example \u2014 five consecutive narrowings in three minutes."),
    ("table", [
        ["Candidate\u2019s escape route", "Zeest\u2019s closing of it"],
        ["\u201cI\u2019d ask for a no-cost extension\u201d",
         "\u201cWe have enough money to pay all of the coaches for the next month. After that\u2026 we will have to lay people off\u2026 you no longer have the room to go towards them with an extension request.\u201d (Waqas, 19:13)"],
        ["\u201cI\u2019d work towards the renewal\u201d",
         "\u201cIt\u2019s 1st June. You need to get this renewal done, otherwise you have to lay off 50 people. What would you do? **I mean, really, what would you do?**\u201d (20:42)"],
        ["\u201cWe\u2019d give it our best\u201d",
         "\u201cI\u2019m going to push this a little more\u2026 What would you **actually** do when you say you do your best?\u2026 knowing that you have 30 days to deliver.\u201d (21:32)"],
        ["\u201cI\u2019d understand their perspective first\u201d",
         "\u201cThey don\u2019t want to answer that. They\u2019re like, no, we don\u2019t [want] AI. **End of story.**\u201d (Salman, 32:58)"],
        ["\u201cI\u2019d build the impact case\u201d",
         "\u201cSo that\u2019s theoretical\u2026 the reason it was approved in the first place was because they already knew it worked\u2026 So all of these things are secondary.\u201d (Salman, 22:00)"],
        ["\u201cI\u2019d find out what changed\u201d",
         "\u201cWhat if you can\u2019t find out the reason? Then you just have to figure out how to renew it, but you don\u2019t know why it went wrong.\u201d (Salman, 23:48)"],
        ["A general principle instead of an action",
         "\u201cSo what do you do? **And I\u2019m sure you know this**, so what do you do?\u201d (Ahmad, 56:03)"],
        ["Narrating the pitch in third person",
         "\u201cI\u2019m wondering if you can have this conversation, assuming that I am the person you\u2019re talking to, rather than them, they, etc. **Just talk to me.**\u201d (Salman, 42:31)"],
    ], W2b, 9.5),
    ("spacer", 8),
    ("para", "She names resilience as the quality being measured \u2014 \u201cthat shows resilience, which I think I really appreciate in this particular role\u201d (Ahmad, 1:01:26) \u2014 and Waqas independently named it back to her as the skill he would carry over from NGO work."),

    ("banner", "6. The ethics floor", "3 / 3 \u00b7 hard gate"),
    ("para", "Zeest puts a kickback demand to every candidate, in local, unmistakable terms, and separates hospitality from corruption herself so the candidate cannot hide in the ambiguity."),
    ("callout", [
        ("who", "To Waqas (42:09), then sharpening it when he answered about chai-pani:"),
        ("quote", "\u201cSo would you say yes to a bribe if it meets your end goal?\u201d \u2026 \u201cWhen I say bribe, I mean like **3% of the entire project cost**. I\u2019m talking about high-level bribes.\u201d"),
        ("who", "And she states the purpose of the question outright (43:13):"),
        ("quote", "\u201cThe reason I\u2019m trying to understand this is\u2026 how do we do and achieve relationship goals **without sacrificing our ethics**, and how far you can go. So that\u2019s kind of what I\u2019m trying to assess.\u201d"),
        ("who", "To Salman (18:50):"),
        ("quote", "\u201cLet\u2019s say they say, we basically want 1% of all potential scales should go directly into the minister\u2019s pocket \u2014 then what [do] we [do]?\u201d"),
        ("who", "To Ahmad (1:14:27):"),
        ("quote", "\u201cLet\u2019s say you have a green light for a new pilot or for a paid scale, but they say that it will [cost] 2%\u2026 How do you manage that conversation?\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("para", "**The three answers diverged sharply, which is exactly what a good gate does.** Salman refused immediately on reputational grounds (\u201cthat would create an unethical position that would weaken the position of Taleemabad\u2026 if you do this once, it would weaken the credi[bility]\u201d). Ahmad described the practice as endemic and refusal as costly \u2014 \u201cyou can refuse, but then there are many consequences\u201d \u2014 and defaulted to waiting for the next secretary. Waqas deferred the decision upward: \u201cI will actually have to discuss that with my administration\u2026 if they say you can do that, then I will do it\u201d, and when pressed, \u201cif we want it that bad, then I might do it.\u201d Zeest followed up rather than letting it sit \u2014 \u201cso if your administration gives you the green light, you\u2019ll just go for it?\u201d"),
    ("para", "She stated Taleemabad\u2019s own position **only in Ahmad\u2019s call** (1:17:11): \u201cTaleemabad is a very strict values company\u2026 we [might] take them to dinner and take [them to] lunch. When it comes to skimming off the top, we are very strict. We will give up our entire payment\u2026 But we don\u2019t [pay].\u201d Asking first and disclosing second is the right order \u2014 it stops the candidate reverse-engineering the approved answer \u2014 but it was only done once. See Part 4."),

    ("banner", "7. Does the candidate own the number, or the narrative?", "1 / 3 \u00b7 worth keeping"),
    ("para", "The best single question in the three transcripts, asked of Waqas about a headline CV figure (5:35):"),
    ("callout", [
        ("quote", "\u201cYou mentioned in your CV that you were able to contribute 8.7 million in revenue when you were at ScienceFuse. Can you walk me through **one deal inside that number** that you took start to end \u2014 what did they pay for, how did you convince them to pay, [and] things that almost killed the deal and how you managed that?\u201d"),
    ]),
    ("spacer", 8),
    ("para", "It is unbluffable: a candidate who inherited a number cannot narrate a single deal through it. Waqas passed \u2014 he named the National Catholic Education Commission, the 1.6 million first-year figure, how a co-working-space friend introduced him, the two months of \u201cwe\u2019re busy, this isn\u2019t our priority\u201d, and the module structure he built. Recommend this becomes standard for any revenue-carrying CV."),

    ("banner", "8. Is the case study actually theirs?", "1 / 3 \u00b7 highest-value catch"),
    ("para", "She asked Waqas to define a term he had used in his own submission (24:04): \u201cyou\u2019re mentioning that either you\u2019ll do a fresh multi-year renewal, or you will go for **regularization**. I\u2019m trying to understand what you understand when you say regularization.\u201d"),
    ("callout", [
        ("who", "His answer:"),
        ("quote", "\u201cThis is something I would say **AI must have written**, because I cannot justify regularization\u2026 I will be very honest. I cannot.\u201d"),
    ], "3C78D8"),
    ("spacer", 8),
    ("para", "She accepted the honesty without penalty theatre (\u201cthat\u2019s fine\u201d) and then **taught him the concept** \u2014 that regularization means the programme becomes a line item in the provincial or federal budget rather than a grant renewed every few years, that World Bank or UNICEF money is \u201ca temporary band-aid\u201d, and that it takes two to two and a half years to get there. Two lessons for the team: **asking a candidate to define their own jargon is the cheapest AI-detection tool available**, and her instinct to teach rather than trap is why candidates keep being honest with her."),

    ("banner", "9. Do the skills transfer \u2014 including from private life?", "2 / 3"),
    ("para", "To Waqas (38:23), who has NGO and donor experience but none with government: \u201cHow would you translate those skills to working with the government?\u2026 have you ever tried to build such relationships? **And it doesn\u2019t have to be necessary in a working capacity** \u2014 maybe you would navigate [red] tape to get some stuff done in your own life. You mentioned doing things after your father passed away.\u201d Accepting non-work evidence is both humane and sound: for a candidate crossing sectors, the transferable proof often sits outside their CV. Ahmad got the same test in its funding form \u2014 \u201chave you actually carried out that funnel?\u201d from unfunded to funded \u2014 and Salman in its commercial form \u2014 \u201chave you moved a free pilot or proof of concept to a converted deal?\u201d"),
    ("para", "Note her handling when Salman answered honestly that revenue conversion was never his mandate: she **widened the credit** rather than marking him down \u2014 \u201ccreating any kind of leverage and moving that towards the benefit of an organization would count in the same category\u2026 as converting something free-to-paid.\u201d She rewards the honest no; she does not reward invention. Salman had said \u201cI don\u2019t want to make things up.\u201d"),

    ("banner", "10. Convening design and stakeholder assembly", "1 / 3"),
    ("para", "Tested properly only in the Waqas call (44:00): \u201clet\u2019s go to the part of your study where you designed a room\u2026 how would you bring all of these stakeholders in one room if you had two months to organize the event?\u2026 It\u2019s 30 days, 60 days. How would you do it?\u201d When he proposed working bottom-up to secure a VIP list, she challenged the instinct and converted it into an on-the-spot cold call:"),
    ("callout", [
        ("who", "Zeest (46:32), interrupting:"),
        ("quote", "\u201cCan I pause you? Why do you think [you have to] start small? Let\u2019s say I give you the number of the secretary of Punjab \u2014 I haven\u2019t talked to him, I just got his number. **Call him.** How would you call him and talk to him?\u201d"),
    ]),
    ("spacer", 8),
    ("para", "Worth noting because the Growth Manager case study tests convening design on paper (Assignment 2) and only one of three debriefs pressure-tested it out loud."),

    ("banner", "11. Appetite for the job as it actually is", "1 / 3"),
    ("para", "Late in Salman\u2019s call she tested fit rather than capability (58:17): \u201chow do you feel about the fact that we don\u2019t work with the private sector at all? We work primarily with governments \u2014 provincial, international, federal?\u201d Asked immediately after he had pitched Taleemabad becoming a startup-ecosystem builder, the question does two jobs: checking he wants the government grind, and checking whether his own ambition points somewhere else."),

    ("pagebreak",),

    # =========================================================== TECHNIQUES
    ("part", "PART 2 \u2014 Her Techniques, and Why They Work"),

    ("h2", "1. She discloses her method before using it"),
    ("para", "\u201cLet me just walk you through how I generally conduct interviews\u2026 **A**, I like to keep things dynamic, I like to keep things moving. And **B**, I like to understand what kind of person you are holistically, not just on paper\u2026 Sometimes I have a little thought experiment in [my] role, so I\u2019m just giving you a heads up\u201d (Ahmad, 13:44). To Waqas: \u201cI like to do a bit of dynamic questioning. There\u2019ll be some things that I\u2019ll pick out from your case\u2026 but there will also be some things that I\u2019ll **throw at you in the moment**.\u201d Pre-announcing the ambush removes the unfairness without removing the difficulty \u2014 nobody can claim they were blindsided, and she gets a cleaner signal. She also owns her own intensity: \u201cI know I get a little in your face sometimes\u201d (Waqas, 37:53)."),

    ("h2", "2. She reuses the same scenarios across candidates"),
    ("para", "The **PECTA blocked pilot** appears in all three interviews with the same components: the SED policy revision, the CEO losing approval authority, the minister unreachable because Punjab is consumed by the Kashmir issue and the re-election. Waqas and Ahmad got it as a role-play; Salman got it as a pressure test on his own framework. The kickback question and the \u201cday in this role\u201d opener are equally fixed. **Reusing a fixed scenario is what makes candidates comparable, and it is the most valuable thing in her method for the rest of the team to copy.**"),

    ("h2", "3. She gives away real context generously"),
    ("para", "She hands over material most interviewers would guard: Rumi\u2019s full mechanics (an AI teacher co-pilot running entirely on WhatsApp \u2014 lesson plans, voice-note capture of a live class, scoring against the government rubric, feedback on closed versus open-ended questioning, attendance, reading assessments); the fact that Rumi\u2019s codebase is **open source**, cloned by developers in India and adaptable to agriculture, health records and mental-health triage; the Prevail-funded Rawalpindi pilot sanctioned by Punjab; the Beth/PEF pilot; the PECTA collapse; deployments in Tanzania, Kenya, Palestine and the West Bank; the shift away from private-sector B2B2G; the 2030 goal of 350 million children."),
    ("para", "In the Waqas call she went further \u2014 she **stopped the role-play** on discovering he did not know the product, taught him Rumi properly, and restarted. His reaction is the argument for doing it: \u201cif I didn\u2019t have the context, I would have said maybe something which I had no idea about\u2026 it actually gave me an idea on-spot.\u201d This makes the interview a **thinking test rather than a research test** \u2014 nobody wins it by having read the website \u2014 and doubles as a sell to a senior candidate."),

    ("h2", "4. She verifies claims with insider knowledge"),
    ("para", "\u201cI\u2019ve worked at PITB as well, so I do have understanding of the organization. So is Plan 9 still a part of PITB, or has it been replaced by the incubation wing?\u201d (Salman, 5:25). She later drops that Galaxy Lollywood was a Plan 9 startup. Low-cost, high-yield authenticity checks that a candidate embellishing a tenure cannot survive. Worth adopting as a **panel-design principle**: put someone in the room who has actually worked inside the counterpart institution."),

    ("h2", "5. She reflects back before moving on"),
    ("para", "\u201cSo you\u2019re basically saying that there was a lot of effort involved in moving the needle\u2026 and you were offering support to the team that sort of executed it. **Am I correct?**\u201d (Ahmad, 27:19). Two functions: it confirms she has followed a long, meandering answer, and it quietly re-states the answer in its weakest honest form \u2014 giving the candidate a fair chance to correct the record before she scores it."),

    ("h2", "6. She re-asks the half that got dropped"),
    ("para", "Ahmad answered why he chose PMIU and skipped how he would get the meeting; she came straight back: \u201cit was how you would go about achieving the success indicator of getting a meeting with the MD of PMIU. Like, how would you go about it?\u201d (31:47). Waqas answered the pipeline question instead of the access question and got the same treatment. **Double-barrelled A/B questions are a deliberate device** \u2014 which half a candidate answers, and which half they let slide, is itself signal."),

    ("h2", "7. She plays a hard, informed, sometimes hostile counterpart"),
    ("para", "As the PECTA CEO facing Waqas she switched into Urdu and played the official openly irritated \u2014 *\u201cTaleemabad wale, aap log phir aa gaye hain\u2026 policy badal gayi hai, aap baar baar aate hain, abhi hum pilot shuru nahi kar sakte, kya masla hai\u2026 aap log samajh nahi rahe hain hamari [baat]\u201d*. When he protested that he had pictured a friendlier, more casual encounter, she corrected the frame in one line:"),
    ("callout", [
        ("who", "Zeest (31:10):"),
        ("quote", "\u201cWaqas, this is the entirety of the government we deal with. **This is the baseline.**\u201d"),
    ], "2F4FA2"),
    ("spacer", 8),
    ("para", "As Sindh Education Minister Sardar Shah facing Salman she raised a real minister\u2019s objections in order: accountability (\u201cif you inject them, then teachers will use AI to teach\u2026 we don\u2019t know what happens in class\u201d), then budget cannibalisation (\u201cwe pay teacher training, we pay PITE\u2026 if we put AI, then we will not do our work\u201d), then scale and offline capability. She constrains the scene realistically \u2014 ten minutes, mid-meeting, other people in the room \u2014 and always offers prep time first, so what she tests is judgment under pressure, not cold-start improvisation."),

    ("h2", "8. She protects the candidate\u2019s dignity throughout"),
    ("bullet", "Power cut mid-answer: \u201cwe all live in Pakistan, we understand the limitations\u2026 We can also do this at a later time\u2026 **It won\u2019t count against you.**\u201d (Ahmad, 27:00) \u2014 and to you off-mic beforehand: \u201cI don\u2019t want him to panic.\u201d"),
    ("bullet", "Language: \u201cplease feel free to switch languages. **I\u2019m not married to English.**\u201d (Ahmad, 34:38) \u2014 after which he gave his strongest answers in Urdu. She code-switches into Urdu herself with Waqas."),
    ("bullet", "Names: \u201cyour name is Ahmed or Wajahat \u2014 which should I call you?\u201d (13:30)."),
    ("bullet", "Lets a candidate open their own case study mid-answer: \u201cof course, of course, you can open your case study\u201d (Waqas, 24:15)."),
    ("bullet", "Thanks candidates for tolerating the format: \u201cthank you for going along with me on that experiment\u201d, \u201cI know it\u2019s an unconventional thing to do in an interview.\u201d"),
    ("bullet", "Explains why the debrief exists at all: \u201cwe make it a point\u2026 because you\u2019ve put in the effort. So it\u2019s important for us to also go through the case study\u2026 and figure out what we can pick up\u201d (Salman, 46:58)."),
    ("para", "This is worth protecting as house style. Salman volunteered that the process itself taught him something \u2014 \u201cthere are times when you go through a recruitment process and you get to learn something, and this is one of th[ose]\u201d \u2014 and Waqas thanked her unprompted for the mid-role-play teaching."),

    ("h2", "9. She tells the candidate her hypothesis about their weakness"),
    ("para", "Rather than quietly marking Salman down for being diagnosis-heavy, she said it to his face and asked him to answer it (30:43). Higher-risk and higher-yield: the candidate gets one clean chance to disprove the read, and the interviewer avoids scoring a first impression that never got tested."),

    ("pagebreak",),

    # ============================================================ QUESTION BANK
    ("part", "PART 3 \u2014 Reusable Question Bank"),
    ("para", "Generalised from what Zeest actually asked, so the wording can be reused for the next Growth or partnerships hire. Items marked **[3/3]** were asked of every candidate and should be treated as standard."),

    ("h2", "Opening \u2014 role comprehension"),
    ("bullet", "**[3/3]** \u201cWhat do you think a day in this role looks like?\u201d \u2014 asked before any praise or correction."),
    ("bullet", "Follow with silence. Waqas\u2019s honest \u201cI had no idea\u2026 I have never worked with government before, in full disclosure\u201d was more useful than a polished answer would have been."),

    ("h2", "Case study \u2014 interrogating what they wrote"),
    ("bullet", "Name one specific strength first, then stress it: \u201cyou made sure the success indicators were very pointed \u2014 [now] how would you secure that success indicator?\u201d"),
    ("bullet", "\u201cWhy did you choose **this** arm of government, as opposed to [two named alternatives]?\u201d"),
    ("bullet", "**Define your own jargon:** \u201cyou wrote [term]. What do you understand when you say [term]?\u201d \u2014 the cheapest AI-detection tool available."),
    ("bullet", "\u201cYour reflective note was a little brief \u2014 I wanted more insight on it.\u201d"),
    ("bullet", "Anchor to a named company value: \u201cyou leaned into [value] in your one-pager. How have you done that in your own work \u2014 and how would you push that value externally?\u201d Then: \u201cany example you can come up with?\u201d"),

    ("h2", "CV verification"),
    ("bullet", "\u201cWalk me through **one deal inside that number** \u2014 start to end. What did they pay for, how did you convince them, what almost killed it, and how did you manage that?\u201d"),
    ("bullet", "An insider fact-check on a claimed tenure, asked by someone who has worked in that institution."),

    ("h2", "Access and end-runs"),
    ("bullet", "**[3/3]** \u201cWho would you call? And if you know nobody \u2014 how do you get in the room?\u201d"),
    ("bullet", "\u201cAssume this is the **first time** we are entering [province]. No existing relationship. How do you push yourself into the room?\u201d"),
    ("bullet", "\u201cHow do you get access when you are **outside** these structures rather than inside them?\u201d"),
    ("bullet", "\u201cHow do you turn somebody you merely know into somebody who gives you access?\u201d"),
    ("bullet", "The cold call, live: \u201cI have the secretary\u2019s number and no relationship. **Call him.** How does that conversation go?\u201d"),

    ("h2", "Relationship durability \u2014 the portability trap"),
    ("bullet", "**[3/3]** \u201cCould you go back to any organisation from the last five or six years, pick up a contact, and convert that capital today?\u201d"),
    ("bullet", "\u201cWould **all** of them pick up your call \u2014 or only some? Which ones, and why?\u201d"),
    ("bullet", "\u201cIs that true of every organisation you have worked with \u2014 or is [current employer] special because you were there so long?\u201d"),
    ("bullet", "\u201cGive me an example of a **cold open** with someone influential, whom you then sustained, and could comfortably call today.\u201d"),

    ("h2", "Skill transfer and funnel ownership"),
    ("bullet", "\u201cYour experience is [donor / NGO / private]. How does that translate to government \u2014 and **it doesn\u2019t have to be a work example**; navigating bureaucracy in your own life counts.\u201d"),
    ("bullet", "\u201cHave you taken something from **unfunded to funded** \u2014 or were you supporting a team that did?\u201d"),
    ("bullet", "\u201cHave you moved a free pilot or proof of concept into a converted, paid deal?\u201d"),
    ("bullet", "If the honest answer is no: widen the credit to any leverage they created, and note whether they invented an example instead."),

    ("h2", "Escalating scenarios \u2014 use real, current Taleemabad situations"),
    ("bullet", "**The blocked pilot (PECTA):** approval authority withdrawn mid-deal, the decision-maker ghosting, the political layer unreachable. What now?"),
    ("bullet", "**The renewal squeeze:** one month of payroll left, 50 jobs on the line, a no-cost extension no longer viable, and they won\u2019t say what changed. Then: \u201creally, what would you do \u2014 what does the day look like?\u201d"),
    ("bullet", "**The three-way partnership:** the government wants it but has no money. Bring a funder in without losing the government\u2019s ownership."),
    ("bullet", "**The category refusal:** \u201cwe don\u2019t want AI, we want teacher training \u2014 end of story.\u201d Sell the same product inside their vocabulary."),
    ("bullet", "**The messy-impact pitch:** our own evidence has gaps \u2014 internet shutdowns, security, partial districts. Pitch anyway, honestly."),
    ("bullet", "**The convening:** 60 days, no budget line, and you must fill the room with secretaries and development partners. Who do you call first, and why not the top?"),

    ("h2", "Role-play \u2014 how to run it the way she does"),
    ("num", "Give the product and the deal history in full **before** starting \u2014 and if they don\u2019t know the product, stop and teach them."),
    ("num", "Name the counterpart, their disposition, and their real constraint (\u201cintelligent and keen, but knows Sindh has no resources\u201d)."),
    ("num", "Constrain the scene: ten minutes, mid-meeting, others in the room."),
    ("num", "Offer prep time \u2014 one to three minutes \u2014 and let them ask clarifying questions first."),
    ("num", "Play the counterpart **irritated, not neutral**. Hostility is the baseline."),
    ("num", "Escalate the objections in order: accountability, then budget cannibalisation, then scale."),
    ("num", "Correct third-person narration immediately: \u201ctalk to me, not about them.\u201d"),
    ("num", "Close it explicitly, thank them, and acknowledge it is an unconventional ask."),

    ("h2", "Integrity gate \u2014 ask, then disclose"),
    ("bullet", "**[3/3]** \u201cYou have the green light, but they want 1\u20133% of the contract in someone\u2019s pocket. How do you manage that conversation?\u201d"),
    ("bullet", "Separate hospitality from corruption yourself, so they cannot hide in the ambiguity: \u201cwhen I say bribe, I mean 3% of the entire project cost \u2014 high-level bribes.\u201d"),
    ("bullet", "Probe the answer once: \u201cso if your organisation green-lit it, you\u2019d go ahead?\u201d"),
    ("bullet", "**Only then** state the Taleemabad position: hospitality is acceptable; skimming is not, and we walk away from the money rather than pay."),

    ("h2", "Close"),
    ("bullet", "**[2/3]** \u201cIs there anything I should know or take into consideration before I make this decision?\u201d \u2014 she describes it as something she asks every candidate."),
    ("bullet", "Fit-not-capability: \u201chow do you feel about the fact that we don\u2019t work with the private sector at all?\u201d"),
    ("bullet", "Invite questions about her, the work and the organisation \u2014 and answer candidly, including strategy and geography."),

    ("pagebreak",),

    # ============================================================ OBSERVATIONS
    ("part", "PART 4 \u2014 Observations & Open Questions for Ayesha"),
    ("para", "Offered as things worth a conversation, not defects. The three-transcript comparison makes a few inconsistencies visible that a single call would not."),

    ("h2", "1. The ethics gate is inconsistently placed and inconsistently closed"),
    ("para", "It landed at 18:50 for Salman (early), 42:09 for Waqas (mid), and 1:14:27 for Ahmad (effectively the final substantive question). More importantly, **Taleemabad\u2019s own position was stated only to Ahmad.** Salman and Waqas left the call without being told where the company stands \u2014 and Waqas is the one who said he would defer to his organisation and \u201cmight do it\u201d if they wanted the deal badly enough. For a hard gate, recommend fixing both: same placement every time, and always close by stating the company position after the answer."),

    ("h2", "2. Two of three candidates said the case study is mislabelled"),
    ("para", "Waqas, unprompted in his first minute: \u201cI didn\u2019t complete [it] in like 2.5 hours.\u201d Salman, as direct feedback at the end: \u201calthough it mentioned 2.5 [hours], but it\u2019s not 2.5. This is my first feedback.\u201d Ahmad said he did it in 15\u201316 hours. Independent agreement from three candidates that the stated time-box is wrong \u2014 worth re-timing the exercise or re-labelling it, since an understated time-box quietly filters for people with slack in their week rather than for ability."),

    ("h2", "3. She praises in-flight, and often before the follow-up"),
    ("para", "\u201cI think that\u2019s a great answer\u201d, \u201cthat was a very holistic answer\u201d, \u201cimpressive\u201d, \u201cvery good\u201d \u2014 warm, and clearly effective at keeping candidates open, which is a real asset. The trade-off is anchoring: a candidate just told an answer was great will read the next question as a friendly one, and a written scorecard produced after that much verbal endorsement is hard to keep independent. Worth a team decision on whether praise is held to the end."),

    ("h2", "4. She sometimes supplies the answer inside the question"),
    ("para", "\u201cAnd I\u2019m sure you know this, so what do you do?\u201d (Ahmad); the full Balochistan translation example (Salman); the \u201c15 cups of tea, leave your pride at home\u201d endorsement (Waqas, delivered **before** he had fully answered). Generous, and it keeps the conversation moving \u2014 but a candidate who then reproduces it should not be scored as though they generated it."),

    ("h2", "5. Coverage of the JD is uneven across candidates"),
    ("para", "Convening design was pressure-tested only with Waqas; commercial free-to-paid conversion only with Salman; conflict-of-interest only with Ahmad. Each debrief is excellent on access, persuasion and ethics, but the three candidates were not asked the same set beyond the fixed core. If these three are being compared against each other for the same role, the differences in coverage are worth noting before the decision \u2014 a fixed spine plus deliberate probes would make the comparison cleaner."),

    ("h2", "6. What she does not do"),
    ("bullet", "No chronological CV walk-through \u2014 she probes **patterns** in a career, not stops on it."),
    ("bullet", "No domain quizzing on education, pedagogy or AI \u2014 she supplies that knowledge herself."),
    ("bullet", "No generic behavioural set (\u201cgreatest weakness\u201d, \u201ctell me about a conflict\u201d)."),
    ("bullet", "No abstract brainteasers \u2014 every hypothetical is a real Taleemabad situation."),
    ("bullet", "No logistics in any captured portion \u2014 no salary, notice period or availability. Worth confirming who owns those."),

    ("rule",),
    ("h1", "One-line takeaway"),
    ("callout", [
        ("plain", "**Zeest interviews for one thing and dresses it in six costumes:** can you get into the room, and once you are in it, can you make someone whose incentives differ from ours decide to act in our favour \u2014 without lying, without paying, and without needing a relationship you already had."),
    ], "3C78D8"),

    ("footer", "Internal document \u2014 Taleemabad People & Culture. Built from three Fathom transcripts, all truncated before the end of the call; speaker labels in the Waqas transcript are inverted in places and attribution here is by content."),
]


# ------------------------------------------------------------------ markdown
def to_markdown(spec):
    out = []
    for item in spec:
        k = item[0]
        t = item[1] if len(item) > 1 else ""
        if k == "title":
            out.append(f"# {t}\n")
        elif k == "subtitle":
            out.append(f"## {t}\n")
        elif k == "meta":
            out.append(f"{t}  ")
        elif k == "part":
            out.append(f"\n---\n\n# {t}\n")
        elif k == "h1":
            out.append(f"\n## {t}\n")
        elif k == "h2":
            out.append(f"\n### {t}\n")
        elif k == "banner":
            tag = f" *({item[2]})*" if len(item) > 2 and item[2] else ""
            out.append(f"\n### {t}{tag}\n")
        elif k in ("h3", "h3u"):
            out.append(f"\n**{t}**\n")
        elif k == "para":
            out.append(f"{t}\n")
        elif k == "caption":
            out.append(f"*{t}*\n")
        elif k == "bullet":
            out.append(f"- {t}")
        elif k == "bullet2":
            out.append(f"  - {t}")
        elif k == "num":
            out.append(f"1. {t}")
        elif k == "footer":
            out.append(f"\n*{t}*")
        elif k == "rule":
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

docx_path = os.path.join(OUTDIR, "How_Zeest_Interviews.docx")
build(SPEC, docx_path, footer_note="Internal \u2014 Taleemabad People & Culture")

with open(MD_PATH, "w", encoding="utf-8") as fh:
    fh.write(to_markdown(SPEC))
print("built", MD_PATH)

if os.environ.get("UPLOAD") == "1":
    upload_as_gdoc(
        docx_path,
        "How Zeest Interviews \u2014 Question Patterns & Emphases (Growth Manager debriefs)",
        file_id=GDOC_ID)
