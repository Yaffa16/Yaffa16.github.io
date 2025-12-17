import os

def has_metadata(content):
    return "<!--" in content and "TITLE:" in content and "YEAR:" in content and "IMAGE:" in content

BASE_DIR = os.getcwd()

for year in os.listdir(BASE_DIR):
    year_path = os.path.join(BASE_DIR, year)

    # only process folders like 2024, 2025, etc.
    if not os.path.isdir(year_path):
        continue
    if not year.isdigit():
        continue

    for filename in os.listdir(year_path):
        if not filename.endswith(".html"):
            continue

        file_path = os.path.join(year_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if has_metadata(content):
            print(f"✓ metadata exists: {year}/{filename}")
            continue

        name = filename.replace(".html", "")
        title = name.replace("_", " ").title()
        image = f"{name}.jpg"

        metadata = f"""<!--
TITLE: {title}
YEAR: {year}
IMAGE: {image}
-->

"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(metadata + content)

        print(f"+ added metadata: {year}/{filename}")
