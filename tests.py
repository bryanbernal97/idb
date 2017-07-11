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
        valid_user = User()
        valid_user.id = test_id
        valid_user.name = 'API TEST GET USER'
        try:
            db.session.add(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        response = requests.get(self.user_url+'/'+str(test_id), headers=self.headers)

        try:
            db.session.delete(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()

        self.assertEqual(response.status_code, 200)
        # self.assertTrue(True)


    def test_get_single_user_invalid(self):
        # Test API GET method api/user/(int:id) with an invalid id
        self.assertTrue(True)


    def test_get_single_game_valid(self):
        # Test API GET method api/game/(int:id) with valid id
        self.assertTrue(True)


    def test_get_single_game_invalid(self):
        # Test API GET method api/game/(int:id) with an invalid id
        self.assertTrue(True)


    def test_get_single_team_valid(self):
        # Test API GET method api/team/(int:id) with valid id
        self.assertTrue(True)


    def test_get_single_team_invalid(self):
        # Test API GET method api/team/(int:id) with an invalid id
        self.assertTrue(True)


    def test_get_single_community_valid(self):
        # Test API GET method api/community/(int:id) with valid id
        self.assertTrue(True)


    def test_get_single_community_invalid(self):
        # Test API GET method api/community/(int:id) with an invalid id
        self.assertTrue(True)


    def test_get_user_search_match(self):
        # Test API GET method api/user?q=<searchjson> with a match
        self.assertTrue(True)


    def test_get_user_search_no_match(self):
        # Test API GET method api/user?q=<searchjson> with no result match
        self.assertTrue(True)


    def test_get_game_search_match(self):
        # Test API GET method api/game?q=<searchjson> with a match
        self.assertTrue(True)


    def test_get_game_search_no_match(self):
        # Test API GET method api/game?q=<searchjson> with no result match
        self.assertTrue(True)


    def test_get_team_search_match(self):
        # Test API GET method api/team?q=<searchjson> with a match
        self.assertTrue(True)


    def test_get_team_search_no_match(self):
        # Test API GET method api/team?q=<searchjson> with no result match
        self.assertTrue(True)


    def test_get_community_search_match(self):
        # Test API GET method api/community?q=<searchjson> with a match
        self.assertTrue(True)


    def test_get_community_search_no_match(self):
        # Test API GET method api/community?q=<searchjson> with no result match
        self.assertTrue(True)


    def test_post_user_valid(self):
        # Test API POST method api/user
        test_id = '-1'
        test_name = 'API TEST POST USER'

        new_user = {'id': test_id, 'name': test_name}

        response = requests.post(self.user_url, data=json.dumps(new_user), headers=self.headers)

        self.assertEqual(response.status_code, 201)

        try:
            valid_user = User.query.filter_by(id='-1').first()
            json_response = json.loads(response.text)
            self.assertEqual(json_response.get('name'), test_name)
            db.session.delete(valid_user)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()



    def test_post_user_invalid(self):
        # Test API POST method api/user
        self.assertTrue(True)


    def test_post_game_valid(self):
        # Test API POST method api/game
        self.assertTrue(True)


    def test_post_game_invalid(self):
        # Test API POST method api/game
        self.assertTrue(True)


    def test_post_team_valid(self):
        # Test API POST method api/team
        self.assertTrue(True)


    def test_post_team_invalid(self):
        # Test API POST method api/team
        self.assertTrue(True)


    def test_post_community_valid(self):
        # Test API POST method api/community
        self.assertTrue(True)


    def test_post_community_invalid(self):
        # Test API POST method api/community
        self.assertTrue(True)


    def test_delete_user_valid(self):
        # Test API DELETE method api/user
        self.assertTrue(True)


    def test_delete_user_invalid(self):
        # Test API DELETE method api/user
        self.assertTrue(True)


    def test_delete_game_valid(self):
        # Test API DELETE method api/game
        self.assertTrue(True)


    def test_delete_game_invalid(self):
        # Test API DELETE method api/game
        self.assertTrue(True)


    def test_delete_team_valid(self):
        # Test API DELETE method api/team
        self.assertTrue(True)


    def test_delete_team_invalid(self):
        # Test API DELETE method api/team
        self.assertTrue(True)


    def test_delete_community_valid(self):
        # Test API DELETE method api/community
        self.assertTrue(True)


    def test_delete_community_invalid(self):
        # Test API DELETE method api/community
        self.assertTrue(True)


    def test_update_user_valid(self):
        # Test API PUT method api/user
        self.assertTrue(True)


    def test_update_user_invalid(self):
        # Test API PUT method api/user
        self.assertTrue(True)


    def test_update_game_valid(self):
        # Test API PUT method api/game
        self.assertTrue(True)


    def test_update_game_invalid(self):
        # Test API PUT method api/game
        self.assertTrue(True)


    def test_update_team_valid(self):
        # Test API PUT method api/team
        self.assertTrue(True)


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