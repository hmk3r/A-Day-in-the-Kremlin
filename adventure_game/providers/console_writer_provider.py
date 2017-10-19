from adventure_game.contracts import IWriter


class ConsoleWriterProvider(IWriter):
    def write(self, text):
        print(text)

    def write_separator(self):
        print()
