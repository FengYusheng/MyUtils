#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
import sys
import json
import shlex
import shutil
import ctypes.util
import subprocess

import p4

from preload import Preload

globalSettings = {
    'encoding' : 'utf-8'
}


class MWP4ProxyGuiderException(Exception):
    """Base exception for MWP4ProxyGuider."""
    pass


class InvalidPlatformException(MWP4ProxyGuiderException):
    def __init__(self, exc_info=None):
        super(InvalidPlatformException, self).__init__()
        sys.exc_info = exc_info


class InvalideUserException(MWP4ProxyGuiderException):
    def __init__(self, exc_info=None):
        super(InvalideUserException, self).__init__()
        sys.exc_info = exc_info


class KeyboardInterruption(MWP4ProxyGuiderException):
    def __init__(self, exc_info=None):
        super(KeyboardInterruption, self).__init__()
        sys.exc_info = exc_info


class LackBinaryFiles(MWP4ProxyGuiderException):
    def __init__(self, msg, exc_info=None):
        super(LackBinaryFiles, self).__init__(msg)
        sys.exc_info = exc_info


class PortOccupiedException(MWP4ProxyGuiderException):
    def __init__(self, msg, exc_info=None):
        super(PortOccupiedException, self).__init__(msg)
        sys.exc_info = exc_info


class RunCommandFailed(MWP4ProxyGuiderException):
    def __init__(self, msg, exc_info=None):
        super(RunCommandFailed, self).__init__(msg)
        sys.exc_info = exc_info


