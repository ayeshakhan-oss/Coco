"""
Job 17 — CPD Coach
Filter: Female candidates who are TFP Fellows, not already hired.
"""

import json
import base64
import os
import re

# OCR setup
import fitz  # pymupdf
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PERSISTED_FILE = r"C:\Users\Dell\.claude\projects\c--My-First-Agent\585b1f5b-e55a-43e0-b044-a2981044a0b4\tool-results\toolu_01CyiUzd7ipxtree6bZXkpip.json"

OUTPUT_DIR = r"c:\My First Agent\output\cv_texts_job17"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_text_from_pdf_bytes(pdf_bytes):
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text
            else:
                # OCR fallback
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                text += pytesseract.image_to_string(img)
        doc.close()
    except Exception as e:
        text = f"[ERROR extracting text: {e}]"
    return text.strip()


def is_tfp_fellow(text):
    text_lower = text.lower()
    tfp_patterns = [
        r'teach for pakistan',
        r'tfp\s+fellow',
        r'fellow.*teach for pakistan',
        r'teach for pakistan.*fellow',
        r'\btfp\b',
    ]
    for pat in tfp_patterns:
        if re.search(pat, text_lower):
            return True
    return False


def is_female(text, first_name):
    text_lower = text.lower()
    # Check pronouns
    if re.search(r'\b(she|her|hers)\b', text_lower):
        return True
    # Common female name indicators
    female_names = [
        'zoya', 'fatima', 'ayesha', 'aisha', 'amina', 'sana', 'sara', 'sarah',
        'hira', 'nadia', 'maria', 'maryam', 'mariam', 'zainab', 'zahra', 'mahnoor',
        'anum', 'aroha', 'kiran', 'sobia', 'rabia', 'rida', 'layla', 'laila',
        'noor', 'amber', 'ambreen', 'bushra', 'fizza', 'fizaa', 'gulnaz',
        'hafsa', 'hoorain', 'iqra', 'javeria', 'kinza', 'komal', 'maha',
        'mehwish', 'misbah', 'naima', 'nazia', 'neha', 'nimra', 'pariyal',
        'pari', 'rehma', 'rimsha', 'roshaan', 'ruqayyah', 'sadaf', 'saima',
        'samia', 'scheherazade', 'sehar', 'shabana', 'shagufta', 'shakeela',
        'shamsa', 'shazia', 'sidra', 'siffah', 'sobia', 'sumaiya', 'sumaira',
        'syeda', 'tayyaba', 'ume', 'umm', 'umme', 'urwa', 'wardah', 'yusra',
        'zara', 'zarqa', 'zuha', 'zujajah', 'madiha', 'nabeela', 'nabeelah',
        'faryal', 'midhat', 'sadia', 'pariyal', 'momina', 'alina', 'abeera',
        'abeer', 'anaya', 'aneeza', 'aneeqa', 'aniqa', 'aqsa', 'areeba',
        'areej', 'arwa', 'asma', 'asna', 'athena', 'atiya', 'azka', 'bareerah',
        'dua', 'eisha', 'emaan', 'eman', 'eshal', 'fareeha', 'farida', 'farwa',
        'faten', 'fauzia', 'fiza', 'gul', 'hajra', 'hamna', 'hana', 'haniya',
        'henna', 'hibba', 'huda', 'humna', 'ifra', 'inaya', 'iqra', 'iram',
        'izna', 'jazba', 'khadeeja', 'khadeja', 'khadijah', 'khansa', 'lubna',
        'maham', 'mahnoor', 'mahpara', 'malak', 'maliha', 'marwa', 'mishal',
        'minahil', 'minhal', 'misba', 'momena', 'muneeba', 'muniba', 'nabila',
        'nabiha', 'nadia', 'nailah', 'naila', 'nawal', 'nida', 'niha', 'nisha',
        'noreen', 'nosheen', 'nudrat', 'numra', 'pakiza', 'palwasha', 'qurat',
        'quratulain', 'ramsha', 'rania', 'ranya', 'razia', 'rida', 'romaisa',
        'romesa', 'ruba', 'rukayya', 'ruksana', 'ruma', 'rumaisa', 'rumaysa',
        'saba', 'sabah', 'sabahat', 'sabeen', 'sadaf', 'sahar', 'sahira',
        'sameen', 'sameena', 'samina', 'sana', 'sanaa', 'sania', 'saniya',
        'seerat', 'shaan', 'shahida', 'shahla', 'shaiqa', 'shaista', 'shalimar',
        'shamim', 'shanza', 'shirin', 'shiza', 'shurooq', 'shumaila', 'sibgha',
        'simra', 'sobia', 'sofia', 'sophia', 'sundas', 'surriya', 'syeda',
        'tahira', 'tanzila', 'tasmia', 'tazeen', 'tooba', 'ulfat', 'umara',
        'urooj', 'ushna', 'uzma', 'vaneeza', 'wajeeha', 'warda', 'waseema',
        'yasmeen', 'yasmin', 'yumna', 'zeba', 'zehra', 'zile', 'zoha',
    ]
    fn = first_name.lower().strip() if first_name else ''
    if fn in female_names:
        return True
    return False


