# clickhouse-repl

<center>

[![PyPI - Version](https://badge.fury.io/py/clickhouse-repl.svg)](https://badge.fury.io/py/clickhouse-repl)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/clickhouse-repl)](https://pypi.org/project/clickhouse-repl/)
[![PyPI - License](https://img.shields.io/pypi/l/clickhouse-repl)](https://opensource.org/licenses/MIT)

</center>

A toolkit for running ClickHouse queries interactively, leveraging the perks of an ipython console


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install clickhouse-repl.

```bash
pip install clickhouse-repl
```

## Usage

```
$ clickhouse-repl --help             
Usage: clickhouse-repl [OPTIONS]

  A toolkit for running ClickHouse queries interactively,  leveraging the
  perks of an ipython console.

  You can also set options with environment variables by using this format:
  CLICKHOUSE_REPL_<OPTION>

  Once in, run_query() will be your friend to execute queries.

Options:
  --host TEXT      Hostname or IP  [default: localhost]
  --port INTEGER   Native port  [default: 9000]
  --user TEXT      The ClickHouse user  [default: default]
  --password TEXT  Will be prompted. You can also set the environment variable
                   CLICKHOUSE_REPL_PASSWORD  [required]

  --database TEXT  The database we gonna use  [default: default]
  --help           Show this message and exit. 
```

### Connecting

#### Password prompted

If no environment variable is set, password will be prompted.


```shell
$ clickhouse-repl
Password: 
Welcome to clickhouse-repl 1.0.0 on Python 3.7.2, IPython 7.19.0
Connected to localhost:9000, clickhouser-server version 20.12.5
```
#### Password provided

This is not considered secure since passwords ends up persisted on `.bash_history`, for example.

**Avoid this one!**

```shell
$ clickhouse-repl --password v3ryh4rdp4ssword
```

> _Depending on the shell and settings in place, it is possible to bypass the recording to history by prefixing the command with double space_

#### Password from Environment Variable

You may set `CLICKHOUSE_REPL_PASSWORD` on your `.bashrc`/`.zshrc`/`.bash_profile`.

```shell
$   export CLICKHOUSE_REPL_PASSWORD=v3ryh4rdp4ssword
$ clickhouse-repl
```

Alternatively:
```shell
$   env CLICKHOUSE_REPL_PASSWORD=v3ryh4rdp4ssword clickhouse-repl
```

#### Connecting to specific database

Specify the database name and your session will start automatically from it.

Useful when your tables are somewhere else other than the ClickHouse default's database and you don't want to specify the database every time on your queries.

```
$ clickhouse-repl --database mydatabase
```

### Running Queries

#### Using `run_queries`
```
$ clickhouse-repl
Password: 
Welcome to clickhouse-repl 1.0.0 on Python 3.7.2, IPython 7.19.0
Connected to localhost:9000, clickhouser-server version 20.12.5
In [1]: run_query('select now64()')
Out[1]: [(datetime.datetime(2021, 1, 19, 0, 41, 7, 216000),)]

In [2]: 
```

#### Using `client`/`c`
These are shortcuts to [`clickhouse_driver.Client`](https://github.com/mymarilyn/clickhouse-driver/blob/5b1f4c7c53869cd1c9b1dbbded59bd5459eae14a/clickhouse_driver/client.py#L19) instance, initiated when a clickhouse-repl session is started.

You may use it for whatever purpose you may find.

To run queries with it you need to call `c.execute()`/`client.execute()` instead of `run_query()`. The later is in fact just a idiomatic shortcut pointing to the first.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
