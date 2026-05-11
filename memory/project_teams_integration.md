---
name: Teams Integration — Microsoft Graph API
description: Coco can read all Teams channels via Graph API. Presence channel is primary source for attendance updates. Chat/DMs not accessible (app-only limitation).
type: project
---

Teams reading via Microsoft Graph API set up 2026-04-08.

**Why:** Automate attendance data collection — instead of Ayesha manually copying Teams updates, Coco reads the Presence channel directly and populates the attendance report.

**How to apply:**
- Reader utility: `scripts/utils/teams_reader.py`
- Entry point for attendance: `get_presence_updates(since_hours=24)`
- Read any channel: `search_channel(team_name, channel_name, since_hours=24)`
- Credentials in `.env`: `TEAMS_TENANT_ID`, `TEAMS_CLIENT_ID`, `TEAMS_CLIENT_SECRET`
- Azure app: "Coco" — Client ID `e48c927b-a021-43d0-ac47-e1c2060805a1`, Tenant `629ab41b-cec2-46db-8bb5-7596d8a9243a`
- Secret expires: 4/7/2028

**Permissions granted (Application):**
- `ChannelMessage.Read.All`
- `Team.ReadBasic.All`
- `Channel.ReadBasic.All`
- `Chat.Read.All`
- `Chat.ReadBasic.All`
- `ChatMessage.Read.All`

**Key channel:**
- Team: Mission Comms (`42ce5295-ec94-40a7-9add-329149194606`)
- Channel: Presence (`19:e5de2b6946724b01b40b16df66767556@thread.tacv2`)
- People post WFH, leave, late arrivals here each morning

**Limitation:** Private 1:1 chats and group DMs cannot be read with app-only auth (Microsoft restriction). Workaround: service account with delegated auth — pending decision.

**Next step (confirmed for tomorrow):** Wire `get_presence_updates()` into `attendance_8apr2026.py` so PARTIAL/ON_LEAVE/WFH lists are auto-populated from Presence instead of manual entry.
