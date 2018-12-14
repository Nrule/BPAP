from chicken_dinner.pubgapi import PUBG
from chicken_dinner.pubgapi import PUBGCore
import json

#Creates a json file 
#with open("json/data_file.json", "w") as write_file:
#   json.dump(shroud, write_file, indent=2)

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
pubgcore = PUBGCore(api_key, "pc-eu")

#leaderboardsolo = pubgcore.leaderboard("solo")
#with open("json/leaderboard.json", "w") as write_file:
#   json.dump(leaderboardsolo, write_file, indent=2)
# 
whitemickey = pubgcore.players("player_names", "White-Mickey")
with open("json/whitemickey.json", "w") as write_file:
   json.dump(whitemickey, write_file)

whitemickey = json.load("json/whitemickey.json")
#print (whitemickey)

whitemickeydata = whitemickey["data"]
print (whitemickeydata)

for data in whitemickeydata:
   relationships = data["relationships"]
   for matches in relationships["matches"]["data"]:
      print (matches["id"])

print(whitemickeydata)

#print(shroud["data"])
#print(type(shroud['data']))

#for data in shroud['data']:
#   id = (data['id'])
   #print(id)

#Creates a json file 
#with open("json/data_file.json", "w") as write_file:
#   json.dump(shroud, write_file, indent=2)

#lifetime = pubgcore.lifetime(id)
#print(lifetime)
#new = json.dumps(lifetime, indent=2)
#print(new)

#for data in lifetime['data']:
#   print(data['duo'])