from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from application import db
from application.models import User, Team, Game, Community
from sqlalchemy.sql.expression import func
from sqlalchemy import inspect
import flask_restless
import flask_whooshalchemy as wa

import datetime
import requests

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}
gb_id = '/?api_key=d483af9dcc46474051b451953aa550322df2b793&format=json'

# Create the Flask app
application = Flask(__name__)
application.debug = True


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://dev-env.fkmjb3y3r4.us-west-2.elasticbeanstalk.com'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(application, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT']).after_request(add_cors_headers)
manager.create_api(Team, methods=['GET', 'POST', 'DELETE', 'PUT']).after_request(add_cors_headers)
manager.create_api(Game, methods=['GET', 'POST', 'DELETE', 'PUT']).after_request(add_cors_headers)
manager.create_api(Community, methods=['GET', 'POST', 'DELETE', 'PUT']).after_request(add_cors_headers)

# print a nice greeting.
@application.route('/')
def show_home_page():
    return render_template('index.html')

@application.route('/users')
def show_all_users():
    return render_users(users_filter=None, users_sort=None)


@application.route('/games')
def show_all_games():
    return render_games(games_filter=None, games_sort=None)


@application.route('/teams')
def show_all_teams():
    return render_teams(teams_filter=None, teams_sort=None)    


@application.route('/communities')
def show_all_communities():
    return render_communities(communities_filter=None, communities_sort=None)    


@application.route('/users/<wow>')
def show_users(wow):
    q = User.query.get(wow)
    user = {}
    games = []
    teams = []
    communities = []
    user['id'] = q.id
    user['name'] = q.name
    user['description'] = q.description
    user['language'] = q.language
    user['views'] = q.views
    user['followers'] = q.followers
    user['url'] = q.url
    user['created'] = q.created.date()
    user['updated'] = q.updated.date()
    image_url = q.image_url
    if not image_url:
        image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
    user['image_url'] = image_url

    # Connections

    user['game_id'] = q.game_id
    if user['game_id']:
        user['game'] = get_name_by_id(q.game_id, 'game')

    # Get all games for edit drop down
    game_query = Game.query
    for game in game_query:
        games.append({'name': game.name, 'id': game.id})

    # Get all teams for edit drop down
    team_query = Team.query
    for team in team_query:
        teams.append({'name': team.name, 'id': team.id})

    # Get all communities for edit drop down
    community_query = Community.query
    for community in community_query:
        communities.append({'name': community.name, 'id': community.id})
    
    user['community_id'] = q.community_id
    if user['community_id']:
        user['community'] = get_name_by_id(q.community_id, 'community')
    

    user['team_ids'] = q.team_ids
    user['team_names'] = {}
    if user['team_ids']:
        for _id in user['team_ids']:
            user['team_names'][_id] = get_name_by_id(_id, 'team')

    return render_template('user_template.html', user = user, games = games, communities=communities, teams=teams)

@application.route('/games/<wow>')
def show_games(wow):
    q = Game.query.get(wow)
    game = {}
    users = []
    teams = []
    communities = []
    game['id'] = q.id
    game['name'] = q.name
    game['description'] = q.description
    game['rating'] = q.rating
    game['genres'] = q.genres
    game['platforms'] = q.platforms
    game['release_date'] = q.release_date.date()
    image_url = q.image_url
    if not image_url:
        image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
    game['image_url'] = image_url

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


    # Get all users for edit drop down
    users_query = User.query
    for user in users_query:
        users.append({'name': user.name, 'id': user.id})

    # Get all teams for edit drop down
    team_query = Team.query
    for team in team_query:
        teams.append({'name': team.name, 'id': team.id})

    # Get all communities for edit drop down
    community_query = Community.query
    for community in community_query:
        communities.append({'name': community.name, 'id': community.id})

    return render_template('game_template.html', game = game, streamers=users, teams=teams, communities=communities)

@application.route('/teams/<wow>')
def show_teams(wow):
    q = Team.query.get(wow)
    team = {}
    users = []
    games = []
    team['name'] = q.name
    team['info'] = q.info
    team['created'] = q.created.date()
    team['updated'] = q.updated.date()
    image_url = q.image_url
    if not image_url:
        image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
    team['image_url'] = image_url

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


    # Get all users for edit drop down
    users_query = User.query
    for user in users_query:
        users.append({'name': user.name, 'id': user.id})


    # Get all games for edit drop down
    games_query = Game.query
    for game in games_query:
        games.append({'name': game.name, 'id': game.id})

    return render_template('team_template.html', team = team, streamers=users, games=games)

@application.route('/communities/<wow>')
def show_communities(wow):
    q = Community.query.get(wow)
    community = {}
    games = []
    users = []
    community['name'] = q.name
    community['description'] = q.description
    community['language'] = q.language
    community['rules'] = q.rules
    image_url = q.image_url
    if not image_url:
        image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
    community['image_url'] = image_url

    # Connections

    community['game_id'] = q.game_id
    if community['game_id']:
        community['game'] = get_name_by_id(q.game_id, 'game')

    community['owner_id'] = q.owner_id
    if community['owner_id']:
        community['owner'] = get_name_by_id(q.owner_id, 'user')

    # Get all users for edit drop down
    users_query = User.query
    for user in users_query:
        users.append({'name': user.name, 'id': user.id})

    # Get all games for edit drop down
    games_query = Game.query
    for game in games_query:
        games.append({'name': game.name, 'id': game.id})

    return render_template('community_template.html', community = community, users=users, games=games)


@application.route('/filter/users')
def handle_user_filter_form():
    views = request.args.get('views')
    if views == None:
        return redirect('/')

    return render_users(users_filter=int(views), users_sort=None)


