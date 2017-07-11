from application import db, application
import flask_whooshalchemy as wa

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    # Changed constructor for Python 2 compatibility
    def __init__(self, *args):
        super(BaseModel, self).__init__(*args)

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

    # Changed the constructor for Python 2 compatibility
    def __init__(self, id='-1', name=None, description=None, language=None, views=None,
        followers=None, url=None, created=None, updated=None, image_url=None, game_id=None,
        community_id=None, team_ids=None, *args):

        super(User, self).__init__(*args)
        self.id = id
        self.name = name
        self.description = description
        self.language = language
        self.views = views
        self.followers = followers
        self.url = url
        self.created = created
        self.updated = updated
        self.image_url = image_url
        self.game_id = game_id
        self.community_id = community_id
        self.team_ids = team_ids

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
    __searchable__ = ['name', 'description', 'rating']

    # Changed the constructor for Python 2 compatibility
    def __init__(self):
        super(Game, self).__init__()

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

    # Changed the constructor for Python 2 compatibility
    def __init__(self):
        super(Team, self).__init__()

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

    # Changed the constructor for Python 2 compatibility
    def __init__(self):
        super(Community, self).__init__()

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


# Allow indexing on models
wa.whoosh_index(application, User)
wa.whoosh_index(application, Game)
wa.whoosh_index(application, Team)
wa.whoosh_index(application, Community)