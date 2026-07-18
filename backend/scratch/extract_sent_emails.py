import os
import re

tasks_dir = "/Users/santushtkotai/.gemini/antigravity-ide/brain/b3dcb3d6-9b38-486e-a28e-aee4238cd8a3/.system_generated/tasks"
log_files = ["task-3118.log", "task-3211.log"]

sent_emails = set()

for fName in log_files:
    path = os.path.join(tasks_dir, fName)
    if os.path.exists(path):
        print(f"Parsing: {path}")
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                # Look for lines like "✓ Sent email to xxxx@gmail.com"
                match = re.search(r"Sent email to\s+([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", line)
                if match:
                    sent_emails.add(match.group(1).lower().strip())
    else:
        print(f"Log file not found: {path}")

print(f"Extracted {len(sent_emails)} unique sent email addresses.")

# Save to sent_emails.txt
out_path = "/Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/backend/sent_emails.txt"
with open(out_path, "w", encoding="utf-8") as out:
    for email in sorted(sent_emails):
        out.write(f"{email}\n")

print(f"Saved to local sent_emails.txt: {out_path}")
