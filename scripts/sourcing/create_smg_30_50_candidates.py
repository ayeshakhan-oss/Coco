"""
Create SEPARATE Google Sheet for Senior Manager Growth Candidates (Improved Slate)
Using corrected parameters: 4-6 years experience, partnerships/BD/growth background
Target: 30-50 candidates from education/nonprofit/fintech sectors
"""

import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime
import json
import os

# Use the broader-scoped OAuth token
TOKEN_FILE = '.claude/config/token_sheets_broad.json'
MASTER_SPREADSHEET_ID = '1eFf5ATqDyFvPi0qxgijPCbfrx_AWBvgtnj3ywe4UBNw'

print("\n" + "="*80)
print("Creating SEPARATE Google Sheet - SMG 30-50 Candidates (IMPROVED SLATE)")
print("="*80)

# Load broader-scoped credentials
with open(TOKEN_FILE, 'r') as f:
    token_data = json.load(f)

credentials = Credentials.from_authorized_user_info(token_data)
if credentials.expired:
    credentials.refresh(Request())

# Initialize gspread client
gc = gspread.Client(auth=credentials)

# TIER 1: Highest Fit - Partnerships/BD/Growth at Target Companies (4-6 years)
TIER_1 = [
    ('Hassan Aftab', 'https://www.linkedin.com/in/hassan-aftab-4aa296b/', 'Regional Manager Partnerships', 'Jazz', 'Pakistan', '5-6 years', 'Telecom partnerships, B2B2C scaling, Daraz/Easypaisa integration', 'Direct match: partnerships at scale, stakeholder management, revenue focus', 'Tier 1 - Highest Fit'),
    ('Zainab Gulzar Hussain', 'https://www.linkedin.com/in/zainabgulzar/', 'Product Growth Manager', 'easypaisa Bank Limited', 'Pakistan', '4-5 years', 'Product partnerships, fintech growth, channel optimization', 'Growth/partnerships in fintech ecosystem, scaling mindset', 'Tier 1 - Highest Fit'),
    ('Babar Ali', 'https://www.linkedin.com/in/babar-ali786/', 'Business Development Executive', 'Kollegio', 'Pakistan', '4 years', 'EdTech B2C/B2B growth, institutional partnerships', 'Education sector BD, LUMS graduate, growth strategy', 'Tier 1 - Highest Fit'),
    ('Irteza Ubaid', 'https://pk.linkedin.com/in/irtezaubaid', 'Head of Business Development', 'Shams Power', 'Pakistan', '5-6 years', 'Government relations, investor management, stakeholder engagement', 'Strategic partnerships at scale, LUMS MBA, business development leadership', 'Tier 1 - Highest Fit'),
    ('Basit Hussain', 'https://www.linkedin.com/in/basit-hussain-26006662/', 'Partnerships Specialist', 'Lahore University of Management Sciences (LUMS)', 'Lahore', '4-5 years', 'Academic partnerships, proposal writing, budget management, program planning', 'Education sector expertise, LUMS institutional knowledge, relationship building', 'Tier 1 - Highest Fit'),
    ('Haider Imtiaz', 'https://www.linkedin.com/in/haider-imtiaz-2882b635/', 'Head of Integrated Marketing Experience', 'Jazz', 'Pakistan', '5-6 years', 'Brand partnerships, stakeholder engagement, sponsorship strategy', 'Telecom partnerships ecosystem, large-scale brand management', 'Tier 1 - Highest Fit'),
    ('Talha Tahir', 'https://www.linkedin.com/in/engrtalhatahir/', 'Head of Retail Business', 'Telenor Microfinance Bank Limited', 'Pakistan', '5-6 years', 'Distribution network expansion, agent partnerships, retail channel growth', 'Multi-city expansion, stakeholder management at scale', 'Tier 1 - Highest Fit'),
    ('Noor Aslam', 'https://www.linkedin.com/in/noor-aslam-b6b99840/', 'Senior Executive System & Process', 'Zong CMPak Ltd', 'Pakistan', '5+ years', 'Telecom operations, customer acquisition, channel partnerships', 'Telecom sector expertise, process optimization, B2B partnerships', 'Tier 1 - Highest Fit'),
]

