import json
TITLE = "Availability by Section ID"

with open("/home/olivia/ephinea-better-classic-charts/book/src/availability_by_sectionid.json", "r") as f:
    data = json.loads(f.read())

with open("/home/olivia/ephinea-better-classic-charts/book/src/chapter_1.md", "w") as f:
    f.write("# " + TITLE + "\n\n")
    f.write("This page shows the availability of items by section ID.\n\n")
    section_ids = sorted(data.keys())
    for section_id in section_ids:
        f.write("## " + section_id + "\n\n")
        f.write("### Available Items" + "\n\n")
        f.write("| Item | Drop Info |\n")
        f.write("|------|-----------|\n")
        for item in data[section_id]["Available"]["List"]:
            drop_info = (
                "<table style=\"width: 100%;\"><thead><tr>"
                "<th>Difficulty</th><th>Source</th><th>Episode</th>"
                "<th>Rate</th><th>Percentage</th>"
                "</tr></thead><tbody>"
            )
            for drop_origin in data[section_id]["Available"][item]:
                numerator, denominator = drop_origin["rate"].split("/", 1)
                percentage = float(numerator) / float(denominator) * 100
                fraction = (
                    "<span style=\"white-space: nowrap;\"><sup>"
                    + numerator
                    + "</sup>/<sub>"
                    + denominator
                    + "</sub></span>"
                )
                drop_info += (
                    "<tr><td>" + drop_origin["difficulty"] + "</td>"
                    "<td>" + drop_origin["source"] + "</td>"
                    "<td>" + drop_origin["episode"] + "</td>"
                    "<td>" + fraction + "</td>"
                    "<td>" + f"{percentage:.4f}%" + "</td></tr>"
                )
            f.write("| " + item + " | " + drop_info + "</tbody></table> |\n")

        f.write("### Unavailable Items" + "\n\n")
        for item in data[section_id]["Unavailable"]:
            f.write("- " + item + "\n")