"""
Extract all 42 Soul Architect candidate CVs from Base64 and save as text files for manual review.
"""

import json
import base64
import os
import sys

# Candidate list from database
CANDIDATES = [
    (1111, "Hadia_Sajjad"),
    (1109, "Faizan_Ullah"),
    (1105, "Rimsha_Faisal"),
    (1103, "Nain_Tara"),
    (1102, "Talal_Hassan_Khan"),
    (1101, "Hulalah_Khan"),
    (1099, "Hamza_Jamal"),
    (1098, "Danyal_Haroon"),
    (1097, "hamza_Applicant"),
    (1096, "Aaqib_Khan"),
    (1094, "Ghulam_Qadir"),
    (1092, "Asma_Butt"),
    (1090, "Zikra_Fiaz"),
    (1088, "wajihazainab_Applicant"),
    (1087, "Saad_imran"),
    (1085, "Zehra_Rashid"),
    (1084, "Manahil_Ahmed"),
    (1083, "Muhammad_Ali_1"),
    (1080, "Saad_Sajid"),
    (1079, "Muhammad_Ali_2"),
    (1078, "Asad_Nawaz"),
    (1076, "Sameen_Ali"),
    (1075, "Majid_Raffique"),
    (1074, "Hassan_Bin_Tariq"),
    (1073, "Muhammad_Jaffer"),
    (1072, "Sanaullah_Mukhtar"),
    (384, "Hamza_Ahmed"),
    (1071, "Syed_Manan_Ali"),
    (1066, "Muhammad_Taufeeq"),
    (1064, "Muhammad_Abdullah_Safdar"),
    (1061, "Zia_Ullah"),
    (1060, "Muhammad_Ibrahim_Khan"),
    (1058, "UIxFly_Moheed"),
    (1056, "Muhammad_Wasi_Haider"),
    (1051, "Ahmad_Hamdan_Akram"),
    (1050, "zennab_Applicant"),
    (1048, "Arslan_Saleem"),
    (1047, "Muhammad_Taimoor"),
    (867, "Ameer_Hamza_Tariq"),
    (823, "Aisha_Bashir"),
    (819, "Sholmiyat_Adnan"),
    (817, "Muhammad_Ammar_Khan"),
]

def extract_cv_batch(candidate_ids):
    """
    Fetch a batch of candidates and extract CV text.
    This will be run via the database tool.
    """
    id_list = ",".join(str(cid) for cid in candidate_ids)
    query = f"""
    SELECT id, first_name, last_name, resume_data
    FROM candidates
    WHERE id IN ({id_list})
    ORDER BY id DESC
    """
    return query

# Generate queries for each batch (5 candidates per batch to manage token size)
print("To extract all CVs, run these queries in sequence and save outputs:")
print()

for batch_num in range(0, len(CANDIDATES), 5):
    batch = CANDIDATES[batch_num:batch_num+5]
    ids = [str(c[0]) for c in batch]
    id_list = ",".join(ids)
    print(f"--- BATCH {batch_num//5 + 1} ---")
    print(f"SELECT id, first_name, last_name, resume_data FROM candidates WHERE id IN ({id_list}) ORDER BY id DESC;")
    print()
