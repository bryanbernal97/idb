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
    if request.method == 'GET':
        games = []
        teams = []
        communities = []
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


        today = datetime.datetime.now().date()
        return render_template('add_user.html', games=games, communities=communities, teams=teams, today=today)
    else:
        # do the add to the db here and then render instance page of the added user
        user_id = request.form.get('user-id-add')
        user_image_url = request.form.get('user-image-url-add')
        name = request.form.get('user-name-add')
        description = request.form.get('user-description-add')
        language = request.form.get('user-language-add')
        views = request.form.get('user-views-add')
        if views:
            views = int(views.replace(',', ''))
        followers = request.form.get('user-followers-add')
        if followers:
            followers = int(followers.replace(',', ''))
        url = request.form.get('user-url-add')
        game_id = request.form.get('user-game-add')
        if game_id:
            game_id = int(game_id)
        community_id = request.form.get('user-community-add')
        team_ids = request.form.getlist('user-teams-add')

        if team_ids:
            team_ids = list(map(int, team_ids))

        success = True

        if game_id:
            success = (add_user_to_game(user_id, game_id) and success)

        if community_id:
            success = (add_user_to_community(user_id, community_id) and success)

        if team_ids:
            for team_id in team_ids:
                success = (add_user_to_team(user_id, team_id) and success)

        created = request.form.get('user-created-add')
        updated = request.form.get('user-updated-add')

        try:
            user = User()
            user.id = user_id
            user.image_url = user_image_url
            user.name = name
            user.description = description
            user.language = language
            user.views = views
            user.followers = followers
            user.url = url
            user.game_id = game_id
            user.community_id = community_id
            user.team_ids = team_ids
            user.created = datetime.datetime.strptime(created, '%Y-%m-%d')
            user.updated = datetime.datetime.strptime(updated, '%Y-%m-%d')
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            success = False

        if (success):
            flash('Congratulations, the user was added successfuly!', 'success')
            redirect_url = '/users/' + user_id
        else:
            flash('Sorry, something went wrong :(', 'danger')
            redirect_url = '/users'
        
        return redirect(redirect_url)

@application.route('/addTeam', methods=['POST', 'GET'])
def add_team():
    if request.method == 'GET':
        games = []
        streamers = []

         # Get all users for edit drop down
        users_query = User.query
        for user in users_query:
            streamers.append({'name': user.name, 'id': user.id})

        # Get all games for edit drop down
        game_query = Game.query
        for game in game_query:
            games.append({'name': game.name, 'id': game.id})


        today = datetime.datetime.now().date()
        return render_template('add_team.html', games=games, streamers=streamers, today=today)
    else:
        # do the add to the db here and then render instance page of the added team
        team_id = request.form.get('team-id-add')
        if team_id:
            team_id = int(team_id)
        team_image_url = request.form.get('team-image-url-add')
        name = request.form.get('team-name-add')
        info = request.form.get('team-info-add')
        url = request.form.get('team-url-add')
        game_ids = request.form.getlist('team-games-add')
        # print('team game ids: ' + str(game_ids))
        if game_ids:
            game_ids = list(map(int, game_ids))

        user_ids = request.form.getlist('team-streamers-add')

        success = True

        if game_ids:
            for game_id in game_ids:
                success = (add_team_to_game(team_id, game_id) and success)

        if user_ids:
            for user_id in user_ids:
                success = (add_team_to_user(team_id, user_id) and success)

        created = request.form.get('team-created-add')
        updated = request.form.get('team-updated-add')

        try:
            team = Team()
            team.id = team_id
            team.image_url = team_image_url
            team.name = name
            team.info = info
            team.url = url
            team.game_ids = game_ids
            team.user_ids = user_ids
            #team.team_ids = team_ids
            team.created = datetime.datetime.strptime(created, '%Y-%m-%d')
            team.updated = datetime.datetime.strptime(updated, '%Y-%m-%d')
            db.session.add(team)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            success = False

        if (success):
            flash('Congratulations, the team was added successfuly!', 'success')
            redirect_url = '/teams/' + str(team_id)
        else:
            flash('Sorry, something went wrong :(', 'danger')
            redirect_url = '/teams'
        
        return redirect(redirect_url)


