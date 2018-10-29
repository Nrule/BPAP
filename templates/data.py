# Quelle//
# https://github.com/ramonsaraiva/pubg-python

# Import der entsprechenden Python Libary
from pubg_python import PUBG, Shard

# Aufruf des API-Keys und Auswahl des entsprechenden Shards (wie z.B. PC_EU oder PC_NA)
api = PUBG ('API-KEY', Shard.PC_EU)


# A sample of matches can be retrieved as a starting point
sample = api.samples().get()
for match in sample.matches:
    print(match.id)


# Samples can also be filtered by a creation date
sample = api.samples().filter(created_at_start='2018-01-01T00:00:00Z').get()
for match in sample.matches:
    print(match.id)


# Retrieving a single player
player = api.players().get('account.3654e255b77b409e87b10dcb086ab00d')

for match in player.matches:
    match_data = api.matches().get(match.id)


# Retrieving a list of players filtering by names
players = api.players().filter(player_names=['Name1', 'Name2'])

for player in players:
    player_id = player.id


# Retrieving a list of players filtering by ids
players = api.players().filter(player_ids=['account.3654e255b77b409e87b10dcb086ab00d'])

for player in players:
    player_name = player.name

