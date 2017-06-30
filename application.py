from flask import Flask
from flask import render_template

from models import db


# Create the Flask app
application = Flask(__name__)

POSTGRES = {
    'user': 'group2',
    'pw': 'cs373group2',
    'db': 'streamglean_db',
    'host': 'streamglean-rds.cxx60yvk87ey.us-east-2.rds.amazonaws.com',
    'port': '5432',
}
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(application)

# print a nice greeting.

# print a nice greeting.
@application.route('/')
def say_hello():
    return render_template('index.html')

@application.route('/games/league-of-legends')
def show_league_of_legends():
    return render_template('league-of-legends.html')

@application.route('/games/dota-2')
def show_dota_2():
    return render_template('dota-2.html')

@application.route('/games/counter-strike-global-offensive')
def show_counter_strike():
    return render_template('counter-strike-global-offensive.html')

@application.route('/streamers/LegendaryLea')
def show_legendary_lea():
    return render_template('LegendaryLea.html')

@application.route('/streamers/LIRIK')
def show_lirik():
    return render_template('LIRIK.html')

@application.route('/streamers/MitchJones')
def show_mitch():
    return render_template('MitchJones.html')

@application.route('/communities/positivity')
def show_positivity():
    return render_template('positivity.html')

@application.route('/communities/speedrunning')
def show_speedrunning():
    return render_template('speedrunning.html')

@application.route('/communities/catsonly')
def show_catsonly():
    return render_template('catsonly.html')

@application.route('/teams/tempostorm')
def show_tempostorm():
    return render_template('tempostorm.html')

@application.route('/teams/gfe')
def show_gfe():
    return render_template('gfe.html')

@application.route('/teams/cloud9')
def show_cloud9():
    return render_template('cloud9.html')

# # some bits of text for the page.
# header_text = '''
#     <html>\n<head> <title>StreamGlean</title> </head>\n<body>'''
# instructions = '''
#     <p><em>Hint</em>: This is a RESTful web service! Append a username
#     to the URL (for example: <code>/Thelonious</code>) to say hello to
#     someone specific.</p>\n'''
# home_link = '<p><a href="/">Back</a></p>\n'
# footer_text = '</body>\n</html>'

# # EB looks for an 'application' callable by default.
# application = Flask(__name__)

# # add a rule for the index page.
# application.add_url_rule('/', 'index', (lambda: header_text +
#     say_hello()  + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
# application.add_url_rule('/<username>', 'hello', (lambda username:
#     header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()