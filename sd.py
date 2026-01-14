import os

# Folder containing HTML files (and subfolders)
folder_path = "work"

# Walk through all folders and subfolders
for root, dirs, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith(".html"):
            file_path = os.path.join(root, filename)

            # Read the file content
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Replace the specific hrefs
            content = content.replace('<a href="../../bio.html">Bio</a>', '<a href="../bio.html">Bio</a>')
            content = content.replace('<a href="../../contact.html">Contact</a>',
                                      '<a href="../contact.html">Contact</a>')

            # Write the updated content back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

print("All HTML files in all subfolders have been updated.")
