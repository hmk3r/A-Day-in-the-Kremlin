from adventure_game.models import Puzzle


class HarderLabPuzzle(Puzzle):
    def __init__(self):
        super().__init__("quest",
                         "the hard quest",
                         "This quest is pointless. But so is a circle. What's the answer?",
                         ["You have to guess"],
                         "42")
