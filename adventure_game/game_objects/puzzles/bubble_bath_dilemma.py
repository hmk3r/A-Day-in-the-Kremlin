from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException


class BubbleBathDilemma(Puzzle):
    def __init__(self):
        super().__init__("bubble_bath_dilemma")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True
        elif answer == "1":
            raise PlayerDeadException("STALIN HATES LEMONS. Bad choices lead to GULAG, comrade")
        else:
            return False
