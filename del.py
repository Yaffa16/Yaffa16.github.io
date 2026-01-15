import os
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
root_path = Path("work")  # <-- change this to the root folder
old_snippet = '<b>weird with code</b>'
new_snippet = '''<b id="headerSnap">
  <a href="../../index.html?top=1" style="color: inherit; text-decoration: none;">weird with code</a>
</b>'''

# -----------------------------
# Walk through all subfolders
# -----------------------------
for html_file in root_path.rglob("*.html"):  # recursively find all HTML files
    print(f"Processing: {html_file}")
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    if old_snippet in content:
        content = content.replace(old_snippet, new_snippet)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {html_file}")
    else:
        print(f"No match found in: {html_file}")

print("Done!")
