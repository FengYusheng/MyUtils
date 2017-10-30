# -*- coding: utf-8 -*-

import P4
import os
import sys


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

        




if __name__ == '__main__':
    # args = (P4PORT, P4USER, P4PASSWD)
    args = ('10.86.10.197:1666', 'feng.yusheng', P4PASSWD)
    P4Utils.info(*args)
