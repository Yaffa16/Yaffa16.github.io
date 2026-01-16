from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
root_path = Path("work")  # <-- change this

target_snippet = """<!-- BACK BUTTON -->
    <div class="back-button">
      <a href="#">← Back</a>
    </div>"""

# -----------------------------
# Walk through all subfolders
# -----------------------------
for html_file in root_path.rglob("*.html"):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    if target_snippet in content:
        content = content.replace(target_snippet, "")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Removed back button from: {html_file}")
    else:
        print(f"No back button found in: {html_file}")

print("Done!")
