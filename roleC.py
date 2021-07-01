# -------------------------------------------------------
# Authors:  Sanyam Kadd, Ekamjot Singh
# --------------------------------------------------------

import math
import matplotlib.pyplot as plt
from matplotlib import style

b = 0
style.use("ggplot")

plt.xlabel("X Axis")
plt.ylabel("Y Axis")


# ----------------------------------------------------------------------------------------------------------------------
# --------------------------------------- HEURISTIC FUNCTION IMPLEMENTATION --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def hRC(x1, y1, x2, y2):
    x1 = 0.2 * x1
    x2 = 0.2 * x2
    x2 = x2 - 0.1
    y1 = 0.1 * y1
    y2 = 0.1 * y2
    y2 = y2 - 0.05
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------ METHOD USED TO DETERMINE THE COST OF EDGE ---------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def costOfEdge(n1, n2):
    nn1 = 0
    cost = 0
    if n1 - n2 == 1 or n1 - n2 == -1:
        m = max(n1, n2)
        if 0 < m <= columns:
            nn = m
        elif (rows + 1) * (columns + 1) - 1 - columns < m <= ((rows + 1) * (columns + 1)) - 1:
            nn = m - rows - columns
        else:
            nn = m - m // (columns + 1)
            nn1 = nn - columns
        if nn1 == 0:
            costs = dict_n[nn]
            if costs == 'E':
                cost = 1
            elif costs == 'Q':
                cost = 0
            elif costs == 'V':
                cost = 2
            elif costs == 'P':
                cost = 3
        else:
            g1 = 0
            g2 = 0
            costs = dict_n[nn]
            costs1 = dict_n[nn1]
            if costs == 'E':
                g1 = 1
            elif costs == 'Q':
                g1 = 0
            elif costs == 'V':
                g1 = 2
            elif costs == 'P':
                g1 = 3
            if costs1 == 'E':
                g2 = 1
            elif costs1 == 'Q':
                g2 = 0
            elif costs1 == 'V':
                g2 = 2
            elif costs1 == 'P':
                g2 = 3
            cost = float((g1 + g2) / 2)
    else:
        m = min(n1, n2)
        if m % (columns + 1) == columns:
            nn = m - m // (columns + 1)
            cost1 = dict_n[nn]
            if cost1 == 'E':
                cost = 1
            elif cost1 == 'V':
                cost = 2
            elif cost1 == 'P':
                cost = 3
            elif cost1 == 'Q':
                cost = 0
        elif (m + 1) % (columns + 1) == 1:
            nn = (m + 1) - (m + 1) // (columns + 1)
            cost1 = dict_n[nn]
            if cost1 == 'E':
                cost = 1
            elif cost1 == 'V':
                cost = 2
            elif cost1 == 'P':
                cost = 3
            elif cost1 == 'Q':
                cost = 0
        else:
            nn = m - m // (columns + 1)
            nn1 = nn + 1
            cost1 = str(dict_n[nn])
            cost2 = str(dict_n[nn1])
            g1 = 0
            g2 = 0
            if cost1 == 'E':
                g1 = 1
            elif cost1 == 'V':
                g1 = 2
            elif cost1 == 'P':
                g1 = 3
            elif cost1 == 'Q':
                g1 = 0
            if cost2 == 'E':
                g2 = 1
            elif cost2 == 'V':
                g2 = 2
            elif cost2 == 'P':
                g2 = 3
            elif cost2 == 'Q':
                g2 = 0
            cost = (g1 + g2) / 2
    return float(cost)


# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------- METHOD TO MAKE THE EDGES BETWEEN TWO PLAYGROUNDS INACCESSIBLE ---------------------------
# ----------------------------------------------------------------------------------------------------------------------


def deactivateEdgesBtwPG(impl1):
    for edges in restricted_edges:
        for nd in range(len(impl1[edges[0]])):
            if impl1[edges[0]][nd] == edges[1]:
                impl1[edges[0]][nd] = -1
        for nd in range(len(impl1[edges[1]])):
            if impl1[edges[1]][nd] == edges[0]:
                impl1[edges[1]][nd] = -1
    return impl1


def sort_open_list(o_list):
    for ix in o_list:
        lim = 0
        for jx in range(lim + 1, len(o_list)):
            if o_list[lim][2] > o_list[jx][2]:
                temp = o_list[lim]
                o_list[lim] = o_list[jx]
                o_list[jx] = temp
            lim += 1
    return o_list


