# -*- coding: utf-8 -*-


PLAYERPATH = './names.txt'

def playerGenerator():
    while True:
        with open(PLAYERPATH, 'r', encoding='utf-8') as f:
            for player in f:
                yield player
