from flask import render_template

from wellstep.server import app
from wellstep import conf
from wellstep.server.db_data import get_user_ranking,\
                                    get_team_ranking,\
                                    get_users_time_graph,\
                                    get_teams_time_graph

rt = 5
try:
    rt = int(conf.get('GUI', 'refresh_time'))
except:
    pass

@app.route('/')
def index():
    team_header = 'Plats Lagnamn Minuter'.split()
    team_data = get_team_ranking()
    user_header = 'Plats Minuter Namn Lag'.split()
    user_data = get_user_ranking()
    teams_graph = get_teams_time_graph().render_data_uri()
    users_graph = get_users_time_graph(conf['GUI']['time_graph_users'].split('|')).render_data_uri()
    return render_template(
            'four_sources.html',
            title = 'Cognimatics Team Monitor',
            team_header = team_header,
            team_data = team_data,
            user_header = user_header,
            user_data = user_data,
            teams_graph = teams_graph,
            users_graph = users_graph,
            refresh_time = rt)


@app.route('/teams/')
def show_teams():
    header = 'Plats Lagnamn Minuter'.split()
    data = get_team_ranking()
    return render_template(
            'data.html',
            title = 'Team Statistics',
            header = header,
            data = data,
            refresh_time = rt)


@app.route('/users/')
def show_users():
    header = 'Plats Minuter Namn Lag'.split()
    data = get_user_ranking()
    return render_template(
            'data.html',
            title = 'User Statistics',
            header = header,
            data = data,
            refresh_time = rt)


@app.route('/users_time_graph/')
def users_time_graph():
    graph = get_users_time_graph(conf['GUI']['time_graph_users'].split('|'))
    return render_template(
            'graph.html',
            title = 'User minutes over time',
            graph = graph.render_data_uri(),
            refresh_time = rt)


@app.route('/teams_time_graph/')
def teams_time_graph():
    graph = get_teams_time_graph()
    return render_template(
            'graph.html',
            title = 'Team minutes over time',
            graph = graph.render_data_uri(),
            refresh_time = rt)
