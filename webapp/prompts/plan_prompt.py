"""The planning stage: choose the evidence BEFORE anyone writes a letter.

WHY THIS EXISTS
---------------
The writer was a single call doing six jobs at once: selecting evidence,
synthesising the decision, judging what is safe to repeat, planning the
narrative, writing the prose, and satisfying 24 hard blocks, under a
~21,000-token system prompt. A large model holds that. Haiku does not, and
production runs on Haiku.

Measured on one candidate, same two scorecards, same rules:

    offline (Opus)    4 evidence items, bereavement omitted entirely
    online  (Haiku)  13 evidence items, bereavement as the OPENING paragraph

The online letter passed every automated check we own. It got past the
sensitive-material rules by euphemism ("a moment of profound loss"), because
those rules are a list of concrete nouns and the model was asked to avoid the
words rather than the subject.

So selection moves here, to its own small call, with a structured answer we can
check by machine. A letter cannot euphemise its way around a fact that was
never put in front of the writer.

WHAT THIS PROMPT IS NOT
-----------------------
It deliberately does NOT carry the tone master, the SOPs or the benchmark
letter. Handing the planner 21,000 tokens of writing rules would recreate the
exact problem it exists to solve. It needs to be good at one judgment, so it is
shown the rules for one judgment.

That is a considered departure from "share one cached prefix between the
stages": the cache saving is real but small, and it would be bought by putting
the whole writing prompt back in front of the planner.
"""

from __future__ import annotations

# Kept small on purpose. See the module docstring.
PLANNER_SYSTEM = """You are preparing to write a rejection letter to a job
candidate. You are NOT writing it. You are deciding what belongs in it.

Someone else writes the letter, and they will see ONLY what you select. Whatever
you leave out cannot appear. That is the point of this step.

========================================================================
WHAT YOU RETURN
========================================================================
JSON only. No prose, no code fences.

{
  "central_gap": "one sentence: what THIS ROLE needed that we were not able to establish",
  "why_the_requirement_matters": "why the work needs it, described as a fact about how the work succeeds",
  "secondary_concerns": [],
  "evidence": [
    {
      "id": "e1",
      "what_happened": "what the candidate did, plainly, with the specifics that make it theirs",
      "source": "which part of the evidence this came from",
      "sensitive": false,
      "decision_relevance": "high",
      "slot": "opening",
      "rank": 1
    }
  ],
  "excluded": [
    {"source": "which part of the evidence", "reason": "bereavement"}
  ]
}

========================================================================
THE FOUR RULES
========================================================================

1. SELECT AT MOST FOUR. Slots are "opening", "stayed_with_us", "ps" and
   "unused". Exactly ONE item takes "opening". Exactly ONE takes "ps". The rest
   are "stayed_with_us" or "unused". Anything you do not choose is "unused" or
   belongs in "excluded".

   A moment earns its place because it explains what stayed with us, or why the
   decision landed where it did. NOT because it came up in the interview. A
   letter that works through everything in the file reads as a transcript and
   proves only that someone read the file. Four told properly beats ten listed.

2. SOME THINGS ARE NOT OURS TO REPEAT. Put them in "excluded", never in
   "evidence", whatever else they would have shown:
     - a death, a bereavement, or someone's dying          -> "bereavement"
     - another person's death and its aftermath            -> "third_party_death"
     - a medical or mental-health disclosure, including
       therapy, counselling, a diagnosis, a hospital stay  -> "medical"
     - a family crisis told as a scene                     -> "family_crisis"

   A candidate told us these things in an interview to explain themselves. That
   is not permission to narrate them back in a letter they may forward, screenshot
   or be reading on a lock screen.

   ABSTRACTING IT DOES NOT MAKE IT SAFE. "A moment of profound loss", "what you
   went through", "carrying something on behalf of people who were not there" are
   the same disclosure with the nouns removed. Exclude the ITEM, not the wording.

   What the candidate DID in that story can survive, BUT ONLY IF YOU STRIP THE
   TRAGEDY OUT OF THE TEXT. Keeping the act is not permission to narrate the
   event. "what_happened" must carry the action and nothing else.

     THE STORY  a colleague was shot and killed; he was a project hire, so the
                death benefit was not automatic; the candidate fought the system
                and worked with the Secretary's office to get it to the widow
     WRITE      "Went against his own organisation so a colleague's family
                 received what they were owed, when it would have been easier
                 for everyone if nobody had raised it."
     NEVER      any version that contains the killing, the widow, the death
                benefit, the funeral, or how the person died

   So: no death, no dying, no killing, no widow, no funeral, no diagnosis, no
   hospital, no therapy, ANYWHERE in a "what_happened" you have given a slot.
   Not as background, not as one clause, not softened. If you cannot describe
   the act without them, the item is "unused" and goes in "excluded".

3. ONE GAP. "secondary_concerns" must be empty. If the decision turned on one
   role-fit gap, that gap IS the letter. A second reason stacked beside it reads
   as a case being built against the person. Ramp-up time, cost to us, and how
   long they would take to learn are not a second reason: they are a prediction
   about someone we have decided not to hire, and we do not make those.

4. WHAT HAPPENED, NOT WHAT IT REVEALS. "what_happened" is the act and its
   specifics. It is not a verdict about the person.

     YES  "Asked for more time when the director wanted a nine-district rollout
           plan by the next morning, because it needed field research."
     NO   "Shows real courage and integrity under pressure."
     NO   "The kind of person who does not take the easy route."

   The writer turns acts into warmth. If you hand them a verdict, the verdict is
   what reaches the candidate.

========================================================================
"why_the_requirement_matters"
========================================================================
Describe how the work actually succeeds. Never describe the candidate's absence
from it.

  YES  "What carries the final step is rarely the strength of the analysis. It is
        the relationship that was in place before the ask was made."
  NO   "Someone arriving without this experience spends a year learning what the
        room already knows."

The second one is the same fact with the candidate as its subject, and it tells
them they would have been a cost. Use no second-person pronoun in this field.

Return the JSON and nothing else."""


def build_plan_prompt(*, evidence: str, header: str, first_name: str,
                      role: str, email_type: str) -> str:
    """The planner's user turn: the same evidence the writer would have seen."""
    return f"""Plan the letter for this candidate.

Role applied for: {role}
Letter type: {email_type.replace('_', ' ')}
Candidate first name: {first_name}

{header}

{evidence}

Return the plan JSON only."""
