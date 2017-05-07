# Wellstep-parser

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Purpose
Parser for www.wellstep.se, company activity challanges to show team info and history in broswer/api.

## Setup

### Setup mysql

```bash
apt-get install mysql-server
mysql -uroot -p
```
```mysql
CREATE DATABASE wellstep;
GRANT ALL ON wellstep.* TO wellstep@'127.0.0.1' IDENTIFIED BY '**password**'
```

You also need python3-dev and libmysqlclient-dev
```bash
apt-get install python3-dev
apt-get install libmysqlclient-dev
```

### Deploy wellstep-parser 

Download or clone using git
```bash
git clone https://github.com/daniel-falk/wellstep-parser.git
cd wellstep-parser
```

Set up a virtual env with python 3 and install all dependencies:
```bash
virtualenv -p python3 .env
source .env/bin/activate
pip install -e .
```

Edit the wellstep/config.ini file and add the login info for wellstep and your mysql-database.

To test functionality run unittest:
```bash
make test
```