def filter_path(array):
    cnd = array[len(array) - 1]
    for z in range(len(array) - 1, 0, -1):
        if array[z] == cnd:
            continue
        elif array[z] in impl[cnd]:
            cnd = array[z]
            continue
        else:
            del array[z]
    return array


def findEdgeBtwPG():
    # playground_node_array
    ret = []
    if len(playground_node_array) <= 1:
        return ret
    else:
        v = 0
        for cell in playground_node_array:
            v += 1
            for j_cell in range(v, len(playground_node_array)):
                temp = []
                for c1 in cell:
                    for c2 in playground_node_array[j_cell]:
                        if c1 == c2:
                            temp.append(c1)
                            break
                if len(temp) == 2:
                    ret.append(temp)
        return ret


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------- A STAR ALGORITHM IMPLEMENTATION --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def a_star(x1, y1, x2, y2):
    start_id = x1 + (columns + 1) * (rows - y1)
    start_id_arr = [start_id, 0, 0 + hRC(x1, y1, x2, y2), [start_id]]
    closed_list = []
    open_list = [start_id_arr]
    while len(open_list) > 0:
        open_list = sort_open_list(open_list)
        first_element = open_list[0]
        closed_list.append(first_element[0])
        del open_list[0]
        if isQuarantineAstar(first_element[0]):
            x_values = []
            y_values = []
            final_path = []
            for it in range(len(first_element[3]) - 1, -1, -1):
                final_path = [first_element[3][it]] + final_path
            if b == 0:
                if final_node_id == final_path[-1]:
                    pass
                elif final_node_id == final_path[-1] + 1 or final_node_id == final_path[-1] - columns - 1:
                    final_path += [final_node_id]
                elif final_node_id == final_path[-1] - columns:
                    final_path += [final_node_id - 1, final_node_id]
            pathstr = ""
            for loc in final_path:
                if loc == final_path[-1]:
                    pathstr += str(loc)
                else:
                    pathstr += str(loc)
                    pathstr += "->"
            for value in final_path:
                x_values.append(ret_x(value) * 0.2)
                y_values.append(ret_y(value) * 0.1)
            plt.plot(x_values, y_values)
            plt.annotate("Start Point", (ret_x(final_path[0]) * 0.2, ret_y(final_path[0]) * 0.1))
            plt.annotate("Goal Point", (ret_x(final_path[-1]) * 0.2, ret_y(final_path[-1]) * 0.1))
            print("*****************************")
            print(f"Cost: {first_element[1]}")
            print(f"Path: {pathstr}")
            print("*****************************")
            print("")
            print("Thank You for using our services!")
            plt.show()
        else:
            adj_arr = impl[first_element[0]]
            for t in adj_arr:
                if t != -1:
                    ffc = first_element[1] + costOfEdge(t, first_element[0])
                    if t not in closed_list and not in_open_list(t, open_list):
                        temp = first_element[3] + [t]
                        open_list.append([t, ffc, ffc + hRC(ret_x(t), ret_y(t), x2, y2), temp])


def in_open_list(t, ol):
    for iz in range(len(ol)):
        if t == ol[iz][0]:
            return True
    return False


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------- METHODS TO FIND X AND Y COORDINATES OF A NODE FROM NODE ID ---------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def ret_x(idd):
    x = idd % (columns + 1)
    return x


def ret_y(idd):
    y = rows - idd // (columns + 1)
    return y


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------- METHOD TO CHECK IF NODE ID IS PART OR USER ENTERED END COORDINATES -------------------------
# ----------------------------------------------------------------------------------------------------------------------


def isQuarantine(node_id):
    for iii in roleC_goal:
        if iii == node_id:
            return True
    return False


def isQuarantineAstar(node_id):
    for iii in role_C_goal_enter:
        if iii == node_id:
            return True
    return False


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- STARTING OF MAIN THREAD -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
print("!-------------------------------------!")
print("Welcome to the Covid-19 Map Simulation!")
print("!-------------------------------------!")
print("Enter the number of rows and columns to proceed:")
rows = int(input("Rows: "))
columns = int(input("Columns: "))
n = (rows + 1) * (columns + 1)

plt.ylim(-0.1, (rows * 0.1) + 0.1)
plt.xlim(-0.1, (columns * 0.2) + 0.1)

