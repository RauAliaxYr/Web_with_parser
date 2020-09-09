from flask_login import UserMixin

from siteA import db, manager


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    pic = db.Column(db.String(55))
    isActive = db.Column(db.Boolean, default=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.name


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    aboutMySelf = db.Column(db.Text, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(25), nullable=False)
    matchs = db.Column(db.Integer)
    victories = db.Column(db.Integer)
    draws = db.Column(db.Integer)
    loses = db.Column(db.Integer)
    goalsplaus = db.Column(db.String(12))
    points = db.Column(db.Integer)

    def __init__(self, table):
        self.teamName = table[0]
        self.matchs = table[1]
        self.victories = table[2]
        self.draws = table[3]
        self.loses = table[4]
        self.goalsplaus = table[5]
        self.points = table[6]


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
