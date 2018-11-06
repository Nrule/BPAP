#Herangehensweise nach PUBG Dokumentation
import requests

url = "https://api.pubg.com/shards/pc-na/players/account.d50fdc18fcad49c691d38466bed6f8fd"

header = {
  "Authorization": "Bearer <api-key>",
  "Accept": "application/vnd.api+json"
}

r = requests.get(url, headers=header)
print(r.text)