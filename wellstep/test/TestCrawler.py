import unittest
from time import time

from ..crawl import Crawler
from .. import conf, get_proxy

class TestCrawler(unittest.TestCase):

    def test_create(self):
        crawler = Crawler()

    def test_config(self):
        username = 'test@test.com',
        password = '6a5ds)!"#¤%/',
        proxy = {'https_proxy' : 'mypoxy.local:1234'}
        crawler = Crawler()
        proxy = get_proxy()
        crawler.set_config(
                password = password,
                username = username,
                proxy = proxy)

        conf = crawler.get_config()

        self.assertEqual(conf['username'], username)
        self.assertEqual(conf['password'], password)
        self.assertEqual(conf['proxy'], proxy)
        self.assertTrue(isinstance(conf['proxy'], dict))

    def test_get_data(self):
        crawler = Crawler()
        crawler.set_config(
                username=conf.get('WELLSTEP', 'username'),
                password=conf.get('WELLSTEP', 'password'),
                proxy=get_proxy())
        crawler.fetch()
        header, body, ts = crawler.get_team_data()
        self.assertTrue(isinstance(header, list))
        self.assertTrue(len(header) == 4)
        self.assertTrue(len(body) > 5)
        self.assertTrue(abs(time()-ts) < 5)
        header, body, ts = crawler.get_user_data()
        self.assertTrue(isinstance(header, list))
        self.assertTrue(len(header) == 5)
        self.assertTrue(len(body) > 5)
        self.assertTrue(abs(time()-ts) < 5)

