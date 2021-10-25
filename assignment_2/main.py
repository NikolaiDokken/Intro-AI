from Map import Map_Obj
from A_star import astar

# Instatiate map based on task, replace task number with 1,2,3 or 4
map_obj = Map_Obj(task=5)

# Use astar to get path from start to goal node
path = astar(map_obj, moving_goal=True)

# Draw path for each position in path
for pos in path:
    if pos != map_obj.start_pos and pos != map_obj.goal_pos:
        map_obj.set_cell_value(pos, None)

# Show map with path
map_obj.show_map()