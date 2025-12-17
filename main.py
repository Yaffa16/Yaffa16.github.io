import os

# Root folder
root = "weirdwithcode_site"

# Create main folders
os.makedirs(root, exist_ok=True)
os.makedirs(os.path.join(root, "work"), exist_ok=True)
os.makedirs(os.path.join(root, "images"), exist_ok=True)

# List of project names and corresponding image names
projects = [
    "taming_ai",
    "ai_tell_you",
    "meme_me",
    "berthold_leibinger",
    "doodly_do",
    "if_you_think_you_are_sleeping",
    "botcast",
    "agents",
    "berlin_stallwachter_party",
    "memory_holes",
    "start_festival",
    "prayer_room",
    "bindu",
    "isle_of_coding",
    "reflections",
    "voice_box"
]

# 1️⃣ Generate index.html
index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Weirdwithcode — Home</title>
</head>
<body bgcolor="#ffffff" text="#000000">

<h1>Weird with code</h1>
<p>
  <a href="index.html">Work</a> |
  <a href="press.html">Press</a> |
  <a href="contact.html">Contact</a> |
  <a href="https://www.instagram.com/" target="_blank">Instagram</a>
</p>

<hr>

<h2>Yasha Jain (weirdwithcode) is a new media artist who makes art out of code and curiosity.</h2>
<p>
Blending coding, storytelling, and experimental media to make interactive, generative, and visual art.
</p>

<hr>

<h3>Works</h3>
<ul>
"""
for p in projects:
    index_html += f'  <li><a href="work/{p}.html">{p.replace("_"," ").title()}</a></li>\n'

index_html += """</ul>
</body>
</html>
"""

with open(os.path.join(root, "index.html"), "w") as f:
    f.write(index_html)

# 2️⃣ Generate press.html
press_html = """<!DOCTYPE html>
<html>
<head><title>Press — Weirdwithcode</title></head>
<body>
<h1>Press</h1>
<p><a href="index.html">← back</a></p>
<p>Press links and articles go here.</p>
</body>
</html>
"""
with open(os.path.join(root, "press.html"), "w") as f:
    f.write(press_html)

# 3️⃣ Generate contact.html
contact_html = """<!DOCTYPE html>
<html>
<head><title>Contact — Weirdwithcode</title></head>
<body>
<h1>Contact</h1>
<p><a href="index.html">← back</a></p>
<p>Email: your@email.com</p>
<p>Instagram: <a href="https://www.instagram.com/" target="_blank">@weirdwithcode</a></p>
</body>
</html>
"""
with open(os.path.join(root, "contact.html"), "w") as f:
    f.write(contact_html)

# 4️⃣ Generate work HTML files
for p in projects:
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{p.replace('_',' ').title()} — Weirdwithcode</title>
</head>
<body bgcolor="#ffffff" text="#000000">
<h1>{p.replace('_',' ').title()}</h1>
<center>
  <img src="../images/{p}.jpg" width="400" height="400" alt="{p.replace('_',' ').title()}">
</center>
<p>Description of the project goes here.</p>
<p><a href="../index.html">&larr; Back to Home</a></p>
</body>
</html>
"""
    with open(os.path.join(root, "work", f"{p}.html"), "w") as f:
        f.write(html_content)

# 5️⃣ Create placeholder JPG files
for p in projects:
    img_path = os.path.join(root, "images", f"{p}.jpg")
    if not os.path.exists(img_path):
        with open(img_path, "wb") as f:
            f.write(b"")  # empty placeholder
