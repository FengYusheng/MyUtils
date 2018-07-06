#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import sched
import logging

import P4

PIDFILE = os.getcwd() + '/.preload_pid.txt'

class P4SyncException(P4.P4Exception):
    def __init__(self, msg, exc_info=None):
        super(P4SyncException, self).__init__(msg)
        sys.exc_info = exc_info


class OutputHandler(P4.OutputHandler):
    """Process the output messages during preloading.

    https://github.com/rptb1/p4python/blob/master/p4test.py
    """
    def __init__(self):
        super(OutputHandler, self).__init__()
        self.totalFileCount = 0
        self.totalFileSize = 0
        self.syncedFileCount = 0
        self.timeout = False
        self.fileStat = None


    def outputStat(self, stat):
        """
        stat:

        {
        'depotFile': '//Test/youtube_dl/extractor/internetvideoarchive.py',
        'clientFile': '/home/fengyusheng/M1_1999/M1_1999_workspace/Test/youtube_dl/extractor/internetvideoarchive.py',
        'rev': '1',
        'action': 'added',
        'fileSize': '3764'
        }

        """
        if 'totalFileCount' in stat:
            self.totalFileCount = int(stat['totalFileCount'])
            self.totalFileSize = int(stat['totalFileSize'])
            # print('totalFileCount: {0}, totalFileSize: {1}'.format(stat['totalFileCount'], stat['totalFileSize']))

            logging.info('totalFileCount: {0}, totalFileSize: {1}'.format(stat['totalFileCount'], stat['totalFileSize']))

        self.syncedFileCount += 1
        fmt = 'Preloading files: {0}/{1}\r' if self.syncedFileCount < self.totalFileCount else 'Preloading files: {0}/{1}\n'
        print(fmt.format(self.syncedFileCount, self.totalFileCount), end='')
        logging.info(fmt.format(self.syncedFileCount, self.totalFileCount))
        self.fileStat = stat

        return self.HANDLED


    def outputMessage(self, msg):
        """Check the p4 messages from p4d to determine wheteher p4p should reconnect to server."""
        self.timeout = False if 'up-to-date' in str(msg) else True

        # print('\n'+'#'*10+'Server messages'+'#'*10)
        # print(msg)

        # logging.info('\n'+'#'*10+'Server messages'+'#'*10)
        logging.info(msg)

        if self.timeout:
            # print('Syncing file: {0}'.format(self.fileStat))
            logging.info('Syncing file: {0}'.format(self.fileStat))

        return self.HANDLED


class Preload(P4.P4):
    """The class is used to preload proxy cache only."""
    def __init__(self, **kwargs):
        super(Preload, self).__init__()
        self.port = kwargs['proxy_p4port']
        self.user = kwargs['target_p4user']
        self.password = kwargs['target_p4passwd']
        self.prog = 'MW-P4Proxy-Guider'
        self.version = '0.1'
        self.client = kwargs['preload_p4client']
        self.cwd = kwargs['project'] + '/' + kwargs['preload_p4client']
        self.protocol('proxyload', '')


    def isRunning(self):
        pid = 'NONE'

        if os.access(PIDFILE, os.F_OK):
            with open(PIDFILE, 'r', encoding=sys.getfilesystemencoding()) as f:
                pid = f.read()

        return pid != 'NONE', pid


    def __enter__(self):
        _isRunning, pid = self.isRunning()

        # _isRunning is False means no preloading process is runningself.
        # isRunning is True and pid is the current process pid mean this preloading process need to reconnect to server.
        if (not _isRunning) or (pid == str(os.getpid())):
            with open(PIDFILE, 'w', encoding=sys.getfilesystemencoding()) as f:
                f.write(str(os.getpid()))

            try:
                self.connect()
                self.run_login()
            except P4.P4Exception as e:
                # print(e.value)
                logging.info(e.value)
                raise P4SyncException('Retry to preload cache again in 5 hours.')
        else:
            # print('Preloading "{0}" is running, pid is {1}'.format(self.cwd, pid))
            logging.info('Preloading "{0}" is running, pid is {1}'.format(self.cwd, pid))

        return self


    def __exit__(self, *args, **kwargs):
        if self.connected():
            try:
                self.run_logout()
                self.disconnect()
            except P4.P4Exception as e:
                # print(e)
                logging.info(e)
            finally:
                with open(PIDFILE, 'w', encoding=sys.getfilesystemencoding()) as f:
                    f.write('NONE')


    def start(self):
        if self.connected():
            # self.run_sync('...#none')

            handler = OutputHandler()

            try:
                self.run_sync(handler=handler)
            except P4.P4Exception as e:
                #NOTE: This except can't catch any p4 exceptions if you specify a p4 OutputHandler.
                pass
            except Exception as e:
                # print(e)
                logging.info(e)
            finally:
                with open(PIDFILE, 'w', encoding=sys.getfilesystemencoding()) as f:
                    f.write('NONE')

                if handler.timeout:
                    handler.timeout = False
                    # print('Retry to preload cache again in 5 hours.')
                    logging.info('Retry to preload cache again in 5 hours.')
                    raise P4SyncException('Retry to preload cache again in 5 hours.')


def main(arguments=None):
    def _preload():
        with Preload(**opts) as p:
            p.start()

    if arguments is None:
        arguments = sys.argv[1:]

    opts = {}
    opts['project'] = arguments[0]
    opts['proxy_p4port'] = arguments[1]
    opts['target_p4user'] = arguments[2]
    opts['target_p4passwd'] = arguments[3]
    opts['preload_p4client'] = arguments[4]

    s = sched.scheduler(time.time, time.sleep)
    _old = retry_count = 0

    try:
        _preload()
    except P4SyncException as e:
        retry_count += 1

    while retry_count > 0:
        _old = retry_count
        time.sleep(60)
        # print('Retry {0} time(s).'.format(retry_count))
        logging.info('Retry {0} time(s).'.format(retry_count))

        try:
            _preload()
        except P4SyncException as e:
            retry_count += 1
        except Exception as e:
            # print(e)
            logging.info(e)
        finally:
            if _old == retry_count:
                # print('{0} stops preloading!'.format(os.getpid()))
                logging.info('{0} stops preloading!'.format(os.getpid()))
                break


if __name__ == '__main__':
    logging.basicConfig(filename=sys.argv[1]+'/bin'+'/preloading_log', format='%(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', level=logging.INFO)
    main(sys.argv[1:])
