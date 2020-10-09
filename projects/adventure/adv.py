from room import Room
from player import Player
from world import World

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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
worldGraph = {player.current_room.get_id(): {"score": 0, "rooms": {}}}
traversal_path = []
queue = [[player.current_room]]
visited = []
"""
Loop through every path in paths, setting the current room to 
the latest room in the path. Find all the possible directions
to go. Append a new path to paths with all the possible new 
rooms added. This should find a path that will minimize backtracking.
"""
# while len(stack) > 0:
#     curRoom = stack.pop(-1)
#     for roomExit in curRoom.get_exits():
#         nextRoom = curRoom.get_room_in_direction(roomExit)
#         nextRoomId = nextRoom.get_id()
#         worldGraph[curRoom.get_id()][nextRoomId] = roomExit
#         if nextRoomId not in worldGraph:
#             stack.append(nextRoom)
#             worldGraph[nextRoomId] = {}
#     visited.append(curRoom.get_id())

for path in queue:
    curRoom = path[-1]
    for roomExit in curRoom.get_exits():
        nextRoom = curRoom.get_room_in_direction(roomExit)
        nextRoomId = nextRoom.get_id()
        worldGraph[curRoom.get_id()]["rooms"][nextRoomId] = roomExit
        if nextRoomId not in worldGraph:
            queue.append(path + [nextRoom])
            worldGraph[nextRoomId] = {"score": 1, "rooms": {}}
    visited.append(curRoom.get_id())

"""
This loop scores all the nodes in the list. The more branches a node has the higher the score.
the score of the node's branches is also added to it. The start of a long dead end should. 
have a high score. A short dead end should have a low score.
"""
i = -1
while abs(i) < len(queue):
    latestPath = queue[i]
    # print('latestPath: ', latestPath)
    if len(latestPath) > 2:
        worldGraph[latestPath[-2].get_id()]["score"] += worldGraph[latestPath[-1].get_id()]["score"]
    i -= 1


"""
Quick bfs to find the quickest route to the next node in the list
"""
def bfs(roomId):
    bfsVisited = set()
    bfsPaths = [[currentRoom]]
    for path in bfsPaths:
        vertex = path[-1]
        if vertex == roomId:
            return path
        if vertex not in bfsVisited:
            bfsVisited.add(vertex)
            for key in worldGraph[vertex]["rooms"].keys():
                bfsPaths.append(path + [key])

# print('worldGraph: ', worldGraph)
# print('visited: ', visited)
"""
For every id in visited we want to randomly go down the list 
of connected rooms until we reach one we've visited before or
if the room has only one connection. Every node we hit on that
traversal should be blacklisted so we won't try to get to it again.
"""
visited2 = set()
currentRoom = 0
stack = [0]
while len(stack) > 0:
    roomId = stack.pop(-1)
    if roomId in visited2:
        continue
    if currentRoom != roomId:
        prevRoom = None
        pathToTarget = bfs(roomId)
        for room in pathToTarget:
            if prevRoom == None:
                prevRoom = room
            else:
                traversal_path.append(worldGraph[prevRoom]["rooms"][room])
                prevRoom = room
        currentRoom = roomId
    # while the current room has more than one exit and hasn't been visited yet
    while len(worldGraph[roomId]["rooms"].keys()) > 1 and roomId not in visited2: 
        visited2.add(roomId)
        keysToSort = []
        for key in worldGraph[roomId]["rooms"].keys():
            if key not in visited2:
                keysToSort.append((key, worldGraph[key]["score"]))
        sortedKeys = sorted(keysToSort, key=lambda x: x[1], reverse = True)
        for key in sortedKeys:
            stack.append(key[0])
        if len(sortedKeys) > 0:
            roomId = sortedKeys[-1][0]
        # If all a rooms key's are visited end the loop
        else:
            break
            
        # appends direction from current room to the next room
        traversal_path.append(worldGraph[currentRoom]["rooms"][roomId])
        currentRoom = roomId # Current room becomes the next room
    visited2.add(roomId)






# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    # print('player.current_room: ', player.current_room)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
