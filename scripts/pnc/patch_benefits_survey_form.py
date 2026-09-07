"""
Patch the live Benefits Pulse Check form to match ITEMS in the builder.

Pushes an updateItem for each index given on the command line (0-based), taking
the item definition from build_benefits_survey_form.ITEMS so the script stays the
single source of truth.

Usage:  python scripts/pnc/patch_benefits_survey_form.py 1 7
"""
import sys

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from build_benefits_survey_form import DESCRIPTION, ITEMS, TOKEN

FORM_ID = "1FJeLmuKHw-XVilArMFkodZobTMGep_fLcBER-_yFWmk"
API = "https://forms.googleapis.com/v1/forms"


def main():
    args = sys.argv[1:]
    do_info = "info" in args
    idxs = [int(a) for a in args if a != "info"]
    if not idxs and not do_info:
        print("give 'info' and/or one or more 0-based item indices")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN))
    if not creds.valid:
        creds.refresh(Request())
    hdrs = {"Authorization": "Bearer " + creds.token}

    reqs = []
    if do_info:
        reqs.append(
            {
                "updateFormInfo": {
                    "info": {"description": DESCRIPTION},
                    "updateMask": "description",
                }
            }
        )
    for i in idxs:
        item = dict(ITEMS[i])
        # an item with no description clears any existing one, since the mask covers it
        item.setdefault("description", "")
        reqs.append(
            {
                "updateItem": {
                    "item": item,
                    "location": {"index": i},
                    "updateMask": "title,description,questionItem",
                }
            }
        )

    r = requests.post(f"{API}/{FORM_ID}:batchUpdate", headers=hdrs, json={"requests": reqs})
    if r.status_code != 200:
        print("PATCH FAILED", r.status_code)
        print(r.text)
        sys.exit(1)
    print("patched indices:", idxs)


if __name__ == "__main__":
    main()
