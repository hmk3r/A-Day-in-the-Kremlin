from adventure_game.contracts import IReader


class ConsoleReaderProvider(IReader):
    def read_input(self, prompt=""):
        return input(prompt)
