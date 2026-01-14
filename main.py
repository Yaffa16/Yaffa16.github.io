import os
from bs4 import BeautifulSoup

work_folder = "work"

def create_artwork_tag(soup, year, html_file, image_file):
    title = os.path.splitext(html_file)[0].replace("_", " ").title()

    a = soup.new_tag(
        "a",
        href=f"work/{year}/{html_file}",
        **{"class": "artwork-link"}
    )

    img = soup.new_tag(
        "img",
        src=f"work/{year}/{image_file}",
        alt=f"{title} {year}"
    )

    caption = soup.new_tag("span", **{"class": "artwork-caption"})
    title_span = soup.new_tag("span", **{"class": "artwork-title"})
    title_span.string = title
    year_span = soup.new_tag("span", **{"class": "artwork-year"})
    year_span.string = year

    caption.append(title_span)
    caption.append(year_span)

    a.append(img)
    a.append(caption)

    return a


def update_index_html(index_file):
    with open(index_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    projects_grid = soup.find("div", id="projectsGrid")
    if not projects_grid:
        print("❌ projectsGrid not found")
        return

    # ---------------------------------------
    # 1. Scan filesystem → authoritative list
    # ---------------------------------------
    fs_artworks = {}  # year -> set of html files
    fs_hrefs = set()

    for year in os.listdir(work_folder):
        year_path = os.path.join(work_folder, year)
        if not os.path.isdir(year_path):
            continue

        html_files = {
            f for f in os.listdir(year_path)
            if f.endswith(".html")
        }

        if html_files:
            fs_artworks[year] = html_files
            for f in html_files:
                fs_hrefs.add(f"work/{year}/{f}")

    # ---------------------------------------
    # 2. Remove stale entries from index.html
    # ---------------------------------------
    for a in projects_grid.find_all("a", class_="artwork-link"):
        href = a.get("href")
        if href not in fs_hrefs:
            print(f"🗑 Removed stale entry: {href}")
            a.decompose()

    # ---------------------------------------
    # 3. Remove empty year sections
    # ---------------------------------------
    for year_section in projects_grid.find_all("div", class_="year-section"):
        if not year_section.find("a", class_="artwork-link"):
            year_section.decompose()

    # ---------------------------------------
    # 4. Add missing artworks (latest year first)
    # ---------------------------------------
    for year in sorted(fs_artworks.keys(), reverse=True):
        year_section = projects_grid.find("div", id=f"year-{year}")

        if not year_section:
            year_section = soup.new_tag(
                "div",
                id=f"year-{year}",
                **{"class": "year-section"}
            )
            projects_grid.insert(0, "\n\n    ")
            projects_grid.insert(1, year_section)

        for html_file in sorted(fs_artworks[year]):
            href = f"work/{year}/{html_file}"

            if projects_grid.find("a", href=href):
                continue

            base = os.path.splitext(html_file)[0]
            image_file = None

            for ext in (".jpg", ".png", ".jpeg"):
                candidate = base + ext
                if os.path.exists(os.path.join(work_folder, year, candidate)):
                    image_file = candidate
                    break

            if not image_file:
                print(f"⚠️ No image for {year}/{html_file}")
                continue

            artwork = create_artwork_tag(soup, year, html_file, image_file)
            year_section.append("\n        ")
            year_section.append(artwork)

            print(f"➕ Added {year}/{html_file}")

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print("✅ index.html fully synchronized with /work")


update_index_html("Hyperlinks/index.html")
