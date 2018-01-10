# -*- coding: utf-8 -*-
import Global


def playerGenerator(filePath=Global.PLAYERSPATH):
    while True:
        with open(filePath, 'r', encoding='utf-8') as f:
            for player in f:
                yield player
