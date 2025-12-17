import re
from pathlib import Path

ROOT = Path(__file__).parent
WORK_DIR = ROOT / "work"
OUTPUT = ROOT / "index.html"

META_RE = re.compile(r"<!--(.*?)-->", re.S)

def parse_metadata(html_path):
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    meta = {}

    match = META_RE.search(text)
    if match:
        for line in match.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().upper()] = v.strip()

    year = html_path.parent.name
    title = meta.get(
        "TITLE",
        html_path.stem.replace("_", " ").title()
    )

    return {
        "title": title,
        "year": int(meta.get("YEAR", year)),
        "image": meta.get("IMAGE", f"{html_path.stem}.jpg"),
        "link": f"work/{year}/{html_path.name}",
        "image_path": f"work/{year}/{meta.get('IMAGE', f'{html_path.stem}.jpg')}"
    }

def collect_all_works():
    works = []

    for year_dir in WORK_DIR.iterdir():
        if not year_dir.is_dir():
            continue
        if not year_dir.name.isdigit():
            continue

        for html in year_dir.glob("*.html"):
            works.append(parse_metadata(html))

    works.sort(key=lambda w: w["year"], reverse=True)
    return works

def build_grid(works):
    html = "<div style='display:flex; flex-wrap:wrap; justify-content:center; gap:15px;'>\n"

    for work in works:
        html += f"""
<div style='text-align:left; width:18%;'>
  <a href="{work['link']}" class="artwork-link" style="text-decoration:none; color:#000000;">
    <img src="{work['image_path']}" style="width:100%; aspect-ratio:1/1; object-fit:cover; display:block; margin-bottom:5px;">
    <span class="artwork-hover" style="font-size:0.9em;">{work['title']} | {work['year']}</span>
  </a>
</div>
"""
    html += "</div>\n"
    return html


def build_index():
    works = collect_all_works()
    grid_html = build_grid(works)

    OUTPUT.write_text(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Weirdwithcode — Home</title>
  <style>
    body {{
      background-color: #cccccc; /* grey background */
      font-family: monospace, sans-serif;
      margin: 0;
      padding: 0;
    }}
    .content {{
      background-color: #ffffff; /* “paper” block */
      max-width: 1200px;
      margin: 40px auto;
      padding: 0;
      box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }}
    .header-bar {{
      background-color: #000000;
      color: #ffffff;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 15px 40px;
    }}
    .header-bar a {{
      color: #ffffff;
      text-decoration: none;
      margin-left: 15px;
    }}
    .header-bar a:hover {{
      text-decoration: underline;
    }}
    .content-inner {{
      padding: 40px;
    }}
    a.artwork-link:hover .artwork-hover {{
      background: #000000;
      color: #ffffff;
    }}
    h1, h2 {{
      text-align: center;
    }}
    hr {{
      margin-top: 30px;
      margin-bottom: 30px;
      border: 0;
      border-top: 1px solid #999999;
    }}
    h2.works-heading {{
      margin-top: 0;
      margin-bottom: 20px; /* space between heading and images */
    }}
  </style>
</head>

<body>

<div class="content">
  <div class="header-bar">
    <div><b>weird with code</b></div>
    <div>
      <a href="bio.html">Bio</a>
      <a href="cv.html">CV</a>
      <a href="press.html">Press</a>
      <a href="contact.html">Contact</a>
      <a href="https://www.instagram.com/" target="_blank">Instagram</a>
    </div>
  </div>

  <div class="content-inner">
    <h2>
    Yasha Jain (weirdwithcode) is a new media artist who makes art out of code and curiosity.
    </h2>

    <p>
    Blending coding, storytelling, and experimental media to make interactive,
    generative, and visual art. Looking at the narrative potential of code —
    how simple rules can evoke meaning, emotion, or memory.
    </p>

    <hr>
    <h2 class="works-heading">Works</h2>

    {grid_html}

    <hr>
    <small>
    JIYO  · AUR · Jeene · Do <br>
    Index generated automatically
    </small>
  </div>
</div>

</body>
</html>
""", encoding="utf-8")


if __name__ == "__main__":
    build_index()
    print("✓ index.html rebuilt")
