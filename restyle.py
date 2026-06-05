#!/usr/bin/env python3
"""
restyle_projects.py
-------------------
Run from the ROOT of your site (Yaffa16.github.io-main):

    python3 restyle_projects.py

Media grid strategy (this version):
  - ALL fixed row heights removed — media renders at its natural aspect ratio.
  - 1 item  → full width, natural height.
  - 2 items → side by side, each 50% wide, natural height.
  - 3 items → first spans full width, then two side by side.
  - 4 items → 2×2 grid, natural heights per row.
  - 5+ items → 2-column grid, items flow naturally; odd last item spans full width.
  - Videos get a 16:9 wrapper so they don't collapse to zero height before load.
  - Images and iframes expand freely to their intrinsic ratio.
"""

import os
import re

META = {
    "2016/reflections.html": {
        "num": "27", "year": "2016", "title": "Reflections",
        "type": "Interactive Installation",
        "tools": ["Max/MSP/Jitter", "Millumin", "Syphon", "iPhone Accelerometer", "Projectors & Cameras"],
        "themes": ["Power & Perspective", "Time & Memory", "Human Interaction"],
        "meta_right": "Personal project<br>2016<br>Installation",
    },
    "2017/bindu.html": {
        "num": "24", "year": "2017", "title": "Bindu",
        "type": "Generative Art",
        "tools": ["Processing", "p5.js"],
        "themes": ["Meditation", "Sacred Geometry", "Algorithmic Pattern"],
        "meta_right": "Personal project<br>2017<br>Generative",
    },
    "2017/start_festival.html": {
        "num": "25", "year": "2017", "title": "Start Festival",
        "type": "Festival Identity & Visuals",
        "tools": ["After Effects", "Illustrator"],
        "themes": ["Music", "Identity", "Motion Graphics"],
        "meta_right": "Commission<br>2017<br>Graphic Design",
    },
    "2017/prayer_room.html": {
        "num": "26", "year": "2017", "title": "Prayer Room",
        "type": "Installation",
        "tools": ["Projection Mapping", "Max/MSP"],
        "themes": ["Ritual", "Space", "Light"],
        "meta_right": "Personal project<br>2017<br>Installation",
    },
    "2019/memory_holes.html": {
        "num": "23", "year": "2019", "title": "Memory Holes",
        "type": "Interactive Installation",
        "tools": ["openFrameworks", "Computer Vision"],
        "themes": ["Memory", "Digital Amnesia", "Surveillance"],
        "meta_right": "Personal project<br>2019<br>Installation",
    },
    "2022/taming_ai.html": {
        "num": "19", "year": "2022", "title": "Taming AI",
        "type": "Interactive Performance",
        "tools": ["Machine Learning", "Python", "p5.js"],
        "themes": ["Human-Machine", "Control", "AI"],
        "meta_right": "Exhibition<br>2022<br>Interactive",
    },
    "2022/agents.html": {
        "num": "20", "year": "2022", "title": "Agents",
        "type": "Generative Software",
        "tools": ["Python", "p5.js", "Autonomous Agents"],
        "themes": ["Agency", "Emergence", "Systems"],
        "meta_right": "Personal project<br>2022<br>Generative",
    },
    "2022/botcast.html": {
        "num": "21", "year": "2022", "title": "Botcast",
        "type": "Bot-generated Podcast",
        "tools": ["GPT-3", "Text-to-Speech", "Python"],
        "themes": ["Automation", "Media", "Language"],
        "meta_right": "Team project<br>2022<br>Audio / Web",
    },
    "2022/berlin_stallwachter_party.html": {
        "num": "22", "year": "2022", "title": "Berlin Stallwachter Party",
        "type": "Live Event Visualisation",
        "tools": ["TouchDesigner", "MIDI", "Live Audio"],
        "themes": ["Party", "Live Performance", "Generative Visuals"],
        "meta_right": "Commission<br>2022<br>Live AV",
    },
    "2023/isle_of_coding.html": {
        "num": "16", "year": "2023", "title": "Live Coding",
        "type": "Live Coding Performance",
        "tools": ["Tidal Cycles", "SuperCollider", "Hydra"],
        "themes": ["Algorithmic Music", "Live Performance", "Code as Art"],
        "meta_right": "Live event<br>2023<br>Performance",
    },
    "2023/if_you_think_you_are_sleeping.html": {
        "num": "17", "year": "2023", "title": "If You Think You Are Sleeping",
        "type": "Interactive Video",
        "tools": ["p5.js", "Web Audio API"],
        "themes": ["Dreams", "Consciousness", "Time"],
        "meta_right": "Personal project<br>2023<br>Interactive Video",
    },
    "2023/berthold_leibinger.html": {
        "num": "18", "year": "2023", "title": "Berthold Leibinger",
        "type": "Generative Identity",
        "tools": ["Processing", "Illustrator"],
        "themes": ["Corporate", "Generative Design", "Brand"],
        "meta_right": "Commission<br>2023<br>Graphic Design",
    },
    "2024/voice_box.html": {
        "num": "13", "year": "2024", "title": "Voice Box",
        "type": "Speech-to-Visual Interface",
        "tools": ["Web Speech API", "Three.js", "JavaScript"],
        "themes": ["Voice", "Visualisation", "Interaction"],
        "meta_right": "Personal project<br>2024<br>Web / Interactive",
    },
    "2024/Flatware_Hardware_Software_Wetware.html": {
        "num": "14", "year": "2024", "title": "Flatware Hardware Software Wetware",
        "type": "Hybrid Object Performance",
        "tools": ["3D Printing", "Arduino", "Max/MSP"],
        "themes": ["Body", "Technology", "Materiality"],
        "meta_right": "Exhibition<br>2024<br>Installation",
    },
    "2024/meme_me.html": {
        "num": "15", "year": "2024", "title": "Meme Me",
        "type": "Internet Culture Generator",
        "tools": ["Python", "GPT", "Web Scraping"],
        "themes": ["Memes", "Culture", "Automation"],
        "meta_right": "Personal project<br>2024<br>Web",
    },
    "2025/Animated_Drawings.html": {
        "num": "01", "year": "2025", "title": "Animated Drawings",
        "type": "Generative Drawing System",
        "tools": ["Meta Animated Drawings", "p5.js", "Python"],
        "themes": ["Animation", "Children", "Generative"],
        "meta_right": "Personal project<br>2025<br>Generative",
    },
    "2025/Electronic_Petting_Zoo.html": {
        "num": "02", "year": "2025", "title": "Electronic Petting Zoo",
        "type": "Interactive Installation",
        "tools": ["Arduino", "Sensors", "p5.js"],
        "themes": ["Touch", "Animal", "Interaction"],
        "meta_right": "Commission<br>2025<br>Installation",
    },
    "2025/Bring_Your_Own_Model.html": {
        "num": "03", "year": "2025", "title": "Bring Your Own Model",
        "type": "AI-participatory Art",
        "tools": ["Machine Learning", "Python", "Web"],
        "themes": ["AI", "Participation", "Data"],
        "meta_right": "Exhibition<br>2025<br>Interactive",
    },
    "2025/Terms_Of_Confession.html": {
        "num": "04", "year": "2025", "title": "Terms Of Confession",
        "type": "Data Privacy Performance",
        "tools": ["Web", "JavaScript", "Legal Text Analysis"],
        "themes": ["Privacy", "Consent", "Language"],
        "meta_right": "Personal project<br>2025<br>Web",
    },
    "2025/OHL_Plants.html": {
        "num": "05", "year": "2025", "title": "OHL Plants",
        "type": "Living Sensor Garden",
        "tools": ["Arduino", "Plant Sensors", "p5.js"],
        "themes": ["Plants", "Biofeedback", "Environment"],
        "meta_right": "Residency<br>2025<br>Installation",
    },
    "2025/Kamuna.html": {
        "num": "06", "year": "2025", "title": "Kamuna",
        "type": "Community Web Experience",
        "tools": ["JavaScript", "WebSockets", "p5.js"],
        "themes": ["Community", "Collaboration", "Web"],
        "meta_right": "Team project<br>2025<br>Web",
    },
    "2025/Interplanetary_Texting.html": {
        "num": "07", "year": "2025", "title": "Interplanetary Texting",
        "type": "Speculative Communication Tool",
        "tools": ["JavaScript", "Web APIs", "Creative Writing"],
        "themes": ["Space", "Communication", "Speculation"],
        "meta_right": "Personal project<br>2025<br>Web / Concept",
    },
}