class DeployP4Proxy(object):
    """Deploy a Peforce proxy service

    1. Specify a project directory.
    2. copy all the necessary things into the project file.
    3. Specify default values for logs, cache and portself.
    4. Make sure the "p4p" and "p4" software version is appropriate. This depends on the "p4d" version.
    5. Start the p4p process.

    Available options:

    p4port:             Specify the port on which P4P will listen for requests from Perforce applications.
    p4cache:            Specify the directory where revisions are cached.
    p4log:              Specify the location of the log file.
    p4target:           Specify the port of the target Perforce server.
    """
    def __init__(self, opts):
        super(DeployP4Proxy, self).__init__()
        self.opts = opts


    def _modifyOption(self, option_name, old_value, reason=None):
        if reason is not None:
            print('#WARING: You need to modify {0}, because {1}'.format(option_name, reason))

        print('Old {0} value: {1}'.format(option_name, old_value))
        new_value = input('New "{0}": '.format(option_name))
        while new_value == old_value:
            new_value =  input('New "{0}": '.format(option_name))

        return new_value


    def _remind(self, option_name, opt_value, reason):
        modified = input('{0}. Do you want to specify a new "{1}"? [y/n]: '.format(reason, option_name)).lower()
        while modified not in ('y', 'n'):
            modified = input('{0}. Do you want to specify a new "{1}"? [y/n]: '.format(reason, option_name)).lower()

        return modified


    def _saveConf(self):
        dst = self.opts['project'] + '/proxyConf.json'
        with open(dst, 'w', encoding='utf-8') as f:
            json.dump(self.opts, f, indent=4)


    def _downloadProxy(self, version):
        pass


    def _cleanInvalidProject(self, project):
        pass


    def createProject(self, dest=None):
        if dest is None:
            dest = self.opts['project'] + '_' + self.opts['proxy_p4port']

        dest = '~/' + dest
        dest = os.path.expandvars(os.path.expanduser(dest))
        while os.path.islink(dest):
            self.opts['project'] = self._modifyOption('project', '"{0}" is a symbolic link.'.format(dest))
            dest = '~/' + self.opts['project']
            dest = os.path.expandvars(os.path.expanduser(dest))

        while os.path.isdir(dest):
            if 'y' == self._remind('project', dest, '"{0}" is an existing directory'.format(dest)):
                self.opts['project'] = self._modifyOption('project', self.opts['project'])
                self.opts['proxy_p4port'] = self._modifyOption('proxy_p4port', self.opts['proxy_p4port'])
                dest = '~/' + self.opts['project'] + '_' + self.opts['proxy_p4port']
                dest = os.path.expandvars(os.path.expanduser(dest))
            else:
                break

        # UNITTEST: Check p4port.
        # pattern = re.compile(r'\d$')
        # while pattern.match(self.opts['proxy_p4port']) is None:
        #     # print(pattern.match(self.opts['proxy_p4port']))
        #     break

        os.path.isdir(dest) == False and os.mkdir(dest)
        self.opts['project'] = dest

        cache = self.opts['project'] + '/' + self.opts['proxy_p4cache']
        os.path.isdir(cache) or os.mkdir(cache)
        self.opts['proxy_p4cache'] = cache

        self.opts['proxy_p4log'] = self.opts['project'] + '/' + self.opts['proxy_p4log']


    def copyToolsIntoProject(self, dest=None):
        if dest is None:
            dest = self.opts['project']

        with p4.P4Connection(**self.opts) as p4conn:
            version = p4conn.server_version()

        # Copy "p4p"
        src = os.path.dirname(os.getcwd()) + '/bin/proxy/' + version
        p4pFile = src + '/p4p'

        if os.path.isdir(src) and os.access(p4pFile, os.R_OK):
            dst = self.opts['project'] + '/bin'
            os.path.isdir(dst) or os.mkdir(dst)

            try:
                # TODO: Assign appropriate permissions to the p4p
                shutil.copy2(p4pFile, dst)
            except OSError as e:
                # This OSError ("Text file busy") indicates that this port has been occupied by another p4 proxy process.
                raise PortOccupiedException('#WARNING: The port "{0}"" has been occupied by another p4 proxy process.'.format(self.opts['proxy_p4port']))

            self.opts['p4pFileLocation'] = dst + '/p4p'
        else:
            raise LackBinaryFiles("The p4p of version {0} doesn't exists.".format(version), sys.exc_info())

        # Copy 'p4'.
        src = os.path.dirname(os.getcwd()) + '/bin/p4cl/' + version
        p4File = src + '/p4'

        if os.path.isdir(src) and os.access(p4File, os.R_OK):
            dst = self.opts['project'] + '/bin'
            os.path.isdir(dst) or os.mkdir(dst)

            try:
                # TODO: Assign appropriate permissions to the p4 file.
                shutil.copy2(p4File, dst)
            except OSError as e:
                # This OSError ("Text file busy") indicates that this proxy is preloading now.
                raise PortOccupiedException('#WARNING: The Proxy {0} is preloading now.'.format(self.opts['project']))

            self.opts['p4FileLocation'] = dst + '/p4'
        else:
            raise LackBinaryFiles("The p4 of version {0} doesn't exists.".format(version), sys.exc_info())


    def installPreloader(self):
        if not hasattr(sys, 'frozen'):
            src = os.path.dirname(os.path.realpath(os.path.abspath(__file__))) + '/preload.py'
        else:
            src = os.getcwd() + '/preload'

        dst = self.opts['project'] + '/bin'

        try:
            shutil.copy2(src, dst)
        except OSError as e:
            raise PortOccupiedException('#WARNING: The Proxy {0} is preloading now.'.format(self.opts['project']))

        if not hasattr(sys, 'frozen'):
            cmd = '#!/usr/bin/env bash\n\n\n' + self.opts['project'] + '/bin/preload.py' + ' ' + self.opts['project'] + ' ' + self.opts['proxy_p4port'] + ' ' + self.opts['target_p4user'] + ' ' + self.opts['target_p4passwd'] + ' ' + self.opts['preload_p4client'] + '\n'
        else:
            cmd = '#!/usr/bin/env bash\n\n\n' + self.opts['project'] + '/bin/preload' + ' ' + self.opts['project'] + ' ' + self.opts['proxy_p4port'] + ' ' + self.opts['target_p4user'] + ' ' + self.opts['target_p4passwd'] + ' ' + self.opts['preload_p4client'] + '\n'

        with open(dst+'/preload.bash', 'w+', encoding=globalSettings['encoding']) as f:
            f.write(cmd)


    def createP4Workspace(self, workspace=None):
        if workspace is None:
            workspace = self.opts['preload_p4client']

        workspace = self.opts['project'] + '/' + workspace
        os.path.isdir(workspace) or os.mkdir(workspace)

        self.opts['target_p4port'] = '127.0.0.1:' + self.opts['proxy_p4port']

        with p4.P4Connection(**self.opts) as p4conn:
            p4conn.createWorkspace(self.opts['preload_p4client'], workspace, self.opts['preload_p4depots'])

        shutil.copy2('./p4config.txt', workspace)


    def startProxy(self, **kwargs):
        # NOTE: I don't validate these arguments.
        # TODO: Assign appropriate permissions to the p4p.
        # cmd = self.opts['p4pFileLocation'] + ' -d -q -c -r ' + self.opts['project'] + '/cache' + ' -L ' + self.opts['project'] + '/log' + ' -p ' + self.opts['proxy_p4port'] + ' -t ' + self.opts['target_p4port']
        cmd = self.opts['p4pFileLocation'] + ' -d -q -c -r ' + self.opts['proxy_p4cache'] + ' -L ' + self.opts['proxy_p4log'] + ' -p ' + self.opts['proxy_p4port'] + ' -t ' + self.opts['target_p4port']

        # print(shlex.split(cmd))
        # /bin/sh -c /home/fengyusheng/M1_1999/bin/p4p -d -q -c -r /home/fengyusheng/M1_1999/cache -L /home/fengyusheng/M1_1999/log -p 1999 -t 10.0.250.3:1818
        # ps = subprocess.Popen(shlex.split(cmd), shell=True, stdout=subprocess.PIPE)

        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        pid = ps.pid
        ps.stdout.close()
        result = ps.wait()

        if result == 0:
            print('Success! Your Perforce proxy is running')
        else:
            raise RunCommandFailed('Failed to start Perforce proxy. Port "{0}" may have been occupied by another p4 proxy process. Error number: {1}'.format(self.opts['proxy_p4port'], result))


    def preload(self):
        self.opts['target_p4port'] = '127.0.0.1:' + self.opts['proxy_p4port']
        with p4.P4Connection(**self.opts) as p4conn:
            p4conn.preload()


    def __enter__(self):
        return self


    def __exit__(self, *args):
        self._saveConf()


