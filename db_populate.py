# This is where we are making the calls to the API's and populating our data

#Ignore for now

from application import db
from application.models import User
from application.models import Team
from application.models import Community
from application.models import User

import datetime
import iso639
import requests

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}
top = {}
teams = {}
communities = {}
streamers = {}
games = {}

teams_api_url = 'https://api.twitch.tv/kraken/teams/'
channel_api_url = 'https://api.twitch.tv/kraken/channels/'
gb_api_url = 'http://www.giantbomb.com/api/search/?api_key=0ac0037d403fff412c9e9ac9e60a23acc5b2e736&format=json&query='

json = requests.get(teams_api_url, headers=headers).json()

my_teams = ''

for t in json.get('teams'):
	team_api_url = teams_api_url + str(t.get('name'))
	team = requests.get(team_api_url, headers=headers).json()
	team_db = Team()
	team_db.name = team.get('display_name')
	team_db.id = team.get('_id')
	team_db.info = team.get('info')
	team_db.image_url = team.get('logo')
	team_db.created = team.get('created_at')
	team_db.updated = team.get('updated_at')
	user_ids = []
	for user in team.get('users'):
		user_db = User()
		user_db.id = user.get('_id')
		
		if team_db.user_ids == None:
			team_db.user_ids = []
		team_db.user_ids.append(user_db.id) # Connect team model with user model


		# Have to do another request to get description for user because not included in teams users response
		user_json = requests.get((channel_api_url+str(user_db.id)), headers=headers).json()
		user_db.name = user.get('display_name')
		user_db.description = user_json.get('description')


		language_code = user.get('language')
		language = language_code
		if language_code:
			try:
				language_iso = iso639.to_name(language_code)
			except:
				pass
			if language_iso:
				language = language_iso
		user_db.language = language
		user_db.views = user.get('views')
		user_db.followers = user.get('followers')
		user_db.url = user.get('url')
		user_db.created = user.get('created_at')
		user_db.updated = user.get('updated_at')
		user_db.image_url = user.get('logo')
		user_db.team_id = team_db.id # Connect user model with team model

		user_game_name = user.get('game')

		if user_game_name != None:
			# Get game information from 2nd API
			gb_request_url = gb_api_url + user_game_name + '&resources=game'
			print('GB REQUEST: ' + gb_request_url + '\n')
			game_response = requests.get(gb_request_url)
			game_json = None
			if game_response:
				game_json = game_response.json()

			if game_json:
				game_db = Game()
				print('CREATED A GAME \n')

		# print('USER DB: ' + str(user_db) + '\n')



	# print('TEAM DB: ' + str(team_db) + '\n')
	# print(str(team_db.id) + '\n')

# print(my_teams)
