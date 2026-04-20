"""Check Teams Presence channel for any missed leave/WFH messages"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

from scripts.utils.teams_reader import get_channel_messages, PRESENCE_TEAM, PRESENCE_CHANNEL

print("=" * 80)
print("TEAMS PRESENCE CHANNEL - LAST 24 HOURS (April 14-15)")
print("=" * 80)

try:
    messages = get_channel_messages(PRESENCE_TEAM, PRESENCE_CHANNEL, since_hours=24)
    print(f"\nTotal messages found: {len(messages)}\n")

    for msg in messages:
        print(f"[{msg['timestamp'].strftime('%Y-%m-%d %H:%M')}] {msg['sender']}")
        print(f"  Message: {msg['text']}")
        print()

except Exception as e:
    print(f"Error reading Teams: {e}")

print("=" * 80)
