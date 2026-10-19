import html
import json
import re
from pathlib import Path


TITLE = "Availability by Section ID"
SOURCE_DIR = Path(__file__).parent
DATA_PATH = SOURCE_DIR / "availability_by_sectionid.json"
BLACKLIST_PATH = SOURCE_DIR / "section_ids" / "resources" / "blacklist"
CHAPTER_PATH = SOURCE_DIR / "chapter_1.md"
SUMMARY_PATH = SOURCE_DIR / "SUMMARY.md"
SECTION_DIR = SOURCE_DIR / "section_ids"


def slug(value):
    return re.sub(r"[^a-z0-9-]", "-", value.lower()).strip("-")


def group_by_initial(items):
    groups = {}
    for item in items:
        groups.setdefault(item[0].upper(), []).append(item)
    return groups


def render_drop_info(drop_origins):
    drop_info = (
        '<table style="width: 100%;"><thead><tr>'
        "<th>Difficulty</th><th>Source</th><th>Episode</th>"
        "<th>Rate</th><th>Percentage</th>"
        "</tr></thead><tbody>"
    )
    for drop_origin in drop_origins:
        numerator, denominator = drop_origin["rate"].split("/", 1)
        percentage = float(numerator) / float(denominator) * 100
        fraction = (
            '<span style="white-space: nowrap;"><sup>'
            + html.escape(numerator)
            + "</sup>/<sub>"
            + html.escape(denominator)
            + "</sub></span>"
        )
        drop_info += (
            "<tr><td>"
            + html.escape(drop_origin["difficulty"])
            + "</td><td>"
            + html.escape(drop_origin["source"])
            + "</td><td>"
            + html.escape(drop_origin["episode"])
            + "</td><td>"
            + fraction
            + "</td><td>"
            + f"{percentage:.4f}%"
            + "</td></tr>"
        )
    return drop_info + "</tbody></table>"


with DATA_PATH.open("r") as source_file:
    data = json.load(source_file)

with BLACKLIST_PATH.open("r") as blacklist_file:
    blacklist = {
        line.strip() for line in blacklist_file if line.strip()
    }

SECTION_DIR.mkdir(exist_ok=True)
section_ids = sorted(data)

with CHAPTER_PATH.open("w") as chapter_file:
    chapter_file.write(f"# {TITLE}\n\n")
    chapter_file.write("Select a section ID to view its item availability.\n\n")
    for section_id in section_ids:
        chapter_file.write(
            f"- [{section_id}](./section_ids/{slug(section_id)}.md)\n"
        )

for section_id in section_ids:
    section_data = data[section_id]
    available_items = [
        item
        for item in section_data["Available"]["List"]
        if item not in blacklist
    ]
    available_groups = group_by_initial(available_items)
    exclusive_items = [
        item
        for item in available_items
        if all(
            item not in data[other_section_id]["Available"]["List"]
            for other_section_id in section_ids
            if other_section_id != section_id
        )
    ]
    exclusive_groups = group_by_initial(exclusive_items)
    unavailable_groups = group_by_initial(
        item for item in section_data["Unavailable"] if item not in blacklist
    )

    with (SECTION_DIR / f"{slug(section_id)}.md").open("w") as section_file:
        section_file.write(f"# {section_id}\n\n")
        section_file.write("## Contents\n\n")
        available_links = " &middot; ".join(
            f"[{initial}](#available-{slug(initial)})"
            for initial in available_groups
        )
        exclusive_links = " &middot; ".join(
            f"[{initial}](#exclusive-{slug(initial)})"
            for initial in exclusive_groups
        )
        unavailable_links = " &middot; ".join(
            f"[{initial}](#unavailable-{slug(initial)})"
            for initial in unavailable_groups
        )
        section_file.write(
            f"- [Available Items](#available-items): {available_links}\n"
        )
        section_file.write(
            f"- [Exclusive Items](#exclusive-items): {exclusive_links}\n"
        )
        section_file.write(
            f"- [Unavailable Items](#unavailable-items): {unavailable_links}\n"
        )

        section_file.write('\n<a id="available-items"></a>\n## Available Items\n\n')
        for initial, items in available_groups.items():
            section_file.write(
                f'<a id="available-{slug(initial)}"></a>\n'
                f'<strong>{initial}</strong>\n\n'
            )
            section_file.write(
                '<table style="width: 100%; table-layout: fixed;">'
                '<colgroup><col style="width: 20%;"><col style="width: 80%;">'
                "</colgroup><thead><tr><th>Item</th><th>Drop Info</th>"
                "</tr></thead><tbody>"
            )
            for item in items:
                drop_info = render_drop_info(section_data["Available"][item])
                section_file.write(
                    '<tr><td style="vertical-align: top;">'
                    + html.escape(item)
                    + "</td><td>"
                    + drop_info
                    + "</td></tr>"
                )
            section_file.write("</tbody></table>\n\n")

        section_file.write(
            '<a id="exclusive-items"></a>\n## Exclusive Items\n\n'
        )
        for initial, items in exclusive_groups.items():
            section_file.write(
                f'<a id="exclusive-{slug(initial)}"></a>\n'
                f'<strong>{initial}</strong>\n\n'
            )
            section_file.write(
                '<table style="width: 100%; table-layout: fixed;">'
                '<colgroup><col style="width: 20%;"><col style="width: 80%;">'
                "</colgroup><thead><tr><th>Item</th><th>Drop Info</th>"
                "</tr></thead><tbody>"
            )
            for item in items:
                drop_info = render_drop_info(section_data["Available"][item])
                section_file.write(
                    '<tr><td style="vertical-align: top;">'
                    + html.escape(item)
                    + "</td><td>"
                    + drop_info
                    + "</td></tr>"
                )
            section_file.write("</tbody></table>\n\n")

        section_file.write(
            '<a id="unavailable-items"></a>\n## Unavailable Items\n\n'
        )
        for initial, items in unavailable_groups.items():
            section_file.write(
                f'<a id="unavailable-{slug(initial)}"></a>\n'
                f'<strong>{initial}</strong>\n\n'
            )
            for item in items:
                section_file.write(f"- {html.escape(item)}\n")
            section_file.write("\n")

with SUMMARY_PATH.open("w") as summary_file:
    summary_file.write("# Summary\n\n")
    summary_file.write("- [Availability by Section ID](./chapter_1.md)\n")
    for section_id in section_ids:
        summary_file.write(
            f"  - [{section_id}](./section_ids/{slug(section_id)}.md)\n"
        )
    summary_file.write("- [Availability by Item](./chapter_2.md)\n")
    summary_file.write("- [Section ID Recommendations](./chapter_3.md)\n")