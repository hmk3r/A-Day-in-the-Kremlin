import os
from adventure_game.contracts import IWriter


class ConsoleWriterProvider(IWriter):
    def write(self, text):
        print(text)

    def write_separator(self):
        print()

    # reference:
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python Jan 18 '10 at 7:34
    # Clears the terminal/cmd
    def clear(self):
        os.system('cls||clear')
