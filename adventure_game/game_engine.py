from adventure_game.contracts import *
from adventure_game.exceptions import PlayerDeadException
import adventure_game.constants as constants


class GameEngine(IEngine):
    rooms = {}
    items = {}
    puzzles = {}
    player = None

    def __init__(self, writer: IWriter, reader: IReader, parser: IParser, objects_loader: IObjectsLoader):
        self.writer = writer
        self.reader = reader
        self.parser = parser
        self.objects_loader = objects_loader
        self.setup()

    def run(self):
        try:
            self.print_welcome_screen()
            while True:
                self.print_current_game_info()

                user_input = self.reader.read_input(constants.PROMPT_ENTER_COMMAND)
                command = self.parser.parse_command(user_input)
                self.writer.clear()
                self.execute_command(command)
                if self.check_win():
                    self.print_game_won_screen()
                    break
        except PlayerDeadException as player_dead_exception:
            self.print_game_over_screen(str(player_dead_exception))
        except KeyboardInterrupt:
            self.writer.write_separator()
            self.writer.write_separator()
            self.writer.write_info(constants.THANKS_FOR_PLAYING_MESSAGE)
            self.writer.write_separator()

    def setup(self):
        [self.items, self.puzzles, self.rooms, self.player] = self.objects_loader.load()

    def restart(self):
        [self.items, self.puzzles, self.rooms, self.player] = self.objects_loader.reload()

    def get_next_room(self, room_id):
        if room_id not in self.rooms:
            return None

        return self.rooms[room_id]

    def check_win(self):
        for room_id in self.rooms:
            if not self.rooms[room_id].check_if_completed():
                return False

        return True

    def execute_go(self, direction):

        if direction not in self.player.location.exits:
            self.writer.write_separator()
            self.writer.write_error(constants.INVALID_DIRECTION_ERROR_MESSAGE)
            return

        next_room = self.get_next_room(self.player.location.exits[direction])

        if not next_room:
            self.writer.write_separator()
            self.writer.write_error(constants.INVALID_NEXT_ROOM_ERROR_MESSAGE)
            return

        self.player.move_to(next_room)

    def execute_look(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write_error(constants.ITEM_DOES_NOT_EXIST_ERROR_MESSAGE)
            return
        item = self.items[item_id]

        if (item in self.player.inventory) or (item in self.player.location.items):
            self.writer.write_separator()
            self.writer.write(item.description)
        else:
            self.writer.write_separator()
            self.writer.write_error(constants.ITEM_UNAVAILABLE_FOR_INSPECTION_ERROR_MESSAGE)

    def execute_take(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write_error(constants.ITEM_DOES_NOT_EXIST_ERROR_MESSAGE)
            return
        item = self.items[item_id]

        if item not in self.player.location.items:
            self.writer.write_separator()
            self.writer.write_error(constants.ITEM_NOT_IN_ROOM_ERROR_MESSAGE)
            return

        if len(self.player.inventory) < constants.PLAYER_MAX_INVENTORY_CAPACITY:
            self.player.location.items.remove(item)
            self.player.take_item(item)
            self.writer.write_separator()
            self.writer.write_info(constants.ITEM_PICKED_UP.format(item.name))
        else:
            self.writer.write_separator()
            self.writer.write_error(constants.PLAYER_INVENTORY_FULL_ERROR_MESSAGE
                                    .format(constants.PLAYER_MAX_INVENTORY_CAPACITY))

    def execute_drop(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write_error(constants.ITEM_DOES_NOT_EXIST_ERROR_MESSAGE)
            return
        item = self.items[item_id]

        if item not in self.player.inventory:
            self.writer.write_separator()
            self.writer.write_error(constants.ITEM_NOT_IN_PLAYER_INVENTORY_ERROR_MESSAGE)
            return

        self.player.inventory.remove(item)
        self.player.location.items.append(item)
        self.writer.write_separator()
        self.writer.write_info(constants.ITEM_DROPPED_INFO.format(item.name))

    def execute_solve(self, puzzle_id):
        if puzzle_id not in self.puzzles:
            self.writer.write_separator()
            self.writer.write_error(constants.PUZZLE_DOES_NOT_EXIST_ERROR_MESSAGE)
            return
        puzzle = self.puzzles[puzzle_id]

        if puzzle not in self.player.location.puzzles:
            self.writer.write_separator()
            self.writer.write_error(constants.PUZZLE_NOT_AVAILABLE_ERROR_MESSAGE)
            return

        if puzzle.is_solved:
            self.writer.write_separator()
            self.writer.write_error(constants.PUZZLE_ALREADY_SOLVED_ERROR_MESSAGE)
            return

        if not set(puzzle.required_items).issubset(self.player.inventory):
            self.writer.write_separator()
            self.writer.write_error(constants.PUZZLE_NEEDS_MORE_ITEMS_ERROR_MESSAGE)
            return

        if puzzle.reward and (not puzzle.takes_items) \
                and (len(self.player.inventory) == constants.PLAYER_MAX_INVENTORY_CAPACITY):
            self.writer.write_separator()
            self.writer.write_error(constants.PUZZLE_PLAYER_INVENTORY_FULL_ERROR_MESSAGE)
            return

        self.writer.write_separator()
        self.writer.write_info(puzzle.name.upper())

        self.writer.write_separator()
        if puzzle.is_annoying:
            self.writer.write_slowly(puzzle.description)
        else:
            self.writer.write(puzzle.description)

        if puzzle.reward:
            self.writer.write(constants.PUZZLE_AWARD_INFO_MESSAGE.format(puzzle.reward.name))

        self.writer.write_separator()
        self.writer.write_info(constants.PUZZLE_POSSIBLE_ANSWERS_HEADER)
        for possible_answer in puzzle.possible_answers:
            self.writer.write(possible_answer)

        answer_raw = self.reader.read_input(constants.PUZZLE_ANSWER_PROMPT)
        answer = self.parser.normalise_string(answer_raw)
        if puzzle.answer_is_correct(answer):
            self.writer.write_separator()
            self.writer.write_success(constants.PUZZLE_CORRECT_ANSWER_MESSAGE)
            if puzzle.win_message:
                self.writer.write(puzzle.win_message)
            if puzzle.reward:
                self.player.take_item(puzzle.reward)
            if puzzle.takes_items:
                for used_item in puzzle.required_items:
                    self.player.drop_item(used_item)
        else:
            self.writer.write_separator()
            self.writer.write_error(constants.PUZZLE_WRONG_ANSWER_ERROR_MESSAGE)

    def execute_suicide(self):
        happiness = self.items[constants.ITEM_HAPPINESS_ID]
        if happiness in self.player.inventory:
            self.writer.write_error(constants.PLAYER_STILL_HAPPY_ERROR_MESSAGE)
            return

        raise PlayerDeadException(constants.PLAYER_SUICIDE_ERROR_MESSAGE)

    def execute_command(self, command):

        if 0 == len(command):
            return

        self.writer.write_separator()

        if command[0] == constants.COMMAND_GO:
            if len(command) > 1:
                self.execute_go(command[1])
            else:
                self.writer.write_error(constants.COMMAND_GO_UNCLEAR_ERROR_MESSAGE)

        elif command[0] == constants.COMMAND_TAKE:
            if len(command) > 1:
                self.execute_take(command[1])
            else:
                self.writer.write_error(constants.COMMAND_TAKE_UNCLEAR_ERROR_MESSAGE)

        elif command[0] == constants.COMMAND_DROP:
            if len(command) > 1:
                self.execute_drop(command[1])
            else:
                self.writer.write_error(constants.COMMAND_DROP_UNCLEAR_ERROR_MESSAGE)

        elif command[0] == constants.COMMAND_SOLVE:
            if len(command) > 1:
                self.execute_solve(command[1])
            else:
                self.writer.write_error(constants.COMMAND_SOLVE_UNCLEAR_ERROR_MESSAGE)
        
        elif command[0] == constants.COMMAND_LOOK:
            if len(command) > 1:
                self.execute_look(command[1])
            else:
                self.writer.write_error(constants.COMMAND_LOOK_UNCLEAR_ERROR_MESSAGE)
        elif command[0] == constants.COMMAND_SUICIDE:
            self.execute_suicide()
        elif command[0] == constants.COMMAND_RESTART:
            self.restart()
        else:
            self.writer.write_error(constants.COMMAND_INVALID_ERROR_MESSAGE)

    def stringify_items(self, items):
        separator = ", "
        item_names = []
        for item in items:
            item_names.append(item.name)

        return separator.join(item_names)

    def print_current_game_info(self):
        self.writer.write_separator()
        self.writer.write_info(self.player.location.name.upper())
        self.writer.write_separator()

        self.writer.write(self.player.location.description)
        self.writer.write_separator()

        if len(self.player.location.items) > 0:
            self.writer.write(constants.ROOM_ITEMS_INFO.format(self.stringify_items(self.player.location.items)))

        if len(self.player.inventory) > 0:
            self.writer.write(constants.PLAYER_INVENTORY_INFO.format(self.stringify_items(self.player.inventory)))
        else:
            self.writer.write(constants.PLAYER_INVENTORY_EMPTY_INFO_MESSAGE)

        self.writer.write_separator()

        self.writer.write_info(constants.COMMAND_AVAILABLE_COMMANDS_HEADER)

        for puzzle in self.player.location.puzzles:
            if not puzzle.is_solved:
                self.writer.write(constants.COMMAND_SOLVE_INFO.format(puzzle.id.upper(), puzzle.name))

        self.writer.write(constants.COMMAND_LOOK_INFO)
        for item in self.player.location.items:
            self.writer.write(constants.COMMAND_TAKE_INFO.format(item.id.upper(), item.name))

        for i in self.player.inventory:
            self.writer.write(constants.COMMAND_DROP_INFO.format(i.id.upper(), i.name))

        for direction in self.player.location.exits:
            if not self.player.location.exits[direction]:
                continue

            room_exit = self.rooms[self.player.location.exits[direction]]

            self.writer.write(constants.COMMAND_GO_INFO.format(direction.upper(), room_exit.name))

        happiness = self.items[constants.ITEM_HAPPINESS_ID]
        if happiness not in self.player.inventory:
            self.writer.write_error(constants.COMMAND_SUICIDE_INFO)

    def print_welcome_screen(self):
        self.writer.clear()
        self.writer.write(constants.WELCOME_SCREEN_MESSAGE)
        self.reader.read_input(constants.PRESS_ANY_KEY_TO_CONTINUE_PROMPT)
        self.writer.clear()

    def print_game_over_screen(self, cause_of_death):
        self.writer.clear()
        self.writer.write_error(constants.GULAG_LOGO)
        self.writer.write(cause_of_death)
        self.writer.write(constants.GAME_OVER_WISH_MESSAGE)
        self.reader.read_input(constants.PRESS_ANY_KEY_TO_EXIT_PROMPT)

    def print_game_won_screen(self):
        self.writer.clear()
        self.writer.write(constants.USSR_LOGO)
        self.writer.write(constants.GAME_WON_MESSAGE)
        self.reader.read_input(constants.PRESS_ANY_KEY_TO_EXIT_PROMPT)