# ---------------------------------------------------------------------------
# CSS — no fixed row heights; all media at natural aspect ratio
# ---------------------------------------------------------------------------
STYLE = """*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior:smooth; }
body {
  font-family:'Barlow',sans-serif; font-weight:300;
  line-height:1.75; background:var(--bg); color:#1a1a1a;
  cursor:none; overflow-x:hidden;
}
:root {
  --green:#39ff14; --bg:#bdbdbd; --bg2:#b0b0b0; --bg3:#a8a8a8;
  --ink:#1a1a1a; --ink2:#3a3a3a; --ink3:#6a6a6a;
  --line:rgba(0,0,0,0.12); --line2:rgba(0,0,0,0.07);
}
#cursor {
  position:fixed; pointer-events:none; z-index:9999;
  width:8px; height:8px; border-radius:50%;
  background:var(--green); box-shadow:0 0 6px var(--green),0 0 14px var(--green);
  transform:translate(-50%,-50%); transition:width 0.15s,height 0.15s;
}
#cursor.big { width:20px; height:20px; background:transparent; border:1.5px solid var(--green); box-shadow:none; }
.site-header {
  position:sticky; top:0; z-index:100;
  display:flex; align-items:center; justify-content:space-between;
  padding:18px 44px; border-bottom:1px solid var(--line); background:var(--bg);
}
.site-header-name {
  font-family:'Barlow Condensed',sans-serif;
  font-weight:700; font-size:20px; letter-spacing:0.06em; text-transform:uppercase;
  color:#fff; text-decoration:none; cursor:pointer; transition:color 0.2s,filter 0.2s;
}
.site-header-nav { display:flex; gap:32px; }
.site-header-nav a {
  font-family:'Barlow Condensed',sans-serif;
  font-weight:300; font-size:16px; letter-spacing:0.14em; text-transform:uppercase;
  color:#fff; text-decoration:none; transition:color 0.2s,filter 0.2s;
}
.site-header-name:hover,.site-header-nav a:hover {
  color:var(--green); filter:drop-shadow(0 0 6px var(--green));
}
.project-hero {
  padding:52px 44px 36px; border-bottom:1px solid var(--line);
  display:grid; grid-template-columns:1fr auto; gap:24px; align-items:end; background:#fff;
}
.project-num {
  font-family:'Barlow Condensed',sans-serif; font-weight:700;
  font-size:13px; letter-spacing:0.35em; text-transform:uppercase;
  color:var(--ink3); margin-bottom:12px;
}
.project-title {
  font-family:'Barlow Condensed',sans-serif; font-weight:900;
  font-size:clamp(40px,7vw,100px); letter-spacing:-0.03em; text-transform:uppercase;
  color:#000; line-height:0.88;
}
.project-meta-block { text-align:right; padding-bottom:6px; }
.project-meta-block p {
  font-family:'Barlow Condensed',sans-serif; font-weight:300;
  font-size:12px; letter-spacing:0.2em; text-transform:uppercase;
  color:var(--ink3); line-height:1.8;
}
.project-body {
  display:grid; grid-template-columns:240px 1fr;
  border-bottom:1px solid var(--line); background:#fff;
}
.project-sidebar {
  padding:36px 24px 36px 44px; border-right:1px solid var(--line);
  position:sticky; top:57px; height:calc(100vh - 57px);
  overflow-y:auto; display:flex; flex-direction:column; gap:24px; background:#fff;
}
.project-sidebar::-webkit-scrollbar { width:2px; }
.project-sidebar::-webkit-scrollbar-thumb { background:#ddd; }
.sidebar-section-label {
  font-family:'Barlow Condensed',sans-serif; font-weight:700;
  font-size:10px; letter-spacing:0.4em; text-transform:uppercase;
  color:#999; margin-bottom:8px; padding-bottom:6px; border-bottom:1px solid #e8e8e8;
}
.sidebar-tag {
  font-family:'Barlow Condensed',sans-serif; font-weight:400;
  font-size:13px; letter-spacing:0.04em; color:#444; padding:2px 0; line-height:1.5;
}
.project-content { padding:40px 44px 80px 44px; background:#fff; }
.project-lead {
  font-family:'Barlow Condensed',sans-serif; font-weight:300;
  font-size:clamp(20px,2.2vw,28px); letter-spacing:0.01em; line-height:1.35;
  color:#444; margin-bottom:32px; width:100%;
}
.content-h2 {
  font-family:'Barlow Condensed',sans-serif; font-weight:700;
  font-size:11px; letter-spacing:0.4em; text-transform:uppercase; color:#999;
  margin:36px 0 12px; padding-top:36px; border-top:1px solid #e8e8e8;
}
.project-content p {
  font-family:'Barlow',sans-serif; font-weight:300;
  font-size:15px; line-height:1.85; color:#444; width:100%; margin-bottom:16px;
}
.project-content p em { color:#1a1a1a; font-style:italic; }

/* ── MEDIA LAYOUT ── natural aspect ratios, no fixed heights ── */
.media-block { margin:28px 0; width:100%; }

/* single item: full width, height follows content */
.media-block.solo .media-item { width:100%; }

/* 2-column grid: items sit side by side, each at its own natural height */
.media-block.duo,
.media-block.multi {
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:3px;
}

/* last odd item in a multi grid spans both columns */
.media-block.multi .media-item.span-full {
  grid-column:1 / -1;
}

/* 3-item layout: first full width, then two side by side */
.media-block.trio { display:grid; gap:3px; grid-template-columns:1fr 1fr; }
.media-block.trio .media-item:first-child { grid-column:1 / -1; }

/* every media item: let content define height */
.media-item { width:100%; overflow:hidden; background:#f0f0f0; }

/* images: full width, height auto — NEVER crop */
.media-item img {
  width:100%; height:auto; display:block;
}

/* videos: 16:9 aspect-ratio box so they don't collapse before metadata loads */
.media-item .video-wrap {
  position:relative; width:100%; padding-top:56.25%;
}
.media-item .video-wrap video {
  position:absolute; inset:0; width:100%; height:100%; display:block; object-fit:contain;
  background:#000;
}

/* iframes (YouTube, Vimeo, etc.): 16:9 */
.media-item .iframe-wrap {
  position:relative; width:100%; padding-top:56.25%;
}
.media-item .iframe-wrap iframe {
  position:absolute; inset:0; width:100%; height:100%; border:none; display:block;
}

.media-caption {
  font-family:'Barlow Condensed',sans-serif; font-weight:300;
  font-size:11px; letter-spacing:0.15em; text-transform:uppercase;
  color:#999; margin-top:8px; width:100%;
}
.project-footer {
  padding:22px 44px; display:flex; align-items:center; justify-content:space-between;
  background:#fff; border-top:1px solid #e8e8e8;
}
.footer-left {
  font-family:'Barlow Condensed',sans-serif; font-weight:300;
  font-size:11px; letter-spacing:0.3em; text-transform:uppercase; color:#999;
}
.footer-back {
  font-family:'Barlow Condensed',sans-serif; font-weight:700;
  font-size:13px; letter-spacing:0.2em; text-transform:uppercase;
  color:#1a1a1a; text-decoration:none; border-bottom:1px solid #999;
  padding-bottom:1px; transition:color 0.18s,border-color 0.18s,filter 0.18s;
}
.footer-back:hover { color:var(--green); border-color:var(--green); filter:drop-shadow(0 0 4px var(--green)); }"""

