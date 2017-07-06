from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from application import db
from application.models import User, Team, Game, Community

import datetime
import requests

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}
gb_id = '/?api_key=d483af9dcc46474051b451953aa550322df2b793&format=json'

# Create the Flask app
application = Flask(__name__)
application.debug = True

# print a nice greeting.
@application.route('/')
def say_hello():
    return render_site(users_filter=None, games_filter=None, teams_filter=None, communities_filter=None, users_sort=None, games_sort=None, teams_sort=None, communities_sort=None)

@application.route('/users/<wow>')
def show_users(wow):
    q = User.query.get(wow)
    user = {}
    user['name'] = q.name
    user['description'] = q.description
    user['language'] = q.language
    user['views'] = q.views
    user['followers'] = q.followers
    user['url'] = q.url
    user['created'] = q.created
    user['updated'] = q.updated
    user['image_url'] = q.image_url

    # Connections

    user['game_id'] = q.game_id
    if user['game_id']:
        user['game'] = get_name_by_id(q.game_id, 'game')
    
    user['community_id'] = q.community_id
    if user['community_id']:
        user['community'] = get_name_by_id(q.community_id, 'community')
    

    user['team_ids'] = q.team_ids
    user['team_names'] = {}
    if user['team_ids']:
        for _id in user['team_ids']:
            user['team_names'][_id] = get_name_by_id(_id, 'team')

    return render_template('model_template.html', name = user)

@application.route('/games/<wow>')
def show_games(wow):
    q = Game.query.get(wow)
    game = {}
    game['name'] = q.name
    game['description'] = q.description
    game['genres'] = q.genres
    game['platforms'] = q.platforms
    game['release_date'] = q.release_date
    game['image_url'] = q.image_url

    # Connections

    game['user_ids'] = q.user_ids
    game['user_names'] = {}
    if game['user_ids']:
        for _id in game['user_ids']:
            game['user_names'][_id] = get_name_by_id(_id, 'user')
    game['team_ids'] = q.team_ids
    game['team_names'] = {}
    if game['team_ids']:
        for _id in game['team_ids']:
            game['team_names'][_id] = get_name_by_id(_id, 'team')
    game['community_ids'] = q.community_ids
    game['community_names'] = {}
    if game['community_ids']:
        for _id in game['community_ids']:
            game['community_names'][_id] = get_name_by_id(_id, 'community')

    return render_template('model_template.html', name = game)

@application.route('/teams/<wow>')
def show_teams(wow):
    q = Team.query.get(wow)
    team = {}
    team['name'] = q.name
    team['info'] = q.info
    team['created'] = q.created
    team['updated'] = q.updated
    team['image_url'] = q.image_url

    # Connections

    team['user_ids'] = q.user_ids
    team['user_names'] = {}
    if team['user_ids']:
        for _id in team['user_ids']:
            team['user_names'][_id] = get_name_by_id(_id, 'user')

    team['game_ids'] = q.game_ids
    team['game_names'] = {}
    if team['game_ids']:
        for _id in team['game_ids']:
            team['game_names'][_id] = get_name_by_id(_id, 'game')

    return render_template('model_template.html', name = team)

@application.route('/communities/<wow>')
def show_communities(wow):
    q = Community.query.get(wow)
    community = {}
    community['name'] = q.name
    community['description'] = q.description
    community['language'] = q.language
    community['rules'] = q.rules
    community['image_url'] = q.image_url

    # Connections

    community['game_id'] = q.game_id
    if community['game_id']:
        community['game'] = get_name_by_id(q.game_id, 'game')

    community['owner_id'] = q.owner_id
    if community['owner_id']:
        community['owner'] = get_name_by_id(q.owner_id, 'user')

    return render_template('model_template.html', name = community)

@application.route('/api/v0/user/<wow>', methods=['GET'])
def get_user(wow):
    id_num = Integer.parseInt(wow)
    q = User.query.get(id_num)
    user = {}
    user['name'] = q.name
    user['description'] = q.description
    user['language'] = q.language
    user['views'] = q.views
    user['followers'] = q.followers
    user['url'] = q.url
    user['created'] = q.created
    user['updated'] = q.updated
    user['image_url'] = q.image_url
    user['game_id'] = q.game_id
    user['community_id'] = q.community_id
    user['team_ids'] = q.team_ids
    user['team_names'] = {}
    if user['team_ids']:
        for _id in user['team_ids']:
            user['team_names'][_id] = get_name_by_id(_id, 'team')

    return jsonify({'user': user})

@application.route('/api/v0/game/<wow>', methods=['GET'])
def get_game(wow):
    id_num = Integer.parseInt(wow)
    q = Game.query.get(id_num)
    game = {}
    game['name'] = q.name
    game['description'] = q.description
    game['genres'] = q.genres
    game['platforms'] = q.platforms
    game['release_date'] = q.release_date
    game['image_url'] = q.image_url
    game['user_ids'] = q.user_ids
    game['team_ids'] = q.team_ids
    game['team_names'] = {}
    if game['team_ids']:
        for _id in game['team_ids']:
            game['team_names'][_id] = get_name_by_id(_id, 'team')
    game['community_ids'] = q.community_ids
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
    team['user_ids'] = q.user_ids
    team['game_ids'] = q.game_ids
    return jsonify({'team': team})