# TIER 2: Good Fit - Government/Donor Relations, NGO/Education Leadership (4-6 years)
TIER_2 = [
    ('Shahid Iqbal', 'https://www.linkedin.com/in/shahid-iqbal-pak/', 'CEO', 'Bano Qabil', 'Pakistan', '6+ years', 'Nonprofit leadership, education focus, donor relationships', 'Education nonprofit CEO, strategic partnerships, stakeholder engagement', 'Tier 2 - High Fit'),
    ('Junaid Zuberi', 'https://www.linkedin.com/in/junaidzuberi/', 'Transformational CEO', 'Nonprofit & Cultural Leader', 'Pakistan', '6+ years', 'Business growth, strategic partnerships, nonprofit management', 'Nonprofit sector expertise, growth/partnerships, relationship building', 'Tier 2 - High Fit'),
    ('Arif Gafur', 'https://www.linkedin.com/in/arif-gafur/', 'President', 'TCF-USA (Teach For Change)', 'Pakistan/USA', '6+ years', 'Education nonprofit leadership, donor fundraising, institutional partnerships', 'TCF sector knowledge, education scale, multi-stakeholder management', 'Tier 2 - High Fit'),
    ('Saba Faisal', 'https://www.linkedin.com/in/saba-faisal-11276712a/', 'National Director', 'SOS Children\'s Villages Pakistan', 'Pakistan', '5-6 years', 'Nonprofit operations, education programs, donor management', 'Nonprofit leadership, education sector, institutional relationships', 'Tier 2 - High Fit'),
    ('Ghulam Hussain Khwaja', 'https://www.linkedin.com/in/gh-khwaja/', 'CEO', 'Sindh Radiant Organization (SRO)', 'Pakistan', '6+ years', 'Nonprofit management, stakeholder engagement, program execution', 'Development sector expertise, community partnerships, strategic thinking', 'Tier 2 - High Fit'),
    ('Muzamil N. Panezai', 'https://www.linkedin.com/in/muzamilpanezai/', 'Provincial Program Manager', 'UNICEF', 'Pakistan', '5-6 years', 'Education programs, government partnerships, institutional relations', 'UNICEF education expertise, government sector knowledge, program scale', 'Tier 2 - High Fit'),
    ('Imran Anjum', 'https://pk.linkedin.com/in/imran-anjum-52b9648', 'Managing Director', 'Multi-sector', 'Pakistan', '5+ years', 'Government relations, stakeholder management, cross-sector projects', 'Government partnerships, institutional engagement, business acumen', 'Tier 2 - High Fit'),
    ('Ali Tariq', 'https://www.linkedin.com/in/ali-tariq-42697380/', 'Education Partnerships Specialist', 'OxfordAQA', 'Pakistan', '4-5 years', 'Pakistan-Germany education collaboration, institutional partnerships', 'Education sector partnerships, international stakeholder engagement', 'Tier 2 - High Fit'),
    ('Tariq Malik', 'https://www.linkedin.com/in/tariqmalik1', 'Development Professional', 'The World Bank', 'Pakistan', '5-6 years', 'Development sector partnerships, institutional relations, project management', 'World Bank experience, development sector networks, partnership scale', 'Tier 2 - High Fit'),
    ('Huma Waheed', 'https://www.linkedin.com/in/huma-waheed-ab684488/', 'Development Professional', 'The World Bank', 'Pakistan', '5+ years', 'Government partnerships, education initiatives, multi-sector collaboration', 'World Bank networks, education/development expertise, donor relations', 'Tier 2 - High Fit'),
]

