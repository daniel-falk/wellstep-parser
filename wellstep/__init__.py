from configparser import ConfigParser
from pkg_resources import resource_filename

f = resource_filename('wellstep', 'config.ini')
conf = ConfigParser()
conf.read(f)

