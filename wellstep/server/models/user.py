from wellstep.server import db


class UserPost(db.Model):
    id = db.Column('user_post_id', db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer)
    percent = db.Column(db.String(10))
    team = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, name=None, score=None, position=None, percent=None, team=None, timestamp=None):
        self.name = name
        self.score = score
        self.position = position
        self.team = team
        self.percent = percent

