from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()


player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def traversal(world, traversal_path):
    # construct your own traversal graph You start in room 0, which contains exits
    # ['n', 's', 'w', 'e']. Your starting graph should look something like this:

    # create an empty stack
    stack = Stack()

    # initialize current room
    initial = 0
    visited = {0: {}}
    reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    # function to return the direction that is available in a room
    def new_move(visited, current_room):
        exits = visited[current_room.id]
        # print('this is the exit', exits)

        # n, s, w, e && current room (direction) not in visited
        for direction in exits:
            if exits[direction] == '?' and current_room.get_room_in_direction(direction).id not in visited:
                # print('this is the next direction', direction)
                return direction
        return None

    # function that will find a new room
    def new_room(traversal_path, visited, current_room, stack, reverse):

        while True:
            # remove the last item of the stack
            next_move = stack.pop()
            # print('this is the next move', next_move)
            # add the next direction to the traversal
            traversal_path.append(next_move)
            # get the next room, call get_room_in_direction from room
            next_room = current_room.get_room_in_direction(next_move)
            # if it is visited, then return the id
            if '?' in visited[next_room.id].values():
                return next_room.id
            # set the current_room to the next room
            current_room = next_room

    # while visited has value and has rooms
    while len(visited) < len(world.rooms):
        # initiate current_room
        current_room = world.rooms[initial]
        # print(current_room)

        # if current room is not in visited then set it to ?
        # 0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        if current_room not in visited:
            for direction in current_room.get_exits():
                # print('this is the direction', direction)
                visited[current_room.id][direction] = '?'

        # for test in visited:
        #     print(test)

        next_move = new_move(visited, current_room)
        # print('this is the next move', next_move)

        # When you reach a dead-end (i.e. a room with no unexplored paths),
        # walk back to the nearest room that does contain an unexplored path.
        # if next move is equal to None then initiate new_room
        if next_move is None:
            # pop off the room and continue to next room
            initial = new_room(traversal_path, visited,
                               current_room, stack, reverse)

        else:
            # if it has a next move direction then append to traversal_path
            traversal_path.append(next_move)

            # set the next_room from the current_room
            next_room = current_room.get_room_in_direction(next_move)
            # print('this is the next room', next_room)

            # if next room is not in visited then set the next room to empty
            if next_room.id not in visited:
                visited[next_room.id] = {}

            # push the reverse direction in the stack
            stack.push(reverse[next_move])

            # next loop initial will be the next room id
            initial = next_room.id
            print('next room during the loop will be', initial)


traversal(world, traversal_path)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
