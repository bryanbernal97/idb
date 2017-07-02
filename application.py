from flask import Flask
from flask import render_template
from application import db
from application.models import Data

import datetime
import requests

headers = {'client-id' : 'rpd5zvz9ofz3s7jeisuddqjo3fvfj0', 'Accept' :'application/vnd.twitchtv.v5+json'}
gb_id = '/?api_key=d483af9dcc46474051b451953aa550322df2b793&format=json'
top = {}
teams = {}
communities = {}
streamers = {}
games = {}

# Create the Flask app
application = Flask(__name__)
application.debug = True


# print a nice greeting.
@application.route('/')
def say_hello():
    json = requests.get('https://api.twitch.tv/kraken/communities/top', headers=headers).json()
    top['communities'] = json['communities']
    json = requests.get('https://api.twitch.tv/kraken/games/top', headers=headers).json()
    top['games'] = json['top']
    json = requests.get('https://api.twitch.tv/kraken/streams', headers=headers).json()
    channels = json['streams']
    top['channels'] = channels
    return render_template('index2.html', name=top)

@application.route('/teams/<wow>')
def show_teams(wow):
    global teams
    url = 'https://api.twitch.tv/kraken/teams/' + wow
    teams[wow] = requests.get(url, headers=headers).json()

    return render_template('test_template.html', name = teams[wow])

@application.route('/communities/<wow>')
def show_communities(wow):
    global communities
    url = 'https://api.twitch.tv/kraken/communities?name=' + wow
    communities[wow] = requests.get(url, headers=headers).json()
    communities[wow]['model_type'] = 'community'

    return render_template('test_template.html', name = communities[wow])

@application.route('/streamers/<wow>')
def show_streamers(wow):
    global streamers
    url = 'https://api.twitch.tv/kraken/channels/' + wow
    streamers[wow] = requests.get(url, headers=headers).json()
    streamers[wow]['model_type'] = 'streamer'

    print(streamers[wow])

    return render_template('test_template.html', name = streamers[wow])

@application.route('/games/<wow>')
def show_games(wow):
    global games, gb_id
    url = 'http://www.giantbomb.com/api/game/' + wow + gb_id
    json = requests.get(url, headers={'user-agent' : '1234'}).json()
    print("hi")
    game = json['results']
    games[game['name']] = game
    games[game['name']]['_id'] = wow
    games[game['name']]['model_type'] = 'game'

    return render_template('test_template.html', name = games[game['name']])


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()