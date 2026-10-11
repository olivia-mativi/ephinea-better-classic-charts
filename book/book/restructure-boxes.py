import json

CLEAR_FILE = False
active_file = "boxes-n-e2.json"
difficulty = "Normal"
episode = "E2"
top_lvl_key = "normal"

if CLEAR_FILE:
    with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "w") as f:
        f.write("[]")

with open(f"/home/olivia/ephinea-better-classic-charts/book/src/finished_json/{active_file}", "r") as f:
    data = json.loads(f.read())

drop_data = []
try:
    with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "r") as f:
        drop_data = json.loads(f.read())
        for area in data[top_lvl_key]:
            for drop in area["drops"]:
                for sidDrop in drop["drops"]:
                    try:
                        drop_data.append(
                            {
                                "item": sidDrop["item"],
                                "source": f"{area['area']} - Box",
                                "episode": episode,
                                "difficulty": difficulty,
                                "sectionId": drop["sectionId"],
                                "rate": sidDrop["rate"]
                            }
                        )
                    except:
                        print(f"skipping drop for {drop["sectionId"]} - {drop["difficulty"]} - {drop["episode"]}")
    with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "w") as f:
        f.write(json.dumps(drop_data, indent=4))
except FileNotFoundError:
    with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "w") as f:
        for area in data["normal"]:
            for drop in area["drops"]:
                drop_data.append(
                    {
                        "item": drop["item"],
                        "source": f"{area['area']} - Box",
                        "episode": drop["episode"],
                        "difficulty": drop["difficulty"],
                        "sectionId": drop["sectionId"],
                        "rate": drop["totalDropRateFraction"]
                    }
                )
        f.write(json.dumps(drop_data, indent=4))
    