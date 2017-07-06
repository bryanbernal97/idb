# This is where we are making the calls to the API's and populating our data

#Ignore for now

from application import db
from application.models import User
from application.models import Team
from application.models import Community
from application.models import Game
from collections import Iterable
from multiprocessing import Process, Manager

import datetime
import iso639
import requests
import time
import json

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}

teams_api_url = 'https://api.twitch.tv/kraken/teams/'
communities_api_url = 'https://api.twitch.tv/kraken/communities/top?limit=100'
channel_api_url = 'https://api.twitch.tv/kraken/channels/'
gb_api_url = 'http://www.giantbomb.com/api/search/?api_key=0ac0037d403fff412c9e9ac9e60a23acc5b2e736&format=json&query='

# To make sure not entering duplicates into the db. Teams and Communities are guaranteed to be unique because they are top-level
games_dict = dict()
users_dict = dict()

def lookup_user(parent_db, user_id):
	'''
	parent_db: The parent object that the user is nested under
	user_id: The user to lookup

	This method will perform the necessary API calls to lookup a Twitch user and their associated game and returns their associated game's id.
	'''
	global games_dict
	global users_dict

	if user_id not in users_dict:
		# users_set.add(user_id)

		user_db = User()
		user_db.id = user_id

		# Have to do another request to get description for user because not included in teams users response
		user_json = requests.get((channel_api_url+str(user_db.id)), headers=headers).json()
		user_db.name = user_json.get('display_name')
		user_db.description = user_json.get('description')
		if not user_db.description:
			user_db.description = 'This user has no bio.' # This is what Twitch displays if a user leaves this field empty.


		language_code = user_json.get('language')
		language = language_code
		if language_code:
			try:
				language_iso = iso639.to_name(language_code)
				if language_iso:
					language = language_iso
			except:
				pass
		user_db.language = language
		user_db.views = user_json.get('views')
		user_db.followers = user_json.get('followers')
		user_db.url = user_json.get('url')
		user_db.created = user_json.get('created_at')
		user_db.updated = user_json.get('updated_at')
		user_db.image_url = user_json.get('logo')
		if user_db.image_url == None:
			user_db.image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png' # This is Twitch's default user logo

		if isinstance(parent_db, Team):
			user_db.team_ids = [parent_db.id]
		elif isinstance(parent_db, Community):
			user_db.community_id = parent_db.id

		user_game_name = user_json.get('game')

		if user_game_name != None:
			# Get game information from 2nd API
			gb_request_url = gb_api_url + user_game_name + '&resources=game'
			game_response = requests.get(gb_request_url, headers={'user-agent' : 'streamGlean'})
			game_json = None
			if game_response:
				game_json = game_response.json()

				if game_json:
					game_json = game_json.get('results')
					if game_json:
						game_json = game_json[0]
						game_id = game_json.get('id')
						if game_id and game_id not in games_dict:
							# games_set.add(game_id)
							user_db.game_id = game_id

							# print('GOT HERE \n')
							game_db = Game()
							# print('CREATED A GAME \n')
							game_db.id = game_id
							game_db.user_ids = [user_db.id]

							if isinstance(parent_db, Team):
								game_db.team_ids = [parent_db.id]
							elif isinstance(parent_db, Community):
								game_db.community_ids = [parent_db.id]

							game_db.name = game_json.get('name')
							game_db.description = game_json.get('deck')
							genres = []
							# need a new request for genres
							giantbomb_game_api_url = 'http://www.giantbomb.com/api/game/' + str(game_db.id) + '?api_key=0ac0037d403fff412c9e9ac9e60a23acc5b2e736&format=json'
							game_response = requests.get(giantbomb_game_api_url, headers={'user-agent' : 'streamGlean'})
							# print('GAME RESPONSE: ' + str(game_response) + '\n')
							if game_response:
								game_response = game_response.json().get('results')
								# game_response = game_response.get('results').json()
								# print('GAME JSON: ' + str(game_response) + '\n')
								genres_response = game_response.get('genres')
								# print('GENRES RESPONSE: ' + str(genres_response))
								if genres_response:
									for genre_dict in game_response.get('genres'):
										genres.append(genre_dict.get('name'))
									game_db.genres = genres
							platforms = []
							game_platforms = game_json.get('platforms')
							if (game_platforms and isinstance(game_platforms, Iterable)):
								for platform_dict in game_json.get('platforms'):
									platforms.append(platform_dict.get('name'))
							game_db.platforms = platforms
							game_db.release_date = game_json.get('original_release_date')
							rating = game_json.get('original_game_rating')
							# print('RATING: ' + str(rating) + '\n')
							if rating:
								for d in rating:
									if 'ESRB' in d.get('name'):
										actual_rating = d.get('name').replace('ESRB: ', '')
										# print('ACTUAL RATING: ' + '\n' + str(actual_rating))
										game_db.rating = actual_rating
							game_image = game_json.get('image')
							if game_image:
								game_image_small_url = game_image.get('small_url')
								if game_image_small_url:
									game_db.image_url = game_image_small_url

							# print('GAME DB: ' + str(game_db) + '\n')
							games_dict[game_db.id] = game_db
						elif game_id:
							game_db = games_dict[game_id]
							if user_db.id not in game_db.user_ids:
								game_db.user_ids += [user_db.id]
							if isinstance(parent_db, Team):
								if parent_db.id not in game_db.team_ids:
									game_db.team_ids += [parent_db.id]
							elif isinstance(parent_db, Community):
								if parent_db.id not in game_db.community_ids:
									game_db.community_ids += [parent_db.id]
							# print('GAME DB: ' + str(game_db) + '\n')
					

		# print('USER DB: ' + str(user_db) + '\n')
		users_dict[user_db.id] = user_db
		# print('UPDATING USER DICT: ' + str(users_dict))
		return user_db.game_id
	else:
		user_db = users_dict[user_id]
		if isinstance(parent_db, Team):
			if user_db.team_ids != None:
				user_db.team_ids += [parent_db.id]
			else:
				user_db.team_ids = [parent_db.id]
		elif isinstance(parent_db, Community):
			user_db.community_id = parent_db.id
		# print('USER DB: ' + str(user_db) + '\n')


