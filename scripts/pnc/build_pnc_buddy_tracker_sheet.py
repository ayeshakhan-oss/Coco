"""
P&C Buddy Tracker Sheet - Google Sheet builder / updater

Spreadsheet "P&C Buddy Tracker Sheet" in Ayesha's own Drive, one tab per P&C Buddy
counterpart. First tab: "Sabeena".

  A Date | B Topic | C Task | D Owner | E Priority | F Done (checkbox)

TASK LIST ONLY. Ayesha iterated this down three times: one row per task with the topic
and minutes repeated was too much, paragraph minutes written once per block was still too
much, a one-line summary column was still too much. What she wants on the page is the
tasks. Topic is shown once per block for grouping and left blank on the rows beneath it.

The full unabridged minutes for each topic are kept as a HOVER NOTE on the topic cell, so
the meeting record survives at zero visual cost. Nothing else carries the minutes.

Ticking F strikes through and greys A:E for that row.

Source: Fathom transcript "Sabeena / Ayesha - September 04" plus Ayesha's own in-meeting
notes. The transcript is a lossy auto-transcript, so uncertain items are flagged with a
warning glyph rather than guessed (per memory/pnc_buddy_tracker_project_2026_08_19.md).

Usage:
  python scripts/pnc/build_pnc_buddy_tracker_sheet.py            # create (aborts if it exists)
  python scripts/pnc/build_pnc_buddy_tracker_sheet.py --update   # rewrite the Sabeena tab

Token: .claude/config/token_sheets_broad.json  (OAuth user token for ayesha.khan@)
"""

import json
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = '.claude/config/token_sheets_broad.json'
SHEET_NAME = 'P&C Buddy Tracker Sheet'
TAB_NAME = 'Sabeena'
KNOWN_SSID = '17eb8v55YQOKIiqpd3c2Bq6dDM8_6Wu9EzgsKh0WHr6w'
RECORDING = 'https://fathom.video/share/N2YRsTRkYFxjJXY8U8hEAz8b6sV2xbYd'
W = '⚠'

HEADERS = ['Date', 'Topic', 'Task', 'Owner', 'Priority', 'Done']

D = '2026-09-04'