JS = """var cur=document.getElementById('cursor');
document.addEventListener('mousemove',function(e){cur.style.left=e.clientX+'px';cur.style.top=e.clientY+'px';});
document.addEventListener('mouseover',function(e){if(e.target.closest('a,button'))cur.classList.add('big');});
document.addEventListener('mouseout',function(e){if(e.target.closest('a,button'))cur.classList.remove('big');});"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).strip()


def is_video(tag):
    return bool(re.match(r'<video', tag, re.IGNORECASE))

def is_iframe(tag):
    return bool(re.match(r'<iframe', tag, re.IGNORECASE))


def wrap_tag(tag):
    """Wrap a bare media tag in a .media-item div with appropriate inner wrapper."""
    if is_video(tag):
        return f'<div class="media-item"><div class="video-wrap">{tag}</div></div>'
    elif is_iframe(tag):
        return f'<div class="media-item"><div class="iframe-wrap">{tag}</div></div>'
    else:
        # img — no wrapper needed, just let it be natural height
        return f'<div class="media-item">{tag}</div>'


# ---------------------------------------------------------------------------
# Media grid builder — natural aspect ratios
# ---------------------------------------------------------------------------
def make_media_grid(tags, page_title):
    if not tags:
        return ''

    count = len(tags)
    items = [wrap_tag(t) for t in tags]

    if count == 1:
        block_class = 'media-block solo'
        inner = items[0]

    elif count == 2:
        block_class = 'media-block duo'
        inner = ''.join(items)

    elif count == 3:
        block_class = 'media-block trio'
        inner = ''.join(items)

    else:
        # 4+ items: 2-column grid, last item spans full width if count is odd
        block_class = 'media-block multi'
        if count % 2 == 1:
            # make last item span both columns
            last = items[-1].replace('class="media-item"', 'class="media-item span-full"', 1)
            inner = ''.join(items[:-1]) + last
        else:
            inner = ''.join(items)

    return (
        f'<div class="{block_class}">{inner}</div>\n'
        f'<div class="media-caption">{page_title}</div>'
    )


# ---------------------------------------------------------------------------
# Content extractor
# ---------------------------------------------------------------------------
def extract_content(html, title_override=None):
    if title_override:
        page_title = title_override
    else:
        m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
        if m:
            page_title = strip_tags(m.group(1))
        else:
            t = re.search(r'<title[^>]*>(.*?)(?:\s*[—–-]\s*Weird.*?)?</title>',
                          html, re.DOTALL | re.IGNORECASE)
            page_title = strip_tags(t.group(1)).strip() if t else "Project"
        if not page_title or page_title == "Project":
            pt = re.search(r'class=["\']project-title["\'][^>]*>(.*?)</div>',
                           html, re.DOTALL | re.IGNORECASE)
            if pt:
                page_title = strip_tags(pt.group(1))

    body_m = re.search(
        r'<!-- MAIN CONTENT -->(.*?)(?:<div[^>]+class=["\'][^"\']*footer|<footer\b)',
        html, re.DOTALL | re.IGNORECASE)
    if not body_m:
        body_m = re.search(
            r'class=["\']header-bar["\'].*?</div>\s*</div>'
            r'(.*?)(?:<div[^>]+class=["\'][^"\']*footer|<footer\b|\Z)',
            html, re.DOTALL | re.IGNORECASE)
    if not body_m:
        body_m = re.search(
            r'<main[^>]*class=["\']project-content["\'][^>]*>(.*?)</main>',
            html, re.DOTALL | re.IGNORECASE)
    raw = body_m.group(1).strip() if body_m else html

    raw = re.sub(r'<h1[^>]*>.*?</h1>', '', raw, flags=re.DOTALL | re.IGNORECASE)

    media_tags = {}
    media_counter = [0]

    def capture_media(tag_html):
        idx = media_counter[0]
        media_tags[idx] = tag_html.strip()
        media_counter[0] += 1
        return f'__MEDIA__{idx}__'

    # strip old media-block / media-grid wrappers first
    raw = re.sub(
        r'<div[^>]*class=["\'][^"\']*media-block[^"\']*["\'][^>]*>.*?</div>'
        r'(?:\s*<div[^>]*class=["\'][^"\']*media-caption[^"\']*["\'][^>]*>.*?</div>)?',
        lambda m: capture_media(m.group(0)),
        raw, flags=re.DOTALL | re.IGNORECASE)

    raw = re.sub(
        r'<div[^>]*class=["\'][^"\']*media-grid[^"\']*["\'][^>]*>.*?</div>'
        r'(?:\s*<div[^>]*class=["\'][^"\']*media-caption[^"\']*["\'][^>]*>.*?</div>)?',
        lambda m: capture_media(m.group(0)),
        raw, flags=re.DOTALL | re.IGNORECASE)

    raw = re.sub(
        r'<div[^>]*class=["\'][^"\']*media-container[^"\']*["\'][^>]*>.*?</div>',
        lambda m: capture_media(m.group(0)),
        raw, flags=re.DOTALL | re.IGNORECASE)

    raw = re.sub(
        r'<(video|iframe)[^>]*>.*?</\1>|<img[^>]*/?>',
        lambda m: capture_media(m.group(0)),
        raw, flags=re.DOTALL | re.IGNORECASE)

    parts = re.split(
        r'(<h2[^>]*>.*?</h2>|<div[^>]*class=["\']content-h2["\'][^>]*>.*?</div>)',
        raw, flags=re.DOTALL | re.IGNORECASE)

    sections = []
    cur_heading = None
    cur_paras = []

    def flush():
        if cur_paras or cur_heading is not None:
            sections.append((cur_heading, list(cur_paras)))

    for part in parts:
        if re.match(r'<h2|<div[^>]*class=["\']content-h2', part, re.IGNORECASE):
            flush()
            cur_heading = strip_tags(part)
            cur_paras = []
        else:
            chunks = re.split(
                r'(<p[^>]*>.*?</p>|__MEDIA__\d+__)',
                part, flags=re.DOTALL | re.IGNORECASE)
            for chunk in chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue
                if re.match(r'__MEDIA__\d+__', chunk):
                    cur_paras.append(chunk)
                elif re.match(r'<p', chunk, re.IGNORECASE):
                    inner = re.sub(r'^<p[^>]*>|</p>$', '', chunk,
                                   flags=re.IGNORECASE).strip()
                    if inner and 'project-lead' not in chunk:
                        cur_paras.append(inner)

    flush()
    return page_title, sections, media_tags


# ---------------------------------------------------------------------------
# Flatten captured wrappers → bare individual media tags
# ---------------------------------------------------------------------------
def flatten_media_tags(raw_tags):
    bare = []
    for tag in raw_tags:
        found = re.findall(
            r'<(?:video|iframe)[^>]*>.*?</(?:video|iframe)>|<img[^>]*/?>'
            , tag, flags=re.DOTALL | re.IGNORECASE)
        if found:
            bare.extend(found)
        else:
            bare.append(tag)
    return bare


# ---------------------------------------------------------------------------
# Content builder
# ---------------------------------------------------------------------------
def build_content(page_title, sections, media_tags):
    raw_tags = [media_tags[i] for i in sorted(media_tags)]
    all_media = flatten_media_tags(raw_tags)
    out = []
    lead_done = False
    media_inserted = False

    def maybe_insert_media():
        nonlocal media_inserted
        if not media_inserted and all_media:
            out.append(make_media_grid(all_media, page_title))
            media_inserted = True

    for heading, paras in sections:
        if heading:
            maybe_insert_media()
            out.append(f'<div class="content-h2">{heading}</div>')
        for item in paras:
            if re.match(r'__MEDIA__\d+__', item):
                continue
            elif not lead_done and not heading:
                out.append(f'<p class="project-lead">{item}</p>')
                lead_done = True
                maybe_insert_media()
            else:
                out.append(f'<p>{item}</p>')

    maybe_insert_media()
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Sidebar builder
# ---------------------------------------------------------------------------
def build_sidebar(meta):
    parts = [
        f'<div><div class="sidebar-section-label">Type</div>'
        f'<div class="sidebar-tag">{meta["type"]}</div></div>',
        f'<div><div class="sidebar-section-label">Year</div>'
        f'<div class="sidebar-tag">{meta["year"]}</div></div>',
    ]
    if meta.get("tools"):
        tags = ''.join(f'<div class="sidebar-tag">{t}</div>' for t in meta["tools"])
        parts.append(f'<div><div class="sidebar-section-label">Tools</div>{tags}</div>')
    if meta.get("themes"):
        tags = ''.join(f'<div class="sidebar-tag">{t}</div>' for t in meta["themes"])
        parts.append(f'<div><div class="sidebar-section-label">Themes</div>{tags}</div>')
    return '\n    '.join(parts)


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------
def depth_prefix(rel_path):
    """'2016/reflections.html' -> '../../'"""
    depth = rel_path.count(os.sep)
    return '../' * (depth + 1)


# ---------------------------------------------------------------------------
# Page assembler
# ---------------------------------------------------------------------------
def build_page(page_title, meta, sidebar_html, content_html, pfx):
    num  = meta["num"]
    year = meta["year"]
    mr   = meta.get("meta_right", f"Project<br>{year}")
    work_href  = f"{pfx}work.html"
    about_href = f"{pfx}work/bio.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{page_title} — Weird With Code</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;700;900&family=Barlow:wght@300;400&display=swap" rel="stylesheet">
<style>
{STYLE}
</style>
</head>
<body>
<div id="cursor"></div>

<header class="site-header">
  <a href="{pfx}index.html" class="site-header-name">Weird With Code</a>
  <nav class="site-header-nav">
    <a href="{work_href}">Work</a>
    <a href="{about_href}">About</a>
  </nav>
</header>

<div class="project-hero">
  <div>
    <div class="project-num">{num} / {year}</div>
    <div class="project-title">{page_title}</div>
  </div>
  <div class="project-meta-block"><p>{mr}</p></div>
</div>

<div class="project-body">
  <aside class="project-sidebar">
    {sidebar_html}
  </aside>
  <main class="project-content">
{content_html}
  </main>
</div>

<footer class="project-footer">
  <a href="{work_href}" class="footer-back">← Back to Work</a>
  <span class="footer-left">Jiyo · Aur · Jeene · Do</span>
</footer>

<script>
{JS}
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    work_dir   = os.path.join(script_dir, 'work')

    if not os.path.isdir(work_dir):
        print(f"ERROR: 'work/' not found at {work_dir}")
        print("Run this script from the root of your site folder.")
        return

    updated, skipped = 0, 0

    for root, dirs, files in os.walk(work_dir):
        dirs[:] = sorted(d for d in dirs if not d.startswith('__'))
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            if fname in ('bio.html', 'contact.html'):
                print(f"  skip (bio/contact): {fname}")
                continue

            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, work_dir)

            if rel_path not in META:
                print(f"  skip (no meta):     {rel_path}")
                skipped += 1
                continue

            print(f"  updating:           {rel_path}")
            meta = META[rel_path]

            with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                old_html = f.read()

            page_title, sections, media_tags = extract_content(
                old_html, title_override=meta.get("title"))
            sidebar_html = build_sidebar(meta)
            content_html = build_content(page_title, sections, media_tags)
            pfx          = depth_prefix(rel_path)
            new_html     = build_page(page_title, meta, sidebar_html, content_html, pfx)

            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(new_html)

            updated += 1

    print(f"\nDone — {updated} pages updated, {skipped} skipped (no metadata entry).")


if __name__ == '__main__':
    main()