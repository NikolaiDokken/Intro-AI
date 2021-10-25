import numpy as np
from Node import Node

def get_path(current_node):
    """
    Gets path from stat node to current node
    :param current_node: Node that we are to find path to from start
    :return: array of positions from start node to end node
    """
    path = []
    current = current_node

    # Loop through parents until start node is reached
    while current is not None:
        path.append(current.position)
        current = current.parent
    
    # Return path from start to finish
    return path[::-1]

def astar(map_obj, moving_goal=False):
    """
    A* algorithm

    :param map_obj: A map object representing the 2D grid map
    :param start: Position of start node
    :param end: Position of end node
    :return: Array of positions from start node to end node
    """

    # Initilize start and end node
    start_node = Node(None, map_obj.start_pos)
    end_node = Node(None, map_obj.goal_pos)

    # List of nodes that we yet have to expand
    open = []

    # List of expanded nodes
    closed = []

    open.append(start_node)

    # Defined a maximum number of iterations to avoid infinite loop
    outer_iterations = 0
    max_iterations = len(map_obj.int_map // 2) ** 10

    # Define all possible moves from current position
    moves = [
        [1, 0], # go down
        [-1, 0],# go up
        [0, 1], # go right
        [0, -1] # go left
    ]

    rows, cols = np.shape(map_obj.int_map)

    while len(open) > 0:
        
        outer_iterations += 1

        current_node = open[0]
        current_index = 0

        # Find node in open with the lowest f value to expand
        for index, node in enumerate(open):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # If algorithm is stuck, give error message and return path to current node
        if outer_iterations > max_iterations:
            print("Giving up on pathfinding, too many iterations")
            return get_path(current_node)

        # Remove the node that is to be expanded from open, and add it to closed
        open.pop(current_index)
        closed.append(current_node)

        # Is goal reached?
        if current_node == end_node:
            return get_path(current_node)

        # Get current_node's children
        children = []
        for new_position in moves:
            
            # Position of child
            node_position = [current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]]

            # Check boundaries
            if (node_position[0] < 0 or node_position[0] > rows-1) or (node_position[1] < 0 or node_position[1] > cols-1):
                continue

            # If node is wall, don't add to children
            if map_obj.int_map[node_position[0]][node_position[1]] == -1:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)
        
        for child in children:
            
            # Don't update g or h values if child is already visited
            if child in closed:
                continue
            
            # Update child's path-cost to start_node
            child.g = current_node.g + map_obj.int_map[child.position[0]][child.position[1]]

            # Heuristic cost calculated using Manhattan distance
            child.h = abs(end_node.position[0] - child.position[0]) + abs(end_node.position[1] - child.position[1])

            child.f = child.g + child.h

            # If child is in open list with lower g, don't add to open
            if child in open and child.g > open[open.index(child)].g:
                continue

            # Add child to open list
            open.append(child)
        
        if moving_goal:
            map_obj.tick()
            if end_node.position != map_obj.goal_pos:
                end_node = Node(None, map_obj.goal_pos)

