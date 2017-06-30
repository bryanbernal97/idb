import requests

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}

resp = requests.get('https://api.twitch.tv/kraken/games/top?limit=100', headers=headers)
games_json = resp.json()

games = {}

for game in games_json['top']:
	games[game['game']['name']] = game['game']

resp2 = requests.get('https://api.twitch.tv/kraken/streams?limit=100', headers=headers)
streams_json = resp2.json()

streams = {}

for stream in streams_json['streams']:
	streams[stream['_id']] = stream

resp3 = requests.get('https://api.twitch.tv/kraken/communities/top?limit=100', headers=headers)
communities_json = resp3.json()

communities = {}

for community in communities_json['communities']:
	communities[community['name']] = community

resp4 = requests.get('https://api.twitch.tv/kraken/teams?limit=100', headers=headers)
teams_json = resp4.json()

teams = {}

for team in teams_json['teams']:
	teams[team['name']] = team

print(teams)