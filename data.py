from chicken_dinner.pubgapi import PUBG
from chicken_dinner.pubgapi import PUBGCore

# Returns the PUBG ApiKey for the access to the API
def Apikey():
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5OGNiYzI3MC1iYTlkLTAxMzYtNjg3MS02YjU5NWYzNGI3NjciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTQwNDgzNDc3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImJwYXAifQ.hr--q6zWIXB6Fkba3XGhgMaQUubCo9vn1h1YgMm1dVk"
    return(api_key)

# Gets Player Core data with the name of a player 
def Player_Core(playername):
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    playerCore = pubgcore.players("player_names", playername)
    return playerCore

# Gets all the Liftetime data with the Player Core
def Player_Lifetime_Stats(playercore):
    playercoredata = playercore["data"]
    for ids in playercoredata:
        playerid = ids["id"]
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    player_Lfstats =[]
    player_Lfstats = pubgcore.lifetime(playerid)
    player_Lfstats = player_Lfstats["data"]["attributes"]["gameModeStats"]
    modes = player_Lfstats.keys()

    # Append new fields to player_Lfstats
    for mode in modes:
        if player_Lfstats[mode]["kills"] != 0:
            player_Lfstats[mode]["headshotRate"] = player_Lfstats[mode]["headshotKills"] / player_Lfstats[mode]["kills"] 
        else:
            player_Lfstats[mode]["headshotRate"] = ''

        if player_Lfstats[mode]["losses"] != 0:
            player_Lfstats[mode]["KD"] = player_Lfstats[mode]["kills"] / player_Lfstats[mode]["losses"]
        else:
            player_Lfstats[mode]["KD"] = ''

        if player_Lfstats[mode]["roundsPlayed"] != 0:
            player_Lfstats[mode]["rankPointsMatch"] = player_Lfstats[mode]["rankPoints"] / player_Lfstats[mode]["roundsPlayed"]
            player_Lfstats[mode]["winRate"] = player_Lfstats[mode]["wins"] / player_Lfstats[mode]["roundsPlayed"]
            player_Lfstats[mode]["top10s%"] = player_Lfstats[mode]["top10s"] / player_Lfstats[mode]["roundsPlayed"]
        else:
            player_Lfstats[mode]["rankPointsMatch"] = ''
            player_Lfstats[mode]["winRate"] = ''
            player_Lfstats[mode]["top10s%"] = ''

    return player_Lfstats

# Gets all the Liftetime data with the Player Core
def Player_Lifetime_Stats_all(playercore):
    playercoredata = playercore["data"]
    for ids in playercoredata:
        playerid = ids["id"]
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    player_Lfstats =[]
    player_Lfstats = pubgcore.lifetime(playerid)

    return player_Lfstats

# Gets all Match Stats with the player core data
def Player_Matches_Stats(playercore):
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    playercoredata = playercore["data"]
    playerMatches = []
    for data in playercoredata:
        relationships = data["relationships"]
        for matches in relationships["matches"]["data"]:
            playerMatches.append(pubgcore.match(matches["id"]))            
    return playerMatches

# Gets only the first five matches from a player 
def Player_Matches_Stats_firstten(playercore):
    api_key = Apikey()
    pubgcore = PUBGCore(api_key, "steam")
    playercoredata = playercore["data"]
    playerMatches = []
    for data in playercoredata:
        relationships = data["relationships"]
        for idx, matches in enumerate(relationships["matches"]["data"]):
            playerMatches.append(pubgcore.match(matches["id"])) 
            if (idx+1) % 10 == 0:
                break           
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


