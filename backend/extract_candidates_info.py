import re
import os
import sys
import csv
import json
import pypdf

pdf_path = "/Users/santushtkotai/.gemini/antigravity-ide/brain/b3dcb3d6-9b38-486e-a28e-aee4238cd8a3/media__1784287968676.pdf"
reader = pypdf.PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text() or ""

# Regex pattern matching tightly packed cells
pattern = re.compile(
    r'(\d+)([a-zA-Z\s\.\'-]+?)(Mr\.|Ms\.|Miss|Mr|Ms)(Male|Female|Others)?(\d{10})?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10})'
)

candidates = []
seen_emails = set()

# Process line by line or findall matches
for line in text.split("\n"):
    # Sometimes multiple records are on the same line or run together
    # Let's find all matches in the line
    matches = pattern.finditer(line)
    for m in matches:
        serial = m.group(1)
        name = m.group(2).strip()
        phone = m.group(5) or ""
        email = m.group(6).lower()
        
        # Clean trailing "ct" or "dt" from ref IDs on email
        if email.endswith("comct") or email.endswith("comdt"):
            email = email[:-2]
        elif email.endswith("inct") or email.endswith("indt"):
            email = email[:-2]
        
        # Filter email extensions
        m_email = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?:com|in|org|net|edu|ac\.in))', email)
        if m_email:
            email = m_email.group(1)

        # Ignore systems/git/test emails
        if any(x in email for x in ["git@github.com", "interleet.local", "example.com", "tcs.com"]):
            continue
            
        if email not in seen_emails:
            seen_emails.add(email)
            candidates.append({
                "serial": serial,
                "name": name,
                "email": email,
                "phone": phone
            })

# Sort by name
candidates.sort(key=lambda x: x["name"])

# Save as CSV
csv_path = "/Users/santushtkotai/.gemini/antigravity-ide/brain/b3dcb3d6-9b38-486e-a28e-aee4238cd8a3/candidates_info.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["serial", "name", "email", "phone"])
    writer.writeheader()
    writer.writerows(candidates)

# Save as JSON
json_path = "/Users/santushtkotai/.gemini/antigravity-ide/brain/b3dcb3d6-9b38-486e-a28e-aee4238cd8a3/candidates_info.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(candidates, f, indent=2)

print(f"Successfully processed {len(candidates)} candidates.")
print(f"Saved CSV file to: {csv_path}")
print(f"Saved JSON file to: {json_path}")
for c in candidates[:10]:
    print(f"  - {c['name']} <{c['email']}>")