# implementing the map using a 2D array where each index corresponds to a node id and it stores an array of its
# adjacent node ids
impl = [-1] * n
q = 0
for i in range(n):
    j = 0
    yy = [-1] * 4
    if 0 <= i % (columns + 1) < columns:
        yy[j] = i + 1
        j += 1
    if 0 < i % (columns + 1) <= columns:
        yy[j] = i - 1
        j += 1
    if 0 <= (i - (columns + 1)) <= (n - 1) - (columns + 1):
        yy[j] = i - columns - 1
        j += 1
    if columns + 1 <= (i + (columns + 1)) <= n - 1:
        yy[j] = i + columns + 1
    impl[q] = yy
    q += 1

a = 1
map_grid = ""
h: int = rows
# printing the grid table according to the values entered by the user
# and alongside storing it in a string variable
dict_n = {}
for i in range(1, (rows * columns) + 1):
    dict_n[i] = 'E'

for i in range(0, rows):
    map_grid = map_grid + str(h)
    for j in range(0, columns):
        if j == 0:
            map_grid += str(f"{str('+').center(3, ' ')}- - - - ")
        else:
            map_grid += str(f"{str('+').center(3, ' ')}- - - - ")
        print(f"{str('+').center(3, ' ')}- - - -", end=" ")
        if j == columns - 1:
            print(f"{str('+').center(3, ' ')}", end=" ")
            map_grid += str(f"{str('+').center(3, ' ')} \n")
    h -= 1
    print("")
    map_grid = map_grid + " "
    for j in range(0, columns):
        s = str('C.' + str(a)).center(6, " ")
        print(f" |  {s}", end=" ")
        map_grid += str(f" |   {s}")
        a += 1
        if j == columns - 1:
            print(" |", end=" ")
            map_grid += str(" | \n")
    print("")
map_grid = map_grid + str(h)
for j in range(0, columns):
    print(f"{str('+').center(3, ' ')}- - - -", end=" ")
    map_grid += str(f"{str('+').center(3, ' ')}- - - - ")
    if j == columns - 1:
        print(f"{str('+').center(3, ' ')}", end=" ")
        map_grid += str(f"{str('+').center(3, ' ')} ")
print("")
print("* C. means cell number")
print(" ")
# Asking user to enter number of different places and cell number of those places and then printing the graph
# with user specified positions
roleC_goal = []
top_right_C_goal = []
roleC_2D = []
n_qp = input("How many quarantine cells are on the map?: ")
for i in range(int(n_qp)):
    sub = []
    a = int(input(f"Enter quarantine cell number {i + 1}: "))
    hh = (a * (columns + 1)) // columns
    if a % columns == 0:
        roleC_goal.append(hh - 1)
        sub.append(hh - 1)
        top_right_C_goal.append(hh - 1)
        roleC_goal.append(hh - 2)
        sub.append(hh - 2)
        roleC_goal.append(hh + columns - 1)
        sub.append(hh + columns - 1)
        roleC_goal.append(hh + columns)
        sub.append(hh + columns)
    else:
        roleC_goal.append(hh)
        sub.append(hh)
        top_right_C_goal.append(hh)
        sub.append(hh - 1)
        roleC_goal.append(hh - 1)
        sub.append(hh + columns)
        roleC_goal.append(hh + columns)
        sub.append(hh + columns + 1)
        roleC_goal.append(hh + columns + 1)
    dict_n[a] = 'Q'
    roleC_2D.append(sub)
    map_grid = map_grid.replace(str('C.' + str(a)), str("Q").center(len(str('C.' + str(a))), ' '), 1)

print("")
n_vs = input("How many vaccine spot cells are on the map?: ")
for i in range(int(n_vs)):
    a = int(input(f"Enter vaccine spot cell number {i + 1}: "))
    dict_n[a] = 'V'
    map_grid = map_grid.replace(str('C.' + str(a)), str("V").center(len(str('C.' + str(a))), ' '), 1)

