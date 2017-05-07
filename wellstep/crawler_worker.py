from time import sleep

from wellstep.crawl import Crawler
from wellstep import conf
from wellstep.server import db
from wellstep.server.models.team import TeamPost
from wellstep.server.models.user import UserPost


class CrawlerWorker(object):

    crawler = None

    def __init__(self):
        self.crawler = Crawler()
        self.crawler.set_config(**dict(conf.items('WELLSTEP')))


    def work(self):
        while True:
            self.fetch_to_db()
            sleep(5)

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



