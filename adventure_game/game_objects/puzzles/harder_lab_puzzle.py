from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException


class HarderLabPuzzle(Puzzle):
    def __init__(self):
        super().__init__("challenge")

    def answer_is_correct(self, answer):
        if answer != self.correct_answer:
            raise PlayerDeadException("NO!!! Wrong answer! You're going to GULAG, comrade!")
        else:
            self._is_solved = True
            return True
