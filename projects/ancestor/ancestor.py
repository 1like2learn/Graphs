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
    # for node in ancestors:
    #     if "child" in tree[node[0]]:
    #         tree[node[0]]["child"].append(node[1])
    #     else:
    #         tree[node[0]]["child"] = node[1]
    #     if "parent" in tree[node[1]]:
    #         tree[node[0]]["parent"].append(node[0])
    #     else:
    #         tree[node[1]]["parent"] = node[0]
    # node = tree[starting_node]
    # stackToCheck = [node]
    # while len(stackToCheck) > 0:
    #     node = stackToCheck.pop(-1)
    #     for parent in stackToCheck[node]["parent"]:
    #         stackToCheck.append(parent)
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
    score plus one and add them to the list. For every parent turn it into a node and grab it's grandparents
    """
    nodeToCheck = [starting_node]
    highestScore = {"node": "", "value": 0}
    while len(nodeToCheck) > 0:
        print('nodeToCheck: ', nodeToCheck)
        node = ancestorsReverse[nodeToCheck.pop(-1)]
        print('node: ', node)
        for parent in node["parent"]:
            if parent not in ancestorsReverse:
                if node["score"] + 1 > highestScore["value"]:
                    highestScore["node"] = parent
                continue
            parentNode = ancestorsReverse[parent]
            parentNode["score"] += 1 + node["score"]
            # for grandparent in parentNode:
            #     if grandparent not in ancestorsReverse and parentNode["score"] + 1 > highestScore["value"]:
            #         highestScore["node"] = parentNode["parent"]
            nodeToCheck.append(parent)
    return highestScore["node"]

print(earliest_ancestor(exampleInput, 6))