def main():
    print(f"Loading persisted results...")
    with open(PERSISTED_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)

    # The persisted file has a 'text' key with JSON string
    if isinstance(raw, list) and len(raw) > 0 and 'text' in raw[0]:
        candidates = json.loads(raw[0]['text'])
    else:
        candidates = raw

    print(f"Total applicants (non-hired): {len(candidates)}")

    results = []
    for i, c in enumerate(candidates):
        first_name = c.get('first_name') or ''
        last_name = c.get('last_name') or ''
        full_name = f"{first_name} {last_name}".strip()
        app_id = c.get('app_id')
        candidate_id = c.get('candidate_id')
        email = c.get('email', '')
        status = c.get('status', '')
        location = c.get('location', '')
        resume_b64 = c.get('resume_data', '')

        print(f"[{i+1}/{len(candidates)}] Processing: {full_name} (app {app_id})")

        if not resume_b64:
            print(f"  -> No resume data, skipping")
            continue

        try:
            pdf_bytes = base64.b64decode(resume_b64)
        except Exception as e:
            print(f"  → Base64 decode error: {e}")
            continue

        cv_text = extract_text_from_pdf_bytes(pdf_bytes)

        # Save CV text
        safe_name = re.sub(r'[^\w\s-]', '', full_name).replace(' ', '_')
        txt_path = os.path.join(OUTPUT_DIR, f"{app_id}_{safe_name}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(cv_text)

        tfp = is_tfp_fellow(cv_text)
        female = is_female(cv_text, first_name)

        print(f"  -> TFP Fellow: {tfp} | Female: {female}")

        if tfp and female:
            results.append({
                'app_id': app_id,
                'candidate_id': candidate_id,
                'name': full_name,
                'email': email,
                'status': status,
                'location': location,
                'cv_text_path': txt_path,
                'cv_text_preview': cv_text[:500],
            })

    print(f"\n{'='*60}")
    print(f"FEMALE TFP FELLOWS - Job 17 CPD Coach")
    print(f"{'='*60}")
    if not results:
        print("No female TFP Fellows found.")
    for r in results:
        print(f"\n#{results.index(r)+1} {r['name']}")
        print(f"   App ID: {r['app_id']} | Candidate ID: {r['candidate_id']}")
        print(f"   Email: {r['email']}")
        print(f"   Status: {r['status']} | Location: {r['location']}")
        print(f"   CV saved: {r['cv_text_path']}")
        preview = r['cv_text_preview'][:200].encode('ascii', 'replace').decode('ascii')
        print(f"   Preview: {preview}...")

    print(f"\nTotal female TFP Fellows found: {len(results)}")


if __name__ == '__main__':
    main()
