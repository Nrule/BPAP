from chicken_dinner.pubgapi import PUBG
from chicken_dinner.pubgapi import PUBGCore
from data import *
import json

#Creates a json file 
#with open("json/data_file.json", "w") as write_file:
#   json.dump(shroud, write_file, indent=2)


playername = "P4wnyhof"
ponyhof = Player_Core(playername)

matches = Player_Matches_Stats_firstten(ponyhof)
print (matches)

for match in matches:
   for participant in match["included"]:
      if participant["type"] == "participant":
         if participant["attributes"]["stats"]["name"] == playername:
            print(participant["attributes"]["stats"])

         for participantstats in participant["attributes"]:
         #if participantstats["name"] == "P4wnyhof":
            print (participant)


# Api-Key and PUBG Core
api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
pubgcore = PUBGCore(api_key, "steam")
pubg = PUBG(api_key, "steam")

# Player Information, e.g. playerId, matchIds, etc.; White-Mickey Platz 1 bei Solo-Matches
whitemickey = pubgcore.players("player_names", "White-Mickey")
#whitemickey = json.loads("json/whitemickey.json")
print (whitemickey)

whitemickeydata = whitemickey["data"]

# Player Lifetime data
for ids in whitemickeydata:
   whitemickeylifetime = pubgcore.lifetime(ids["id"])
   with open("json/whitemickeylifetime.json", "w") as write_file:
         json.dump(whitemickeylifetime, write_file, indent=2)

print (whitemickeylifetime["data"]["attributes"]["gameModeStats"]["solo"]["assists"])

print (whitemickeylifetime.data)

# Player Season data
for ids in whitemickeydata:
   player_season = pubgcore.player_season(ids["id"],"current")

print (player_season)  

# Telemetry

print (pubgcore.telemetry("https://telemetry-cdn.playbattlegrounds.com/bluehole-pubg/pc-krjp/2018/11/30/14/03/aa36f2f0-f4a8-11e8-bc9d-0a58646ff0fd-telemetry.json"))

 

# Matches 
for data in whitemickeydata:
   relationships = data["relationships"]
   for matches in relationships["matches"]["data"]:
      matches["id"]

for data in whitemickeydata:
   relationships = data["relationships"]
   for matches in relationships["matches"]["data"]:
      whitemickeymatches = pubgcore.match(matches["id"])
      with open("json/whitemickeymatches.json", "w") as write_file:
         json.dump(whitemickeymatches, write_file, indent=2)
   
# Tournaments 
tournaments = pubgcore.tournaments()
print (tournaments)

# Leaderboard
leaderboardsolo = pubgcore.leaderboard("solo")
print (leaderboardsolo)
with open("json/leaderboard.json", "w") as write_file:
   json.dump(leaderboardsolo, write_file, indent=2)


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