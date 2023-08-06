import os
from pybis import Openbis
from notebook.base.handlers import IPythonHandler

openbis_connections = {}
fake_password = "******"

def register_connection(connection_info):

    conn = OpenBISConnection(
        name                = connection_info.get('name'),
        url                 = connection_info.get('url'),
        verify_certificates = connection_info.get('verify_certificates', False),
        username            = connection_info.get('username'),
        password            = connection_info.get('password'),
        http_only           = connection_info.get('http_only', False),
        status              = 'not connected',
    )
    openbis_connections[conn.name] = conn
    return conn


class OpenBISConnection:
    """register an openBIS connection
    """

    def __init__(self, **kwargs):
        for needed_key in ['name', 'url']:
            if needed_key not in kwargs:
                raise KeyError("{} is missing".format(needed_key))

        for key in kwargs:
            setattr(self, key, kwargs[key])

        openbis = Openbis(
            url = self.url,
            verify_certificates = self.verify_certificates,
            allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks = self.http_only
        )
        self.openbis = openbis
        self.status = "not connected"

    def is_session_active(self):
        return self.openbis.is_session_active()

    def check_status(self):
        if self.openbis.is_session_active():
            self.status = "connected"
        else:
            self.status = "not connected"

    def login(self, username=None, password=None):
        if username is None:
            username=self.username
        if password is None or password == fake_password:
            password=self.password
        self.openbis.login(
            username = username,
            password = password,
        )
        # store username and password in memory
        self.username = username
        self.password = password
        self.status  = 'connected'

    def logout(self):
        self.openbis.logout()
        self.status = "not connected"

    def mount(self, username=None, password=None, hostname=None):
        if username is None:
            username=self.username
        if password is None or password == fake_password:
            password=self.password
        if hostname is None:
            hostname=self.openbis.hostname

        self.openbis.mount(
            username = username,
            password = password,
            hostname = hostname,
        )
        self.mount_status = 'mounted'

    def unmount(self):
        
        mountpoint = getattr(self.openbis, 'mountpoint', None)

        if mountpoint is None:
            try:
                mountpoint = self.openbis.get_mountpoint(search_mountpoint=True)
            except Exception:
                pass
        self.openbis.unmount(mountpoint=mountpoint)


    def get_info(self):
        is_mounted = self.openbis.is_mounted()
        mountpoint = ''
        if is_mounted:
            mountpoint = self.openbis.get_mountpoint()
        
        return {
            'name'      : self.name,
            'url'       : self.url,
            'status'    : self.status,
            'username'  : self.username,
            'password'  : fake_password,
            'isMounted' : is_mounted,
            'mountpoint': mountpoint,
        }

class OpenBISConnections(IPythonHandler):

    def _notebook_dir(self):
        notebook_dir = os.getcwd()
        if 'SingleUserNotebookApp' in self.config and 'notebook_dir' in self.config.SingleUserNotebookApp:
            notebook_dir = self.config.SingleUserNotebookApp.notebook_dir
        elif 'notebook_dir' in self.config.NotebookApp:
            notebook_dir = self.config.NotebookApp.notebook_dir
        return notebook_dir

    def post(self):
        """create a new connection

        :return: a new connection object
        """
        data = self.get_json_body()
        conn = register_connection(data)
        if conn.username and conn.password:
            try:
                conn.login()
            except Exception:
                pass
        self.get()
        return

    def get(self):
        """returns all available openBIS connections
        """

        connections= []
        for conn in openbis_connections.values():
            conn.check_status()
            connections.append(conn.get_info())

        self.write({
            'status'       : 200,
            'connections'  : connections,
            'notebook_dir' : self._notebook_dir()
        })
        return


class OpenBISConnectionHandler(IPythonHandler):
    """Handle the requests to /openbis/conn
    """

    def _notebook_dir(self):
        notebook_dir = os.getcwd()
        if 'SingleUserNotebookApp' in self.config and 'notebook_dir' in self.config.SingleUserNotebookApp:
            notebook_dir = self.config.SingleUserNotebookApp.notebook_dir
        elif 'notebook_dir' in self.config.NotebookApp:
            notebook_dir = self.config.NotebookApp.notebook_dir
        return notebook_dir

    def delete(self, connection_name):
        """logout and unmount a connection, remove from connection list
        """
        try:
            conn = openbis_connections[connection_name]
        except KeyError:
            self.set_status(404)
            self.write({
                "reason" : 'No such connection: {}'.format(data)
            })
            return

        try:
            conn.unmount()
        except Exception:
            pass

        try:
            conn.logout()
        except Exception:
            pass

        del openbis_connections[connection_name]


    def put(self, connection_name):
        """reconnect to a current connection
        :return: an updated connection object
        """
        data = self.get_json_body()

        try:
            conn = openbis_connections[connection_name]
        except KeyError:
            self.set_status(404)
            self.write({
                "reason" : 'No such connection: {}'.format(data)
            })
            return

        if data.get('action','') == 'mount':
            try:
                conn.mount(
                    username=data.get('username'),
                    password=data.get('password'),
                )
                self.write({
                    'status'     : 200,
                    'connection' : conn.get_info(),
                })
            except Exception as err:
                self.set_status(500)
                self.write({
                    "reason": "Mounting failed: {}".format(err)
                })
            return

        if data.get('action','') == 'unmount':
            try:
                conn.unmount()
                self.write({
                    'status'     : 200,
                    'connection' : conn.get_info(),
                })
            except Exception as err:
                self.set_status(500)
                self.write({
                    "reason": "Unmounting failed: {}".format(err)
                })
            return

        if data.get('action','') == 'logout':
            try:
                conn.logout()
                self.write({
                    'status'     : 200,
                    'connection' : conn.get_info(),
                })
            except Exception as err:
                self.set_status(500)
                self.write({
                    "reason": "logout failed: {}".format(err)
                })
            return

        # no action given, try to connect instead

        try:
            conn.login(data.get('username'), data.get('password'))
        except ConnectionError:
            self.set_status(500)
            self.write({
                "reason": "Could not establish connection to {}".format(connection_name)
            })
            return
        except ValueError:
            self.set_status(401)
            self.write({
                "reason": "Incorrect username or password for {}".format(connection_name)
            })
            return
        except Exception:
            self.set_status(500)
            self.write({
                "reason": "General Network Error"
            })

        self.write({
            'status'       : 200,
            'connection'   : conn.get_info(),
            'notebook_dir' : self._notebook_dir()
        })

    def get(self, connection_name):
        """returns  information about a connection name
        """

        try:
            conn = openbis_connections[connection_name]
        except KeyError:
            self.set_status(404)
            self.write({
                "reason" : 'No such connection: {}'.format(connection_name)
            })
            return

        conn.check_status()

        self.write({
            'status'        : 200,
            'connection'    : conn.get_info(),
            'noteboook_dir' : self._notebook_dir()
        })
        return
