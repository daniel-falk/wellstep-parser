from distutils.core import setup

setup(
        name = 'wellstep',
        version = 0.1,
        description = 'Parser and user API for wellstep.se',
        author = 'Daniel Falk',
        author_email = 'daniel@da-robotteknik.se',
        url = 'https://github.com/daniel-falk/wellstep-parser',
        license = 'MIT',
        install_requires = [
            'requests',
            'beautifulsoup4',
            'html5lib',
            'configparser'],
        package_data = {'wellstep' : [
                'config.ini'
            ]}
        zip_safe = False)

