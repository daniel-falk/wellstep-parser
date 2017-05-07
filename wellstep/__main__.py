import threading

from wellstep.server import app, db
import wellstep.server.api
from wellstep.crawler_worker import CrawlerWorker

cw = None
worker = threading.Thread()


def start_crawler():

    def start_worker():
        global worker
        global cw
        worker = threading.Thread(target=cw.work, args=())
        try:
            worker.setDaemon(True)
            worker.start()
        except (KeyboardInterrupt, SystemExit):
            cw.clean_up()

    def init():
        global cw
        global worker

        db.create_all()

        cw = CrawlerWorker()


    init()
    start_worker()


start_crawler()
app.run()
