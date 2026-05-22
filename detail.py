

import re

def clean_email(email):
    if email:
        return email.strip().replace(" ", "").lower()
    return None

def clean_mobile(mobile):
    if mobile:
        mobile = re.sub(r"[^\d+]", "", mobile)

        if mobile.startswith("91") and not mobile.startswith("+91"):
            mobile = "+" + mobile

        return mobile
    return None

def normalize_contact(result):
    return {
        "name": result.get("name"),
        "email": clean_email(result.get("email")),
        "mobile": clean_mobile(result.get("mobile_number"))
    }