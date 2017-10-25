import os
import time
import sys
from adventure_game.contracts import IWriter


class ConsoleWriterProvider(IWriter):
    def write(self, text):
        print(text)

    # reference:
    # https://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing Nov 4 '10 at 17:29
    # Simulates typing
    def write_slowly(self, text):
        for letter in text:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(.1)
        print()

    # end reference

    def write_separator(self):
        print()

    # reference:
    # https://stackoverflow.com/questions/2084508/clear-terminal-in-python Jan 18 '10 at 7:34
    # Clears the terminal/cmd
    def clear(self):
        os.system('cls||clear')
    # end reference
