from distutils.core import setup

setup(
        name = 'wellstep-parser',
        version = 0.1,
        description = 'Parser and user API for wellstep.se',
        author = 'Daniel Falk',
        author_email = 'daniel@da-robotteknik.se',
        url = 'https://github.com/daniel-falk/wellstep-parser',
        license = 'MIT',
        install_requires = ['requests', 'BeautifulSoup'],
        zip_safe = False)

