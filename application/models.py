from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class Channel (BaseModel, db.Model) :
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key = True, nullable = False)

    mature = db.Column(db.String(128), nullable = True)
    partner = db.Column(db.Boolean(), nullable = True)
    status = db.Column(db.String(128))
    broadcaster_language = db.Column(db.String(128))
    display_name = db.Column(db.String(128))
    game = db.Column(db.String(128))
    language = db.Column(db.String(128))
    name = db.Column(db.String(128))
    created_at = db.Column(db.String(128))
    updated_at = db.Column(db.String(128))
    delay = db.Column(db.Integer, nullable = True)
    logo = db.Column(db.String(128), nullable = True)
    banner = db.Column(db.String(128), nullable = True)
    video_banner = db.Column(db.String(128), nullable = True)
    background = db.Column(db.String(128), nullable = True)
    profile_banner  = db.Column(db.String(128), nullable = True)
    profile_banner_background_color = db.Column(db.String(128), nullable = True)
    url = db.Column(db.String(128))
    views = db.Column(db.Integer)
    followers = db.Column(db.Integer)
#    links = db.Column(db.Array(db.String(128))) # self, follows, commercial, stream_key, chat
                                             # features, subscriptions, editors, teams, videos

class Stream (BaseModel, db.Model) :
    __tablename__ = 'stream'
    id = db.Column(db.Integer, primary_key = True, nullable = False)

    game = db.Column(db.String(128))
    viewers = db.Column(db.Integer)
    video_height = db.Column(db.Integer)
    average_fps = db.Column(db.Float)
    delay = db.Column(db.Integer, nullable = True)
    created_at = db.Column(db.String(128))
    is_playlist = db.Column(db.String(128))
    stream_type = db.Column(db.String(128))

# https://stackoverflow.com/questions/28280507/setup-relationship-one-to-one-in-flask-sqlalchemy
# https://www.codementor.io/sheena/understanding-sqlalchemy-cheat-sheet-du107lawl
class Streamer (BaseModel, db.Model) :
    __tablename__ = 'streamer'
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))   # <-----
    stream_id = db.Column(db.Integer, db.ForeignKey('stream.id'))     # <-----
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable = True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable = True)

    channel = relationship("Channel",backref = 'streamers') # one-to-one
    stream = relationship("Stream", backref = 'streamers') # one-to-one
    team = relationship("Team", backref = 'streamers')
    community = relationship("Community", backref = 'streamers')    

class Team (BaseModel, db.Model) :

    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(128))
    info = db.Column(db.String(500), nullable = True)
    display_name = db.Column(db.String(128))
    created_at = db.Column(db.String(128))
    updated_at = db.Column(db.String(128))
    logo = db.Column(db.String(128), nullable = True)
    banner = db.Column(db.String(128), nullable = True)
    background = db.Column(db.String(128), nullable = True)

class Community (BaseModel, db.Model) :

    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(128))
    display_name = db.Column(db.String(128))
    viewers = db.Column(db.Integer)
    channels = db.Column(db.Integer, nullable = True)
    avatar_image_url = db.Column(db.String(128), nullable = True)

class Game (BaseModel, db.Model) :

    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(128))
    popularity = db.Column(db.Integer)
    giantbomb_id = db.Column(db.Integer)
#    box = db.Column(db.Array(db.String(128)))  # Game.box[0] is large, Game.box[1] is medium, etc
#    logo = db.Column(db.Array(db.String(128)))
    localized_name = db.Column(db.String(128))
    locale = db.Column(db.String(128), nullable = True)
    viewers = db.Column(db.Integer)
    channels = db.Column(db.Integer)
