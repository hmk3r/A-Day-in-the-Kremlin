from adventure_game.models import Puzzle
from adventure_game.exceptions import PlayerDeadException

NOT_ENOUGH_BUBBLES_ERROR_MESSAGE = "YOU'VE FAILED COMRADE! Stalin loves bubbles. Try with more next time. GULAG!"
FLOODED_BATH_ERROR_MESSAGE = "The whole room turns into a bathtub. Stalin rushes in with fury and sends you to GULAG!"


class BathtubDilemma(Puzzle):
    def __init__(self):
        super().__init__("bathtub_dilemma")

    def answer_is_correct(self, answer):
        correct_answer = int(self.correct_answer)
        try:
            answer = int(answer)
        except ValueError:
            return False

        if answer == correct_answer:
            self._is_solved = True
            return True

        if answer < correct_answer:
            raise PlayerDeadException(NOT_ENOUGH_BUBBLES_ERROR_MESSAGE)

        if answer > correct_answer:
            raise PlayerDeadException(FLOODED_BATH_ERROR_MESSAGE)

