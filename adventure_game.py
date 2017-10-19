#!/usr/bin/python3

from adventure_game.providers import *
from adventure_game.game_engine import GameEngine


def main():
    console_writer = ConsoleWriterProvider()
    console_reader = ConsoleReaderProvider()
    command_parser = CommandParserProvider()
    game_engine = GameEngine(console_writer, console_reader, command_parser)

    game_engine.run()


if __name__ == "__main__":
    main()
