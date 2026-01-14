import os

# Root folder to start searching
root_folder = 'work'  # <-- CHANGE THIS to your folder

# Text to find and replace
search_text = '<a href="../../index.html">Works</a>'
replace_text = '<a href="../../index.html?top=1">Works</a>'

# Walk through all directories and files
for subdir, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Only replace if the text exists
            if search_text in content:
                content = content.replace(search_text, replace_text)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {file_path}")
