# Herangehensweise nach dem Python-PUBG-Wrapper
# Quelle//
# https://github.com/ramonsaraiva/pubg-python

# Import der entsprechenden Python Libary
from pubg_python import PUBG, Shard

# Aufruf des API-Keys und Auswahl des entsprechenden Shards (wie z.B. PC_EU oder PC_NA)
api = PUBG ('api-key', Shard.PC_NA)


players = api.players().get('account.d50fdc18fcad49c691d38466bed6f8fd')
player = players
#print("Accountname: ", (players), sep=' ')
#print("Accountid: ", players.name, sep=' ')

for idx, match in enumerate(player.matches):
    match_data = api.matches().get(match.id)

    match = api.matches().get(player.matches[0].id)
    match.rosters
    roster = match.rosters[0]
    roster.participants
    participant = roster.participants[0]
    participant.name
    print(participant.name)


    print(idx, players, players.name, match_data, sep= ' ')