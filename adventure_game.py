#!/usr/bin/python3

from adventure_game.models import Room
from adventure_game.models import Item
from adventure_game.models import RoomExitsScheme
from adventure_game.models import Player
import adventure_game.constants as constants

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

    library_exits_scheme = \
        RoomExitsScheme(east_room_id="restaurant", west_room_id="lab", north_room_id="workshop", south_room_id="office")

    library = \
        Room("library", "Cardiff library", "You can find books here", library_exits_scheme, [items["0"], items["2"]])
    rooms[library.id] = library

    restaurant_exits_scheme = RoomExitsScheme(west_room_id="library")
    restaurant = Room("restaurant", "The Restaurant", "Drink and eat", restaurant_exits_scheme)
    rooms[restaurant.id] = restaurant

    lab_exits_scheme = RoomExitsScheme(east_room_id="library")
    lab = Room("lab", "PC Lab", "A room full of computers", lab_exits_scheme, [items["1"]])
    rooms[lab.id] = lab

    workshop_exits_scheme = RoomExitsScheme(south_room_id="library")
    workshop = Room("workshop", "The Workshop", "vrum vrum", workshop_exits_scheme, [items["3"], items["5"]])
    rooms[workshop.id] = workshop

    office = Room("office", "The main office", "You are trapped. There are no exits", items=[items["4"]])
    rooms[office.id] = office

    global player
    player = Player("John Doe", library)


def get_next_room(room_id):
    if room_id not in rooms:
        return None

    return rooms[room_id]


def execute_go(direction):

    if direction == constants.DIRECTION_EAST:
        next_room = get_next_room(player.location.exits.east_room_id)
    elif direction == constants.DIRECTION_WEST:
        next_room = get_next_room(player.location.exits.west_room_id)
    elif direction == constants.DIRECTION_NORTH:
        next_room = get_next_room(player.location.exits.north_room_id)
    elif direction == constants.DIRECTION_SOUTH:
        next_room = get_next_room(player.location.exits.south_room_id)
    else:
        print("Uhm what?")
        return

    if not next_room:
        print("You can't go there")
        return

    player.move_to(next_room)


def execute_take(item_id):
    item = items[item_id]
    player.location.items.remove(item)
    player.take_item(item)


def execute_drop(item_id):
    item = items[item_id]
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

    print("Try wondering")


def main():
    while True:
        print_current_game_info()

        user_input = input("What would you ike to do? ")
        command = normalise_input(user_input)
        execute_command(command)


if __name__ == "__main__":
    setup_game()
    main()

