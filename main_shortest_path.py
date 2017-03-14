# python3

import sys

from Bot_shortest_path.game import Game

from Bot_shortest_path.bot import Bot


def __main__():
    bot = Bot()
    game = Game()
    game.run(bot)

__main__()
