import json

with open("d:/python/test/old.json", "rb") as old_file:
    old_datas = json.loads(old_file.read())

with open("d:/python/test/new.json", "w", encoding="utf-8") as new_file:
    new_file.write(
        json.dumps(
            {old_data["name"]: old_data["url"] for old_data in old_datas},
            indent=None,
            sort_keys=True,
        )
    )
