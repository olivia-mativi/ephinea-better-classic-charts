import json

with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "r") as f:
    itemsdb = json.loads(f.read())

item_list = []
for item_data in itemsdb:
    item_list.append(item_data["item"])

by_item = {item: [] for item in item_list}

for item_data in itemsdb:
    by_item[item_data["item"]].append({
        "source": item_data["source"],
        "sectionId": item_data["sectionId"],
        "difficulty": item_data["difficulty"],
        "episode": item_data["episode"],
        "rate": item_data["rate"]
    })

sorted = dict(sorted(by_item.items(), key=lambda x: x[0]))

with open("/home/olivia/ephinea-better-classic-charts/book/src/by_item.json", "w") as f:
    f.write(json.dumps(sorted, indent=4))