# (topic, full minutes -> hover note on the topic cell, [(task, owner, priority), ...])
TOPICS = [
    ('Usman | team management',
     "Fundraising team has difficult dynamics and Usman is not yet equipped to manage them. "
     "Sabeena's framing to him: treat it as a challenge, not a reason to step back, because a "
     "manager has to learn techniques for handling difficult people. Team management is his "
     "biggest gap given he heads the team. Format for the sessions: listen to what he brings, "
     "then leave him one or two techniques to apply that week. Sabeena will review the plan and "
     "said Ayesha can pull in Zaheb if he can help.",
     [("One page coaching plan, team management first", 'Ayesha', 'CRITICAL'),
      ("Start weekly coaching sessions", 'Ayesha', 'CRITICAL'),
      ("Review the coaching plan", 'Sabeena', 'High'),
      (W + " Confirm the name (Zaheb or Zohaib) as coaching support", 'Ayesha', 'Medium')]),

    ('Usman | salary',
     "Usman is unhappy with his pay and has asked for a raise. Sabeena holds her performance "
     "feedback, which was not good, and is not changing it; what she is willing to explore is "
     "parity, since his salary sits far below the other department heads. Company policy sets "
     "increment percentages. Agreed sequence: Ayesha takes it to Dr Zeeshan first, including "
     "how the last increment was decided, then Sabeena joins a combined call. " + W +
     " She named at least 400 to 450, units not stated in the transcript.",
     [("Benchmark him against department head salary ranges", 'Ayesha', 'High'),
      ("Take the parity case to Dr Zeeshan", 'Ayesha', 'High'),
      ("Then a combined call with Sabeena and Zeeshan", 'Ayesha', 'High')]),

    ('Nawal | onsite and conduct',
     "Nawal is working to an expectation of remote or hybrid. Jawwad confirmed nothing concrete "
     "was committed at hiring; the standing rule is that the line manager approves work from "
     "home. Sabeena's brief for the conversation: polite but assertive, the onsite expectation "
     "comes from Haroon as CEO, proposals cannot be written without knowing what is happening "
     "in the organisation, meetings have to be attended, Slack off mute during working hours, "
     "and replies hours later are a red flag. Set a two week monitoring window and say plainly "
     "that a warning letter follows if nothing changes. Separately, Nawal complained about "
     "Usman without going to him first: everyone is accessible and there is no closed door "
     "policy, but the line manager is still answered and respected. " + W +
     " Passage badly garbled, the transcript switches between he and she and between Nawal "
     "and Namal. Nawal is on site, so this is an in person 1:1.",
     [("In person 1:1 on onsite, meetings, Slack, two week window", 'Ayesha', 'High'),
      ("Add the line manager expectation to the same 1:1", 'Ayesha', 'High')]),

    ('Ahwaz | resources and workload',
     "Ahwaz keeps saying in meetings that he did not know he had access to resources, and "
     "Sabeena wants that closed off: there is no restriction and he should ask openly, "
     "including for things like Claude credits running out. She also thinks he is overworked "
     "and does not flag it, having found out about problems by accident, and wants his plate "
     "checked twice a month. Ayesha already holds a weekly recurring with him, so it folds in. "
     "Sabeena named this one of her two critical asks.",
     [("Ask what resources he needs, confirm there is no restriction", 'Ayesha', 'High'),
      ("Check his plate, what to offload, what support he needs", 'Ayesha', 'CRITICAL')]),

    ('Standards and Evals | tracker and goals',
     "Sabeena's template, shared on screen: goals down the side with an owner against each, "
     "dates across the top, tracked weekly, one tab per two week sprint. Owners named were "
     "Momina, Sameer and Ahwaz. Goals must carry measurable metrics, an LP count target or a "
     "reduction in error rate, so that achievement is judged rather than argued. Ahwaz drafts "
     "his own sheet and Sabeena reviews it directly, so the goal setting session is not "
     "Ayesha's to run. " + W + " Momna Tariq in Standards and Evals and Momina in Impact and "
     "Policy may be two different people, confirm before sharing.",
     [("Build and maintain the tracker, share with the three owners", 'Ayesha', 'High'),
      ("Ask Ahwaz to draft his goals sheet for Sabeena", 'Ayesha', 'High'),
      ("Reinforce measurable goals with Muzzammil on Friday", 'Ayesha', 'Medium')]),

    ('Standards and Evals | clarity',
     "The team cannot see where they are headed and raise it in check ins. Sabeena reads Ahwaz "
     "as research minded and deeply expert, which breeds an assumption that others already "
     "follow, and people are reluctant to say that they do not. Her fix is the tracker plus a "
     "one pager on direction.",
     [("Write the direction and expectations one pager", 'Sabeena', 'High')]),

    ('Retros | planning',
     "Ayesha's suggestion in the meeting: a planning session before every retro, announced in "
     "the general group, concrete for the two weeks ahead on goals, targets and owners. "
     "Standards and Evals runs next week. The non sprint teams do not need a fortnightly cycle, "
     "so monthly or two monthly is enough for them.",
     [("Add a planning session before each retro, post in the general group",
       'Ayesha', 'Medium')]),

    ('Retro day | team showcase',
     "Sabeena wants the old cadence back: two to three hours in the first half of retro day "
     "where every team presents for five to ten minutes on what they are working on, with Q&A. "
     "Her reasoning is cross learning and visibility, which should cut the duplication and "
     "confusion between teams. " + W + " She mentioned Haroon and Osman Imtiaz, names partly "
     "garbled.",
     [("Share the proposal with Zeeshan", 'Ayesha', 'Medium'),
      ("Raise it with Haroon", 'Sabeena', 'Medium')]),

    ('Sameer | team overlaps',
     "Ayesha offered to hold Sameer if Sabeena needs him in her team. Sabeena spent a full day "
     "with Haroon mapping where her teams and Sameer's mandate overlap, where they can work "
     "together and where the domains are genuinely separate; her read is that the duplication "
     "comes from teams not knowing what the others are doing. She asked that P&C not approach "
     "team members directly about moves, because people see the shiny opportunity and get "
     "unsettled, and because not all of the work is shiny. This is a standing process point, "
     "not a one off. " + W + " Heavily garbled passage.",
     [("Route moves via Zeeshan and the leads, consent before the individual",
       'Ayesha', 'High')]),

    ('Hiring | pipeline',
     "Zeeshan will reach out to Ayesha. Sabeena wants an active pipeline ready with interviews "
     "already scheduled, because Nawal's team needs people. " + W + " The reference to Nawal "
     "having only a year is unclear.",
     [("Build the pipeline with interviews scheduled", 'Ayesha', 'High')]),

    ('Follow up',
     "Sabeena asked for the discussed items listed out after the call so they can be followed "
     "up. Her two critical ones are coaching Usman on team management, and understanding "
     "Ahwaz's plate and giving him more support. This tracker is that list.",
     [("Send Sabeena this list", 'Ayesha', 'CRITICAL')]),
]