@application.route('/filter/games')
def handle_game_filter_form():
    rating = request.args.get('rating')
    if rating == None:
        return redirect('/')

    return render_games(games_filter=rating, games_sort=None)


@application.route('/filter/teams')
def handle_team_filter_form():
    members = request.args.get('members')
    if members == None:
        return redirect('/')

    return render_teams(teams_filter=int(members), teams_sort=None)

@application.route('/filter/communities')
def handle_communities_filter_form():
    image_filter = False
    has_image = request.args.get('has-image')
    if has_image == None:
        return redirect('/')
    else:
        image_filter = True

    return render_communities(communities_filter=image_filter, communities_sort=None)

@application.route('/sort/<model_type>/<type_sort>')
def handle_sort_az(type_sort, model_type):
    if type_sort == None:
        return redirect('/')
    if model_type == 'users':
        return render_users(users_filter=None, users_sort=type_sort)
    elif model_type == 'games':
        return render_games(games_filter=None, games_sort=type_sort)
    elif model_type == 'teams':
        return render_teams(teams_filter=None, teams_sort=type_sort)
    elif model_type == 'communities':
        return render_communities(communities_filter=None, communities_sort=type_sort)

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


def render_users(users_filter, users_sort):
    users = []
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
            image_url = q.image_url
            if not image_url:
                image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
            user['image_url'] = image_url
            if user['name']:
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
    return render_template('users.html', users=users, user_filter=users_filter)

def render_games(games_filter, games_sort):
    games = []
    try:  
        if games_filter:
            query_db = Game.query.filter(Game.rating == games_filter)
        else:
            query_db = Game.query
        for q in query_db:
            game = {}
            game['id'] = q.id
            game['name'] = q.name
            image = q.image_url
            if not image:
                image = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png' # Twitch's default image
            game['image_url'] = image
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
    return render_template('games.html', games=games, games_filter=games_filter)


def render_teams(teams_filter, teams_sort):
    teams = []
    try:  
        if teams_filter:
            query_db = Team.query.filter(func.array_length(Team.user_ids,1) > teams_filter)
        else:
            query_db = Team.query
        for q in query_db:
            team = {}
            team['id'] = q.id
            team['name'] = q.name
            image_url = q.image_url
            if not image_url:
                image_url = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
            team['image_url'] = image_url
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
    return render_template('teams.html', teams=teams, team_filter=teams_filter)


def render_communities(communities_filter, communities_sort):
    communities = []
    try:
        query_db = Community.query
        for q in query_db:
            community = {}
            community['id'] = q.id
            community['name'] = q.name
            community_image = q.image_url
            if community_image == '':
                if not communities_filter:
                    community['image_url'] = 'https://static-cdn.jtvnw.net/jtv_user_pictures/xarth/404_user_70x70.png'
                    communities.append(community)
            else:
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
    return render_template('communities.html', communities=communities, communities_filter=communities_filter)

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


@application.route('/search', methods = ['GET', 'POST'])
def search():
    search_string = request.args.get('search_string')
    wildcard_search_string = ''
    and_wildcard_search_string = ''

    # Split search string to make each term into a wildcard keyword
    # only used for OR searches
    split_search_string = search_string.split(' ')
    for i in split_search_string:
        wildcard_search_string += '*' + i + '* '

    # Wildcard search string, only used for AND searches. THere's a long explanation why
    # but im not going to bother
    # NVM Scratch that. wildcard searches when connected with AND operators make things really
    # weird, so don't make it default for this
#    and_wildcard_search_string = '*' + search_string + '*' + ' ' + search_string

    split_terms = search_string.split()
    num_terms = len(split_terms)

    #Separated results in case it's more convenient...depends on how we do the search results page I guess
    #user_search_result = User.query.whoosh_search(input).all()
    #game_search_result = Game.query.whoosh_search(input).all()
    #team_search_result = Team.query.whoosh_search(input).all()
    #community_search_result = Community.query.whoosh_search(input).all()


    # returns search results with default "and" operator
    user_search_results = []
    game_search_results = []
    team_search_results = []
    community_search_results = []
    for user in User.query.whoosh_search(search_string).all() :
        user_search_results.append(object_as_dict(user))
    for game in Game.query.whoosh_search(search_string).all() :
        game_search_results.append(object_as_dict(game))
    for team in Team.query.whoosh_search(search_string).all() :
        team_search_results.append(object_as_dict(team))
    for community in Community.query.whoosh_search(search_string).all() :
        community_search_results.append(object_as_dict(community))

    print(len(user_search_results))
    # returns search results using "or" operator
    user_search_results_or = []
    game_search_results_or = []
    team_search_results_or = []
    community_search_results_or = []
    if num_terms > 1 :
        for user in User.query.whoosh_search(wildcard_search_string, or_=True).all() :
            user_search_results_or.append(object_as_dict(user))
        for game in Game.query.whoosh_search(wildcard_search_string, or_=True).all() :
            game_search_results_or.append(object_as_dict(game))
        for team in Team.query.whoosh_search(wildcard_search_string, or_=True).all() :
            team_search_results_or.append(object_as_dict(team))
        for community in Community.query.whoosh_search(wildcard_search_string, or_=True).all() :
            community_search_results_or.append(object_as_dict(community))

    print(len(user_search_results))

    return render_template('search_results_template.html', num_terms=num_terms, search_string=search_string, split_terms = split_terms, 
        user_search_results=user_search_results, game_search_results=game_search_results, team_search_results=team_search_results, 
        community_search_results=community_search_results, user_search_results_or=user_search_results_or, game_search_results_or=game_search_results_or, 
        team_search_results_or=team_search_results_or, community_search_results_or=community_search_results_or)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()