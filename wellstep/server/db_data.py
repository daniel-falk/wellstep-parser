from wellstep.server import db
from wellstep import conf
from wellstep.server.models.team import TeamPost
from wellstep.server.models.user import UserPost


def get_team_ranking():
    ts = db.session.query(db.func.max(TeamPost.time)).one()[0]
    data = map(
            lambda post: [post.position, post.team, post.score],
            db.session.query(TeamPost).filter(TeamPost.time==ts).order_by(TeamPost.position))
    return data


def get_user_ranking():
    ts = db.session.query(db.func.max(UserPost.time)).one()[0]
    data = map(
            lambda post: [post.position, post.score, post.name, post.team],
            db.session.query(UserPost).filter(UserPost.time==ts).order_by(UserPost.position))
    return data
