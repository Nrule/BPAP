from chicken_dinner.pubgapi import PUBG
from chicken_dinner.pubgapi import PUBGCore
import json

def Apikey():
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
    return(api_key)

def Player_Stats_Solo(playername):
    # API-KEY
    api_key = Apikey()
    # (server) beschreibt, von wo die Daten bezogen werden sollen
    pubg = PUBG(api_key, "pc-eu")
    shroud = pubg.players_from_names(playername)[0]
    shroud_season = shroud.get_current_season()
    solo_tpp_stats = shroud_season.game_mode_stats("solo")
    solo_fpp_stats = shroud_season.game_mode_stats("solo", "fpp")
    return solo_tpp_stats, solo_fpp_stats


def Player_Stats(playername):
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "pc-na")
    shroud = pubgcore.players("player_names", "shroud")
    print(shroud)





api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
pubgcore = PUBGCore(api_key, "pc-eu")
shroud = pubgcore.players("player_names", "Vengaard")

#print(shroud["data"])
#print(type(shroud['data']))

for data in shroud['data']:
   id = (data['id'])
   #print(id)

lifetime = pubgcore.lifetime(id)
print(lifetime)
new = json.dumps(lifetime, indent=2)
print(new)

for data in lifetime['data']:
   print(data['duo'])