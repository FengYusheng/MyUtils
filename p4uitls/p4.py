# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil

import P4


P4PORT = '127.0.0.1:1818'
P4USER = 'fengys'
P4PASSWD = 'dongfeng7101!'


class P4Utils():
    @staticmethod
    def info(*args, **keywords):
        port, user, password = args
        p4 = P4.P4()

        # Restrict the format of the command output to version 2015.2, no matter what actual version of your server is.
        p4.api_level = 79

        # The string returned by a non-unicode server is encode in UTF-8. This
        # variable is availabe in python 3.
        p4.encoding = 'utf-8'

        # Check p4.errors and p4.warnings arrays.
        p4.exception_level = 0

        # You also can speicify P4HOST in your P4CONFIG file.
        # p4.host = '127.0.0.1'

        p4.port = P4PORT

        # Give a name to your script.
        p4.prog = 'my-script-no-mans-land'

        # Indicate the version of your program.
        p4.version = '0.1'


class OutputHandler(P4.OutputHandler):
    """Process the output messages during preloading.

    https://github.com/rptb1/p4python/blob/master/p4test.py
    """
    def __init__(self):
        super(OutputHandler, self).__init__()
        self.totalFileCount = 0
        self.totalFileSize = 0
        self.syncedFileCount = 0


    def outputStat(self, stat):
        if 'totalFileCount' in stat:
            self.totalFileCount = int(stat['totalFileCount'])
            self.totalFileSize = int(stat['totalFileSize'])
            print('totalFileCount: {0}, totalFileSize: {1}'.format(stat['totalFileCount'], stat['totalFileSize']))

        self.syncedFileCount += 1
        fmt = 'Preloading files: {0}/{1}\r' if self.syncedFileCount < self.totalFileCount else 'Preloading files: {0}/{1}\n'
        print(fmt.format(self.syncedFileCount, self.totalFileCount), end='')

        return self.HANDLED


    def outputMessage(self, msg):
        print('\n'+'#'*10+'Server messages'+'#'*10)
        print(msg)
        return self.HANDLED


class P4Connection(P4.P4):
    """Create a P4 connecton.

    kwargs:

    port:       The address of the target Perforce server.
    user:       The Perforce account.
    password:   The Perforce account's password
    """
    def __init__(self, **kwargs):
        super(P4Connection, self).__init__()

        # Set these p4 connection options before connecting th the Perforce server.
        self.port = kwargs['target_p4port']
        self.user = kwargs['target_p4user']
        self.password = kwargs['target_p4passwd']
        self.prog = 'MW-P4Proxy-Guider'
        self.version = '0.1'

        if 'preload_p4client' in kwargs:
            self.client = kwargs['preload_p4client']
            self.cwd = kwargs['project'] + '/' + kwargs['preload_p4client']
            self.protocol('proxyload', '') # p4 -Zproxyload sync

        #NOTE: Document says set_env() only works on Windows and OS X.
        # self.set_env('P4CONFIG', './p4config.txt')


    def __enter__(self):
        self.connect()
        self.run_login()
        return self


    def __exit__(self, *args, **kwargs):
        if self.connected():
            self.run_logout()
            self.disconnect()


    def apiMessage(self):
        print('p4 encoding: {0}'.format(self.encoding))
        print('p4 cwd: {0}'.format(self.cwd))
        print('p4 exception_level: {0}'.format(self.exception_level))
        print('p4 host: {0}'.format(self.host))
        print('p4 maxlocktime: {0}'.format(self.maxlocktime))
        print('p4 prog: {0}'.format(self.prog))
        print('config: {0}'.format(self.p4config_file))
        # TODO: Support SSL?


    def server_version(self):
        info = self.run_info()
        if len(info) > 0:
            info = info[0]
            version = info['serverVersion']
            pattern = re.compile(r'(\d{4}\.\d)/(\d+?)\s')
            m = pattern.search(version)

            return m.group(1) + '-' + m.group(2)

        else:
            #TODO: Raise a p4 exception.
            pass


    def createWorkspace(self, client, path, depots):
        workspaces = [(c['client'], c['Root']) for c in self.run_clients()]

        if (client, path) not in workspaces:
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            self.run_client('-d', client)

        client_spec = self.fetch_client(client)
        client_spec['Client'] = client
        client_spec['Root'] = path
        client_spec['View'] = [d+' '+'//'+client+'/'+d.partition('//')[2] for d in depots]
        self.save_client(client_spec)


    def createWorkspace2(self, client, path, depots):
        workspaces = [(c['client'], c['Root']) for c in self.run_clients()]

        if (client, path) not in workspaces:
            shutil.rmtree(path)
            os.mkdir(path)
            client_spec = self.fetch_client(client)
            client_spec['Client'] = client
            client_spec['Root'] = path
            client_spec['View'] = [d+' '+'//'+client+'/'+d.partition('//')[2] for d in depots]
            self.save_client(client_spec)


    def preload(self):
        # Set "-Zproxyload" with p4python. https://community.perforce.com/s/article/5338
        self.run_sync(handler=OutputHandler())


if __name__ == '__main__':
    # args = (P4PORT, P4USER, P4PASSWD)
    args = ('10.86.10.197:1666', 'feng.yusheng', P4PASSWD)
    P4Utils.info(*args)
