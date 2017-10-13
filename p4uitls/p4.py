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
        



if __name__ == '__main__':
    args = (P4PORT, P4USER, P4PASSWD)
    P4Utils.info(*args)
