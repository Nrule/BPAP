from chicken_dinner.pubgapi import PUBG
from chicken_dinner.pubgapi import PUBGCore

def Apikey():
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
    return(api_key)

def Player_Core(playername):
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    playerCore = pubgcore.players("player_names", playername)
    return playerCore

def Player_Lifetime_Stats(playercore):
    playercoredata = playercore["data"]
    for ids in playercoredata:
        playerid = ids["id"]
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    player_Lfstats = pubgcore.lifetime(playerid)
    return player_Lfstats

def Player_Matches_Stats(playercore):
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    playercoredata = playercore["data"]
    for data in playercoredata:
        relationships = data["relationships"]
        for matches in relationships["matches"]["data"]:
            playerMatches = pubgcore.match(matches["id"])
    return playerMatches

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


