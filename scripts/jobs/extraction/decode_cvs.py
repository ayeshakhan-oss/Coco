#!/usr/bin/env python
"""
Decode all 42 Soul Architect CVs from Base64 and extract text.
Saves each as a text file for manual review.
"""

import json
import base64
import sys
import os

# Read from tool results file (from database query)
result_file = sys.argv[1] if len(sys.argv) > 1 else None

if not result_file:
    print("Usage: python decode_cvs.py <path_to_result_file>")
    sys.exit(1)

# Create output directory
output_dir = "soul_architect_cvs_decoded"
os.makedirs(output_dir, exist_ok=True)

try:
    with open(result_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # The file contains JSON in a special format - extract the actual JSON
    # Look for the JSON array start
    start_idx = content.find('[\n  {')
    if start_idx == -1:
        start_idx = content.find('[{')

    if start_idx > -1:
        json_str = content[start_idx:]
        # Find the end
        end_idx = json_str.rfind(']')
        if end_idx > -1:
            json_str = json_str[:end_idx+1]
    else:
        json_str = content

    data = json.loads(json_str)

    if isinstance(data, list) and len(data) > 0 and 'text' in data[0]:
        # Nested format - extract the actual JSON from 'text' field
        actual_json = data[0]['text']
        data = json.loads(actual_json)

    # Process each candidate
    for record in data:
        cand_id = record.get('id')
        first_name = record.get('first_name', 'Unknown')
        last_name = record.get('last_name', '')
        resume_data = record.get('resume_data', '')

        if not resume_data:
            print(f"Skipping {first_name} {last_name} ({cand_id}) - no resume data")
            continue

        try:
            # Decode Base64
            pdf_bytes = base64.b64decode(resume_data)

            # Try to extract as text (PDFs have embedded text)
            text = pdf_bytes.decode('utf-8', errors='ignore')

            # Save to file
            filename = f"{output_dir}/{cand_id}_{first_name}_{last_name}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f"OK {first_name} {last_name} ({cand_id}) - {len(text)} chars")

        except Exception as e:
            print(f"FAIL {first_name} {last_name} ({cand_id}) - Error: {str(e)[:50]}")

    print(f"\nDone! CVs saved to {output_dir}/")

except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)
