from adventure_game.models.contracts import IPuzzle


class Puzzle(IPuzzle):
    def __init__(self, puzzle_id, name=None, description=None, possible_answers=None, correct_answer=None, reward=None):
        self._id = puzzle_id
        self._name = name
        self._description = description
        self._possible_answers = possible_answers if possible_answers else []
        self._correct_answer = correct_answer
        self._reward = reward
        self._is_solved = False

    @property
    def is_solved(self):
        return self._is_solved

    @property
    def possible_answers(self):
        return self._possible_answers

    @property
    def description(self):
        return self._description

    @property
    def reward(self):
        return self._reward

    @reward.setter
    def reward(self, value):
        self._reward = value

    @property
    def correct_answer(self):
        return self._correct_answer

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def answer_is_correct(self, answer):
        self._is_solved = answer[0] == self.correct_answer
        return self.is_solved