@application.route('/addCommunity', methods=['POST', 'GET'])
def add_community():
    if request.method == 'GET':
        games = []
        users = []
        # Get all games for edit drop down
        game_query = Game.query
        for game in game_query:
            games.append({'name': game.name, 'id': game.id})

        # Get all users for edit drop down
        users_query = User.query
        for user in users_query:
            users.append({'name': user.name, 'id': user.id})

        return render_template('add_community.html', games=games, users=users)
    else:
        # do the add to the db here and then render instance page of the added user
        community_id = request.form.get('community-id-add')
        community_image_url = request.form.get('community-image-url-add')
        name = request.form.get('community-name-add')
        description = request.form.get('community-description-add')
        language = request.form.get('community-language-add')
        rules = request.form.get('community-rules-add')
        game_id = request.form.get('community-game-add')
        if game_id:
            game_id = int(game_id)
        owner_id = request.form.get('community-owner-add')

        success = True

        if game_id:
            success = (add_community_to_game(community_id, game_id) and success)

        if owner_id:
            success = (add_community_to_user(community_id, owner_id) and success)

        try:
            community = Community()
            community.id = community_id
            community.image_url = community_image_url
            community.name = name
            community.description = description
            community.language = language
            community.rules = rules
            community.game_id = game_id
            community.owner_id = owner_id
            db.session.add(community)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            success = False

        if (success):
            flash('Congratulations, the community was added successfuly!', 'success')
            redirect_url = '/communities/' + community_id
        else:
            flash('Sorry, something went wrong :(', 'danger')
            redirect_url = '/communities'

        return redirect(redirect_url)

@application.route('/addGame', methods=['POST', 'GET'])
def add_game():
    if request.method == 'GET':
        streamers = []
        teams = []
        communities = []

        # Get all streamers for edit drop down
        users_query = User.query
        for user in users_query:
            streamers.append({'name': user.name, 'id': user.id})

        # Get all teams for edit drop down
        team_query = Team.query
        for team in team_query:
            teams.append({'name': team.name, 'id': team.id})

        # Get all communities for edit drop down
        community_query = Community.query
        for community in community_query:
            communities.append({'name': community.name, 'id': community.id})

        today = datetime.datetime.now().date()
        return render_template('add_game.html', streamers=streamers, communities=communities, teams=teams, today=today)
    else:
        game_id = request.form.get('game-id-add')
        if game_id:
            game_id = int(game_id)
        game_image_url = request.form.get('game-pic-add')
        name = request.form.get('game-name-add')
        description = request.form.get('game-description-add')
        rated = request.form.get('game-rating-add')
        genres = request.form.getlist('genres[]')
        genres = list(filter(None, genres))
        platforms = request.form.getlist('platforms[]')
        platforms = list(filter(None, platforms))
        release_date = request.form.get('game-release-date-add')
        
        user_ids = request.form.getlist('game-streamers-add')

        community_ids = request.form.getlist('game-communities-add')
        
        team_ids = request.form.getlist('game-teams-add')
        if team_ids:
            team_ids = list(map(int, team_ids))

        success = True

        if user_ids:
            for user_id in user_ids:
                success = (add_game_to_user(game_id, user_id) and success)

        if community_ids:
            for community_id in community_ids:
                success = (add_game_to_community(game_id, community_id) and success)

        if team_ids:
            for team_id in team_ids:
                success = (add_game_to_team(game_id, team_id) and success)

        try:
            game = Game()
            game.id = game_id
            game.image_url = game_image_url
            game.name = name
            game.description = description
            game.rated = rated
            game.platforms = platforms
            game.genres = genres
            game.user_ids = user_ids
            game.community_ids = community_ids
            game.team_ids = team_ids
            game.release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
            db.session.add(game)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(str(e))
            success = False

        if (success):
            flash('Congratulations, the game was added successfuly!', 'success')
            redirect_url = '/games/' + str(game_id)
        else:
            flash('Sorry, something went wrong :(', 'danger')
            redirect_url = '/games'
        
        return redirect(redirect_url)

####################### UPDATE MODELS ################################

