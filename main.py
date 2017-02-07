# python3

import sys

from Bot.game import Game

from Bot.bot import Bot


def __main__():
    bot = Bot()
    game = Game()
    game.run(bot)

__main__()
