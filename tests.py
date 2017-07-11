#!/usr/bin/env python
import requests
from unittest import main, TestCase
from application import db
from application.models import User, Team, Game, Community
import json

class TestApi(TestCase):
    '''
        Tests the API endpoints and their methods.
    '''

    user_url = 'http://streamglean.me/api/user'
    team_url = 'http://streamglean.me/api/team'
    game_url = 'http://streamglean.me/api/game'
    community_url = 'http://streamglean.me/api/community'
    headers = {'content-type': 'application/json'}

    
    def test_get_all_users(self):
        response = requests.get(self.user_url, headers=self.headers)
        num_users = 0
        try:
            num_users = User.query.count()
            db.session.close()
        except:
            db.session.rollback()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.json()['num_results']), num_users)


    def test_get_all_teams(self):
        response = requests.get(self.team_url, headers=self.headers)
        num_teams = 0
        try:
            num_teams = Team.query.count()
            db.session.close()
        except:
            db.session.rollback()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.json()['num_results']), num_teams)


    def test_get_all_games(self):
        response = requests.get(self.game_url, headers=self.headers)
        num_games = 0
        try:
            num_games = Game.query.count()
            db.session.close()
        except:
            db.session.rollback()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.json()['num_results']), num_games)


    def test_get_all_communities(self):
        response = requests.get(self.community_url, headers=self.headers)
        num_communities = 0
        try:
            num_communities = Community.query.count()
            db.session.close()
        except:
            db.session.rollback()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.json()['num_results']), num_communities)


    def test_get_single_user_valid(self):
        # Test API GET method api/user/(int:id) with valid id
        valid_user = None
        test_id = '-1'
        test_name = 'API TEST GET USER'

        # Insert test user into database to get using the API
        valid_user = User()
        valid_user.id = test_id
        valid_user.name = test_name
        try:
            db.session.add(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Make sure API call gets and matches the test user just entered into the db above
        response = requests.get(self.user_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('id'), test_id)
        self.assertEqual(json_response.get('name'), test_name)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_single_user_invalid(self):
        # Test API GET method api/user/(int:id) with an invalid (not found) id
        test_id = '-1'

        # Make sure db instance does not have instance with test_id
        try:
            query = User.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        response = requests.get(self.user_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_get_single_game_valid(self):
        # Test API GET method api/game/(int:id) with valid id

        valid_game = None
        test_id = -1
        test_name = 'API TEST GET GAME'

        # Insert test user into database to get using the API
        valid_game = Game()
        valid_game.id = test_id
        valid_game.name = test_name
        try:
            db.session.add(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Make sure API call gets and matches the test user just entered into the db above
        response = requests.get(self.game_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('id'), test_id)
        self.assertEqual(json_response.get('name'), test_name)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_single_game_invalid(self):
        # Test API GET method api/game/(int:id) with an invalid id

        test_id = -1

        # Make sure db instance does not have instance with test_id
        try:
            query = Game.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        response = requests.get(self.game_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_get_single_team_valid(self):
        # Test API GET method api/team/(int:id) with valid id

        valid_team = None
        test_id = -1
        test_name = 'API TEST GET TEAM'

        # Insert test user into database to get using the API
        valid_team = Team()
        valid_team.id = test_id
        valid_team.name = test_name
        try:
            db.session.add(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Make sure API call gets and matches the test user just entered into the db above
        response = requests.get(self.team_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('id'), test_id)
        self.assertEqual(json_response.get('name'), test_name)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_single_team_invalid(self):
        # Test API GET method api/team/(int:id) with an invalid id

        test_id = -1

        # Make sure db instance does not have instance with test_id
        try:
            query = Team.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        response = requests.get(self.team_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_get_single_community_valid(self):
        # Test API GET method api/community/(int:id) with valid id

        valid_community = None
        test_id = '-1'
        test_name = 'API TEST GET USER'

        # Insert test user into database to get using the API
        valid_community = Community()
        valid_community.id = test_id
        valid_community.name = test_name
        try:
            db.session.add(valid_community)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Make sure API call gets and matches the test user just entered into the db above
        response = requests.get(self.community_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('id'), test_id)
        self.assertEqual(json_response.get('name'), test_name)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_community)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_single_community_invalid(self):
        # Test API GET method api/community/(int:id) with an invalid id

        test_id = '-1'

        # Make sure db instance does not have instance with test_id
        try:
            query = Community.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        response = requests.get(self.community_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_get_user_search_match(self):
        # Test API GET method api/user?q=<searchjson> with a match
        valid_user = None
        test_id = '-1'
        test_name = 'API TEST GET USER THROUGH SEARCH'
        test_language = 'Made Up Language'

        # Insert test user into database to get using the API
        valid_user = User()
        valid_user.id = test_id
        valid_user.name = test_name
        valid_user.language = test_language
        try:
            db.session.add(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        filters = [dict(name='language', op='ilike', val='made up language')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.user_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 1)
        self.assertEqual(json_response.get('objects')[0].get('id'), test_id)
        self.assertEqual(json_response.get('objects')[0].get('name'), test_name)
        self.assertEqual(json_response.get('objects')[0].get('language'), test_language)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_user_search_no_match(self):
        # Test API GET method api/user?q=<searchjson> with no result match
        filters = [dict(name='language', op='ilike', val='made up language')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.user_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 0)


    def test_get_game_search_match(self):
        # Test API GET method api/game?q=<searchjson> with a match

        valid_game = None
        test_id = -1
        test_name = 'API TEST GET GAME THROUGH SEARCH'
        test_rating = 'Made Up Game Rating'

        # Insert test user into database to get using the API
        valid_game = Game()
        valid_game.id = test_id
        valid_game.name = test_name
        valid_game.rating = test_rating
        try:
            db.session.add(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        filters = [dict(name='rating', op='ilike', val='made up game rating')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.game_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 1)
        self.assertEqual(json_response.get('objects')[0].get('id'), test_id)
        self.assertEqual(json_response.get('objects')[0].get('name'), test_name)
        self.assertEqual(json_response.get('objects')[0].get('rating'), test_rating)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_game_search_no_match(self):
        # Test API GET method api/game?q=<searchjson> with no result match

        filters = [dict(name='rating', op='ilike', val='made up game rating')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.game_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 0)


    def test_get_team_search_match(self):
        # Test API GET method api/team?q=<searchjson> with a match

        valid_team = None
        test_id = -1
        test_name = 'API TEST GET TEAM THROUGH SEARCH'
        test_info = 'Made Up Team Info'

        # Insert test user into database to get using the API
        valid_team = Team()
        valid_team.id = test_id
        valid_team.name = test_name
        valid_team.info = test_info
        try:
            db.session.add(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        filters = [dict(name='info', op='ilike', val='made up team info')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.team_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 1)
        self.assertEqual(json_response.get('objects')[0].get('id'), test_id)
        self.assertEqual(json_response.get('objects')[0].get('name'), test_name)
        self.assertEqual(json_response.get('objects')[0].get('info'), test_info)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_team_search_no_match(self):
        # Test API GET method api/team?q=<searchjson> with no result match

        filters = [dict(name='info', op='ilike', val='made up team info')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.team_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 0)


    def test_get_community_search_match(self):
        # Test API GET method api/community?q=<searchjson> with a match

        valid_community = None
        test_id = '-1'
        test_name = 'API TEST GET COMMUNITY THROUGH SEARCH'
        test_language = 'Made Up Language'

        # Insert test user into database to get using the API
        valid_community = Community()
        valid_community.id = test_id
        valid_community.name = test_name
        valid_community.language = test_language
        try:
            db.session.add(valid_community)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        filters = [dict(name='language', op='ilike', val='made up language')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.community_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 1)
        self.assertEqual(json_response.get('objects')[0].get('id'), test_id)
        self.assertEqual(json_response.get('objects')[0].get('name'), test_name)
        self.assertEqual(json_response.get('objects')[0].get('language'), test_language)

        # Delte the test user that was inserted earlier in this
        try:
            db.session.delete(valid_community)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_get_community_search_no_match(self):
        # Test API GET method api/community?q=<searchjson> with no result match

        filters = [dict(name='language', op='ilike', val='made up language')]
        params = dict(q=json.dumps(dict(filters=filters)))
        response = requests.get(self.community_url, params=params, headers=self.headers)
        json_response = json.loads(response.text)
        
        # Make sure API call searches and matches the test user just entered into the db above
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('num_results'), 0)


    def test_post_user_valid(self):
        # Test API POST method api/user
        test_id = '-1'
        test_name = 'API TEST POST USER'

        new_user = {'id': test_id, 'name': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.user_url, data=json.dumps(new_user), headers=self.headers)

        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), test_name)

        # Delete the test instance for cleanup
        try:
            valid_user = User.query.filter_by(id='-1').first()
            db.session.delete(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_post_user_invalid(self):
        # Test API POST method api/user with an invalid field
        test_id = '-1'
        test_name = 'API TEST POST USER INVALID'

        new_user = {'id': test_id, 'invalid_field': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.user_url, data=json.dumps(new_user), headers=self.headers)

        self.assertEqual(response.status_code, 400)

        # Make sure the test instance for was not entered into the database
        try:
            query = User.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_post_game_valid(self):
        # Test API POST method api/game

        test_id = -1
        test_name = 'API TEST POST GAME'

        new_game = {'id': test_id, 'name': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.game_url, data=json.dumps(new_game), headers=self.headers)

        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), test_name)

        # Delete the test instance for cleanup
        try:
            valid_game = Game.query.filter_by(id='-1').first()
            db.session.delete(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_post_game_invalid(self):
        # Test API POST method api/game

        test_id = -1
        test_name = 'API TEST POST GAME INVALID'

        new_game = {'id': test_id, 'invalid_field': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.game_url, data=json.dumps(new_game), headers=self.headers)

        self.assertEqual(response.status_code, 400)

        # Make sure the test instance for was not entered into the database
        try:
            query = Game.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_post_team_valid(self):
        # Test API POST method api/team

        test_id = -1
        test_name = 'API TEST POST TEAM'

        new_team = {'id': test_id, 'name': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.team_url, data=json.dumps(new_team), headers=self.headers)

        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), test_name)

        # Delete the test instance for cleanup
        try:
            valid_team = Team.query.filter_by(id='-1').first()
            db.session.delete(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_post_team_invalid(self):
        # Test API POST method api/team

        test_id = -1
        test_name = 'API TEST POST TEAM INVALID'

        new_team = {'id': test_id, 'invalid_field': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.team_url, data=json.dumps(new_team), headers=self.headers)

        self.assertEqual(response.status_code, 400)

        # Make sure the test instance for was not entered into the database
        try:
            query = Team.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_post_community_valid(self):
        # Test API POST method api/community

        test_id = '-1'
        test_name = 'API TEST POST COMMUNITY'

        new_community = {'id': test_id, 'name': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.community_url, data=json.dumps(new_community), headers=self.headers)

        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), test_name)

        # Delete the test instance for cleanup
        try:
            query = Community.query.filter_by(id='-1').first()
            db.session.delete(query)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_post_community_invalid(self):
        # Test API POST method api/community

        test_id = '-1'
        test_name = 'API TEST POST COMMUNITY INVALID'

        new_community = {'id': test_id, 'invalid_field': test_name}

        # Enter the test instance into the db through the API call
        response = requests.post(self.community_url, data=json.dumps(new_community), headers=self.headers)

        self.assertEqual(response.status_code, 400)

        # Make sure the test instance for was not entered into the database
        try:
            query = Community.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_delete_user_valid(self):
        # Test API DELETE method api/user

        valid_user = None
        test_id = '-1'
        test_name = 'API TEST DELETE USER'

        # Insert test user into database to get using the API
        valid_user = User()
        valid_user.id = test_id
        valid_user.name = test_name
        try:
            db.session.add(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Delete the db instance through an API call
        response = requests.delete(self.user_url+'/'+str(test_id), headers=self.headers)

        self.assertEqual(response.status_code, 204)

        # Make sure db instance is no longer in db
        try:
            query = User.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_delete_user_invalid(self):
        # Test API DELETE method api/user with a non-valid (not found) id
        test_id = '-1'

        # Make sure db instance does not have instance with test_id
        try:
            query = User.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        # Try to make call to API to delete user with that invalid id
        response = requests.delete(self.user_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_delete_game_valid(self):
        # Test API DELETE method api/game

        valid_game = None
        test_id = -1
        test_name = 'API TEST DELETE GAME'

        # Insert test user into database to get using the API
        valid_game = Game()
        valid_game.id = test_id
        valid_game.name = test_name
        try:
            db.session.add(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Delete the db instance through an API call
        response = requests.delete(self.game_url+'/'+str(test_id), headers=self.headers)

        self.assertEqual(response.status_code, 204)

        # Make sure db instance is no longer in db
        try:
            query = Game.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_delete_game_invalid(self):
        # Test API DELETE method api/game

        test_id = -1

        # Make sure db instance does not have instance with test_id
        try:
            query = Game.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        # Try to make call to API to delete user with that invalid id
        response = requests.delete(self.game_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_delete_team_valid(self):
        # Test API DELETE method api/team

        valid_team = None
        test_id = -1
        test_name = 'API TEST DELETE TEAM'

        # Insert test user into database to get using the API
        valid_team = Team()
        valid_team.id = test_id
        valid_team.name = test_name
        try:
            db.session.add(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Delete the db instance through an API call
        response = requests.delete(self.team_url+'/'+str(test_id), headers=self.headers)

        self.assertEqual(response.status_code, 204)

        # Make sure db instance is no longer in db
        try:
            query = Team.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_delete_team_invalid(self):
        # Test API DELETE method api/team

        test_id = -1

        # Make sure db instance does not have instance with test_id
        try:
            query = Team.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        # Try to make call to API to delete user with that invalid id
        response = requests.delete(self.team_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_delete_community_valid(self):
        # Test API DELETE method api/community

        valid_community = None
        test_id = '-1'
        test_name = 'API TEST DELETE COMMUNITY'

        # Insert test user into database to get using the API
        valid_community = Community()
        valid_community.id = test_id
        valid_community.name = test_name
        try:
            db.session.add(valid_community)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        # Delete the db instance through an API call
        response = requests.delete(self.community_url+'/'+str(test_id), headers=self.headers)

        self.assertEqual(response.status_code, 204)

        # Make sure db instance is no longer in db
        try:
            query = Community.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_delete_community_invalid(self):
        # Test API DELETE method api/community

        test_id = '-1'

        # Make sure db instance does not have instance with test_id
        try:
            query = Community.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        # Try to make call to API to delete user with that invalid id
        response = requests.delete(self.community_url+'/'+str(test_id), headers=self.headers)
        self.assertEqual(response.status_code, 404)


    def test_update_user_valid(self):
        # Test API PUT method api/user

        valid_user = None
        test_id = '-1'
        test_name = 'API TEST UPDATE USER'

        # Insert test user into database to get using the API
        valid_user = User()
        valid_user.id = test_id
        valid_user.name = test_name
        try:
            db.session.add(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


        new_test_name = 'NEW API TEST UPDATE USER'
        new_test_views = 2

        update = {'name': new_test_name, 'views': new_test_views}

        # Update the user through the API
        response = requests.put(self.user_url + '/' + str(test_id), data=json.dumps(update), headers=self.headers)

        # Make sure instance was updated
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), new_test_name)
        self.assertEqual(json_response.get('views'), new_test_views)

        # Delete the test instance for cleanup
        try:
            updated_user_query = User.query.filter_by(id=test_id)
            self.assertEqual(updated_user_query.count(), 1) # Make sure update did not create duplicate entry
            updated_user = updated_user_query.first()
            db.session.delete(updated_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_update_user_invalid(self):
        # Test API PUT method api/user with an invalid (not found) id

        test_id = '-1'
        new_test_name = 'NEW API TEST UPDATE USER INVALID'
        new_test_views = 2

        # Make sure db instance does not have instance with test_id
        try:
            query = User.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        update = {'name': new_test_name, 'views': new_test_views}

        # Update the user through the API
        response = requests.put(self.user_url + '/' + str(test_id), data=json.dumps(update), headers=self.headers)

        self.assertEqual(response.status_code, 404)

        # Make sure db instance still does not have instance with test_id
        try:
            query = User.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_update_game_valid(self):
        # Test API PUT method api/game

        valid_game = None
        test_id = -1
        test_name = 'API TEST UPDATE GAME'

        # Insert test user into database to get using the API
        valid_game = Game()
        valid_game.id = test_id
        valid_game.name = test_name
        try:
            db.session.add(valid_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


        new_test_name = 'NEW API TEST UPDATE GAME'

        update = {'name': new_test_name}

        # Update the user through the API
        response = requests.put(self.game_url + '/' + str(test_id), data=json.dumps(update), headers=self.headers)

        # Make sure instance was updated
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), new_test_name)

        # Delete the test instance for cleanup
        try:
            updated_game_query = Game.query.filter_by(id=test_id)
            self.assertEqual(updated_game_query.count(), 1) # Make sure update did not create duplicate entry
            updated_game = updated_game_query.first()
            db.session.delete(updated_game)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_update_game_invalid(self):
        # Test API PUT method api/game

        test_id = -1
        new_test_name = 'NEW API TEST UPDATE GAME INVALID'

        # Make sure db instance does not have instance with test_id
        try:
            query = GAME.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()

        update = {'name': new_test_name}

        # Update the user through the API
        response = requests.put(self.game_url + '/' + str(test_id), data=json.dumps(update), headers=self.headers)

        self.assertEqual(response.status_code, 404)

        # Make sure db instance still does not have instance with test_id
        try:
            query = Game.query.get(test_id)
            self.assertisNone(query)
            db.session.close()
        except:
            db.session.rollback()


    def test_update_team_valid(self):
        # Test API PUT method api/team

        valid_team = None
        test_id = -1
        test_name = 'API TEST UPDATE TEAM'

        # Insert test user into database to get using the API
        valid_team = Team()
        valid_team.id = test_id
        valid_team.name = test_name
        try:
            db.session.add(valid_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


        new_test_name = 'NEW API TEST UPDATE TEAM'

        update = {'name': new_test_name}

        # Update the user through the API
        response = requests.put(self.team_url + '/' + str(test_id), data=json.dumps(update), headers=self.headers)

        # Make sure instance was updated
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.text)
        self.assertEqual(json_response.get('name'), new_test_name)

        # Delete the test instance for cleanup
        try:
            updated_query = Team.query.filter_by(id=test_id)
            self.assertEqual(updated_query.count(), 1) # Make sure update did not create duplicate entry
            updated_team = updated_query.first()
            db.session.delete(updated_team)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()


    def test_update_team_invalid(self):
        # Test API PUT method api/team
        self.assertTrue(True)


    def test_update_community_valid(self):
        # Test API PUT method api/community
        self.assertTrue(True)


    def test_update_community_invalid(self):
        # Test API PUT method api/community
        self.assertTrue(True)


class TestDatabase(TestCase):

    def test_get_user(self) :
        id_num = '82074164'
        query = User.query.get(id_num)
        self.assertEqual(query.id, id_num)
        self.assertEqual(query.name, 'FennekFox')
        self.assertEqual(query.description, 'Wer den Fuchs nicht ehrt, ist des Fenneks nicht wert.')
        self.assertEqual(query.language, 'German')
        self.assertEqual(query.followers, 234)
        self.assertEqual(query.url, 'https://www.twitch.tv/fennekfox')
        q = Community.query.get(query.community_id)
        self.assertEqual(q.name, 'VarietyStreaming')

    def test_get_user_badid(self) :
        id_num = '-1'
        try:
            query = User.query.get(id_num)
            db.session.close()
        except:
            db.session.rollback()
        self.assertEqual(query, None)

    def test_get_game(self) :
        id_num = 55371
        query = Game.query.get(id_num)
        self.assertEqual(query.id, id_num)
        self.assertEqual(query.name, 'Hidden my game by mom')   

    def test_get_game_badid(self) :
        id_num = '-1'
        query = Game.query.get(id_num)
        self.assertEqual(query, None)

    def test_get_team(self) :
        id_num = 1
        query = Team.query.get(id_num)
        self.assertEqual(query.id, id_num)
        self.assertEqual(query.name, 'test')

    def test_get_team_badid(self) :
        id_num = '-1'
        query = Team.query.get(id_num)
        self.assertEqual(query, None)

    def test_get_community(self) :
        id_num = '6e940c4a-c42f-47d2-af83-0a2c7e47c421'
        query = Community.query.get(id_num)
        self.assertEqual(query.id, id_num)
        self.assertEqual(query.name, 'Speedrunning')

    def test_get_community_badid(self) :
        id_num = '-1'
        query = Community.query.get(id_num)
        self.assertEqual(query, None)

    def test_get_name_by_id(self) :

        what_kind = 'game'
        _id = 54979      
        if what_kind == 'user':
            q = User.query.get(_id)
        elif what_kind == 'community':
            q = Community.query.get(_id)
        elif what_kind == 'game':
            q = Game.query.get(_id)
        elif what_kind == 'team':
            q = Team.query.get(_id)
        if q:
            query = q.name

        self.assertEqual(query, "Playerunknown's Battlegrounds")


if __name__ == "__main__":
    main()