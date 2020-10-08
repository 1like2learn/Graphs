from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
"""
Store Rooms visited in a set. Store paths in queue.
test_line:
visited = {0, 1, 2}
queue = [[0],[0,1],[0,1,2]]
traversal_path = ['n']
test_cross:
visited = {0, 1, 5, 3, 7, 2, 4, 6, 8}
queue = {[0]/,[0,1]/,[0,5]/,[0,3]/,[0,7]/,[0,1,2]/,[0,5,6]/,[0,3,4]/,[0,7,8]/}
"""
worldGraph = {player.current_room.get_id(): {}}
traversal_path = []
paths = [[player.current_room]]
# prevRoom = player.current_room
visited = []
"""
Loop through every path in paths, setting the current room to 
the latest room in the path. Find all the possible directions
to go. Append a new path to paths with all the possible new 
rooms added. This should find the shortest possible path to 
every node using a BFT.
"""
while len(paths) > 0:
    path = paths.pop(-1)
    curRoom = path[-1]
    # lastCommonNode = path[-2]
    # i = 1
    # while lastCommonRoom != prevRoom:
    #     roomExit = traversal_path[-i]
    #     if roomExit == 'n':
    #         reverseExit = 's'
    #     elif roomExit == 's':
    #         reverseExit = 'n'
    #     elif roomExit == 'e':
    #         reverseExit = 'w'
    #     elif roomExit == 'w':
    #         reverseExit = 'e'

    for roomExit in curRoom.get_exits():
        nextRoom = curRoom.get_room_in_direction(roomExit)
        nextRoomId = nextRoom.get_id()
        worldGraph[curRoom.get_id()][nextRoomId] = roomExit
        if nextRoomId not in worldGraph:
            visited.append(nextRoomId)
            paths.append(path + [nextRoom])
            worldGraph[nextRoomId] = {}

print('traversal_path: ', traversal_path)
print('worldGraph: ', worldGraph)
print('visited: ', visited)




# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
