from time import sleep
from random import randint
from configparser import NoOptionError

from wellstep.crawl import Crawler
from wellstep import conf
from wellstep.server import db
from wellstep.server.models.team import TeamPost
from wellstep.server.models.user import UserPost


class CrawlerWorker(object):

    crawler = None
    simulate = False

    def __init__(self):
        try:
            if conf.get('WELLSTEP', 'simulate') == 'True':
                self.simulate = True
        except NoOptionError:
            pass

        if not self.simulate:
                self.crawler = Crawler()

        proxy = dict()
        try:
            proxy.update({'http' : conf.get('WELLSTEP', 'http_proxy')})
        except NoOptionError:
            pass
        try:
            proxy.update({'https' : conf.get('WELLSTEP', 'https_proxy')})
        except NoOptionError:
            pass

        self.crawler.set_config(
                username = conf.get('WELLSTEP', 'username'),
                password = conf.get('WELLSTEP', 'password'),
                proxy = proxy)


    def work(self):
        while True:
            if self.simulate:
                self.simulate_to_db()
            else:
                self.fetch_to_db()
            sleep(float(conf.get('WELLSTEP', 'fetch_delay')))


    def clean_up(self):
        print('Clean up..')

    # Helper functions comes here:

    def fetch_to_db(self):
        self.crawler.fetch()

        header, body, ts = self.crawler.get_team_data()
        for row in body:
            team_post = TeamPost(
                    position = row[0],
                    team = row[1],
                    score = row[2],
                    percent = row[3])
            db.session.add(team_post)

        header, body, ts = self.crawler.get_user_data()
        for row in body:
            user_post = UserPost(
                    position = row[0],
                    name = row[1],
                    score = row[2],
                    percent = row[3],
                    team = row[4])
            db.session.add(user_post)

        db.session.commit()


    def simulate_to_db(self):
        ## SIMULATE A TEAM

        # Get the last values
        last_ts = db.session.query(db.func.max(TeamPost.time)).one()[0]
        team_data = list(map(
                lambda post: post.get_dict(),
                db.session.query(TeamPost).filter(TeamPost.time==last_ts).all()))

        # Randomize an increase
        for row in team_data:
            row['score'] += randint(0,60)

        # Make ordered list for scores to calc position
        ordered_scores = sorted(map(lambda d: d['score'], team_data), key=lambda v: -v)

        for row in team_data:
            team_post = TeamPost(
                    position = ordered_scores.index(row['score'])+1,
                    team = row['team'],
                    score = row['score'],
                    percent = "? %") # Not implemented
            db.session.add(team_post)

        ## SIMULATE AN USER
        last_ts = db.session.query(db.func.max(UserPost.time)).one()[0]
        user_data = list(map(
                lambda post: post.get_dict(),
                db.session.query(UserPost).filter(UserPost.time==last_ts).all()))

        # Randomize an increase
        for row in user_data:
            row['score'] += randint(0,60)

        # Make ordered list for scores to calc position
        ordered_scores = sorted(map(lambda d: d['score'], user_data), key=lambda v: -v)

        for row in user_data:
            user_post = UserPost(
                    position = ordered_scores.index(row['score'])+1,
                    name = row['name'],
                    team = row['team'],
                    score = row['score'],
                    percent = "? %") # Not implemented
            db.session.add(user_post)

        db.session.commit()


    # TODO: Add simulated users and teams if none
