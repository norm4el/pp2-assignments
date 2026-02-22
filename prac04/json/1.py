import json

with open("sample.json", "r") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print("DN                                                 Description           Speed    MTU")
print("-" * 80)

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]   # в файле обычно так

    dn = attrs["dn"]
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(f"{dn:<50} {descr:<20}  {speed:<8} {mtu}")