@application.route('/updateUser', methods=['POST'])
def update_user():

    action = request.form.get('action')

    user_id = request.form.get('user-id-edit')

    if (action == 'Delete'):
        delete_success = delete_user(user_id)
        if delete_success:
            flash('Congratulations, the user was deleted successfuly!', 'success')
        else:
            flash('Sorry, something went wrong :(', 'danger')
        return redirect('/users')
    else:

        new_name = request.form.get('user-name-edit')
        new_description = request.form.get('user-description-edit')
        new_language = request.form.get('user-language-edit')
        new_views = request.form.get('user-views-edit')
        new_followers = request.form.get('user-followers-edit')
        new_url = request.form.get('user-url-edit')
        new_image_url = request.form.get('user-pic-edit')
        
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
                    successful_game_update = (remove_user_from_game(user_id, old_game_id) and successful_game_update)

                if new_game_id:
                    successful_game_update = (add_user_to_game(user_id, new_game_id) and successful_game_update)

            user.game_id = new_game_id                                                                  # UPDATED USER INSTANCE: GAME ID

            if old_community_id != new_community_id:
                if old_community_id:
                    successful_community_update = (remove_user_from_community(user_id, old_community_id) and successful_community_update)

                if new_community_id:
                    successful_community_update = (add_user_to_community(user_id, new_community_id) and successful_community_update)

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
                            successful_teams_update = (remove_user_from_team(user_id, old_team_id) and successful_teams_update)

                if new_team_ids:
                    for new_team_id in new_team_ids:
                        if new_team_id not in old_team_ids:
                            # User did not previously have team but now does so need to add user to that team
                            successful_teams_update = (add_user_to_team(user_id, new_team_id) and successful_teams_update)

            # db.session.flush()
            user.image_url = new_image_url
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

def delete_user(user_id):
    success = True
    try:
        user = User.query.get(user_id)
        old_game_id = user.game_id
        old_community_id = user.community_id
        old_team_ids = user.team_ids
        if old_game_id:
            success = (remove_user_from_game(user_id, old_game_id) and success)
        if old_community_id:
            success = (remove_user_from_community(user_id, old_community_id) and success)
        if old_team_ids:
            for team_id in old_team_ids:
                success = (remove_user_from_team(user_id, team_id) and success)
        db.session.delete(user)
        db.session.commit()
    except:
        db.session.rollback()
        success = False
    return success

@application.route('/updateGame', methods=['POST'])
def update_game():

    action = request.form.get('action')

    game_id = request.form.get('game-id-edit')

    if (action == 'Delete'):
        delete_success = delete_game(game_id)
        if delete_success:
            flash('Congratulations, the user was deleted successfuly!', 'success')
        else:
            flash('Sorry, something went wrong :(', 'danger')
        return redirect('/games')
    else:
        game_id = int(request.form.get('game-id-edit'))
        new_image_url = request.form.get('game-pic-edit')
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
                            successful_user_update = (remove_game_from_user(game_id, old_user_id) and successful_user_update)

                if new_user_ids:
                    for new_user_id in new_user_ids:
                        if new_user_id not in old_user_ids:
                            # User did not previously have user but now does so need to add game to that user
                            successful_user_update = (add_game_to_user(game_id, new_user_id) and successful_user_update)

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
                            successful_community_update = (remove_game_from_community(game_id, old_community_id) and successful_community_update)

                if new_community_ids:
                    for new_community_id in new_community_ids:
                        if new_community_id not in old_community_ids:
                            successful_community_update = (add_game_to_community(game_id, new_community_id) and successful_community_update)

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
                            successful_teams_update = (remove_game_from_team(game_id, old_team_id) and successful_teams_update)

                if new_team_ids:
                    for new_team_id in new_team_ids:
                        if new_team_id not in old_team_ids:
                            # Game did not previously have team but now does so need to add game to that team
                            successful_teams_update = (add_game_to_team(game_id, new_team_id) and successful_teams_update)

            game.image_url = new_image_url
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
            flash('Congratulations, the game was updated successfuly!', 'success')
        else:
            flash('Sorry, something went wrong :(', 'danger')

        redirect_url = '/games/' + str(game_id)
        return redirect(redirect_url)

def delete_game(game_id):
    success = True
    try:
        game = Game.query.get(game_id)
        old_user_id = game.user_ids
        old_community_id = game.community_id
        old_team_ids = game.team_ids
        if old_user_id:
            success = (remove_game_from_user(game_id, old_user_id) and success)
        if old_community_id:
            success = (remove_game_from_community(game_id, old_community_id) and success)
        if old_team_ids:
            for team_id in old_team_ids:
                success = (remove_game_from_team(game_id, team_ids) and success)
        db.session.delete(game)
        db.session.commit()
    except:
        db.session.rollback()
        success = False
    return success

