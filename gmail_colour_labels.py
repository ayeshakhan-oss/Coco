"""
Apply colours to Hiring sub-labels in Gmail.
"""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import time

creds   = Credentials.from_authorized_user_file("token_gmail.json")
service = build("gmail", "v1", credentials=creds)

# Gmail-supported color pairs (backgroundColor, textColor)
# Gmail's allowed palette only (exact hex values required)
COLORS = [
    {"backgroundColor": "#16a766", "textColor": "#ffffff"},  # green
    {"backgroundColor": "#a479e2", "textColor": "#ffffff"},  # purple
    {"backgroundColor": "#e66550", "textColor": "#ffffff"},  # red-orange
    {"backgroundColor": "#ffad47", "textColor": "#ffffff"},  # orange
    {"backgroundColor": "#4986e7", "textColor": "#ffffff"},  # blue
    {"backgroundColor": "#2da2bb", "textColor": "#ffffff"},  # teal
    {"backgroundColor": "#b99aff", "textColor": "#ffffff"},  # lavender
    {"backgroundColor": "#f691b3", "textColor": "#ffffff"},  # pink
    {"backgroundColor": "#c6f3de", "textColor": "#222222"},  # mint
    {"backgroundColor": "#fce8b3", "textColor": "#222222"},  # yellow
    {"backgroundColor": "#e4d7f5", "textColor": "#222222"},  # light purple
    {"backgroundColor": "#4a86e8", "textColor": "#ffffff"},  # blue
    {"backgroundColor": "#43d692", "textColor": "#ffffff"},  # light green
]

PARENT_COLOR = {"backgroundColor": "#16a766", "textColor": "#ffffff"}  # green for Hiring

def get_labels():
    results = service.users().labels().list(userId="me").execute()
    return results.get("labels", [])

def set_label_color(label_id, color):
    service.users().labels().patch(
        userId="me",
        id=label_id,
        body={"color": color}
    ).execute()

def main():
    labels = get_labels()

    # Colour the parent Hiring label
    hiring_label = next((l for l in labels if l["name"] == "Hiring"), None)
    if hiring_label:
        set_label_color(hiring_label["id"], PARENT_COLOR)
        print(f"  Coloured: Hiring (dark green)")
        time.sleep(0.2)

    # Colour each sub-label
    sub_labels = sorted(
        [l for l in labels if l["name"].startswith("Hiring/")],
        key=lambda x: x["name"]
    )

    for i, label in enumerate(sub_labels):
        color = COLORS[i % len(COLORS)]
        set_label_color(label["id"], color)
        print(f"  Coloured: {label['name']}")
        time.sleep(0.2)

    print(f"\nDone. {len(sub_labels) + 1} labels coloured.")

if __name__ == "__main__":
    main()
