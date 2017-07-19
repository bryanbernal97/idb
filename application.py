from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
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
application.secret_key = 'some_secret'
application.debug = True

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(application, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Team, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Game, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(Community, methods=['GET', 'POST', 'DELETE', 'PUT'])

######################## ADD NEW MODELS ##############################

@application.route('/addUser', methods=['POST', 'GET'])
def add_user():
<<<<<<< HEAD
    return 0

@application.route('/addGame', methods=['POST', 'GET'])
def add_game():
    return 0

@application.route('/addTeam', methods=['POST', 'GET'])
def add_team():
    return 0

@application.route('/addCommunity', methods=['POST', 'GET'])
def add_community():
    return 0
=======
    if request.method == 'GET':
        return render_template('add_user.html')
    else:

@application.route('/addGame', methods=['POST', 'GET'])
def add_game():
    if request.method == 'GET':
        return render_template('add_game.html')
    else:

@application.route('/addTeam', methods=['POST', 'GET'])
def add_team():
    if request.method == 'GET':
        return render_template('add_team.html')
    else:

@application.route('/addCommunity', methods=['POST', 'GET'])
def add_community():
    if request.method == 'GET':
        return render_template('add_community.html')
    else:
>>>>>>> 408482ae2f30f21a6c0735539aa4fad490c93ba9

####################### UPDATE MODELS ################################

@application.route('/updateUser', methods=['POST'])
def update_user():
    user_id = request.form.get('user-id-edit')
    new_name = request.form.get('user-name-edit')
    new_description = request.form.get('user-description-edit')
    new_language = request.form.get('user-language-edit')
    new_views = request.form.get('user-views-edit')
    new_followers = request.form.get('user-followers-edit')
    new_url = request.form.get('user-url-edit')
    
    new_game_id = request.form.get('user-game-edit')
    if new_game_id:
        new_game_id = int(new_game_id)
    
    new_community_id = request.form.get('user-community-edit')

    new_team_ids = request.form.getlist('user-teams-edit')
    if new_team_ids:
        new_team_ids = list(map(int, new_team_ids))
    new_created = request.form.get('user-created-edit')
    new_updated = request.form.get('user-updated-edit')
    # user_captcha = request.form.get('')

    successful_user_update = True
    successful_game_update = True
    successful_community_update = True
    successful_teams_update = True

    try:
        user = User.query.get(user_id)
        old_game_id = user.game_id
        old_community_id = user.community_id
        old_team_ids = user.team_ids

        # Update connections

        # Game connection has changed so need to remove user from old game connection instance
        # and add user to new game connection instance
        if old_game_id != new_game_id:
            if old_game_id:
                try:
                    old_game_query = Game.query.filter(Game.id == old_game_id)
                    old_game = old_game_query.first()
                    old_game_user_ids = old_game.user_ids

                    if old_game_user_ids and user_id in old_game_user_ids:
                        old_game_user_ids.remove(user_id)

                    old_game_query.update({'user_ids': old_game_user_ids})                          # UPDATED OLD GAME CONNECTION'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('Old Game Exception: ' + str(e))
                    successful_game_update = False

            if new_game_id:
                try:
                    new_game_query = Game.query.filter(Game.id == new_game_id)
                    new_game = new_game_query.first()
                    new_game_user_ids = new_game.user_ids

                    if new_game_user_ids and user_id not in new_game_user_ids:
                        new_game_user_ids.append(user_id)
                    elif not new_game_user_ids:
                        new_game_user_ids = [user_id]

                    new_game_query.update({'user_ids': new_game_user_ids})                          # UPDATED NEW GAME CONNECTION'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('New Game Exception: ' + str(e))
                    successful_game_update = False

        user.game_id = new_game_id                                                                  # UPDATED USER INSTANCE: GAME ID

        if old_community_id != new_community_id:
            if old_community_id:
                try:
                    old_community = Community.query.get(old_community_id)
                    old_community_owner_id = old_community.owner_id
                    if user_id == old_community_owner_id:
                        old_community.owner_id = None                                               # UPDATED OLD COMMUNITY'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('Old Community Exception: ' + str(e))
                    successful_community_update = False

            if new_community_id:
                try:
                    new_community = Community.query.get(new_community_id)
                    new_community.owner_id = user_id                                                # UPDATED NEW COMMUNITY'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('New Community Exception: ' + str(e))
                    successful_community_update = False

        user.community_id = new_community_id                                                        # UPDATED USER INSTANCE: COMMUNITY ID

        old_team_ids_set = set()
        new_team_ids_set = set()

        if old_team_ids:
            old_team_ids_set = set(old_team_ids)
        if new_team_ids:
            new_team_ids_set = set(new_team_ids)
        if (old_team_ids_set != new_team_ids_set):
            if old_team_ids:
                for old_team_id in old_team_ids:
                    if old_team_id not in new_team_ids:
                        # User used to have team but now doesn't so need to remove user from that team
                        try:
                            old_team_query = Team.query.filter(Team.id == old_team_id)
                            old_team = old_team_query.first()
                            old_team_user_ids = old_team.user_ids
                            if old_team_user_ids and user_id in old_team_user_ids:
                                old_team_user_ids.remove(user_id)

                            old_team_query.update({'user_ids': old_team_user_ids})                  # UPDATED AN OLD TEAM'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            # print('Old Team Exception: ' + str(e))
                            successful_teams_update = False

            if new_team_ids:
                for new_team_id in new_team_ids:
                    if new_team_id not in old_team_ids:
                        # User did not previously have team but now does so need to add user to that team
                        try:
                            new_team_query = Team.query.filter(Team.id == new_team_id)
                            new_team = new_team_query.first()
                            new_team_user_ids = new_team.user_ids
                            
                            if new_team_user_ids:
                                new_team_user_ids.append(user_id)
                            else:
                                new_team_user_ids = [user_id]

                            new_team_query.update({'user_ids': new_team_user_ids})                  # UPDATED A NEW TEAM'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            # print('New Team Exception: ' + str(e))
                            successful_teams_update = False

        # db.session.flush()
        user.team_ids = new_team_ids                                                                # UPDATED USER INSTANCE: TEAM IDS
        user.name = new_name                                                                        # UPDATED USER INSTANCE: NAME
        user.description = new_description                                                          # UPDATED USER INSTANCE: DESCRIPTION
        user.language = new_language                                                                # UPDATED USER INSTANCE: LANGUAGE
        user.views = new_views                                                                      # UPDATED USER INSTACNE: VIEWS
        user.followers = new_followers                                                              # UPDATED USER INSTANCE: FOLLOWERS
        user.url = new_url                                                                          # UPDATED USER INSTANCE: URL
        user.created = datetime.datetime.strptime(new_created, '%Y-%m-%d')                          # UPDATED USER INSTANCE: CREATED
        user.updated = datetime.datetime.strptime(new_updated, '%Y-%m-%d')                          # UPDATED USER INSTANCE: UPDATED
        # db.session.flush()
        db.session.commit()
    except Exception as user_exception:
        db.session.rollback()
        print('User Exception: ' + str(user_exception))
        successful_user_update = False


    if (successful_user_update and successful_game_update and successful_community_update and successful_teams_update):
        flash('Congratulations, the user was updated successfuly!', 'success')
    else:
        flash('Sorry, something went wrong :(', 'danger')

    redirect_url = '/users/' + user_id
    return redirect(redirect_url)

@application.route('/updateGame', methods=['POST'])
def update_game():
    game_id = int(request.form.get('game-id-edit'))
    new_name = request.form.get('game-name-edit')
    new_description = request.form.get('game-description-edit')
    new_rated = request.form.get('game-rating-edit')
    new_genres = request.form.getlist('genres[]')
    new_genres = list(filter(None, new_genres))
    # print('new genres: ' + str(new_genres))
    new_platforms = request.form.getlist('platforms[]')
    new_platforms = list(filter(None, new_platforms))
    # print('new platforms: ' + str(new_platforms))
    new_release_date = request.form.get('game-release-date-edit')
    new_user_ids = request.form.getlist('game-streamers-edit')
    new_team_ids = request.form.getlist('game-teams-edit')

    if new_team_ids:
        new_team_ids = list(map(int, new_team_ids))
    
    new_community_ids = request.form.getlist('game-communities-edit')

    successful_user_update = True
    successful_game_update = True
    successful_team_update = True
    successful_community_update = True

    try:
        game = Game.query.get(game_id)
        old_user_ids = game.user_ids
        old_team_ids = game.team_ids
        old_community_ids = game.community_ids

        old_user_ids_set = set()
        new_user_ids_set = set()
        if old_user_ids:
            old_user_ids_set = set(old_user_ids)
        if new_user_ids:
            new_user_ids_set = set(new_user_ids)

        if (old_user_ids_set != new_user_ids_set):
            if old_user_ids:
                for old_user_id in old_user_ids:
                    if old_user_id not in new_user_ids:
                        try:
                            old_user = User.query.get(old_user_id)
                            old_user.game_id = None                                                 # UPDATED AN OLD USERS'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print('Old User Exception: ' + str(e))
                            successful_user_update = False

            if new_user_ids:
                print('new_user_ids: ' + str(new_user_ids))
                print('type of user ids: ' + str(type(new_user_ids)))
                for new_user_id in new_user_ids:
                    if new_user_id not in old_user_ids:
                        # User did not previously have user but now does so need to add game to that user
                        try:
                            print('new_user_id: ' + str(new_user_id))
                            new_user = User.query.get(new_user_id)
                            print('new_user: ' + str(new_user))
                            new_user.game_id = game_id                                              # UPDATED A NEW USER'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print('New User Exception: ' + str(e))
                            successful_user_update = False

        game.user_ids = new_user_ids                                                                # UPDATED GAME INSTANCE: USER IDS



        old_community_ids_set = set()
        new_community_ids_set = set()
        if old_community_ids:
            old_community_ids_set = set(old_community_ids)
        if new_community_ids:
            new_community_ids_set = set(new_community_ids)

        if (old_community_ids_set != new_community_ids_set):
            if old_community_ids:
                for old_community_id in old_community_ids:
                    if old_community_id not in new_community_ids:
                        try:
                            old_community = Community.query.get(old_community_id)
                            old_community.game_id = None                                            # UPDATED AN OLD COMMUNITY'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print('Old Community Exception: ' + str(e))
                            successful_community_update = False

            if new_community_ids:
                for new_community_id in new_community_ids:
                    if new_community_id not in old_community_ids:
                        try:
                            new_community = Community.query.get(new_community_id)
                            new_community.game_id = game_id                                         # UPDATED A NEW COMMUNITY'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print('New Community Exception: ' + str(e))
                            successful_community_update = False

        game.community_ids = new_community_ids                                                      # UPDATED GAME INSTANCE: COMMUNITY IDS


        old_team_ids_set = set()
        new_team_ids_set = set()
        if old_team_ids:
            old_team_ids_set = set(old_team_ids)
        if new_team_ids:
            new_team_ids_set = set(new_team_ids)

        if (old_team_ids_set != new_team_ids_set):
            if old_team_ids:
                for old_team_id in old_team_ids:
                    if old_team_id not in new_team_ids:
                        try:
                            old_team_query = Team.query.filter(Team.id == old_team_id)
                            old_team = old_team_query.first()
                            old_team_game_ids = old_team.game_ids
                            if old_team_game_ids and game_id in old_team_game_ids:
                                old_team_game_ids.remove(game_id)

                            old_team_query.update({'game_ids': old_team_game_ids})                  # UPDATED AN OLD TEAM'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print('Old Team Exception: ' + str(e))
                            successful_teams_update = False

            if new_team_ids:
                for new_team_id in new_team_ids:
                    if new_team_id not in old_team_ids:
                        # Game did not previously have team but now does so need to add game to that team
                        try:
                            new_team_query = Team.query.filter(Team.id == new_team_id)
                            new_team = new_team_query.first()
                            new_team_game_ids = new_team.game_ids
                            
                            if new_team_game_ids:
                                new_team_game_ids.append(game_id)
                            else:
                                new_team_game_ids = [game_id]

                            new_team_query.update({'game_ids': new_team_game_ids})                  # UPDATED A NEW TEAM'S INSTANCE
                            db.session.commit()
                        except Exception as e:
                            db.session.rollback()
                            print('New Team Exception: ' + str(e))
                            successful_teams_update = False

        game.team_ids = new_team_ids                                                                # UPDATED GAME INSTANCE: TEAM IDS
        game.name = new_name
        game.description = new_description
        game.rated = new_rated
        game.genres = new_genres
        game.platforms = new_platforms
        game.release_date = datetime.datetime.strptime(new_release_date, '%Y-%m-%d')

        db.session.commit()
    except Exception as err:
        db.session.rollback()
        print('Game Exception: ' + str(err))
        successful_game_update = False


    if (successful_user_update and successful_game_update and successful_team_update and successful_community_update):
        flash('Congratulations, the user was updated successfuly!', 'success')
    else:
        flash('Sorry, something went wrong :(', 'danger')

    redirect_url = '/games/' + str(game_id)
    return redirect(redirect_url)

@application.route('/updateTeam', methods=['POST'])
def update_team():
    team_id = request.form.get('team-id-edit')
    team_name = request.form.get('team-name-edit')
    team_info = request.form.get('team-info-edit')

    # team_captcha = request.form.get('')

    successful_user_update = True
    successful_game_update = True       # Need to delete this user from old game and add this user to new game
    successful_team_update = True  # Need to delete this user from old game and add this user to new game
    successful_community_update = True

    if (successful_user_update and successful_game_update and successful_team_update and successful_community_update):
        flash('Congratulations, the user was updated successfuly!', 'success')
    else:
        flash('Sorry, something went wrong :(', 'danger')

    redirect_url = '/teams/' + team_id
    return redirect(redirect_url)

@application.route('/updateCommunity', methods=['POST'])
def update_community():
    community_id = request.form.get('community-id-edit')
    new_name = request.form.get('community-name-edit')
    new_description = request.form.get('community-description-edit')
    new_language = request.form.get('community-language-edit')
    new_rules = request.form.get('community-rules-edit')
    
    new_game_id = request.form.get('community-game-edit')
    if new_game_id:
        new_game_id = int(new_game_id)
    
    new_owner_id = request.form.get('community-owner-edit')
    if new_owner_id:
        new_owner_id = int(new_owner_id)

    # community_captcha = request.form.get('')

    successful_owner_update = True
    successful_game_update = True       # Need to delete this community from old game and add this community to new game

    try:
        community = Community.query.get(community_id)
        old_game_id = community.game_id
        old_owner_id = community.owner_id

        # Update connections

        # Game connection has changed so need to remove community from old game connection instance
        # and add community to new game connection instance
        if old_game_id != new_game_id:
            if old_game_id:
                try:
                    old_game_query = Game.query.filter(Game.id == old_game_id)
                    old_game = old_game_query.first()
                    old_game_community_ids = old_game.community_ids

                    if old_game_community_ids and community_id in old_game_community_ids:
                        old_game_community_ids.remove(community_id)

                    old_game_query.update({'community_ids': old_game_community_ids})                          # UPDATED OLD GAME CONNECTION'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('Old Game Exception: ' + str(e))
                    successful_game_update = False

            if new_game_id:
                try:
                    new_game_query = Game.query.filter(Game.id == new_game_id)
                    new_game = new_game_query.first()
                    new_game_community_ids = new_game.community_ids

                    # Use list() constructor to copy the list so it actually updates
                    if new_game_community_ids and community_id not in new_game_community_ids:
                        new_game_community_ids.append(community_id)
                    elif not new_game_community_ids:
                        new_game_community_ids = [community_id]

                    new_game_query.update({'community_ids': new_game_community_ids})                          # UPDATED NEW GAME CONNECTION'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('New Game Exception: ' + str(e))
                    successful_game_update = False

        community.game_id = new_game_id                                                                  # UPDATED community INSTANCE: GAME ID

        if old_owner_id != new_owner_id:
            if old_owner_id:
                try:
                    old_community = Community.query.get(old_owner_id)
                    old_community_owner_id = old_community.owner_id
                    if owner_id == old_community_owner_id:
                        old_community.owner_id = None                                               # UPDATED OLD COMMUNITY'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('Old Community Exception: ' + str(e))
                    successful_owner_update = False

            if new_owner_id:
                try:
                    new_community = Community.query.get(new_owner_id)
                    new_community.owner_id = owner_id                                                # UPDATED NEW COMMUNITY'S INSTANCE
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    # print('New Community Exception: ' + str(e))
                    successful_owner_update = False

        community.owner_id = new_owner_id                                          # UPDATED community INSTANCE: COMMUNITY ID

        # db.session.flush()
        community.name = new_name
        community.description = new_description
        community.language = new_language 
        community.rules = new_rules
        # db.session.flush()
        db.session.commit()
    except Exception as community_exception:
        db.session.rollback()
        print('community Exception: ' + str(community_exception))
        successful_owner_update = False


    if (successful_owner_update and successful_game_update):
        flash('Congratulations, the community was updated successfuly!', 'success')
    else:
        flash('Sorry, something went wrong :(', 'danger')

    redirect_url = '/communities/' + community_id
    return redirect(redirect_url)


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
    team['id'] = wow
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
    community['id'] = wow
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
        user_search_results.append(user)
    for game in Game.query.whoosh_search(search_string).all() :
        game_search_results.append(game)
    for team in Team.query.whoosh_search(search_string).all() :
        team_search_results.append(team)
    for community in Community.query.whoosh_search(search_string).all() :
        community_search_results.append(community)
    for user in User.query.whoosh_search(wildcard_search_string).all() :
        user_search_results.append(user)
    for game in Game.query.whoosh_search(wildcard_search_string).all() :
        game_search_results.append(game)
    for team in Team.query.whoosh_search(wildcard_search_string).all() :
        team_search_results.append(team)
    for community in Community.query.whoosh_search(wildcard_search_string).all() :
        community_search_results.append(community)

    user_search_results = list(set(user_search_results))
    game_search_results = list(set(game_search_results))
    team_search_results = list(set(team_search_results))
    community_search_results = list(set(community_search_results))

    user_search_results2 = user_search_results
    game_search_results2 = game_search_results
    team_search_results2 = team_search_results
    community_search_results2 = community_search_results

    user_search_results = []
    game_search_results = []
    team_search_results = []
    community_search_results = []

    for user in user_search_results2:
        user_search_results.append(object_as_dict(user))
    for game in game_search_results2:
        game_search_results.append(object_as_dict(game))
    for team in team_search_results2:
        team_search_results.append(object_as_dict(team))
    for community in community_search_results2:
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