@application.route('/updateTeam', methods=['POST'])
def update_team():

    action = request.form.get('action')

    team_id = request.form.get('team-id-edit')

    if (action == 'Delete'):
        delete_success = delete_team(team_id)
        if delete_success:
            flash('Congratulations, the user was deleted successfuly!', 'success')
        else:
            flash('Sorry, something went wrong :(', 'danger')
        return redirect('/teams')
    else:
        team_id = int(request.form.get('team-id-edit'))
        new_image_url = request.form.get('team-pic-edit')
        new_name = request.form.get('team-name-edit')
        new_info = request.form.get('team-info-edit')
        new_created = request.form.get('team-created-edit')
        new_updated = request.form.get('team-updated-edit')
        new_user_ids = request.form.getlist('team-streamers-edit')
        new_game_ids = request.form.getlist('team-games-edit')
        if new_game_ids:
            new_game_ids = list(map(int, new_game_ids))

        successful_user_update = True
        successful_game_update = True       
        successful_team_update = True 
        successful_community_update = True

        try:
            team = Team.query.get(team_id)
            old_user_ids = team.user_ids
            old_game_ids = team.game_ids

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
                            successful_user_update = (remove_team_from_user(team_id, old_user_id) and successful_user_update)

                if new_user_ids:
                    for new_user_id in new_user_ids:
                        if new_user_id not in old_user_ids:
                            # User did not previously have user but now does so need to add game to that user
                            successful_user_update = (add_team_to_user(team_id, new_user_id) and successful_user_update)

            team.user_ids = new_user_ids                                                                # UPDATED TEAM INSTANCE: USER IDS

            old_game_ids_set = set()
            new_game_ids_set = set()
            if old_game_ids:
                old_game_ids_set = set(old_game_ids)
            if new_game_ids:
                new_game_ids_set = set(new_game_ids)

            if (old_game_ids_set != new_game_ids_set):
                if old_game_ids:
                    for old_game_id in old_game_ids:
                        if old_game_id not in new_game_ids:
                            successful_game_update = (remove_team_from_game(team_id, old_game_id) and successful_game_update)

                if new_game_ids:
                    for new_game_id in new_game_ids:
                        if new_game_id not in old_game_ids:
                            # User did not previously have user but now does so need to add game to that user
                            successful_game_update = (add_team_to_game(team_id, new_game_id) and successful_game_update)

            team.game_ids = new_game_ids                                                                # UPDATED TEAM INSTANCE: GAME IDS

            team.image_url = new_image_url
            team.name = new_name                                                                        # UPDATED TEAM INSTANCE: NAME
            team.info = new_info                                                                        # UPDATED TEAM INSTANCE: INFO
            team.created = new_created                                                                  # UPDATED TEAM INSTANCE: CREATED
            team.updated = new_updated                                                                  # UPDATED TEAM INSTANCE: UPDATED
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print('Team Exception: ' + str(err))
            successful_team_update = False

        if (successful_user_update and successful_game_update and successful_team_update and successful_community_update):
            flash('Congratulations, the team was updated successfuly!', 'success')
        else:
            flash('Sorry, something went wrong :(', 'danger')

        redirect_url = '/teams/' + str(team_id)
        return redirect(redirect_url)

def delete_team(team_id):
    success = True
    try:
        team = Team.query.get(team_id)
        old_game_ids = team.game_ids
        old_user_ids = team.user_ids
        #old_team_ids = user.team_ids
        if old_game_ids:
            success = (remove_team_from_game(team_id, old_game_ids) and success)
        if old_user_ids:
            success = (remove_team_from_user(team_id, old_user_ids) and success)
        #if old_team_ids:
            #for team_id in old_team_ids:
                #success = (remove_user_from_team(user_id, team_id) and success)
        db.session.delete(team)
        db.session.commit()
    except:
        db.session.rollback()
        success = False
    return success