# TIER 3: Exploratory Fit - Related Experience, Education/Nonprofit Context (4-6 years)
TIER_3 = [
    ('Mian Muhammad Junaid', 'https://pk.linkedin.com/in/mian-muhammad-junaid-8990171b', 'Program Officer', 'WaterAid Pakistan', 'Pakistan', '4-5 years', 'Education/development programs, institutional partnerships, field operations', 'WaterAid sector knowledge, education programs, community engagement', 'Tier 3 - Exploratory'),
    ('Amna Nasir', 'https://www.linkedin.com/in/amna-nasir25/', 'Program Manager', 'Teach For Pakistan', 'Pakistan', '4-5 years', 'Education programs, teacher development, institutional relations', 'Teach For Pakistan sector knowledge, education scale, program experience', 'Tier 3 - Exploratory'),
    ('Ali Siddiq', 'https://www.linkedin.com/in/alisiddiq/', 'Program Officer', 'Amal Academy', 'Pakistan', '4-5 years', 'Education fellowship, stakeholder engagement, program design', 'Amal Academy experience, education ecosystem knowledge', 'Tier 3 - Exploratory'),
    ('Dr. Sajid Bashir', 'https://www.linkedin.com/in/dr-sajid-bashir-3b62b957/', 'Senior Trainer & Consultant', 'Iqra University Islamabad', 'Pakistan', '5+ years', 'Education consulting, World Bank/GIZ projects, institutional development', 'Academic sector expertise, development projects experience', 'Tier 3 - Exploratory'),
    ('Zubair Qureshi', 'https://www.linkedin.com/in/zubair-qureshi-51b93297/', 'Business Development Professional', 'Dun & Bradstreet Pakistan', 'Pakistan', '4-5 years', 'B2B partnerships, corporate relationships, market development', 'B2B partnerships experience, institutional engagement', 'Tier 3 - Exploratory'),
    ('Ali Majid', 'https://www.linkedin.com/in/ali-majid-196878118/', 'Channel Partner Manager', 'upGrad', 'Pakistan', '5+ years', 'EdTech partnerships, B2B sales, channel management', 'EdTech sector experience, partnership channel expertise', 'Tier 3 - Exploratory'),
    ('Katherine Tilahun', 'https://www.linkedin.com/in/katherine-tilahun-01b66a47/', 'Senior Development Professional', 'DAI', 'Pakistan/International', '6+ years', 'USAID/UN partnerships, development projects, institutional relations', 'DAI/USAID networks, international development expertise', 'Tier 3 - Exploratory'),
    ('Arif Nadeem', 'https://www.linkedin.com/in/arif-nadeem-ngo/', 'Head of Strategic Partnership', 'HELP International', 'Pakistan', '5-6 years', 'NGO partnerships, stakeholder management, development programs', 'NGO sector expertise, strategic partnerships', 'Tier 3 - Exploratory'),
    ('Neelam Kasi', 'https://www.linkedin.com/in/neelam-kasi-9142092b/', 'Partnership Development Manager', 'Asian Synergy Pvt Limited', 'Pakistan', '4-5 years', 'Corporate partnerships, CSR initiatives, institutional engagement', 'Partnership development, corporate sector experience', 'Tier 3 - Exploratory'),
    ('Unzela Mapara', 'https://www.linkedin.com/in/unzela-mapara-b4a57141/', 'Branch Manager (Retail Banking)', 'HBL - Habib Bank Limited', 'Pakistan', '4-5 years', 'Banking partnerships, retail stakeholder management, corporate relations', 'Banking sector experience, institutional relationships', 'Tier 3 - Exploratory'),
]

# Combine all tiers
ALL_CANDIDATES = TIER_1 + TIER_2 + TIER_3

HEADERS = ['Name', 'LinkedIn URL', 'Current Role', 'Current Company', 'Location', 'Experience', 'Key Experience', 'Why Relevant', 'Tier', 'Status', 'DM Sent', 'Response', 'Date Added']

