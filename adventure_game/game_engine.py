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

                user_input = self.reader.read_input("What would you like to do? >")
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
            self.writer.write("Thanks for playing! You're welcome back anytime!")
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
            self.writer.write("Invalid direction")
            return

        next_room = self.get_next_room(self.player.location.exits[direction])

        if not next_room:
            self.writer.write_separator()
            self.writer.write("You can't go there")
            return

        self.player.move_to(next_room)

    def execute_look(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write("This item does not exist")
            return
        item = self.items[item_id]

        if (item in self.player.inventory) or (item in self.player.location.items):
            self.writer.write_separator()
            self.writer.write(item.description)
        else:
            self.writer.write_separator()
            self.writer.write("You can't inspect this item right now.")

    def execute_take(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write("No such thing exists")
            return
        item = self.items[item_id]

        if item not in self.player.location.items:
            self.writer.write_separator()
            self.writer.write("There's no such item in the room")
            return

        self.player.location.items.remove(item)
        self.player.take_item(item)

    def execute_drop(self, item_id):
        if item_id not in self.items:
            self.writer.write_separator()
            self.writer.write("No such thing exists")
            return
        item = self.items[item_id]

        if item not in self.player.inventory:
            self.writer.write_separator()
            self.writer.write("You don't have this item")
            return

        self.player.inventory.remove(item)
        self.player.location.items.append(item)

    def execute_solve(self, puzzle_id):
        if puzzle_id not in self.puzzles:
            self.writer.write_separator()
            self.writer.write("There's no such puzzle")
            return
        puzzle = self.puzzles[puzzle_id]

        if puzzle not in self.player.location.puzzles:
            self.writer.write_separator()
            self.writer.write("You can't solve this puzzle right now")
            return

        if puzzle.is_solved:
            self.writer.write_separator()
            self.writer.write("You've already solved this puzzle")
            return

        if not set(puzzle.required_items).issubset(self.player.inventory):
            self.writer.write_separator()
            self.writer.write("You don't have the required items to complete this puzzle!")
            self.writer.write("Think logically and you'll find out what you need.")
            return

        self.writer.write_separator()
        self.writer.write(puzzle.name.upper())

        self.writer.write_separator()
        if puzzle.is_annoying:
            self.writer.write_slowly(puzzle.description)
        else:
            self.writer.write(puzzle.description)

        if puzzle.reward:
            self.writer.write("You'll get {0} if you solve this correctly".format(puzzle.reward.name))

        self.writer.write_separator()
        self.writer.write("Possible answers:")
        for possible_answer in puzzle.possible_answers:
            self.writer.write(possible_answer)

        answer_raw = self.reader.read_input("Answer: ")
        answer = self.parser.normalise_string(answer_raw)
        if puzzle.answer_is_correct(answer):
            self.writer.write_separator()
            self.writer.write("Correct answer!")
            if puzzle.win_message:
                self.writer.write(puzzle.win_message)
            if puzzle.reward:
                self.player.take_item(puzzle.reward)
            if puzzle.takes_items:
                for used_item in puzzle.required_items:
                    self.player.drop_item(used_item)
        else:
            self.writer.write("Wrong answer!")

    def execute_suicide(self):
        happiness = self.items["happiness"]
        if happiness in self.player.inventory:
            self.writer.write("You are still happy! Why would you even consider doing that?")
            return

        raise PlayerDeadException("You've killed yourself, but your spirit is not free. Instead of ending up in front of the Heaven's door, your spirit was transferred to GULAG!")

    def execute_command(self, command):

        if 0 == len(command):
            return

        if command[0] == constants.COMMAND_GO:
            if len(command) > 1:
                self.execute_go(command[1])
            else:
                self.writer.write("Go where?")

        elif command[0] == constants.COMMAND_TAKE:
            if len(command) > 1:
                self.execute_take(command[1])
            else:
                self.writer.write("Take what?")

        elif command[0] == constants.COMMAND_DROP:
            if len(command) > 1:
                self.execute_drop(command[1])
            else:
                self.writer.write("Drop what?")

        elif command[0] == constants.COMMAND_SOLVE:
            if len(command) > 1:
                self.execute_solve(command[1])
            else:
                self.writer.write("Solve what?")
        
        elif command[0] == constants.COMMAND_LOOK:
            if len(command) > 1:
                self.execute_look(command[1])
            else:
                self.writer.write("Look at what?")
        elif command[0] == constants.COMMAND_SUICIDE:
            self.execute_suicide()
        elif command[0] == constants.COMMAND_RESTART:
            self.restart()
        else:
            self.writer.write("This makes no sense.")

    def stringify_items(self, items):
        separator = ", "
        item_names = []
        for item in items:
            item_names.append(item.name)

        return separator.join(item_names)

    def print_current_game_info(self):
        self.writer.write_separator()
        self.writer.write(self.player.location.name.upper())
        self.writer.write_separator()

        self.writer.write(self.player.location.description)
        self.writer.write_separator()

        if len(self.player.location.items) > 0:
            self.writer.write("In this room you can find {0}.".format(self.stringify_items(self.player.location.items)))

        if len(self.player.inventory) > 0:
            self.writer.write("You have {0}.".format(self.stringify_items(self.player.inventory)))
        else:
            self.writer.write("You don't have anything.")

        self.writer.write_separator()

        self.writer.write("You can:")

        for puzzle in self.player.location.puzzles:
            if not puzzle.is_solved:
                self.writer.write("Type SOLVE {0} to {1}.".format(puzzle.id.upper(), puzzle.name))

        self.writer.write("Type LOOK AT {ITEM} to inspect an item in your inventory or room.")
        for item in self.player.location.items:
            self.writer.write("Type TAKE {0} to take {1}.".format(item.id.upper(), item.name))

        for i in self.player.inventory:
            self.writer.write("Type DROP {0} to drop {1}.".format(i.id.upper(), i.name))

        for direction in self.player.location.exits:
            if not self.player.location.exits[direction]:
                continue

            room_exit = self.rooms[self.player.location.exits[direction]]

            self.writer.write("Type GO {0} to go to {1}.".format(direction.upper(), room_exit.name))

        happiness = self.items["happiness"]
        if happiness not in self.player.inventory:
            print("Type SUICIDE to kill yourself and escape this communist hell once and for all.")

    def print_welcome_screen(self):
        message = """

A DAY IN THE KREMLIN

Hello and welcome to our game! 

Are you tired of capitalism? Have you ever wanted to experience communism? 
This game will teleport you back to the time of Stalin, placing you in the centre of the USSR - Kremlin.
The rules are simple really, just don't die. You are Stalin's aid and he has a few jobs for you to do... check the list 
to keep track and don't upset Stalin or it's the Gulag for you. 
You can type 'RESTART' in order to restart the whole game if you get stuck.
You can exit the game by pressing Ctrl + C.
If you're desperate you can leave your happiness behind and a special cheatcode will unlock for you!

Good luck!
        
"""
        self.writer.clear()
        self.writer.write(message)
        self.reader.read_input("Press any key to continue...")
        self.writer.clear()

    def print_game_over_screen(self, cause_of_death):
        gulag = """
           _____   _    _   _                    _____   _ 
          / ____| | |  | | | |          /\      / ____| | |
         | |  __  | |  | | | |         /  \    | |  __  | |
         | | |_ | | |  | | | |        / /\ \   | | |_ | | |
         | |__| | | |__| | | |____   / ____ \  | |__| | |_|
          \_____|  \____/  |______| /_/    \_\  \_____| (_)
                                                           
                                                           
"""
        self.writer.clear()
        self.writer.write(gulag)
        self.writer.write(cause_of_death)
        self.writer.write("Better luck next time!")
        self.reader.read_input("Press any key to exit...")

    def print_game_won_screen(self):
        flag = """
                         '
                        '@'
                       '@@@'
                      '@@@@@'
               '@@@@@@@@@@@@@@@@@@@'
                 '@@@@@@@@@@@@@@@'
                   '@@@@@@@@@@@'
                  '@@@@@@'@@@@@@'
                  @@@@'     '@@@@
                 ;@'           '@;
                   _   _   _   _
                  (   (   (   |_)
                   ~   ~   ~  |

        """

        message = """
Congratulations, comrade! 
You have managed to survive the day! I hope you've enjoyed, because you will be doing it all over again tomorrow. 
Good Luck xoxo
"""
        self.writer.clear()
        self.writer.write(flag)
        self.writer.write(message)
        self.reader.read_input("Press any key to exit...")


