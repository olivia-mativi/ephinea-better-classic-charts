import html
import json
import re
from pathlib import Path


TITLE = "Availability by Item"
SOURCE_DIR = Path(__file__).parent
DATA_PATH = SOURCE_DIR / "availability_by_item.json"
BLACKLIST_PATH = SOURCE_DIR / "section_ids" / "resources" / "blacklist"
CHAPTER_PATH = SOURCE_DIR / "chapter_2.md"
SUMMARY_PATH = SOURCE_DIR / "SUMMARY.md"
RESOURCE_DIR = SOURCE_DIR / "section_ids" / "resources"


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
		"<th>Section ID</th><th>Difficulty</th><th>Source</th>"
		"<th>Episode</th><th>Rate</th><th>Percentage</th>"
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
		section_id = html.escape(drop_origin["sectionId"])
		image_name = f"48px-{drop_origin['sectionId']}_icon.webp"
		image_path = (
			f"./section_ids/resources/{slug(image_name)}"
			if not (RESOURCE_DIR / image_name).exists()
			else f"./section_ids/resources/{image_name}"
		)
		image = (
			f'<img src="{html.escape(image_path)}" alt="{section_id}" '
			'width="16">'
		)
		drop_info += (
			"<tr><td align='center'>"
			+ image
			+ "</td><td>"
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

items = sorted(item for item in data if item not in blacklist)
item_groups = group_by_initial(items)

with CHAPTER_PATH.open("w") as chapter_file:
	chapter_file.write(f"# {TITLE}\n\n")
	chapter_file.write("Select an item to view its availability.\n\n")
	chapter_file.write("## Contents\n\n")
	chapter_file.write(
		"Alphabet: "
		+ " &middot; ".join(
			f"[{initial}](#items-{slug(initial)})" for initial in item_groups
		)
		+ "\n\n"
	)

	for initial, item_names in item_groups.items():
		chapter_file.write(
			f'<a id="items-{slug(initial)}"></a>\n'
			f"<strong>{initial}</strong>\n\n"
		)
		chapter_file.write(
			'<table style="width: 100%;">'
			'<colgroup><col style="width: 20%;"><col style="width: 80%;">'
			"</colgroup><thead><tr><th>Item</th><th>Drop Info</th>"
			"</tr></thead><tbody>"
		)
		for item in item_names:
			drop_origins = [
				drop_origin
				for section_id in data[item]["Available"]["Ids"]
				for drop_origin in data[item]["Available"][section_id]
			]
			drop_info = render_drop_info(drop_origins)
			chapter_file.write(
				'<tr><td style="vertical-align: top;">'
				f'<a id="item-{slug(item)}"></a>{html.escape(item)}'
				"</td><td>"
				+ drop_info
				+ "</td></tr>"
			)
		chapter_file.write("</tbody></table>\n\n")

with SUMMARY_PATH.open("w") as summary_file:
	summary_file.write("# Summary\n\n")
	summary_file.write("- [Availability by Section ID](./chapter_1.md)\n")
	for section_id in sorted(
		json.loads((SOURCE_DIR / "availability_by_sectionid.json").read_text())
	):
		summary_file.write(
			f"  - [{section_id}](./section_ids/{slug(section_id)}.md)\n"
		)
	summary_file.write("- [Availability by Item](./chapter_2.md)\n")
	summary_file.write("- [Section ID Recommendations](./chapter_3.md)\n")