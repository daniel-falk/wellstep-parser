from wellstep.server import db


class TeamPost(db.Model):
    id = db.Column('team_post_id', db.Integer, primary_key=True)
    team = db.Column(db.String(255), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer)
    percent = db.Column(db.String(10))
    time = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, team=None, score=None, position=None, percent=None, timestamp=None):
        self.team = team
        self.score = score
        self.position = position
        self.percent = percent

    def get_dict(self):
        return dict(
                team = self.team,
                score = self.score,
                position = self.position,
                percent = self.percent,
                time = self.time)