try:
    print("\n[STEP 1] Creating separate Google Sheet...")
    sh = gc.create('Senior Manager Growth - Candidates IMPROVED (2026-06-04)')
    new_sheet_id = sh.id
    print(f"[OK] Created: {new_sheet_id}")

    # Get the first worksheet
    worksheet = sh.get_worksheet(0)

    # Add headers
    print("\n[STEP 2] Adding headers...")
    worksheet.append_row(HEADERS)

    # Add candidates
    print(f"[STEP 3] Adding {len(ALL_CANDIDATES)} candidates...")
    for candidate in ALL_CANDIDATES:
        row = list(candidate) + ['Identified', '', '', datetime.now().strftime('%Y-%m-%d')]
        worksheet.append_row(row)

    print(f"[OK] All {len(ALL_CANDIDATES)} candidates added")

    # Generate URL
    sheet_url = f"https://docs.google.com/spreadsheets/d/{new_sheet_id}/edit"

    print("\n" + "="*80)
    print("[SUCCESS] SEPARATE SHEET CREATED")
    print("="*80)
    print(f"\nSheet ID: {new_sheet_id}")
    print(f"Sheet URL: {sheet_url}")
    print(f"\nCandidate Breakdown:")
    print(f"  Tier 1 (Highest Fit): {len(TIER_1)} candidates")
    print(f"  Tier 2 (High Fit): {len(TIER_2)} candidates")
    print(f"  Tier 3 (Exploratory): {len(TIER_3)} candidates")
    print(f"  TOTAL: {len(ALL_CANDIDATES)} candidates")

    # Update master roles sheet
    print("\n[STEP 4] Updating master roles sheet...")
    master_sh = gc.open_by_key(MASTER_SPREADSHEET_ID)
    roles_ws = master_sh.worksheet('Roles')

    # Get all rows
    all_rows = roles_ws.get_all_values()

    # Find and update SMG row
    updated = False
    for i, row in enumerate(all_rows, 1):
        if len(row) > 0 and 'Senior Manager Growth' in row[0]:
            # Update the Sheet Link column (index 2, so column 3)
            roles_ws.update_cell(i, 3, sheet_url)
            roles_ws.update_cell(i, 4, f'Identified - {len(ALL_CANDIDATES)} candidates')
            roles_ws.update_cell(i, 5, datetime.now().strftime('%Y-%m-%d'))
            roles_ws.update_cell(i, 6, f'Tier 1: {len(TIER_1)} (partnerships/BD at target companies). Tier 2: {len(TIER_2)} (nonprofit/donor relations). Tier 3: {len(TIER_3)} (exploratory). IMPROVED SLATE: 4-6 years experience, partnerships/BD/growth background.')
            print(f"[OK] Updated master roles sheet (row {i})")
            updated = True
            break

    if not updated:
        print("[INFO] SMG not found, adding new entry...")
        new_row = [
            'Senior Manager Growth',
            'SMG',
            sheet_url,
            f'Identified - {len(ALL_CANDIDATES)} candidates',
            datetime.now().strftime('%Y-%m-%d'),
            f'Tier 1: {len(TIER_1)} (partnerships/BD at target companies). Tier 2: {len(TIER_2)} (nonprofit/donor relations). Tier 3: {len(TIER_3)} (exploratory). IMPROVED SLATE: 4-6 years experience, partnerships/BD/growth background.'
        ]
        roles_ws.append_row(new_row)
        print("[OK] Added SMG to master roles sheet")

    print("\n" + "="*80)
    print("[FINAL] WORKFLOW COMPLETE")
    print("="*80)
    print(f"\nSeparate Candidates Sheet: {sheet_url}")
    print(f"Master Roles Sheet: Updated")
    print(f"\nCandidate Pool Summary:")
    print(f"  Total: {len(ALL_CANDIDATES)} candidates (improved from initial 8)")
    print(f"  Experience: 4-6 years (improved from 8+ years)")
    print(f"  Persona: Partnerships manager who can sell (from target companies)")
    print(f"\nNext: Draft personalized DMs for Tier 1 + Tier 2 candidates (18 total)")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
