#!/usr/bin/env python
import requests
from unittest import main, TestCase
from application import db
from application.models import User, Team, Game, Community
import json

class TestApi(TestCase) :

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


if __name__ == "__main__":
    main()