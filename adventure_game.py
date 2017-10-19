#!/usr/bin/python3

from adventure_game.models import Item
from adventure_game.models import Player
import adventure_game.constants as constants
from adventure_game.factories import RoomFactory

rooms = {}
items = {}
player = None


def print_separator():
    print()


def normalise_input(user_input):
    words = user_input.lower().split(" ")
    return words


def setup_game():
    for x in range(0, 6):
        new_item = Item(str(x), "Item {0}".format(x), "Cool item number {0}".format(x))
        items[str(x)] = new_item

    room_factory = RoomFactory(constants)

    library_exits_scheme = \
        room_factory.get_room_exits(
            east_room_id="restaurant",
            west_room_id="lab",
            north_room_id="workshop")

    library = \
        room_factory.get_room(
            "library",
            "Cardiff library",
            "You can find books here",
            library_exits_scheme,
            [items["0"], items["2"]])
    rooms[library.id] = library

    restaurant_exits_scheme = room_factory.get_room_exits(west_room_id="library")
    restaurant = room_factory.get_room("restaurant", "The Restaurant", "Drink and eat", restaurant_exits_scheme)
    rooms[restaurant.id] = restaurant

    lab_exits_scheme = room_factory.get_room_exits(east_room_id="library")
    lab = room_factory.get_room("lab", "PC Lab", "A room full of computers", lab_exits_scheme, [items["1"]])
    rooms[lab.id] = lab

    workshop_exits_scheme = room_factory.get_room_exits(south_room_id="library")
    workshop = \
        room_factory.get_room("workshop", "The Workshop", "vrum vrum", workshop_exits_scheme, [items["3"], items["5"]])
    rooms[workshop.id] = workshop

    office = \
        room_factory.get_room("office", "The main office", "You are trapped. There are no exits", items=[items["4"]])
    rooms[office.id] = office

    global player
    player = Player("John Doe", library)


def get_next_room(room_id):
    if room_id not in rooms:
        return None

    return rooms[room_id]


def execute_go(direction):

    if direction not in player.location.exits:
        print_separator()
        print("Invalid direction")

    next_room = get_next_room(player.location.exits[direction])

    if not next_room:
        print_separator()
        print("You can't go there")
        return

    player.move_to(next_room)


def execute_take(item_id):
    if item_id not in items:
        print_separator()
        print("No such thing exists")
        return
    item = items[item_id]

    if item not in player.location.items:
        print_separator()
        print("There's no such item in the room")
        return

    player.location.items.remove(item)
    player.take_item(item)


def execute_drop(item_id):
    if item_id not in items:
        print_separator()
        print("No such thing exists")
        return
    item = items[item_id]

    if item not in player.inventory:
        print_separator()
        print("You don't have this item")
        return

    player.inventory.remove(item)
    player.location.items.append(item)


def execute_command(command):

    if 0 == len(command):
        return

    if command[0] == constants.COMMAND_GO:
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == constants.COMMAND_TAKE:
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == constants.COMMAND_DROP:
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    else:
        print("This makes no sense.")


def print_current_game_info():
    print_separator()
    print(player.location.name.upper())
    print_separator()

    print(player.location.description)
    print_separator()

    print("You can:")
    for item in player.location.items:
        print("Type TAKE {0} to take {1}".format(item.id, item.name))

    for i in player.inventory:
        print("Type DROP {0} to drop {1}".format(i.id, i.name))

    for direction in player.location.exits:
        if not player.location.exits[direction]:
            continue

        room_exit = rooms[player.location.exits[direction]]

        print("Type GO {0} to go to {1}".format(direction.upper(), room_exit.name))


def main():
    while True:
        print_current_game_info()

        user_input = input("What would you ike to do? ")
        command = normalise_input(user_input)
        execute_command(command)


if __name__ == "__main__":
    setup_game()
    main()

