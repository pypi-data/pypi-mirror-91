"_json builder"
import json

data = {}
"the json to build to"

data["baseKeys"] = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_+"


with open("intConversions.json", "w") as wfile:
    json.dump(data, wfile)