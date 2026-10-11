import json

SECTION_ID_LIST = ["Viridia", "Greenill", "Skyly", "Bluefull", "Purplenum", "Pinkal", "Redria", "Oran", "Yellowboze", "Whitill"]

with open("/home/olivia/ephinea-better-classic-charts/book/src/by_item.json", "r") as f:
    by_item = json.loads(f.read())

availability = {}

for item, item_data in by_item.items():
    availability[item] = {"Available":{"Ids":[]},"Unvailable":[]}
    for entry in item_data:
        if entry["sectionId"] not in availability[item]["Available"]["Ids"]:
            availability[item]["Available"]["Ids"].append(entry["sectionId"])
            availability[item]["Available"][entry["sectionId"]] = []
        availability[item]["Available"][entry["sectionId"]].append(entry)
    for section in SECTION_ID_LIST:
        if section not in availability[item]["Available"]["Ids"]:
            availability[item]["Unvailable"].append(section)
    

sorted = dict(sorted(availability.items(), key=lambda x: x[0]))

with open("/home/olivia/ephinea-better-classic-charts/book/src/availability_by_item.json", "w") as f:
    f.write(json.dumps(sorted, indent=4))