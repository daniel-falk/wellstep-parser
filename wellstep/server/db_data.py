from pygal import Line
from math import floor

from wellstep.server import db
from wellstep import conf
from wellstep.server.models.team import TeamPost
from wellstep.server.models.user import UserPost

GRAPH_LEN = 100
try:
    GRAPH_LEN = int(conf.get('GUI', 'graph_len'))
except:
    pass


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


def get_users_time_graph(users):
    tvec = get_time_vector(UserPost, GRAPH_LEN)
    
    graph = Line(x_label_rotation=90)
    graph.x_labels = tvec

    for user in users:
        user_y = get_user_time_serie(user, tvec)
        graph.add(user, user_y)
    return graph


def get_teams_time_graph(teams=None):
    tvec = get_time_vector(TeamPost, GRAPH_LEN)
    if teams is None:
        teams = get_teams_list()
    graph = Line(x_label_rotation=90)
    graph.x_labels = tvec

    for team in teams:
        team_y = get_team_time_serie(team, tvec)
        graph.add(team, team_y)
    return graph


# Helper functions goes here:

def get_teams_list():
    return map(
            lambda e: e[0],
            db.session.query(TeamPost.team).distinct(TeamPost.team).all())


def get_user_time_serie(username, tvec):
    return list(map(
            lambda e: e[0],
            db.session.query(UserPost.score).filter(UserPost.name==username, UserPost.time.in_(tvec)).order_by(UserPost.time).all()))


def get_team_time_serie(teamname, tvec):
    return list(map(
            lambda e: e[0],
            db.session.query(TeamPost.score).filter(TeamPost.team==teamname, TeamPost.time.in_(tvec)).order_by(TeamPost.time).all()))


def get_time_vector(model, length):
    tvec = list(map(
        lambda d: d[0].strftime('%Y-%m-%d %H:%M'),
        db.session.query(model.time).order_by(model.time).distinct(model.time).all()))
    l = len(tvec)
    div = int(max(1, floor(l/length)))
    return [tvec[l-id] for id in range(1, l+1, div)]
