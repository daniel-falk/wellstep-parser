from configparser import ConfigParser, NoOptionError
from pkg_resources import resource_filename

f = resource_filename('wellstep', 'config.ini')
conf = ConfigParser()
conf.read(f)

def get_proxy():
    proxy = dict()
    try:
        proxy.update({'http' : conf.get('WELLSTEP', 'http_proxy')})
    except NoOptionError:
        pass
    try:
        proxy.update({'https' : conf.get('WELLSTEP', 'https_proxy')})
    except NoOptionError:
        pass
    return proxy