@application.route('/updateCommunity', methods=['POST'])
def update_community():

    action = request.form.get('action')

    community_id = request.form.get('community-id-edit')

    if (action == 'Delete'):
        delete_success = delete_community(community_id)
        if delete_success:
            flash('Congratulations, the community was deleted successfuly!', 'success')
        else:
            flash('Sorry, something went wrong :(', 'danger')
        return redirect('/teams')
    else:
        community_id = request.form.get('community-id-edit')
        new_image_url = request.form.get('community-pic-edit')
        new_name = request.form.get('community-name-edit')
        new_description = request.form.get('community-description-edit')
        new_language = request.form.get('community-language-edit')
        new_rules = request.form.get('community-rules-edit')
        
        new_game_id = request.form.get('community-game-edit')
        if new_game_id:
            new_game_id = int(new_game_id)
        
        new_owner_id = request.form.get('community-owner-edit')
        # print(new_owner_id)

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
                    successful_game_update = (remove_community_from_game(community_id, old_game_id) and successful_game_update)

                if new_game_id:
                    successful_game_update = (add_community_to_game(community_id, new_game_id) and successful_game_update)

            community.game_id = new_game_id                                                                  # UPDATED community INSTANCE: GAME ID

            if old_owner_id != new_owner_id:
                if old_owner_id:
                    successful_owner_update = (remove_community_from_user(community_id, old_owner_id) and successful_owner_update)

                if new_owner_id:
                    successful_owner_update = (add_community_to_user(community_id, new_owner_id) and successful_owner_update)

            community.owner_id = new_owner_id                                          # UPDATED community INSTANCE: COMMUNITY ID

            # db.session.flush()
            community.image_url = new_image_url
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
            redirect_url = '/communities/' + community_id
        else:
            flash('Sorry, something went wrong :(', 'danger')
            redirect_url = '/communities'

        return redirect(redirect_url)

def delete_community(community_id):
    success = True
    try:
        community = Community.query.get(community_id)
        old_game_ids = community.game_ids
        old_user_ids = community.user_ids
        #old_team_ids = user.team_ids
        if old_game_ids:
            success = (remove_community_from_game(community_id, old_game_ids) and success)
        if old_user_ids:
            success = (remove_community_from_user(community_id, old_user_ids) and success)
        db.session.delete(community)
        db.session.commit()
    except:
        db.session.rollback()
        success = False
    return success


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
    created = q.created
    if created:
        created = created.date()
    updated = q.updated
    if updated:
        updated = updated.date()
    user['created'] = created
    user['updated'] = updated
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

def remove_user_from_game(user_id, game_id):
    try:
        game_query = Game.query.filter(Game.id == game_id)
        game = game_query.first()

        if game:
            game_user_ids = game.user_ids

            if game_user_ids and user_id in game_user_ids:
                game_user_ids.remove(user_id)

            game_query.update({'user_ids': game_user_ids})                          
            db.session.commit()
        return True
    except Exception as e:
        print('remove user from game exception: ' + str(e))
        db.session.rollback()
        return False

