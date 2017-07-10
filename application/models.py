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
            for column, value in self.__dict__.items()
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
    __searchable__ = ['name', 'description', 'language']

    id = db.Column(db.String, primary_key = True)

    # Attributes
    name = db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    language = db.Column(db.TEXT)
    views = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    url = db.Column(db.TEXT)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    image_url = db.Column(db.TEXT)

    # Connections to other models
    game_id = db.Column(db.Integer)
    community_id = db.Column(db.String)
    team_ids = db.Column(db.ARRAY(db.Integer))


class Game (BaseModel, db.Model):
    __tablename__ = 'game'
    __searchable__ = ['name', 'description', 'genres', 'platforms', 'rating']

    id = db.Column(db.Integer, primary_key = True)

    # Attributes
    name = db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    genres = db.Column(db.ARRAY(db.TEXT))
    platforms = db.Column(db.ARRAY(db.TEXT))
    release_date = db.Column(db.DateTime)
    image_url = db.Column(db.TEXT)
    rating = db.Column(db.String)

    # Connections to other models
    user_ids = db.Column(db.ARRAY(db.String))
    team_ids = db.Column(db.ARRAY(db.Integer))
    community_ids = db.Column(db.ARRAY(db.String))


class Team (BaseModel, db.Model):
    __tablename__ = 'team'
    __searchable__ = ['name', 'info']

    id = db.Column(db.Integer, primary_key = True)

    # Attributes
    name = db.Column(db.TEXT)
    info = db.Column(db.TEXT)
    image_url = db.Column(db.TEXT)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    # Connection to other models
    user_ids = db.Column(db.ARRAY(db.String))
    game_ids = db.Column(db.ARRAY(db.Integer))


class Community (BaseModel, db.Model):
    __tablename__ = 'community'
    __searchable__ = ['name', 'description', 'language', 'rules']

    id = db.Column(db.String(128), primary_key = True)

    # Attributes
    name = db.Column(db.TEXT)
    description = db.Column(db.TEXT)
    language = db.Column(db.String(128))
    rules = db.Column(db.TEXT)
    image_url = db.Column(db.TEXT)

    # Connection to other models
    game_id = db.Column(db.Integer)
    owner_id = db.Column(db.String)
