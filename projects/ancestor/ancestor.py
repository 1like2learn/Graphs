mapOfInput = {
    1: {"child": [3], "parent": [10]},
    2: {"child": [3], "parent": []},
    3: {"child": [6], "parent": [1,2]},
    4: {"child": [5,8], "parent": []},
    5: {"child": [6,7], "parent": [4]},
    6: {"child": [], "parent": [3,5]},
    7: {"child": [], "parent": [5]},
    8: {"child": [9], "parent": []},
    9: {"child": [], "parent": [9]},
    10: {"child": [1], "parent": []},
    11: {"child": [8], "parent": []},
}
exampleInput = [[1, 3], [2, 3], [3, 6], [4, 5], [4, 8], [5, 6], [5, 7], [8, 9], [10, 1], [11, 8]]
def earliest_ancestor(ancestors, starting_node):
    ancestorsReverse = {}
    """
    Take every node in ancestors and store it's first index as 
    a value in a list and the second index as the key. If the second 
    index already exists in the new dict add the first index to the array.
    """
    for node in ancestors:
        if node[1] in ancestorsReverse:
            ancestorsReverse[node[1]]["parent"].append(node[0])
        else:
            ancestorsReverse[node[1]] = {"parent": [node[0]], "score": 0}

    """
    Loop until nodeToCheck is empty and all the possible paths have been
    taken. Every loop remove the last node from the list. Loop through the
    current node's parents, add their current score to their child's 
    score plus one and add them to the list. For every parent check if it 
    has parents and compare to highest score. If the parent has a higher 
    score make it the highest score node and update it's value. If the 
    scores are equal pick the one with the lower value. 4 and 11 have the 
    same score but choose 4.
    """
    nodeToCheck = [starting_node]
    highestScore = {"node": "", "value": 0}
    while len(nodeToCheck) > 0:
        # In case the node has no parents
        if nodeToCheck[-1] not in ancestorsReverse:
            return -1
        node = ancestorsReverse[nodeToCheck.pop(-1)]

        for parent in node["parent"]:

            if parent not in ancestorsReverse:

                if node["score"] + 1 > highestScore["value"]:
                    highestScore["node"] = parent
                    highestScore["value"] = node["score"] + 1
                if node["score"] + 1 == highestScore["value"] and parent < highestScore["node"]:
                    highestScore["node"] = parent
                    highestScore["value"] = node["score"] + 1

                continue

            parentNode = ancestorsReverse[parent]
            parentNode["score"] += 1 + node["score"]
            nodeToCheck.append(parent)

    # Return node with the highest score
    return highestScore["node"]

print(earliest_ancestor(exampleInput, 6))
print(earliest_ancestor(exampleInput, 2))
print(earliest_ancestor(exampleInput, 4))
print(earliest_ancestor(exampleInput, 1))
print(earliest_ancestor(exampleInput, 8))

