"""
Standards and Evals Tracker - formatting pass (Sabeena Abbasi's sheet, Ayesha is an editor)

Spreadsheet: 1gF5-Ng7iNbFtS0SVSZ83bFxEDIZGvJpA6_PI1aU7mXY  "Standards and Evals Tracker"
Owner: sabeena.abbasi@taleemabad.com   Editor used here: ayesha.khan@taleemabad.com

FORMATTING ONLY. This script never writes a cell value and never adds, deletes or moves a
row or column. The tracker's content belongs to Sabeena's team; we only make it readable.
Per memory/pnc_buddy_tracker_project_2026_08_19.md a tracker is a task list, not a
write-up, so this stays quiet: no full grid, no colour coding, no added columns.

Layout it produces:
  A Goals (goal named once per block, blank beneath) | B Owner | C+ one column per fortnight
  - header row: deep blue band, white bold, frozen
  - frozen A:B so the goal and owner stay put as fortnight columns are added rightward
  - body top-aligned and wrapped (the fortnight cells are multi-line paragraphs)
  - gridlines ON, every row and column reading as its own cell
  - a slightly stronger rule above each goal block, as a separator only

🔴 CORRECTION 2026-09-08 (Ayesha, first pass): the first version hid the gridlines and gave
each goal block one continuous background tint. Ayesha read that as Unsa+Momna and
Sameer+Ahwaz having been MERGED - one shaded area with no line between the two owner rows
looks like a merged cell, even though nothing was merged and no value was touched. Her
instruction: "keep the option of columns and rows". So: gridlines stay ON and there is no
block tint. Row separation beats prettiness on a sheet other people type into.

Usage:
  python scripts/pnc/beautify_standards_evals_tracker.py --dry-run
  python scripts/pnc/beautify_standards_evals_tracker.py
  python scripts/pnc/beautify_standards_evals_tracker.py --revert   # back to plain defaults

Token: .claude/config/token_sheets_broad.json  (Ayesha's own OAuth user token)
"""

import argparse
import json
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = '.claude/config/token_sheets_broad.json'
SSID = '1gF5-Ng7iNbFtS0SVSZ83bFxEDIZGvJpA6_PI1aU7mXY'
EXPECTED_TITLE = 'Standards and Evals Tracker'
TAB = 'Sheet1'

# ---- palette -------------------------------------------------------------------
HEADER_BG = {'red': 0.184, 'green': 0.310, 'blue': 0.635}    # #2F4FA2 Taleemabad accent
WHITE = {'red': 1.0, 'green': 1.0, 'blue': 1.0}
# BLOCK_TINT deliberately removed 2026-09-08: a shared block background read as a merged cell.
RULE = {'red': 0.780, 'green': 0.804, 'blue': 0.851}         # #C7CDD9
GOAL_TEXT = {'red': 0.122, 'green': 0.169, 'blue': 0.271}    # #1F2B45
BODY_TEXT = {'red': 0.129, 'green': 0.145, 'blue': 0.161}    # #212528

# ---- original state, captured before the first run, for --revert ---------------
ORIG_WIDTHS = {0: 129, 1: 100, 2: 173}
ORIG_ROW_H = 21

FIRST_DATA_COL = 2          # column C: first fortnight column

# Body rows are deliberately left WITHOUT an explicit pixelSize. Sheets stores the default
# 21 in rowMetadata and auto-fits wrapped content at render time, so setting any explicit
# height (even a generous floor) freezes the row and clips the fortnight paragraph. The
# first run of this script did exactly that and had to be undone. Only the header row
# gets a fixed height.


def creds():
    info = json.load(open(TOKEN_FILE))
    c = Credentials.from_authorized_user_info(info, info.get('scopes'))
    if not c.valid:
        c.refresh(Request())
    return c


def read_shape(svc):
    """Return (sheet_id, rows_used, cols_used, block_start_rows, values)."""
    meta = svc.spreadsheets().get(spreadsheetId=SSID).execute()
    if meta['properties']['title'] != EXPECTED_TITLE:
        sys.exit('ABORT: expected %r, found %r'
                 % (EXPECTED_TITLE, meta['properties']['title']))
    sheet = next((s for s in meta['sheets'] if s['properties']['title'] == TAB), None)
    if sheet is None:
        sys.exit('ABORT: no tab named %r' % TAB)
    sid = sheet['properties']['sheetId']

    vals = svc.spreadsheets().values().get(
        spreadsheetId=SSID, range=TAB, valueRenderOption='FORMATTED_VALUE'
    ).execute().get('values', [])
    if not vals:
        sys.exit('ABORT: sheet is empty, nothing to format')

    n_rows = len(vals)
    n_cols = max(len(r) for r in vals)
    # a block starts on any row below the header whose column A is non-blank
    blocks = [i for i, r in enumerate(vals) if i > 0 and r and r[0].strip()]
    if not blocks:
        sys.exit('ABORT: no goal blocks found in column A, layout assumption is wrong')
    return sid, n_rows, n_cols, blocks, vals


