import matplotlib.pyplot as plt
import random
import math
from shapely.geometry import Point, Polygon, LineString

#Functions
def CheckIfValidPoint(point, node_to_connect):
    is_valid = True
    for obj in obstacles:
        if(obj.polygon.contains(Point(point[0], point[1]))):
            is_valid = False
            break

        for j in range(len(obj.coord_list) - 1):
            line_a = LineString([point, (node_to_connect.x_coord, node_to_connect.y_coord)])
            line_b = LineString([(obj.coord_list[j][0], obj.coord_list[j][1]), (obj.coord_list[j+1][0], obj.coord_list[j+1][1])])
            if(line_a.intersects(line_b)):
                is_valid = False
                break

    return is_valid

def AddPointToTree(rand_point, parent_index, min_node_dist, found_goal, search_radius):
    #RRT* things
    #Find neighbouring points within search_radius
    neighbouring_nodes = []
    for i in range(len(nodes_in_tree)):
        curr_dist = math.sqrt((rand_point[0] - nodes_in_tree[i].x_coord) ** 2 + (rand_point[1] - nodes_in_tree[i].y_coord) ** 2)
        if (curr_dist < search_radius):
            neighbouring_nodes.append(i)
    
    #Finding point to be joined which results in minimum cost
    min_cost = nodes_in_tree[parent_index].cost + min_node_dist
    for index in neighbouring_nodes:
        curr_dist = math.sqrt((rand_point[0] - nodes_in_tree[index].x_coord) ** 2 + (rand_point[1] - nodes_in_tree[index].y_coord) ** 2)
        curr_cost = nodes_in_tree[index].cost + curr_dist
        if(curr_cost < min_cost and CheckIfValidPoint(rand_point, nodes_in_tree[index])):
            min_cost = curr_cost
            parent_index = index

    nodes_in_tree.append(Nodes(rand_point[0], rand_point[1], parent_index, min_cost))

    #Finding if any modifications can be made to the existing tree with the adition of this new point
    for index in neighbouring_nodes:
        curr_dist = math.sqrt((rand_point[0] - nodes_in_tree[index].x_coord) ** 2 + (rand_point[1] - nodes_in_tree[index].y_coord) ** 2)
        modified_cost = min_cost + curr_dist
        if(modified_cost < nodes_in_tree[index].cost and CheckIfValidPoint(rand_point, nodes_in_tree[index])):
            nodes_in_tree[index].parent_index = len(nodes_in_tree) - 1
            nodes_in_tree[index].cost = modified_cost

    if(goal.polygon.contains(Point(rand_point[0], rand_point[1]))):
        found_goal = True

    return found_goal

def SamplePoint(counter, found_goal):
    rand_point = [random.uniform(0, bounds_of_plane[0]), random.uniform(0, bounds_of_plane[1])]

    if(counter % sample_goal == 0 and (not found_goal)):
        min_x, min_y, max_x, max_y = goal.polygon.bounds
        rand_point = [random.uniform(min_x, max_x), random.uniform(min_y, max_y)]
    
    return rand_point

def PlotTree(goal_index):
    for node in nodes_in_tree:
        plt.plot([node.x_coord, nodes_in_tree[node.parent_index].x_coord], [node.y_coord, nodes_in_tree[node.parent_index].y_coord], "r.-", markersize = 3, linewidth = 0.3)

    #Connecting Goal to the start point
    curr_index = goal_index
    while(curr_index != 0):
        parent_index = nodes_in_tree[curr_index].parent_index
        plt.plot([nodes_in_tree[curr_index].x_coord, nodes_in_tree[parent_index].x_coord], [nodes_in_tree[curr_index].y_coord, nodes_in_tree[parent_index].y_coord], 'b.-', markersize = 5, linewidth = 0.5)
        curr_index = parent_index

#Classes
class Figures:

    def __init__(self, coord_list):
        self.coord_list = coord_list
        self.polygon = Polygon(coord_list)

class Nodes:

    def __init__(self, x_coord, y_coord, parent_index, cost):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.parent_index = parent_index
        self.cost = cost

#Variables
point_of_origin = (5, 50) #start point
bounds_of_plane = (100, 100)
fixed_distance = 2
search_radius = 5
sample_goal = 5
points_to_sample = 5000

counter = 0
found_goal = False
goal_index = 0

obstacles = []
obstacles.append(Figures([[20, 100], [23, 100], [23, 30], [20, 30], [20, 100]]))
obstacles.append(Figures([[40, 70], [43, 70], [43, 0], [40, 0], [40, 70]]))
obstacles.append(Figures([[60, 100], [63, 100], [63, 30], [60,30], [60, 100]]))

goal = Figures([[80, 52], [84, 52], [84, 48], [80, 48], [80, 52]])

nodes_in_tree = []
nodes_in_tree.append(Nodes(point_of_origin[0], point_of_origin[1], 0, 0))

#draw obstacles
for obj in obstacles:
    xs, ys = zip(*obj.coord_list)
    plt.plot(xs, ys, "k-")

#draw goal
xs, ys = zip(*goal.coord_list)
plt.plot(xs, ys, "g-", linewidth = 2)


#Main loop of RRT
while ((not found_goal) or (counter < points_to_sample)):
    rand_point = SamplePoint(counter, found_goal)
    counter = counter + 1
    
    min_node_dist = math.sqrt((rand_point[0] - point_of_origin[0]) ** 2 + (rand_point[1] - point_of_origin[1]) ** 2)
    parent_index = 0
    
    for i in range(len(nodes_in_tree)):
        curr_dist = math.sqrt((rand_point[0] - nodes_in_tree[i].x_coord) ** 2 + (rand_point[1] - nodes_in_tree[i].y_coord) ** 2)
        if (curr_dist < min_node_dist):
            min_node_dist = curr_dist
            parent_index = i

    if(min_node_dist > fixed_distance):
        rand_point[0] = (((rand_point[0] - nodes_in_tree[parent_index].x_coord) * fixed_distance)/min_node_dist) + nodes_in_tree[parent_index].x_coord
        rand_point[1] =  (((rand_point[1] - nodes_in_tree[parent_index].y_coord) * fixed_distance)/min_node_dist) + nodes_in_tree[parent_index].y_coord
        min_node_dist = fixed_distance
        
    if(not CheckIfValidPoint(rand_point, nodes_in_tree[parent_index])):
        continue

    found_goal = AddPointToTree(rand_point, parent_index, min_node_dist, found_goal, search_radius)

    if(goal_index == 0 and found_goal):
        goal_index = len(nodes_in_tree) - 1

PlotTree(goal_index)

plt.show()