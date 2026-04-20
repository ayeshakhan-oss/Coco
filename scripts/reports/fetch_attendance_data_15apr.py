"""Fetch accurate attendance data for April 15, 2026 from Teams and Markaz"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

from scripts.utils.teams_reader import get_channel_messages, PRESENCE_TEAM, PRESENCE_CHANNEL

print("=" * 80)
print("FETCHING ATTENDANCE DATA FOR 15 APRIL 2026")
print("=" * 80)

# ────────────────────────────────────────────────────────────────────────────
# STEP 1: Markaz leaves on April 15 (from MCP query)
# ────────────────────────────────────────────────────────────────────────────
print("\n[STEP 1] Leaves approved for 2026-04-15 from Markaz:")

# Data from MCP query result
leaves_raw = [
    ("Iqra Arshad", "grant", "2026-03-31", "2026-04-29"),
    ("Mehwish Allah Ditta", "medical", "2026-03-15", "2026-06-15"),
    ("Muhammad Danish Iqbal", "grant", "2026-03-23", "2026-04-23"),
    ("Syeda Mehwish Ali", "grant", "2026-04-07", "2026-05-07"),
    ("Tariq Asim", "grant", "2026-03-31", "2026-04-29"),
]

on_leave_data = []
print(f"Found {len(leaves_raw)} approved leaves on 2026-04-15:")
for name, leave_type, start_date, end_date in leaves_raw:
    status = leave_type.replace('_', ' ').title()
    on_leave_data.append((name, status))
    print(f"  - {name}: {status} ({start_date} to {end_date})")

# ────────────────────────────────────────────────────────────────────────────
# STEP 2: Pull Teams Presence Channel (last 24h)
# ────────────────────────────────────────────────────────────────────────────
print("\n[STEP 2] Reading Teams Presence channel (last 24h)...")
teams_messages = []
try:
    messages = get_channel_messages(PRESENCE_TEAM, PRESENCE_CHANNEL, since_hours=24)
    print(f"Found {len(messages)} messages in last 24h:")
    for msg in messages:
        print(f"  [{msg['timestamp'].strftime('%H:%M')}] {msg['sender']}: {msg['text']}")
        teams_messages.append({
            'sender': msg['sender'],
            'text': msg['text'],
            'time': msg['timestamp']
        })
except Exception as e:
    print(f"ERROR reading Teams: {e}")

# ────────────────────────────────────────────────────────────────────────────
# STEP 3: Extract attendance updates from Teams messages
# ────────────────────────────────────────────────────────────────────────────
print("\n[STEP 3] Parsing Teams messages for attendance patterns...")

wfh_teams = []
arriving_late = []
out_sick = []

for msg in teams_messages:
    text = msg['text'].lower()
    sender = msg['sender']

    if any(x in text for x in ['wfh', 'work from home', 'working from home', 'remote']):
        wfh_teams.append((sender, msg['text']))
        print(f"  [WFH] {sender}: {msg['text']}")

    if any(x in text for x in ['arriving', 'late', 'coming at', 'will be there']):
        arriving_late.append((sender, msg['text']))
        print(f"  [ARRIVING] {sender}: {msg['text']}")

    if any(x in text for x in ['sick', 'unwell', 'not feeling', 'out sick']):
        out_sick.append((sender, msg['text']))
        print(f"  [SICK] {sender}: {msg['text']}")

# ────────────────────────────────────────────────────────────────────────────
# STEP 4: Summary Report
# ────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("SUMMARY FOR APRIL 15, 2026")
print("=" * 80)

print(f"\nON LEAVE (Markaz approved): {len(on_leave_data)}")
for name, status in on_leave_data:
    print(f"  • {name}: {status}")

print(f"\nWFH (Teams mentions): {len(wfh_teams)}")
for sender, text in wfh_teams:
    print(f"  • {sender}: {text}")

print(f"\nARRIVING LATE (Teams): {len(arriving_late)}")
for sender, text in arriving_late:
    print(f"  • {sender}: {text}")

print(f"\nOUT SICK (Teams): {len(out_sick)}")
for sender, text in out_sick:
    print(f"  • {sender}: {text}")

print("\n" + "=" * 80)
print(f"Total On Leave: {len(on_leave_data)}")
print(f"Total WFH (Teams): {len(wfh_teams)}")
print(f"Total Arriving Late: {len(arriving_late)}")
print(f"Total Out Sick: {len(out_sick)}")
print("=" * 80)
