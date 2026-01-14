import os
import re

# ---------------- CONFIG ----------------
# Root folder to start search
root_folder = "dellater"  # change this to your working directory if needed

# The old code snippet (exactly as it appears in HTML)
old_code_pattern = re.compile(
    r"const toggle = document\.getElementById\('modeToggle'\);\s*toggle\.addEventListener\('change', \(\) => {\s*document\.body\.classList\.toggle\('dark-mode'\);\s*}\);",
    re.DOTALL
)

# The new code to replace with
new_code = """<script>
// --------- DARK MODE TOGGLE WITH LOCALSTORAGE ---------
const modeToggle = document.getElementById('modeToggle');

if (modeToggle) {
  // Apply saved preference on load immediately
  if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    modeToggle.checked = true;
  }

  // Toggle dark mode
  modeToggle.addEventListener('change', () => {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
  });
}
</script>"""


# ---------------- FUNCTION ----------------
def replace_dark_mode_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if old code exists
    if old_code_pattern.search(content):
        print(f"Updating dark mode code in: {file_path}")

        # Backup original file
        backup_path = file_path + ".bak"
        with open(backup_path, 'w', encoding='utf-8') as backup_file:
            backup_file.write(content)

        # Replace old code with new code
        new_content = old_code_pattern.sub(new_code, content)

        # Write back to original file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)


# ---------------- WALK THROUGH FOLDERS ----------------
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.lower().endswith(".html"):
            file_path = os.path.join(dirpath, filename)
            replace_dark_mode_code(file_path)

print("All HTML files processed!")
