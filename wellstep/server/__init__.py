from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wellstep import conf

app = Flask(__name__)

app.config.update(**dict(conf.items('SERVER')))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql://{username}:{password}@{host}/{database}'.format(
        **dict(conf.items('MYSQL'))))

db = SQLAlchemy(app)

