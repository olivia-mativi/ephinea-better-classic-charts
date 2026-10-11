import json

SECTION_ID_LIST = ["Viridia", "Greenill", "Skyly", "Bluefull", "Purplenum", "Pinkal", "Redria", "Oran", "Yellowboze", "Whitill"]

with open("/home/olivia/ephinea-better-classic-charts/book/src/itemsdb.json", "r") as f:
    itemsdb = json.loads(f.read())

availability_by_sectionid = {id: {"Available": {"List": []}, "Unavailable": []} for id in SECTION_ID_LIST}

for item in itemsdb:
    if item["item"] not in availability_by_sectionid[item["sectionId"]]["Available"]["List"]:
        availability_by_sectionid[item["sectionId"]]["Available"]["List"].append(item["item"])
        availability_by_sectionid[item["sectionId"]]["Available"][item["item"]] = []
    availability_by_sectionid[item["sectionId"]]["Available"][item["item"]].append({"source": item["source"],
                                                                                    "episode": item["episode"],
                                                                                    "difficulty": item["difficulty"],
                                                                                    "rate": item["rate"]})

for sectionid in SECTION_ID_LIST:
    item_list = availability_by_sectionid[sectionid]["Available"]["List"]
    sorted_item_list = sorted(item_list, key=lambda x: x.lower())
    availability_by_sectionid[sectionid]["Available"]["List"] = sorted_item_list

with open("/home/olivia/ephinea-better-classic-charts/book/src/by_item.json", "r") as f:
    by_item = json.loads(f.read())
    classic_available_items = list(by_item.keys())

for sectionid in SECTION_ID_LIST:
    for item in classic_available_items:
        if item not in availability_by_sectionid[sectionid]["Available"]:
            availability_by_sectionid[sectionid]["Unavailable"].append(item)

for sectionid in SECTION_ID_LIST:
    item_list = availability_by_sectionid[sectionid]["Unavailable"]
    sorted_item_list = sorted(item_list, key=lambda x: x.lower())
    availability_by_sectionid[sectionid]["Unavailable"] = sorted_item_list

with open("/home/olivia/ephinea-better-classic-charts/book/src/availability_by_sectionid.json", "w") as f:
    f.write(json.dumps(availability_by_sectionid, indent=4))