def add_user_to_game(user_id, game_id):
    try:
        game_query = Game.query.filter(Game.id == game_id)
        game = game_query.first()
        game_user_ids = game.user_ids

        if game_user_ids and user_id not in game_user_ids:
            game_user_ids.append(user_id)
        elif not game_user_ids:
            game_user_ids = [user_id]

        game_query.update({'user_ids': game_user_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

def remove_user_from_community(user_id, community_id):
    try:
        old_community = Community.query.get(community_id)
        if old_community:
            old_community_owner_id = old_community.owner_id
            if user_id == old_community_owner_id:
                old_community.owner_id = None
            db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove user from Community Exception: ' + str(e))
        return False


def add_user_to_community(user_id, community_id):
    try:
        new_community = Community.query.get(community_id)
        new_community.owner_id = user_id
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def remove_user_from_team(user_id, team_id):
    try:
        old_team_query = Team.query.filter(Team.id == team_id)
        old_team = old_team_query.first()
        if old_team:
            old_team_user_ids = old_team.user_ids
            if old_team_user_ids and user_id in old_team_user_ids:
                old_team_user_ids.remove(user_id)

            old_team_query.update({'user_ids': old_team_user_ids})
            db.session.commit()
        return True
    except Exception as e:
        print('Remove user from team exception: ' + str(e))
        db.session.rollback()
        return False


def add_user_to_team(user_id, team_id):
    try:
        new_team_query = Team.query.filter(Team.id == team_id)
        new_team = new_team_query.first()
        new_team_user_ids = new_team.user_ids
        
        if new_team_user_ids:
            new_team_user_ids.append(user_id)
        else:
            new_team_user_ids = [user_id]

        new_team_query.update({'user_ids': new_team_user_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def remove_game_from_user(game_id, user_id):
    try:
        old_user = User.query.get(user_id)
        if (old_user.game_id == game_id):
            old_user.game_id = None
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove game from user Exception: ' + str(e))
        return False


def add_game_to_user(game_id, user_id):
    try:
        new_user = User.query.get(user_id)
        new_user.game_id = game_id
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add game to user Exception: ' + str(e))
        return False


def remove_game_from_community(game_id, community_id):
    try:
        old_community = Community.query.get(community_id)
        old_community.game_id = None
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('remove game from community Exception: ' + str(e))
        return False


def add_game_to_community(game_id, community_id):
    try:
        new_community = Community.query.get(community_id)
        new_community.game_id = game_id
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add game to community Exception: ' + str(e))
        return False


def remove_game_from_team(game_id, team_id):
    try:
        old_team_query = Team.query.filter(Team.id == team_id)
        old_team = old_team_query.first()
        old_team_game_ids = old_team.game_ids
        if old_team_game_ids and game_id in old_team_game_ids:
            old_team_game_ids.remove(game_id)

        old_team_query.update({'game_ids': old_team_game_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove game from team Exception: ' + str(e))
        return False


def add_game_to_team(game_id, team_id):
    try:
        new_team_query = Team.query.filter(Team.id == team_id)
        new_team = new_team_query.first()
        new_team_game_ids = new_team.game_ids
        
        if new_team_game_ids:
            new_team_game_ids.append(game_id)
        else:
            new_team_game_ids = [game_id]

        new_team_query.update({'game_ids': new_team_game_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add game to team Exception: ' + str(e))
        return False


def remove_team_from_user(team_id, user_id):
    try:
        old_user_query = User.query.filter(User.id == user_id)
        old_user = old_user_query.first()
        old_user_team_ids = old_user.team_ids
        if team_id in old_user_team_ids:
            old_user_team_ids.remove(team_id)  
        old_user_query.update({'team_ids': old_user_team_ids})                             
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove team from user Exception: ' + str(e))
        return False


def add_team_to_user(team_id, user_id):
    try:
        new_user_query = User.query.filter(User.id == user_id)
        new_user = new_user_query.first()
        new_user_team_ids = new_user.team_ids
        if team_id not in new_user_team_ids:
            new_user_team_ids.append(team_id)
        new_user_query.update({'team_ids': new_user_team_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add team to user exception: ' + str(e))
        return False


def remove_team_from_game(team_id, game_id):
    try:
        old_game_query = Game.query.filter(Game.id == game_id)
        old_game = old_game_query.first()
        old_game_team_ids = old_game.team_ids
        if team_id in old_game_team_ids:
            old_game_team_ids.remove(team_id)  
        old_game_query.update({'team_ids': old_game_team_ids})                           
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove team from game Exception: ' + str(e))
        return False


def add_team_to_game(team_id, game_id):
    try:
        new_game_query = Game.query.filter(Game.id == game_id)
        new_game = new_game_query.first()
        new_game_team_ids = new_game.team_ids
        if team_id not in new_game_team_ids:
            new_game_team_ids.append(team_id)
        new_game_query.update({'team_ids': new_game_team_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add team to game exception: ' + str(e))
        return False


def remove_community_from_game(community_id, game_id):
    try:
        old_game_query = Game.query.filter(Game.id == game_id)
        old_game = old_game_query.first()
        old_game_community_ids = old_game.community_ids

        if old_game_community_ids and community_id in old_game_community_ids:
            old_game_community_ids.remove(community_id)

        old_game_query.update({'community_ids': old_game_community_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove community from game Exception: ' + str(e))
        return False


def add_community_to_game(community_id, game_id):
    try:
        new_game_query = Game.query.filter(Game.id == game_id)
        new_game = new_game_query.first()
        new_game_community_ids = new_game.community_ids

        # Use list() constructor to copy the list so it actually updates
        if new_game_community_ids and community_id not in new_game_community_ids:
            new_game_community_ids.append(community_id)
        elif not new_game_community_ids:
            new_game_community_ids = [community_id]

        new_game_query.update({'community_ids': new_game_community_ids})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add community to game exception: ' + str(e))
        return False


def remove_community_from_user(community_id, owner_id):
    try:
        old_owner = User.query.get(owner_id)
        old_owner_community_id = old_owner.community_id
        if community_id == old_owner_community_id:
            old_owner.community_id = None
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Remove owner from community Exception: ' + str(e))
        return False


def add_community_to_user(community_id, owner_id):
    try:
        new_owner = User.query.get(owner_id)
        new_owner.community_id = community_id
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print('Add owner to community Exception: ' + str(e))
        return False

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

    # returns search results with default "and" operator
    user_search_results = []
    game_search_results = []
    team_search_results = []
    community_search_results = []

    for user in User.query.whoosh_search(search_string).all() :
        user_search_results.append(user)
        print(user.name)
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