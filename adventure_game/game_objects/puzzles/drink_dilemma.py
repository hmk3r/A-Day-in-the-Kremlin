from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException


class DrinkDilemma(Puzzle):
    def __init__(self):
        super().__init__("drink_dilemma")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True

        if answer == "2":
            reason = "YOU HAVE POURED STALIN'S SPECIAL DRINK!!! This is to be only poured after a great victory. This crime is so great that you and your enitre village are erased from all memory..."
            raise PlayerDeadException(reason)

        if answer == "3":
            reason = "Stalin is offended by your choice and sends you to a labour camp for 5 years, you die slowly of exhaustion..."
            raise PlayerDeadException(reason)

        return False
