from adventure_game.models import Puzzle


class HarderLabPuzzle(Puzzle):
    def __init__(self):
        super().__init__("challenge")

    def answer_is_correct(self, answer):
        print("This puzzle never gets solved no matter the input")
        return False
