# Session Log — Coco

## Session 003: Attendance Report 14 April 2026 (2026-04-14)

**Duration:** Full session
**Focus:** Finalize attendance report for Tuesday, April 14, 2026

### Completed Tasks
1. ✅ Created attendance_14apr2026.py script from pattern
2. ✅ Added on-site list (50 employees) from user's check
3. ✅ Integrated Teams presence channel (get_presence_updates)
   - Flagged arriving late: Afifa, Muhammad Saim, Muhammad Umar Raza, Hareem Fatima
   - Flagged WFH: Zunaira Shahid (not feeling well)
4. ✅ User corrections applied:
   - Removed Sohaib Danish from onsite
   - Added Muhammad Usman Mughal + MUHAMMAD SHOAIB KHAN
   - Removed Alishba Anam & Razia Kausar (permanent exclusion from flagged)
5. ✅ Added Markaz status updates:
   - Mahrah Ashraf: moved to ON_LEAVE (Sick Leave)
   - Momina Tariq: added with half-day exams (Apr 14 & 17)
   - Qurat-ul-ain: noted not available second half
6. ✅ Expanded onsite:
   - Added Fatima Khan, Fatima Rahman, Mahnoor Shafique
7. ✅ Added ARCHIVED_NIETE section:
   - Umama Gul Siddiqui, Shumaila Aslam, Jawwad Ali, QURAT UL AIN, Hareem Fatima, Momina Raja
   - Added: Muhammad Zain ul Abadin, Hamza Shahid
   - Removed: Humna Tayaba
   - Added "Onsite I-10" status notes
8. ✅ Added Haroon Yasin (fundraising, not OPL+OWT)
9. ✅ Queried Markaz database for pending leaves
   - Accessed leave_requests table directly
   - Found 62 pending leaves (not approved)
10. ✅ Created Pending Leaves/WFH section
    - Added 7 leaves initially
    - Removed Mavia (already approved)
    - Removed Saaim Asif (approved)
    - Final 5: Momna Tariq, Muhammad Muzzammil Patel, Aroma Tahir, Ramsha Khurshid, Usman Imtiaz

### Critical Learning
- **Name Matching Rule:** "Muhammad Zeeshan Usaid" vs "Zeeshan Usaid" caused false flagging
- **Markaz Access:** leave_requests table accessible directly from Neon DB
- **Teams Integration:** Working — last 24h message pull

### Files Modified
- scripts/reports/attendance_14apr2026.py (NEW — 350 lines)
- scripts/reports/send_attendance_14apr.py (NEW — helper script)

### Files Saved to Memory
- project_attendance_14apr2026_finalized.md
- project_attendance_report_markaz_integration.md

### Status
**Report Final:** Sent to ayesha.khan@taleemabad.com
**Format:** 10-section PDF (landscape A4)
**Data:** Teams-verified, Markaz-verified, user-corrected

### Next Session
- Create markaz_reader.py utility for reusable pending leaves queries
- Wire into weekly_pipeline_monitor.py for automated flagging
- Test attendance report for April 15-17 (rest of week)
