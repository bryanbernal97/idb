from flask import Flask
from flask import render_template
from application import db
from application.models import User, Team, Game, Community
# from application.models import Data
# from application.models import User
# from application.models import Team
# from application.models import Community
# from application.models import Game

import datetime
import requests

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}
gb_id = '/?api_key=d483af9dcc46474051b451953aa550322df2b793&format=json'
top = {}
teams = {}
communities = {}
users = {}
games = {}

# Create the Flask app
application = Flask(__name__)
application.debug = True


# print a nice greeting.
@application.route('/')
def say_hello():
    global top
    users = []
    communities = []
    teams = []
    games = []
    #users
    try:   
        query_db = User.query
        for q in query_db:
            user = {}
            user['id'] = q.id
            user['name'] = q.name
            user['image_url'] = q.image_url
            users += user
        db.session.close()
    except:
        db.session.rollback()
    #games
    try:   
        query_db = Game.query
        for q in query_db:
            game = {}
            game['id'] = q.id
            game['name'] = q.name
            game['image_url'] = q.image_url
            games += game
        db.session.close()
    except:
        db.session.rollback()
    #teams
    try:   
        query_db = Team.query
        for q in query_db:
            team = {}
            team['id'] = q.id
            team['name'] = q.name
            team['image_url'] = q.image_url
            teams += team
        db.session.close()
    except:
        db.session.rollback()
    #communities
    try:   
        query_db = Community.query
        for q in query_db:
            communities = {}
            community['id'] = q.id
            community['name'] = q.name
            community['image_url'] = q.image_url
            communities += community
        db.session.close()
    except:
        db.session.rollback()

    top['users'] = users
    top['communities'] = communities
    top['games'] = games
    top['teams'] = teams
    return render_template('index.html', name=top)

@application.route('/users/<wow>')
def show_users(wow):
    id_num = Integer.parseInt(wow)
    q = User.query.get(id_num)
    user = {}
    user['name'] = q.name
    user['info'] = q.info
    user['language'] = q.language
    user['views'] = q.views
    user['followers'] = q.followers
    user['url'] = q.url
    user['created'] = q.created
    user['updated'] = q.updated
    user['image_url'] = q.image_url

    return render_template('model_template.html', name = user)

@application.route('/games/<wow>')
def show_games(wow):
    id_num = Integer.parseInt(wow)
    q = Game.query.get(id_num)
    game = {}
    game['name'] = q.name
    game['description'] = q.description
    game['genre'] = q.genre
    game['platform'] = q.platform
    game['release_date'] = q.release_date
    game['image_url'] = q.image_url
    game['user_id'] = q.user_id
    game['team_id'] = q.team_id

    return render_template('model_template.html', name = game)

@application.route('/teams/<wow>')
def show_teams(wow):
    q = Team.query.get(id_num)
    team = {}
    team['name'] = q.name
    team['info'] = q.info
    team['created'] = q.created
    team['updated'] = q.updated
    team['image_url'] = q.image_url
    community['user_ids'] = q.user_ids
    community['game_id'] = q.game_id

    return render_template('model_template.html', name = teams[wow])

@application.route('/communities/<wow>')
def show_communities(wow):
    id_num = Integer.parseInt(wow)
    q = Community.query.get(id_num)
    community = {}
    community['name'] = q.name
    community['info'] = q.info
    community['language'] = q.language
    community['rules'] = q.rules
    community['image_url'] = q.image_url
    community['user_ids'] = q.users
    community['game_ids'] = q.games

    return render_template('model_template.html', name = community)

@application.route('/api/v0/user/<wow>', methods=['GET'])
def get_user(wow):
    id_num = Integer.parseInt(wow)
    q = User.query.get(id_num)
    user = {}
    user['name'] = q.name
    user['info'] = q.info
    user['language'] = q.language
    user['views'] = q.views
    user['followers'] = q.followers
    user['url'] = q.url
    user['created'] = q.created
    user['updated'] = q.updated
    user['image_url'] = q.image_url

    return jsonify({'user': user})

@application.route('/api/v0/game/<wow>', methods=['GET'])
def get_game(wow):
    id_num = Integer.parseInt(wow)
    q = Game.query.get(id_num)
    game = {}
    game['name'] = q.name
    game['description'] = q.description
    game['genre'] = q.genre
    game['platform'] = q.platform
    game['release_date'] = q.release_date
    game['image_url'] = q.image_url
    game['user_id'] = q.user_id
    game['team_id'] = q.team_id
    return jsonify({'game': game})

@application.route('/api/v0/team/<wow>', methods=['GET'])
def get_team(wow):
    q = Team.query.get(id_num)
    team = {}
    team['name'] = q.name
    team['info'] = q.info
    team['created'] = q.created
    team['updated'] = q.updated
    team['image_url'] = q.image_url
    community['user_ids'] = q.user_ids
    community['game_id'] = q.game_id
    return jsonify({'team': team})

@application.route('/api/v0/community/<wow>', methods=['GET'])
def get_community(wow):
    id_num = Integer.parseInt(wow)
    q = Community.query.get(id_num)
    community = {}
    community['name'] = q.name
    community['info'] = q.info
    community['language'] = q.language
    community['rules'] = q.rules
    community['image_url'] = q.image_url
    community['user_ids'] = q.users
    community['game_ids'] = q.games
    return jsonify({'community': community})


"""
@application.route('/testWrite')
def testing_db_write():
    notes = str(datetime.datetime.now())
    data_entered = Data(notes=notes)
    try:     
        db.session.add(data_entered)
        db.session.commit()        
        db.session.close()
    except:
        db.session.rollback()
    return render_template('cloud9.html')
"""


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()