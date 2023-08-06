import os
import re
from urllib.parse import urlparse
import yaml
from notebook.utils import url_path_join

from .connection import OpenBISConnections, OpenBISConnectionHandler, register_connection
from .dataset import DataSetTypesHandler, DataSetDownloadHandler, DataSetUploadHandler
from .sample import SampleHandler
from .requirements import Requirements


def _jupyter_server_extension_paths():
    return [{'module': 'jupyter-openbis-server.server'}]


def _load_configuration(paths, filename='openbis-connections.yaml'):

    if paths is None:
        paths = []
        home = os.path.expanduser("~")
        paths.append(os.path.join(home, '.jupyter'))

    # look in all config file paths of jupyter
    # for openbis connection files and load them
    connections = []
    for path in paths:
        abs_filename = os.path.join(path, filename)
        if os.path.isfile(abs_filename):
            with open(abs_filename, 'r') as stream:
                try:
                    config = yaml.safe_load(stream)
                    for connection in config['connections']:
                        connections.append(connection)
                except yaml.YAMLexception as err:
                    print(err)
                    return None

    return connections


def load_jupyter_server_extension(nb_server_app):
    """Call when the extension is loaded.
    :param nb_server_app: Handle to the Notebook webserver instance.
    """

    # load the configuration file
    # and register the openBIS connections.
    # If username and password is available, try to connect to the server
    connections = _load_configuration(
        paths    = nb_server_app.config_file_paths,
        filename = 'openbis-connections.yaml'
    )

    for connection_info in connections:
        conn = register_connection(connection_info)
        print("Registered: {}".format(conn.url))
        if conn.username and conn.password:
            try:
                conn.login()
                print("Successfully connected to: {}".format(conn.url))
            except ValueError:
                print("Incorrect username or password for: {}".format(conn.url))
            except Exception:
                print("Cannot establish connection to: {}".format(conn.url))

    if "OPENBIS_URL" in os.environ and "OPENBIS_TOKEN" in os.environ:
        up = urlparse(os.environ["OPENBIS_URL"])
        match = re.search(r'(?P<username>.*)-.*', os.environ["OPENBIS_TOKEN"])
        username = match.groupdict()['username']
        connection_info = {
            "name": up.hostname,
            "url":  os.environ["OPENBIS_URL"],
            "verify_certificates" : False,
            "username" : username,
        }
        conn = register_connection(connection_info) 
        conn.token = os.environ["OPENBIS_TOKEN"]

    # Add URL handlers to our web_app
    # see Tornado documentation: https://www.tornadoweb.org
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    base_url = web_app.settings['base_url']

    # DataSet download
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url,
                '/openbis/dataset/(?P<connection_name>.*)?/(?P<permId>.*)?/(?P<downloadPath>.*)'
            ),
            DataSetDownloadHandler
        )]
    )

    # DataSet upload
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url, '/openbis/dataset/(?P<connection_name>.*)'
            ),
            DataSetUploadHandler
        )]
    )

    # DataSet-Types
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url, '/openbis/datasetTypes/(?P<connection_name>.*)'
            ),
            DataSetTypesHandler
        )]
    )

    # DataSets for Sample identifier/permId
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url,
                '/openbis/sample/(?P<connection_name>.*)?/(?P<identifier>.*)'
            ),
            SampleHandler
        )]
    )

    # OpenBIS connections
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url,
                '/openbis/conns'
            ),
            OpenBISConnections
        )]
    )

    # Modify / reconnect to a connection
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url,
                '/openbis/conn/(?P<connection_name>.*)'
            ),
            OpenBISConnectionHandler
        )]
    )

    # OpenBIS connections
    web_app.add_handlers(
        host_pattern, [(
            url_path_join(
                base_url,
                '/requirements'
            ),
            Requirements
        )]
    )
