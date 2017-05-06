# -*- coding: utf-8

import requests
from bs4 import BeautifulSoup
import sys
from time import time

class Crawler(object):

    PAGE_URL = 'https://www.wellstep.se/ws05/main/authenticate.php'

    team_data = None
    user_data = None
    last_fetch = None

    settings = {}

    class NoData(Exception):
        """A successfull fetch has not been done before trying to access data
        """
        pass
    class FetchFailed(Exception):
        """Fatch failed, possibly due to lack of internet connection
        """
        pass

    def fetch(self):
        """Fetch data from wellstep.se

        Args:
            username: The username for wellstep.se
            password: Password to login
            proxy: If you are behins a proxy, specify it as a dict (see requests API)

        Returns:
            bool: True for success, false otherwise
        """
        content = self.get_page_content(**self.settings)
        soup = self.get_soup(content)
        tables = self.get_user_team_stats_table(soup)
        self.team_data = self.parse_stats(tables[0])
        self.user_data = self.parse_stats(tables[1])
        self.last_fetch = time()

    def set_config(self, username=None, password=None, proxy=None):
        args = locals()
        args.pop('self')
        self.settings = args

    def get_config(self):
        return self.settings

    def get_team_data(self):
        """Get the previosuly fetched team data

        Returns:
            list:       Table header
            2d-array:   Team data table
            float:      Time for data fetch as epoch-time
        """
        if self.team_data is None or self.last_fetch is None:
            raise self.NoData()

        return self.team_data[0], self.team_data[1:], self.last_fetch


    def get_user_data(self):
        """Get the previosuly fetched team data

        Returns:
            list:       Table header
            2d-array:   Team data table
            float:      Time for data fetch as epoch-time
        """
        if self.user_data is None or self.last_fetch is None:
            raise self.NoData()

        return self.user_data[0], self.user_data[1:], self.last_fetch

    # Here comes the helper functions:

    def get_page_content(self, **kwargs):
        if not 'username' in kwargs:
            raise ValueError('Webpage requires a username')
        if not 'password' in kwargs:
            raise ValueError('Webpage requires a password')

        if 'proxy' in kwargs:
            proxy = kwargs.pop('proxy')
        else:
            proxy = None

        ans = requests.post(self.PAGE_URL,
                data = kwargs,
                proxies = proxy)

        if ans.status_code != requests.codes.ok:
            raise self.FetchFailed('Response from wellstep was: {}', ans.status_code)
        return ans.content

    def get_soup(self, raw_page):
        return BeautifulSoup(raw_page, 'html5lib')

    def get_user_team_stats_table(self, soup):
        # Find the table contatining the data
        divs = soup.findAll('div', {'class' : 'rubrik_ruta'})
        dlen = [len(div.text) if div.text.find('STA LAG') > 0 else float('inf') for div in divs]
        div = divs[dlen.index(min(dlen))]

        table = div.parent
        while table.name != 'table':
            table = table.parent

        tables = table.findAll('table')
        return tables

    def parse_stats(self, table):
        data = []
        header_len = -1
        rows = table.findAll('tr')
        for row in rows:
            d = [td.text for td in row.findAll('td')]
            header_len = header_len if header_len > 0 else len(d)
            if len(d) == header_len: # Skipp in-table headers, ie colspans
                data.append(d)
        return data

