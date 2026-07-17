import re
import os
import sys
import pypdf

pdf_path = "/Users/santushtkotai/.gemini/antigravity-ide/brain/b3dcb3d6-9b38-486e-a28e-aee4238cd8a3/media__1784287968676.pdf"
reader = pypdf.PdfReader(pdf_path)
text = ""
for page in reader.pages:
    text += page.extract_text() or ""

# Regex to find email patterns
email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}')
raw_emails = email_pattern.findall(text)

cleaned_emails = set()
for email in raw_emails:
    email = email.lower()
    
    # Strip any leading garbage (like numbers, gender Mr. Male etc.)
    # In table cells, sometimes text runs together: "male8349860858harshalmahajan8349@gmail.comct"
    # The email should start with the actual username characters
    # Usually it's preceded by "mr.male" or "ms.female" followed by contact numbers
    # We can split the string by digits, and take the last part that matches an email start
    # E.g. "male8349860858harshalmahajan8349@gmail.comct" -> "harshalmahajan8349@gmail.comct"
    parts = re.split(r'\d{10}', email) # split by phone number (10 digits)
    if len(parts) > 1:
        email = parts[-1]
    
    # Strip trailing "ct" or "dt" from ref IDs
    if email.endswith("comct") or email.endswith("comdt"):
        email = email[:-2]
    elif email.endswith("inct") or email.endswith("indt"):
        email = email[:-2]
    elif "comct" in email:
        email = email.split("comct")[0] + "com"
    elif "comdt" in email:
        email = email.split("comdt")[0] + "com"
    elif "inct" in email:
        email = email.split("inct")[0] + "in"
    elif "indt" in email:
        email = email.split("indt")[0] + "in"
        
    # Standard cleanup of any other trailing letters after .com/.in
    # Usually, it's .com or .in or .org or .net or .edu
    # E.g. "gmail.comct202..." -> "gmail.com"
    m = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?:com|in|org|net|edu|ac\.in))', email)
    if m:
        email = m.group(1)
        
    # Ensure it's a valid email structure
    if "@" in email and "." in email:
        # Ignore system/git/test emails
        if not any(x in email for x in ["git@github.com", "interleet.local", "example.com", "tcs.com"]):
            # Remove any leading non-alphabetic/numeric characters
            email = re.sub(r'^[^a-zA-Z0-9]+', '', email)
            cleaned_emails.add(email)

sorted_emails = sorted(list(cleaned_emails))
print(f"Extracted and cleaned {len(sorted_emails)} unique emails from PDF.")
for email in sorted_emails[:15]:
    print(f"  - {email}")

output_path = "/Users/santushtkotai/.gemini/antigravity-ide/brain/b3dcb3d6-9b38-486e-a28e-aee4238cd8a3/scratch/extracted_emails.txt"
with open(output_path, "w", encoding="utf-8") as f:
    for email in sorted_emails:
        f.write(email + "\n")

print(f"Saved email list to {output_path}")
