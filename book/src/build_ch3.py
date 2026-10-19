import html
import json
import re
from pathlib import Path


TITLE = "Section ID Diff Rankings"
SOURCE_DIR = Path(__file__).parent
DATA_PATH = SOURCE_DIR / "availability_by_sectionid.json"
BLACKLIST_PATH = SOURCE_DIR / "section_ids" / "resources" / "blacklist"
CHAPTER_PATH = SOURCE_DIR / "chapter_3.md"
SUMMARY_PATH = SOURCE_DIR / "SUMMARY.md"
RESOURCE_DIR = SOURCE_DIR / "section_ids" / "resources"


def slug(value):
    return re.sub(r"[^a-z0-9-]", "-", value.lower()).strip("-")


def render_section_id(section_id):
    image_name = f"48px-{section_id}_icon.webp"
    image_path = f"./section_ids/resources/{image_name}"
    image = (
        f'<img src="{html.escape(image_path)}" '
        f'alt="{html.escape(section_id)}" width="16">'
    )
    return f"{image} {html.escape(section_id)}"


with DATA_PATH.open("r") as source_file:
    data = json.load(source_file)

with BLACKLIST_PATH.open("r") as blacklist_file:
    blacklist = {
        line.strip() for line in blacklist_file if line.strip()
    }

section_ids = sorted(data)
items_by_section = {
    section_id: {
        item
        for item in section_data["Available"]["List"]
        if item not in blacklist
    }
    for section_id, section_data in data.items()
}

with CHAPTER_PATH.open("w") as chapter_file:
    chapter_file.write(f"# {TITLE}\n\n")
    chapter_file.write(
        "For each section ID, the table ranks other section IDs by "
        "the number of additional items you would then gain access to. "
        "This might be interesting for deciding which section ID to choose when "
        "making characters after your first.\n\n"
    )
    chapter_file.write("## Contents\n\n")
    chapter_file.write(
        "Section IDs: "
        + " &middot; ".join(
            f"[{section_id}](#section-{slug(section_id)})"
            for section_id in section_ids
        )
        + "\n\n"
    )

    for section_id in section_ids:
        titular_items = items_by_section[section_id]
        rankings = []
        for other_section_id in section_ids:
            if other_section_id == section_id:
                continue
            unlocked_items = sorted(
                items_by_section[other_section_id] - titular_items
            )
            rankings.append((len(unlocked_items), other_section_id, unlocked_items))
        rankings.sort(key=lambda ranking: (-ranking[0], ranking[1]))

        chapter_file.write(
            f'<a id="section-{slug(section_id)}"></a>\n'
            f"## {html.escape(section_id)}\n\n"
        )
        chapter_file.write(
            '<table style="width: 100%; table-layout: fixed;">'
            '<colgroup><col style="width: 20%;"><col style="width: 80%;">'
            "</colgroup><thead><tr>"
            "<th>Section ID</th><th>Additional Items Available</th>"
            "</tr></thead><tbody>"
        )
        for count, other_section_id, unlocked_items in rankings:
            item_list = "<br>".join(html.escape(item) for item in unlocked_items)
            chapter_file.write(
                '<tr><td style="vertical-align: top;">'
                + render_section_id(other_section_id)
                + f"<br><small>{count} items</small>"
                + "</td><td><details><summary>View Items</summary>"
                + item_list
                + "</details></td></tr>"
            )
        chapter_file.write("</tbody></table>\n\n")

with SUMMARY_PATH.open("w") as summary_file:
    summary_file.write("# Summary\n\n")
    summary_file.write("- [Availability by Section ID](./chapter_1.md)\n")
    for section_id in section_ids:
        summary_file.write(
            f"  - [{section_id}](./section_ids/{slug(section_id)}.md)\n"
        )
    summary_file.write("- [Availability by Item](./chapter_2.md)\n")
    summary_file.write(f"- [{TITLE}](./chapter_3.md)\n")
