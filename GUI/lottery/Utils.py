# -*- coding: utf-8 -*-
import Global



def playerGenerator(path=Global.PLAYERSPATH, prizewinners=set()):
    _playerPath = path if len(path) else Global.PLAYERSPATH
    while True:
        with open(_playerPath, 'r', encoding='utf-8') as f:
            for player in f:
                player = player.strip()
                if player not in prizewinners:
                    yield player