print("")
n_pg = input("How many playground cells are on the map?: ")
playground_node_array = []
for i in range(int(n_pg)):
    a = int(input(f"Enter playground cell number {i + 1}: "))
    pg_cell = []
    hh = (a * (columns + 1)) // columns
    if a % columns == 0:
        pg_cell.append(hh - 1)
        pg_cell.append(hh - 2)
        pg_cell.append(hh + columns - 1)
        pg_cell.append(hh + columns)
    else:
        pg_cell.append(hh)
        pg_cell.append(hh - 1)
        pg_cell.append(hh + columns)
        pg_cell.append(hh + columns + 1)
    playground_node_array.append(pg_cell)
    dict_n[a] = 'P'
    map_grid = map_grid.replace(str('C.' + str(a)), str("P").center(len(str('C.' + str(a))), ' '), 1)

print("")

restricted_edges = findEdgeBtwPG()
impl = deactivateEdgesBtwPG(impl)

map_grid = map_grid.replace('C.', '  ')

for ii in range(len(map_grid)):
    if map_grid[ii].isdigit() and map_grid[ii + 2] == '|':
        map_grid = map_grid.replace(map_grid[ii], ' ', 1)

print("Now, the map looks like this (with cell ids, node ids, and user specified locations) : ")

k = 0
for i in range((rows + 1) * (columns + 1)):
    map_grid = map_grid.replace(" + ", str(str(k)).center(3, " "), 1)
    k += 1

print("")
print(map_grid)
print("", end=" ")
g = 0
print("", end=" ")
for i in range(columns + 1):
    print(f'{g}         ', end=" ")
    g += 1
print("")
print("* Q indicates Quarantine Place")
print("* V indicates Vaccine Spot")
print("* P indicates Playground")
print("* Cells with numbers indicate free cells and those numbers indicate cell id")
print("* Numbers on the vertices of each cell indicate node id")
# implementing graph for Role C using adjacency list


w = 0

# getting the start and end point point coordinates from the user and adjusting those coordinates so they correspond to
# the top right corner of the cell
print("")
print("Role C has to drive to the Quarantine Place")
print(f"According to the map shown above, enter the x and y coordinates of the start and goal points. \n")
print("")
sx = float(input("Enter x coordinate of start point: "))
if sx > columns:
    sx = float(input("Point outside of map range. Please see the map and enter within the dimensions of map: "))
sy = float(input("Enter y coordinate of start point: "))
if sy > rows:
    sy = float(input("Point outside of map range. Please see the map and enter within the dimensions of map: "))
gx = float(input("Enter x coordinate of goal point: "))
if gx > columns:
    gx = float(input("Point outside of map range. Please see the map and enter within the dimensions of map: "))
gy = float(input("Enter y coordinate of goal point: "))
if gy > rows:
    gy = float(input("Point outside of map range. Please see the map and enter within the dimensions of map: "))

sx = math.ceil(sx)
sy = math.ceil(sy)
gx = math.ceil(gx)
gy = math.ceil(gy)
if gy == 0:
    gy = 1
if sy == 0:
    sy = 1
if sx == 0:
    sx = 1
if gx == 0:
    gx = 1
print("")

print(
    f"According to Role C convention, your start coordinates are ({sx},{sy}) and your goal coordinates are ({gx},{gy}).")
print("")

print("")
print(map_grid)
print("", end=" ")
g = 0
print("", end=" ")
for i in range(columns + 1):
    print(f'{g}         ', end=" ")
    g += 1
print("")

initial_node_id = sx + (columns + 1) * (rows - sy)
final_node_id = gx + (columns + 1) * (rows - gy)

role_C_goal_enter = []
for sub in roleC_2D:
    if final_node_id in sub:
        role_C_goal_enter = sub
        final_node_id = sub[0]

if isQuarantine(initial_node_id):
    print("No path found because you are already in Quarantine Place. You don't need to move.")
elif isQuarantine(final_node_id):
    a_star(sx, sy, gx, gy)
else:
    b = 1
    print("You did not enter a Quarantine Place as your end point. However, since you are Corona Positive, we have "
          "suggested you the nearest Quarantine Place.")
    nearest = 10000000
    for idd in top_right_C_goal:
        if hRC(sx, sy, ret_x(idd), ret_y(idd)) < hRC(sx, sy, ret_x(nearest), ret_y(nearest)):
            nearest = idd
    role_C_goal_enter = [nearest, nearest - 1, nearest + columns + 1, nearest + columns]
    pas_id = nearest
    final_node_id = nearest
    a_star(sx, sy, ret_x(pas_id), ret_y(pas_id))
print("")
print("Thank You for using our services!")