class PreloadProxyCache(object):
    def __init__(self, opts):
        super(PreloadProxyCache, self).__init__()
        self.opts = opts


    def _modifyOption(self, option_name, old_value, reason=None):
        if reason is not None:
            print('#WARING: You need to modify {0}, because {1}'.format(option_name, reason))

        print('Old {0} value: {1}'.format(option_name, old_value))
        new_value = input('New "{0}": '.format(option_name))
        while new_value == old_value:
            new_value =  input('New "{0}": '.format(option_name))

        return new_value


    def _remind(self, option_name, opt_value, reason):
        modified = input('{0}. Do you want to specify a new "{1}"? [y/n]: '.format(reason, option_name)).lower()
        while modified not in ('y', 'n'):
            modified = input('{0}. Do you want to specify a new "{1}"? [y/n]: '.format(reason, option_name)).lower()

        return modified


    def createProject(self, dest=None):
        if dest is None:
            dest = self.opts['project'] + '_' + self.opts['proxy_p4port']

        dest = '~/' + dest
        dest = os.path.expandvars(os.path.expanduser(dest))

        while os.path.islink(dest):
            self.opts['project'] = self._modifyOption('project', '"{0}" is a symbolic link.'.format(dest))
            dest = '~/' + self.opts['project']
            dest = os.path.expandvars(os.path.expanduser(dest))

        while os.path.isdir(dest):
            if 'y' == self._remind('project', dest, '"{0}" is an existing directory'.format(dest)):
                self.opts['project'] = self._modifyOption('project', self.opts['project'])
                dest = '~/' + self.opts['project'] + '_' + self.opts['proxy_p4port']
                dest = os.path.expandvars(os.path.expanduser(dest))
            else:
                break

        os.path.isdir(dest) == False and os.mkdir(dest)
        self.opts['project'] = dest


    def copyToolsIntoProject(self, dest=None):
        if dest is None:
            dest = self.opts['project']

        with p4.P4Connection(**self.opts) as p4conn:
            version = p4conn.server_version()

        # src = os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))) + '/bin/p4cl/' + version
        src = os.path.dirname(os.getcwd()) + '/bin/p4cl/' + version
        p4File = src + '/p4'

        if os.path.isdir(src) and os.access(p4File, os.R_OK):
            dst = self.opts['project'] + '/bin'
            os.path.isdir(dst) or os.mkdir(dst)

            try:
                # TODO: Assign appropriate permissions to the p4 file.
                shutil.copy2(p4File, dst)
            except OSError as e:
                # This OSError ("Text file busy") indicates that this proxy is preloading now.
                raise PortOccupiedException('#WARNING: The Proxy {0} is preloading now.'.format(self.opts['project']))

            self.opts['p4FileLocation'] = dst + '/p4'
        else:
            raise LackBinaryFiles("The p4 of version {0} doesn't exists.".format(version), sys.exc_info())


    def createP4Workspace(self, workspace=None):
        if workspace is None:
            workspace = self.opts['preload_p4client']

        workspace = self.opts['project'] + '/' + workspace
        os.path.isdir(workspace) or os.mkdir(workspace)

        #NOTE: I use the localhost directly here.
        self.opts['target_p4port'] = '127.0.0.1:' + self.opts['proxy_p4port']

        with p4.P4Connection(**self.opts) as p4conn:
            p4conn.createWorkspace(self.opts['preload_p4client'], workspace, self.opts['preload_p4depots'])

        shutil.copy2('./p4config.txt', workspace)


    def preload(self):
        #NOTE: I use the localhost directly here.
        self.opts['target_p4port'] = '127.0.0.1:' + self.opts['proxy_p4port']
        with p4.P4Connection(**self.opts) as p4conn:
            p4conn.preload()


    def installPreloader(self):
        src = os.getcwd() + '/preload.py'
        src = os.path.dirname(os.path.realpath(os.path.abspath(__file__))) + '/preload.py'
        dst = self.opts['project'] + '/bin'

        try:
            shutil.copy2(src, dst)
        except OSError as e:
            raise PortOccupiedException('#WARNING: The Proxy {0} is preloading now.'.format(self.opts['project']))

        cmd = '#!/usr/bin/env bash\n\n\n' + self.opts['project'] + '/bin/preload.py' + ' ' + self.opts['project'] + ' ' + self.opts['target_p4port'] + ' ' + self.opts['target_p4user'] + ' ' + self.opts['target_p4passwd'] + ' ' + self.opts['preload_p4client'] + '\n'
        with open(dst+'/preload.bash', 'w+', encoding=globalSettings['encoding']) as f:
            f.write(cmd)


    def __enter__(self):
        return self


    def __exit__(self, *args, **kwargs):
        pass


def setProcessTitle(title):
    libc = ctypes.util.find_library('c')
    if libc is not None:
        try:
            libc = ctypes.cdll.LoadLibrary(libc)
        except OSError as e:
            return
        except TypeError as e:
            return

        titleBytes = title.encode(globalSettings['encoding'])
        buf = ctypes.create_string_buffer(len(titleBytes))
        buf.value = titleBytes

        try:
            libc.prctl(15, buf, 0, 0, 0)
        except AttributeError as e:
            return


def writeString(message, out=sys.stdout):
    pass
