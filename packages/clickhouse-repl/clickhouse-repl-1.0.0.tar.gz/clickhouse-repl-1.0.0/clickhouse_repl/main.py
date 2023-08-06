import click


PREFIX = 'CLICKHOUSE_REPL'


@click.command(context_settings=dict(auto_envvar_prefix=PREFIX))
@click.option('--host', default='localhost', help='Hostname or IP', show_default=True)
@click.option('--port', default=9000, help='Native port', show_default=True)
@click.option('--user', default='default', help='The ClickHouse user', show_default=True)
@click.option('--password', required=True, prompt=True, hide_input=True,
              help=f'Will be prompted. You can also set the environment variable {PREFIX}_PASSWORD')
@click.option('--database', default='default', help='The database we gonna use', show_default=True)
def cli(host, port, user, password, database):
    """A toolkit for running ClickHouse queries interactively,  leveraging the perks of an ipython
    console.\n
    You can also set options with environment variables by using this format:
    CLICKHOUSE_REPL_<OPTION>

    Once in, run_query() will be your friend to execute queries.

    """
    import IPython
    import sys
    from traitlets.config.loader import Config
    from clickhouse_driver import Client
    from pkg_resources import get_distribution

    creds = {'host': host, 'port': port, 'user': user, 'password': password, 'database': database}
    params = dict(client_name='clickhouse-repl', **creds)
    client = Client(**params)
    client.connection.connect()
    client.connection.ping()
    server_version = '.'.join(str(x) for x in client.connection.context.server_info.version_tuple())
    banner = "Welcome to clickhouse-repl %s on Python %s, IPython %s\n"
    banner += "Connected to %s, clickhouser-server version %s" % (
        client.connection.get_description(),
        server_version,
    )
    ctx = {'client': client, 'c': client, 'run_query': client.execute}
    c = Config()
    c.TerminalInteractiveShell.banner1 = banner % (
        get_distribution('clickhouse-repl').version,
        sys.version.split()[0],
        get_distribution('ipython').version,
    )

    IPython.start_ipython(argv=[], user_ns=ctx, config=c)