def lookup_teams(users_d, games_d):

	global users_dict
	global games_dict

	# print('users_d: ' + str(users_d) + '\n')
	json = requests.get(teams_api_url, headers=headers).json()

	# users_d['hey'] = 'this sucks balls'

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
		game_ids = []

		for user in team.get('users'):
			user_id = user.get('_id')
			user_ids.append(user_id)
			game_id = lookup_user(team_db, user_id)
			# print('users_dict: ' + str(users_dict) + '\n')
			for k in users_dict:
				users_d[k] = users_dict[k]
			# print('users_d: ' + str(users_d) + '\n')
			if game_id != None:
				game_ids.append(game_id)
			# games_d = dict(games_dict)
			for key in games_dict:
				games_d[key] = games_dict[key]

		# print('done with a for loop')
		team_db.user_ids = user_ids
		team_db.game_ids = game_ids

		# print('user_dict: ' + str(users_dict))
		# users_d['ab'] = 'defghi'
		# users_d = dict(users_dict)
		# games_d = dict(games_dict)

		try:     
			db.session.add(team_db)
			db.session.commit()        
			db.session.close()
		except Exception as e:
			print(str(e) + '\n')
			db.session.rollback()

		# print('TEAM DB: ' + str(team_db) + '\n')


def lookup_communities(users_d, games_d):

	global users_dict
	global games_dict

	json = requests.get(communities_api_url, headers=headers).json()

	for c in json.get('communities'):
		community_id = c.get('_id')
		community_api_url = 'https://api.twitch.tv/kraken/communities/' + str(community_id)
		community_json = requests.get(community_api_url, headers=headers).json()
		community_db = Community()
		community_db.id = community_id
		community_db.name = community_json.get('display_name')
		community_db.description = community_json.get('description')
		language_code = community_json.get('language')
		language = language_code
		if language_code:
			try:
				language_iso = iso639.to_name(language_code)
				if language_iso:
					language = language_iso
			except:
				pass
		community_db.language = language
		community_db.rules = community_json.get('rules')
		community_db.image_url = community_json.get('avatar_image_url')
		owner_id = community_json.get('owner_id')
		community_db.owner_id = owner_id
		game_id = lookup_user(community_db, owner_id)

		if game_id != None:
			community_db.game_id = game_id
		for k in users_dict:
			users_d[k] = users_dict[k]
		# print('users_d: ' + str(users_d) + '\n')
		# games_d = dict(games_dict)
		for key in games_dict:
			games_d[key] = games_dict[key]
		# print('COMMUNITY DB: ' + str(community_db) + '\n')
		try:     
			db.session.add(community_db)
			db.session.commit()        
			db.session.close()
		except Exception as e:
			print(str(e) + '\n')
			db.session.rollback()



def populate_games():
	global games_dict
	# print('GAMES: ' + str(games_dict) + '\n')
	for key in games_dict:
		# print(str(key) + '\n')		
		try:     
			db.session.add(games_dict[key])
			db.session.commit()        
			db.session.close()
		except Exception as e:
			print(str(e) + '\n')
			db.session.rollback()

def populate_users():
	global users_dict
	# print('USERS: ' + str(users_dict) + '\n')
	for key in users_dict:
		# print(str(key) + '\n')
		try:     
			db.session.add(users_dict[key])
			db.session.commit()        
			db.session.close()
		except Exception as e:
			print(str(e) + '\n')
			db.session.rollback()


def populate_teams():
	global users_dict
	global games_dict
	# print('users dict empty: ' + str(users_dict) + '\n')
	with Manager() as manager:
		users = manager.dict(users_dict)
		games = manager.dict(games_dict)
		# print('users: ' + str(users) + '\n')
		p = Process(target=lookup_teams, args=(users, games))
		p.start()

		# Wait 10 seconds for foo
		time.sleep(30)

		# print('users: ' + str(users) + '\n')
		# print('users_dict: ' + str(users_dict) + '\n')
		# Terminate foo
		p.terminate()

		# print('users: ' + str(users) + '\n')

		# Cleanup
		p.join()

		# print('users: ' + str(users) + '\n')
		users_dict = dict(users.copy())
		games_dict = dict(games.copy())
		# for k in users:
		# 	users_dict[k] = users[k]
		# for key in games:
		# 	games_dict[key] = games[key]
		# users_dict = users
		# games_dict = games

def populate_communities():
	global users_dict
	global games_dict
	with Manager() as manager:
		users = manager.dict(users_dict)
		games = manager.dict(games_dict)
		p = Process(target=lookup_communities, args=(users, games))
		p.start()

		# Wait 10 seconds for foo
		time.sleep(30)

		# Terminate foo
		p.terminate()

		# Cleanup
		p.join()

		users_dict = dict(users.copy())
		games_dict = dict(games.copy())
		# print('users: ' + str(users))



if __name__ == '__main__':
	populate_teams()
	populate_communities()
	populate_games()
	populate_users()

	# team = Team()
	# team.id = '1234'
	# team.name = 'Hannahs Test'
	# team.info = 'Hooray'
	# try:     
	# 	db.session.add(team)
	# 	db.session.commit()        
	# 	db.session.close()
	# except:
	# 	db.session.rollback()


	# lookup_teams()
	# lookup_communities()

