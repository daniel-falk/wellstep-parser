from flask import render_template

from wellstep.server import app
from wellstep.server.db_data import get_user_ranking, get_team_ranking

@app.route('/')
def hello_world():
    return 'Hello there!'


@app.route('/teams/')
def show_teams():
    header = 'Plats Lagnamn Minuter'.split()
    data = get_team_ranking()
    return render_template(
            'data.html',
            title = 'Team Statistics',
            header = header,
            data = data)


@app.route('/users/')
def show_users():
    header = 'Plats Minuter Namn Lag'.split()
    data = get_user_ranking()
    return render_template(
            'data.html',
            title = 'User Statistics',
            header = header,
            data = data)

