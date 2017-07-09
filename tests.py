#!/usr/bin/env python
import requests
from unittest import main, TestCase
from application import db
from application.models import User, Team, Game, Community
import json

class TestApi(TestCase):

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
        query = User.query.get(id_num)
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