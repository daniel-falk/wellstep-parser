from wellstep.server import app

from wellstep import conf
from wellstep.crawl import Crawler

from flask import render_template

@app.route('/')
def hello_world():
    return 'Hello there!'


@app.route('/data/')
def show_data():
    header, body, ts = crawler.get_team_data()
    return render_template(
            'data.html',
            title = 'Team Statistics',
            header = header,
            data = body)

