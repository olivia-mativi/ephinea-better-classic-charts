import json

CLEAR_FILE = False
active_file = "n-e2.json"
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
        for monster in data[top_lvl_key]:
            for drop in monster["drops"]:
                try:
                    drop_data.append(
                        {
                            "item": drop["item"],
                            "source": monster["monster"],
                            "episode": episode,
                            "difficulty": difficulty,
                            "sectionId": drop["sectionId"],
                            "rate": drop["rate"]
                        }
                    )
                except:
                    print(f"skipping drop for {monster['monster']} - {drop['item']}")
    with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "w") as f:
        f.write(json.dumps(drop_data, indent=4))
except FileNotFoundError:
    with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "w") as f:
        for monster in data["ultimate"]:
            for drop in monster["drops"]:
                drop_data.append(
                    {
                        "item": drop["item"],
                        "source": monster["monster"],
                        "episode": episode,
                        "difficulty": difficulty,
                        "sectionId": drop["sectionId"],
                        "rate": drop["totalDropRateFraction"]
                    }
                )
        f.write(json.dumps(drop_data, indent=4))
    