def build_values():
    """Rows, plus (block first-row index, hover note) for each topic."""
    values = [HEADERS]
    blocks = []
    first = True
    for topic, note, tasks in TOPICS:
        blocks.append((len(values), note))
        for i, (task, owner, prio) in enumerate(tasks):
            if i == 0:
                date = ('=HYPERLINK("' + RECORDING + '","' + D + '")') if first else D
                values.append([date, topic, task, owner, prio, False])
                first = False
            else:
                values.append(['', '', task, owner, prio, False])
    return values, blocks


def format_requests(sid, last, blocks):
    tail = last + 60
    reqs = [
        {'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 1,
                      'startColumnIndex': 0, 'endColumnIndex': 6},
            'cell': {'userEnteredFormat': {
                'backgroundColor': {'red': 0.184, 'green': 0.310, 'blue': 0.635},
                'horizontalAlignment': 'LEFT', 'verticalAlignment': 'MIDDLE',
                'wrapStrategy': 'WRAP',
                'textFormat': {'bold': True, 'fontSize': 11,
                               'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}}},
            'fields': 'userEnteredFormat'}},
        {'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': tail,
                      'startColumnIndex': 0, 'endColumnIndex': 6},
            'cell': {'userEnteredFormat': {'wrapStrategy': 'WRAP', 'verticalAlignment': 'MIDDLE',
                                           'textFormat': {'fontSize': 10, 'bold': False}}},
            'fields': 'userEnteredFormat(wrapStrategy,verticalAlignment,textFormat)'}},
        {'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': tail,
                      'startColumnIndex': 3, 'endColumnIndex': 6},
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'}},
        {'updateSheetProperties': {
            'properties': {'sheetId': sid,
                           'gridProperties': {'frozenRowCount': 1, 'frozenColumnCount': 2}},
            'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'}},
        {'setDataValidation': {
            'range': {'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': tail,
                      'startColumnIndex': 5, 'endColumnIndex': 6},
            'rule': {'condition': {'type': 'BOOLEAN'}, 'showCustomUi': True}}},
        {'addConditionalFormatRule': {
            'index': 0,
            'rule': {'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': tail,
                                 'startColumnIndex': 0, 'endColumnIndex': 5}],
                     'booleanRule': {
                         'condition': {'type': 'CUSTOM_FORMULA',
                                       'values': [{'userEnteredValue': '=$F2=TRUE'}]},
                         'format': {'backgroundColor': {'red': 0.949, 'green': 0.957,
                                                        'blue': 0.965},
                                    'textFormat': {'strikethrough': True,
                                                   'foregroundColor': {'red': 0.55, 'green': 0.58,
                                                                       'blue': 0.62}}}}}}},
        {'addConditionalFormatRule': {
            'index': 1,
            'rule': {'ranges': [{'sheetId': sid, 'startRowIndex': 1, 'endRowIndex': tail,
                                 'startColumnIndex': 4, 'endColumnIndex': 5}],
                     'booleanRule': {
                         'condition': {'type': 'TEXT_EQ',
                                       'values': [{'userEnteredValue': 'CRITICAL'}]},
                         'format': {'backgroundColor': {'red': 0.988, 'green': 0.898,
                                                        'blue': 0.898},
                                    'textFormat': {'bold': True,
                                                   'foregroundColor': {'red': 0.667,
                                                                       'green': 0.106,
                                                                       'blue': 0.106}}}}}}},
    ]
    for idx, px in [(0, 86), (1, 208), (2, 420), (3, 82), (4, 86), (5, 56)]:
        reqs.append({'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS',
                      'startIndex': idx, 'endIndex': idx + 1},
            'properties': {'pixelSize': px}, 'fields': 'pixelSize'}})
    for r, note in blocks:
        reqs.append({'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': r, 'endRowIndex': r + 1,
                      'startColumnIndex': 1, 'endColumnIndex': 2},
            'cell': {'userEnteredFormat': {'textFormat': {'bold': True, 'fontSize': 10}}},
            'fields': 'userEnteredFormat.textFormat'}})
        reqs.append({'updateBorders': {
            'range': {'sheetId': sid, 'startRowIndex': r, 'endRowIndex': r + 1,
                      'startColumnIndex': 0, 'endColumnIndex': 6},
            'top': {'style': 'SOLID', 'width': 1,
                    'color': {'red': 0.62, 'green': 0.66, 'blue': 0.72}}}})
        # Full minutes kept as a hover note on the topic cell
        reqs.append({'updateCells': {
            'range': {'sheetId': sid, 'startRowIndex': r, 'endRowIndex': r + 1,
                      'startColumnIndex': 1, 'endColumnIndex': 2},
            'rows': [{'values': [{'note': note}]}], 'fields': 'note'}})
    return reqs


