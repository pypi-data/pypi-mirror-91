# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickhouse_repl']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'clickhouse-driver>=0.2.0,<0.3.0',
 'ipython>=7.9.0,<8.0.0',
 'jedi<0.18.0']

entry_points = \
{'console_scripts': ['clickhouse-repl = clickhouse_repl.main:cli']}

setup_kwargs = {
    'name': 'clickhouse-repl',
    'version': '1.0.0',
    'description': 'A toolkit for running ClickHouse queries interactively, leveraging the perks of an ipython console',
    'long_description': "# clickhouse-repl\n\n<center>\n\n[![PyPI - Version](https://badge.fury.io/py/clickhouse-repl.svg)](https://badge.fury.io/py/clickhouse-repl)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/clickhouse-repl)](https://pypi.org/project/clickhouse-repl/)\n[![PyPI - License](https://img.shields.io/pypi/l/clickhouse-repl)](https://opensource.org/licenses/MIT)\n\n</center>\n\nA toolkit for running ClickHouse queries interactively, leveraging the perks of an ipython console\n\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install clickhouse-repl.\n\n```bash\npip install clickhouse-repl\n```\n\n## Usage\n\n```\n$ clickhouse-repl --help             \nUsage: clickhouse-repl [OPTIONS]\n\n  A toolkit for running ClickHouse queries interactively,  leveraging the\n  perks of an ipython console.\n\n  You can also set options with environment variables by using this format:\n  CLICKHOUSE_REPL_<OPTION>\n\n  Once in, run_query() will be your friend to execute queries.\n\nOptions:\n  --host TEXT      Hostname or IP  [default: localhost]\n  --port INTEGER   Native port  [default: 9000]\n  --user TEXT      The ClickHouse user  [default: default]\n  --password TEXT  Will be prompted. You can also set the environment variable\n                   CLICKHOUSE_REPL_PASSWORD  [required]\n\n  --database TEXT  The database we gonna use  [default: default]\n  --help           Show this message and exit. \n```\n\n### Connecting\n\n#### Password prompted\n\nIf no environment variable is set, password will be prompted.\n\n\n```shell\n$ clickhouse-repl\nPassword: \nWelcome to clickhouse-repl 1.0.0 on Python 3.7.2, IPython 7.19.0\nConnected to localhost:9000, clickhouser-server version 20.12.5\n```\n#### Password provided\n\nThis is not considered secure since passwords ends up persisted on `.bash_history`, for example.\n\n**Avoid this one!**\n\n```shell\n$ clickhouse-repl --password v3ryh4rdp4ssword\n```\n\n> _Depending on the shell and settings in place, it is possible to bypass the recording to history by prefixing the command with double space_\n\n#### Password from Environment Variable\n\nYou may set `CLICKHOUSE_REPL_PASSWORD` on your `.bashrc`/`.zshrc`/`.bash_profile`.\n\n```shell\n$   export CLICKHOUSE_REPL_PASSWORD=v3ryh4rdp4ssword\n$ clickhouse-repl\n```\n\nAlternatively:\n```shell\n$   env CLICKHOUSE_REPL_PASSWORD=v3ryh4rdp4ssword clickhouse-repl\n```\n\n#### Connecting to specific database\n\nSpecify the database name and your session will start automatically from it.\n\nUseful when your tables are somewhere else other than the ClickHouse default's database and you don't want to specify the database every time on your queries.\n\n```\n$ clickhouse-repl --database mydatabase\n```\n\n### Running Queries\n\n#### Using `run_queries`\n```\n$ clickhouse-repl\nPassword: \nWelcome to clickhouse-repl 1.0.0 on Python 3.7.2, IPython 7.19.0\nConnected to localhost:9000, clickhouser-server version 20.12.5\nIn [1]: run_query('select now64()')\nOut[1]: [(datetime.datetime(2021, 1, 19, 0, 41, 7, 216000),)]\n\nIn [2]: \n```\n\n#### Using `client`/`c`\nThese are shortcuts to [`clickhouse_driver.Client`](https://github.com/mymarilyn/clickhouse-driver/blob/5b1f4c7c53869cd1c9b1dbbded59bd5459eae14a/clickhouse_driver/client.py#L19) instance, initiated when a clickhouse-repl session is started.\n\nYou may use it for whatever purpose you may find.\n\nTo run queries with it you need to call `c.execute()`/`client.execute()` instead of `run_query()`. The later is in fact just a idiomatic shortcut pointing to the first.\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'klic.tools',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
