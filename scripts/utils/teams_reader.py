"""
Teams Reader Utility — Coco
Reads messages from any Teams channel via Microsoft Graph API.
Primary use: pull attendance updates from Mission Comms >> Presence channel.
"""
import os, re, requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../..", ".env"))

TENANT_ID   = os.getenv("TEAMS_TENANT_ID")
CLIENT_ID   = os.getenv("TEAMS_CLIENT_ID")
CLIENT_SECRET = os.getenv("TEAMS_CLIENT_SECRET")

# Known team IDs
TEAMS = {
    "Mission Comms":     "42ce5295-ec94-40a7-9add-329149194606",
    "People & Culture":  "075f9f43-c47d-44af-b57f-fac35bf2b0ab",
    "HR & Line":         "70853034-7fea-43e0-ad78-298b9771e1f3",
    "Accounts, Admin and HR": "9a69b50b-5e27-476d-a052-b157b1f3e369",
    "All":               "66b12496-e497-4995-bca0-a06349dafd94",
    "Orenda":            "c481dc08-d165-4f2f-8ffd-0fb3ee7d312d",
}

# Presence channel (Mission Comms)
PRESENCE_TEAM    = "42ce5295-ec94-40a7-9add-329149194606"
PRESENCE_CHANNEL = "19:e5de2b6946724b01b40b16df66767556@thread.tacv2"


def get_token():
    r = requests.post(
        f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token",
        data={
            "grant_type":    "client_credentials",
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope":         "https://graph.microsoft.com/.default",
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def clean_html(text):
    """Strip HTML tags and normalise whitespace."""
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    return re.sub(r"\s+", " ", text).strip()


def get_channel_messages(team_id, channel_id, since_hours=24, token=None):
    """Return list of {sender, text, timestamp} from a channel."""
    token = token or get_token()
    headers = {"Authorization": f"Bearer {token}"}
    cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)

    url = (f"https://graph.microsoft.com/v1.0/teams/{team_id}"
           f"/channels/{channel_id}/messages?$top=50")
    messages = []
    while url:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            break
        data = r.json()
        for m in data.get("value", []):
            ts_str = m.get("createdDateTime", "")
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except Exception:
                continue
            if ts < cutoff:
                url = None  # stop paging, messages are older
                break
            sender = (m.get("from") or {}).get("user", {}).get("displayName", "Unknown")
            body   = clean_html(m.get("body", {}).get("content", ""))
            if body and m.get("messageType") == "message":
                messages.append({"sender": sender, "text": body, "timestamp": ts})
        else:
            url = data.get("@odata.nextLink")
            continue
        break

    return messages


def get_all_channels(token=None):
    """Return dict: {team_name: [{id, name}]} for all teams."""
    token = token or get_token()
    headers = {"Authorization": f"Bearer {token}"}
    teams = requests.get("https://graph.microsoft.com/v1.0/teams",
                         headers=headers, timeout=15).json().get("value", [])
    result = {}
    for team in teams:
        tid   = team["id"]
        tname = team["displayName"]
        ch    = requests.get(f"https://graph.microsoft.com/v1.0/teams/{tid}/channels",
                             headers=headers, timeout=15)
        if ch.status_code == 200:
            result[tname] = [{"id": c["id"], "name": c["displayName"]}
                             for c in ch.json().get("value", [])]
    return result


def get_presence_updates(since_hours=24):
    """
    Pull today's Presence channel messages and return raw list.
    Main entry point for attendance report.
    """
    token = get_token()
    msgs  = get_channel_messages(PRESENCE_TEAM, PRESENCE_CHANNEL,
                                 since_hours=since_hours, token=token)
    return msgs


def search_channel(team_name, channel_name, since_hours=24):
    """Convenience: read any channel by team name + channel name."""
    token    = get_token()
    headers  = {"Authorization": f"Bearer {token}"}
    team_id  = TEAMS.get(team_name)
    if not team_id:
        # Search dynamically
        teams = requests.get("https://graph.microsoft.com/v1.0/teams",
                             headers=headers, timeout=15).json().get("value", [])
        for t in teams:
            if t["displayName"].lower() == team_name.lower():
                team_id = t["id"]
                break
    if not team_id:
        raise ValueError(f"Team not found: {team_name}")

    channels = requests.get(f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels",
                            headers=headers, timeout=15).json().get("value", [])
    channel_id = None
    for c in channels:
        if c["displayName"].lower() == channel_name.lower():
            channel_id = c["id"]
            break
    if not channel_id:
        raise ValueError(f"Channel not found: {channel_name} in {team_name}")

    return get_channel_messages(team_id, channel_id, since_hours=since_hours, token=token)


if __name__ == "__main__":
    print("=== Presence Channel — Last 24h ===")
    updates = get_presence_updates(since_hours=24)
    if not updates:
        print("No messages found.")
    for m in updates:
        ts = m["timestamp"].strftime("%H:%M")
        print(f"[{ts}] {m['sender']}: {m['text']}")