def main():
    update = '--update' in sys.argv

    with open(TOKEN_FILE) as f:
        creds = Credentials.from_authorized_user_info(json.load(f))
    if creds.expired:
        creds.refresh(Request())

    drive = build('drive', 'v3', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)

    values, blocks = build_values()

    if update:
        ssid = KNOWN_SSID
        ss = sheets.spreadsheets().get(spreadsheetId=ssid).execute()
        tab = [s for s in ss['sheets'] if s['properties']['title'] == TAB_NAME]
        if not tab:
            print("[ABORT] No tab named '" + TAB_NAME + "' in " + ssid)
            sys.exit(1)
        sid = tab[0]['properties']['sheetId']
        wipe = [{'updateCells': {
            'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 400,
                      'startColumnIndex': 0, 'endColumnIndex': 8},
            'fields': 'userEnteredValue,note'}}]
        wipe += [{'deleteConditionalFormatRule': {'sheetId': sid, 'index': 0}}
                 for _ in tab[0].get('conditionalFormats', [])]
        sheets.spreadsheets().batchUpdate(spreadsheetId=ssid,
                                          body={'requests': wipe}).execute()
        print('[OK] Cleared values and notes on tab ' + TAB_NAME)
    else:
        q = ("mimeType='application/vnd.google-apps.spreadsheet' and trashed=false "
             "and name='" + SHEET_NAME + "'")
        found = drive.files().list(q=q, fields='files(id,webViewLink)',
                                   pageSize=10).execute().get('files', [])
        if found:
            print("[EXISTS] already named '" + SHEET_NAME + "':")
            for f_ in found:
                print('         ' + f_['id'] + '  ' + f_['webViewLink'])
            print('[ABORT] Refusing to create a duplicate. Re-run with --update.')
            sys.exit(1)
        created = sheets.spreadsheets().create(body={
            'properties': {'title': SHEET_NAME},
            'sheets': [{'properties': {
                'title': TAB_NAME,
                'gridProperties': {'rowCount': len(values) + 80,
                                   'columnCount': len(HEADERS)}}}]}).execute()
        ssid = created['spreadsheetId']
        sid = created['sheets'][0]['properties']['sheetId']
        print('[OK] Created spreadsheet ' + ssid)

    sheets.spreadsheets().values().update(
        spreadsheetId=ssid, range=TAB_NAME + '!A1:F' + str(len(values)),
        valueInputOption='USER_ENTERED', body={'values': values}).execute()
    n_tasks = sum(len(t[2]) for t in TOPICS)
    print('[OK] Wrote ' + str(n_tasks) + ' tasks across ' + str(len(TOPICS)) + ' topics')

    sheets.spreadsheets().batchUpdate(
        spreadsheetId=ssid,
        body={'requests': format_requests(sid, len(values), blocks)}).execute()
    print('[OK] Applied checkboxes, rules, block borders and hover notes')

    print('\nSHEET ID : ' + ssid)
    print('URL      : https://docs.google.com/spreadsheets/d/' + ssid + '/edit')


if __name__ == '__main__':
    main()
