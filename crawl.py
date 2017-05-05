# -*- coding: utf-8

import requests
from BeautifulSoup import BeautifulSoup
import sys

PAGE_URL = 'https://www.wellstep.se/ws05/main/authenticate.php'


def get_page_content(username=None, password=None, proxy=None):
    if username is None:
        raise ValueError('Page requires a username')
    if password is None:
        raise ValueError('Page requires a password')

    print(locals())

    form = locals()

    if not proxy is None:
        proxy = form.pop(proxy)
    else:
        proxy = None

    ans = requests.post(PAGE_URL,
            data = form,
            proxies = proxy,
            params = {
                'limit_lag' : 'TRUE'
                })

    if ans.status_code != requests.codes.ok:
        raise RuntimeError('Response from wellstep was: {}', ans.status_code)

    return ans.text.encode('utf-8')



def get_soup(raw_page):
    return BeautifulSoup(raw_page)


def get_user_team_stats_table(soup):
    # Find the table contatining the data
    divs = soup.findAll('div', {'class' : 'rubrik_ruta'})
    print([div.text for div in divs])
    dlen = [len(div.text) if div.text.find('STA LAG'.decode('utf-8')) > 0 else sys.maxint for div in divs]
    print(dlen)
    div = divs[dlen.index(min(dlen))]

    table = div.parent
    while table.name != 'table':
        table = table.parent

    return table


def parse_user_team_stats(soup):
    table = get_user_team_stats_table(soup)

    with open('table.html', 'w') as file:
        file.write(table.prettify())


content = get_page_content(
        username = '********',
        password = '*********')
soup = get_soup(content)
parse_user_team_stats(soup)
