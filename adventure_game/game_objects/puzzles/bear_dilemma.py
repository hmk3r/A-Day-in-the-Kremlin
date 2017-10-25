from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException

class BearDilemma(Puzzle):
    def __init__(self):
        super().__init__("bear_dilemma")

    def answer_is_correct(self, answer):
        correct_answer = int(self.correct_answer)
        try:
            answer = int(answer)
        except ValueError:
            return False

        if answer == correct_answer:
            self._is_solved = True
            return True

        if answer == 2 or answer == 3:
        	reason = """Kirillina runs over to you at full speed and jumps onto you as you try to run away.
With a single slash of her paw she separates your head from the rest of your body.
Blood oozes out onto the ground from where your neck and head once joined.
Kirillina seems to be pleased by the chaos she has caused and she happily strolls to the fountain to drink from vodka."""
        	raise PlayerDeadException(reason)
