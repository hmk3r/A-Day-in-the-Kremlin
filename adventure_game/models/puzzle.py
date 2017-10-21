from adventure_game.models.contracts import IPuzzle


class Puzzle(IPuzzle):
    def __init__(self, puzzle_id, name, description, possible_answers, correct_answer, reward=None):
        self.id = puzzle_id
        self.name = name
        self.description = description
        self.possible_answers = possible_answers
        self.correct_answer = correct_answer
        self.reward = reward

    def answer_is_correct(self, answer):
        self.is_solved = answer == self.correct_answer
        return self.is_solved