def build_requests(sid, n_rows, n_cols, blocks):
    """Grid coords are 0-based, end-exclusive."""
    reqs = []
    wide = max(n_cols, 3)

    def rng(r0, r1, c0, c1):
        return {'sheetId': sid, 'startRowIndex': r0, 'endRowIndex': r1,
                'startColumnIndex': c0, 'endColumnIndex': c1}

    # 1. freeze the header row + Goals/Owner. Gridlines stay ON - see CORRECTION above.
    reqs.append({'updateSheetProperties': {
        'properties': {'sheetId': sid,
                       'gridProperties': {'frozenRowCount': 1, 'frozenColumnCount': 2,
                                          'hideGridlines': False}},
        'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount,'
                  'gridProperties.hideGridlines'}})

    # 2. column widths
    for idx, px in ((0, 200), (1, 130)):
        reqs.append({'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS',
                      'startIndex': idx, 'endIndex': idx + 1},
            'properties': {'pixelSize': px}, 'fields': 'pixelSize'}})
    if n_cols > FIRST_DATA_COL:                      # every fortnight column
        reqs.append({'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS',
                      'startIndex': FIRST_DATA_COL, 'endIndex': n_cols},
            'properties': {'pixelSize': 470}, 'fields': 'pixelSize'}})

    # 3. body base format: wrapped, top-aligned, a little breathing room.
    #    Extends past the used range so newly typed rows inherit the look.
    reqs.append({'repeatCell': {
        'range': rng(1, max(n_rows, 40), 0, wide),
        'cell': {'userEnteredFormat': {
            'wrapStrategy': 'WRAP', 'verticalAlignment': 'TOP',
            'horizontalAlignment': 'LEFT',
            'backgroundColorStyle': {'rgbColor': WHITE},
            'padding': {'top': 6, 'right': 10, 'bottom': 6, 'left': 10},
            'textFormat': {'fontFamily': 'Arial', 'fontSize': 10, 'bold': False,
                           'foregroundColorStyle': {'rgbColor': BODY_TEXT}},
            'borders': {}}},
        'fields': 'userEnteredFormat(wrapStrategy,verticalAlignment,horizontalAlignment,'
                  'backgroundColorStyle,padding,textFormat,borders)'}})

    # 4. NO block tint. A shared background across an owner pair reads as a merged cell;
    #    the block is shown by the rule in step 6 and by the goal name in column A alone.

    # 5. the goal name in column A: bold, dark navy
    for start in blocks:
        reqs.append({'repeatCell': {
            'range': rng(start, start + 1, 0, 1),
            'cell': {'userEnteredFormat': {'textFormat': {
                'fontFamily': 'Arial', 'fontSize': 10, 'bold': True,
                'foregroundColorStyle': {'rgbColor': GOAL_TEXT}}}},
            'fields': 'userEnteredFormat.textFormat'}})

    # 6. one rule above each goal block, and one under the last row to close the table.
    #    Medium weight so it reads as a separator against the ordinary gridlines.
    for start in blocks:
        reqs.append({'updateBorders': {
            'range': rng(start, start + 1, 0, wide),
            'top': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': RULE}}}})
    reqs.append({'updateBorders': {
        'range': rng(n_rows - 1, n_rows, 0, wide),
        'bottom': {'style': 'SOLID_MEDIUM', 'colorStyle': {'rgbColor': RULE}}}})

    # 7. header band
    reqs.append({'repeatCell': {
        'range': rng(0, 1, 0, wide),
        'cell': {'userEnteredFormat': {
            'backgroundColorStyle': {'rgbColor': HEADER_BG},
            'horizontalAlignment': 'LEFT', 'verticalAlignment': 'MIDDLE',
            'wrapStrategy': 'WRAP',
            'padding': {'top': 6, 'right': 10, 'bottom': 6, 'left': 10},
            'textFormat': {'fontFamily': 'Arial', 'fontSize': 11, 'bold': True,
                           'foregroundColorStyle': {'rgbColor': WHITE}}}},
        'fields': 'userEnteredFormat(backgroundColorStyle,horizontalAlignment,'
                  'verticalAlignment,wrapStrategy,padding,textFormat)'}})
    if n_cols > FIRST_DATA_COL:      # centre the fortnight date-range headers
        reqs.append({'repeatCell': {
            'range': rng(0, 1, FIRST_DATA_COL, n_cols),
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER'}},
            'fields': 'userEnteredFormat.horizontalAlignment'}})
    reqs.append({'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
        'properties': {'pixelSize': 40}, 'fields': 'pixelSize'}})

    # 8. let the wrapped paragraphs decide their own row height
    reqs.append({'autoResizeDimensions': {'dimensions': {
        'sheetId': sid, 'dimension': 'ROWS', 'startIndex': 1, 'endIndex': n_rows}}})

    return reqs


def report_row_heights(svc, n_rows):
    """Read back the stored heights. 21 here means 'auto-fit', which is what we want."""
    meta = svc.spreadsheets().get(
        spreadsheetId=SSID, ranges=['%s!A1:A%d' % (TAB, n_rows)], includeGridData=True,
        fields='sheets(data(rowMetadata(pixelSize)))').execute()
    return [r.get('pixelSize') for r in meta['sheets'][0]['data'][0]['rowMetadata']]


def revert_requests(sid, n_rows, n_cols):
    """Put the sheet back to Google's plain defaults, as it was on 2026-09-08."""
    wide = max(n_cols, 4)
    reqs = [{'updateSheetProperties': {
        'properties': {'sheetId': sid,
                       'gridProperties': {'frozenRowCount': 0, 'frozenColumnCount': 0,
                                          'hideGridlines': False}},
        'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount,'
                  'gridProperties.hideGridlines'}}]
    for idx, px in ORIG_WIDTHS.items():
        reqs.append({'updateDimensionProperties': {
            'range': {'sheetId': sid, 'dimension': 'COLUMNS',
                      'startIndex': idx, 'endIndex': idx + 1},
            'properties': {'pixelSize': px}, 'fields': 'pixelSize'}})
    reqs.append({'updateDimensionProperties': {
        'range': {'sheetId': sid, 'dimension': 'ROWS', 'startIndex': 0,
                  'endIndex': max(n_rows, 40)},
        'properties': {'pixelSize': ORIG_ROW_H}, 'fields': 'pixelSize'}})
    reqs.append({'repeatCell': {
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': max(n_rows, 40),
                  'startColumnIndex': 0, 'endColumnIndex': wide},
        'cell': {'userEnteredFormat': {
            'wrapStrategy': 'WRAP', 'verticalAlignment': 'BOTTOM',
            'horizontalAlignment': 'LEFT',
            'backgroundColorStyle': {'rgbColor': WHITE},
            'padding': {'top': 2, 'right': 3, 'bottom': 2, 'left': 3},
            'textFormat': {'fontFamily': 'Arial', 'fontSize': 10, 'bold': False},
            'borders': {}}},
        'fields': 'userEnteredFormat(wrapStrategy,verticalAlignment,horizontalAlignment,'
                  'backgroundColorStyle,padding,textFormat,borders)'}})
    reqs.append({'repeatCell': {           # A1 was the one bold cell
        'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': 1,
                  'startColumnIndex': 0, 'endColumnIndex': 1},
        'cell': {'userEnteredFormat': {'textFormat': {
            'fontFamily': 'Arial', 'fontSize': 10, 'bold': True}}},
        'fields': 'userEnteredFormat.textFormat'}})
    return reqs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--revert', action='store_true')
    a = ap.parse_args()

    svc = build('sheets', 'v4', credentials=creds())
    sid, n_rows, n_cols, blocks, vals = read_shape(svc)

    print('sheet %r / tab %r (sheetId %s)' % (EXPECTED_TITLE, TAB, sid))
    print('  used range: %d rows x %d cols' % (n_rows, n_cols))
    print('  goal blocks start on rows: %s' % [b + 1 for b in blocks])
    for i, r in enumerate(vals, start=1):
        first = (r[0] if r else '')[:28]
        owner = (r[1] if len(r) > 1 else '')[:14]
        body = (r[2] if len(r) > 2 else '')
        print('  R%d: A=%-32r B=%-16r C=%d chars' % (i, first, owner, len(body)))

    reqs = revert_requests(sid, n_rows, n_cols) if a.revert \
        else build_requests(sid, n_rows, n_cols, blocks)

    print('\n%s: %d requests' % ('REVERT' if a.revert else 'FORMAT', len(reqs)))
    if a.dry_run:
        print('--dry-run, nothing written')
        return

    svc.spreadsheets().batchUpdate(
        spreadsheetId=SSID, body={'requests': reqs}).execute()
    print('  applied')

    if not a.revert:
        print('  stored row heights: %s  (21 = auto-fit, header is fixed at 40)'
              % report_row_heights(svc, n_rows))


if __name__ == '__main__':
    main()
