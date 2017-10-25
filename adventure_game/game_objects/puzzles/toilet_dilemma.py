from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException


class ToiletDilemma(Puzzle):
    def __init__(self):
        super().__init__("toilet_dilemma")

    def answer_is_correct(self, answer):
        if answer == self.correct_answer:
            self._is_solved = True
            return True

        if answer == "2":
            reason = """Well you blew it. You scratched the golden bog and you got sent to the Gulag. 
You will spend the rest of your days working generous 14 hour day’s until you freeze to death yay!
"""
            raise PlayerDeadException(reason)

        if answer == "1":
            reason = "You barely clean the toilet, stalin has you, and your family, pubically executed from treason."
            raise PlayerDeadException(reason)

        return False
