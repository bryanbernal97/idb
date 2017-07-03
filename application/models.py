from application import db


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


class User (BaseModel, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)

    # Attributes
    name = db.Column(db.String(128))
    info = db.Column(db.String(500))
    language = db.Column(db.String(128))
    views = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    url = db.Column(db.String(128))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    image_url = db.Column(db.String(128))

    # Connections to other models
    game_id = db.Column(db.Integer)
    community_id = db.Column(db.Integer)


class Game (BaseModel, db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key = True)

    # Attributes
    name = db.Column(db.String(128))
    description = db.Column(db.String(500))
    genre = db.Column(db.String(128))
    platform = db.Column(db.String(128))
    release_date = db.Column(db.DateTime)
    image_url = db.Column(db.String(128))

    # Connections to other models
    user_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer) 


class Team (BaseModel, db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key = True)

    # Attributes
    name = db.Column(db.String(128))
    info = db.Column(db.String(500))
    image_url = db.Column(db.String(128))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    # Connection to other models
    user_ids = db.Column(db.ARRAY(db.Integer))
    game_id = db.Column(db.Integer)


class Community (BaseModel, db.Model):
    __tablename__ = 'community'

    id = db.Column(db.Integer, primary_key = True)

    # Attributes
    name = db.Column(db.String(128))
    info = db.Column(db.String(500))
    language = db.Column(db.String(50))
    rules = db.Column(db.String(500))
    image_url = db.Column(db.String(128))

    # Connection to other models
    games = db.Column(db.ARRAY(db.Integer)) # list of game id's
    users = db.Column(db.ARRAY(db.Integer)) # list of user id's