@application.route('/api/v0/community/<wow>', methods=['GET'])
def get_community(wow):
    id_num = Integer.parseInt(wow)
    q = Community.query.get(id_num)
    community = {}
    community['name'] = q.name
    community['description'] = q.description
    community['language'] = q.language
    community['rules'] = q.rules
    community['image_url'] = q.image_url
    community['owner_id'] = q.owner_id
    community['game_id'] = q.game_id
    return jsonify({'community': community})


@application.route('/filter/users')
def handle_user_filter_form():
    views = request.args.get('views')
    if views == None:
        return redirect('/')

    return render_site(users_filter=int(views), games_filter=None, teams_filter=None, communities_filter=None, users_sort=None, games_sort=None, teams_sort=None, communities_sort=None)

@application.route('/filter/teams')
def handle_team_filter_form():
    members = request.args.get('members')
    if members == None:
        return redirect('/')

    return render_site(users_filter=None, games_filter=None, teams_filter=int(members), communities_filter=None, users_sort=None, games_sort=None, teams_sort=None, communities_sort=None)

@application.route('/sort/<model_type>/<type_sort>')
def handle_sort_az(type_sort, model_type):
    if type_sort == None:
        return redirect('/')
    if model_type == 'users':
        return render_site(users_filter=None, games_filter=None, teams_filter=None, communities_filter=None, users_sort=type_sort, games_sort=None, teams_sort=None, communities_sort=None)
    elif model_type == 'games':
        return render_site(users_filter=None, games_filter=None, teams_filter=None, communities_filter=None, users_sort=None, games_sort=type_sort, teams_sort=None, communities_sort=None)
    elif model_type == 'teams':
        return render_site(users_filter=None, games_filter=None, teams_filter=None, communities_filter=None, users_sort=None, games_sort=None, teams_sort=type_sort, communities_sort=None)
    elif model_type == 'communities':
        return render_site(users_filter=None, games_filter=None, teams_filter=None, communities_filter=None, users_sort=None, games_sort=None, teams_sort=None, communities_sort=type_sort)

def get_name_by_id(_id, what_kind):
    if what_kind == 'user':
        q = User.query.get(_id)
    elif what_kind == 'community':
        q = Community.query.get(_id)
    elif what_kind == 'game':
        q = Game.query.get(_id)
    elif what_kind == 'team':
        q = Team.query.get(_id)
    if q:
        return q.name
    print(_id)
    q = Team.query.get(_id)
    return None


def render_site(users_filter, games_filter, teams_filter, communities_filter, users_sort, games_sort, teams_sort, communities_sort):
    top = {}
    users = []
    communities = []
    teams = []
    games = []
    #users
    try:
        if users_filter:
            query_db = User.query.filter(User.views > users_filter)
        else:
            query_db = User.query
        for q in query_db:
            user = {}
            user['id'] = q.id
            user['name'] = q.name
            user['image_url'] = q.image_url
            users.append(user)
        if users_sort == 'a-z':
            users = sorted(users, key=lambda k: k['name'])
        if users_sort == 'z-a':
            users = sorted(users, key=lambda k: k['name'])
            users = list(reversed(users))
        db.session.close()
    except Exception as e:
        print(str(e))
        db.session.rollback()
    #games
    try:  
        query_db = Game.query
        for q in query_db:
            game = {}
            game['id'] = q.id
            game['name'] = q.name
            game['image_url'] = q.image_url
            games.append(game)
        if games_sort == 'a-z':
            games = sorted(games, key=lambda k: k['name'])
        if games_sort == 'z-a':
            games = sorted(games, key=lambda k: k['name'])
            games = list(reversed(games))
        db.session.close()
    except Exception as e:
        print(str(e))
        db.session.rollback()
    #teams
    try:  
        if teams_filter:
            query_db = Team.query.filter(len(Team.user_ids) > teams_filter)
        else:
            query_db = Team.query
        for q in query_db:
            team = {}
            team['id'] = q.id
            team['name'] = q.name
            team['image_url'] = q.image_url
            teams.append(team)
        if teams_sort == 'a-z':
            teams = sorted(teams, key=lambda k: k['name'])
        if teams_sort == 'z-a':
            teams = sorted(teams, key=lambda k: k['name'])
            teams = list(reversed(teams))
        db.session.close()
    except Exception as e:
        print(str(e))
        db.session.rollback()
    #communities
    try:   
        query_db = Community.query
        for q in query_db:
            community = {}
            community['id'] = q.id
            community['name'] = q.name
            community['image_url'] = q.image_url
            communities.append(community)
        if communities_sort == 'a-z':
            communities = sorted(communities, key=lambda k: k['name'])
        if communities_sort == 'z-a':
            communities = sorted(communities, key=lambda k: k['name'])
            communities = list(reversed(communities))
        db.session.close()
    except Exception as e:
        print(str(e))
        db.session.rollback()

    top['users'] = users
    top['communities'] = communities
    top['games'] = games
    top['teams'] = teams
    return render_template('index.html', name=top, user_filter=users_filter, team_filter=teams_filter, user_sort=users_sort)
    

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