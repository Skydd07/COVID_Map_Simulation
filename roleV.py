# -------------------------------------------------------
# Authors:  Sanyam Kadd, Ekamjot Singh
# --------------------------------------------------------

from matplotlib import pyplot as plt
import math
from matplotlib import style

style.use("ggplot")

plt.xlabel("X Axis")
plt.ylabel("Y Axis")
b = 0


# This method is used to find cell id from the input node id given that node id is bottom left
def find_cell_id(node_id):  # bottom left node id only
    node_id -= columns
    return math.ceil((node_id * columns) / (columns + 1))


def ret_x(idd):
    x = idd % (columns + 1)
    return x


def ret_y(idd):
    y = rows - idd // (columns + 1)
    return y


# heuristic function for RoleV
# After getting the final cell id, it generates an array of manhattan distances of each cell from the final cell
def ManhattanDistanceofAllNodes(x2, y2):
    f_cid = find_cell_id(x2 + (columns + 1) * (rows - y2))
    hvals = [0] * rows * columns
    hvals[f_cid - 1] = 0
    current_row = math.ceil(f_cid / columns)
    current_col = f_cid % columns
    if current_col == 0:
        current_col = columns
    temp = 0
    for iu in range(1, current_col):
        temp += 1
        hvals[f_cid - iu - 1] = temp
    temp = 0
    ig = 0
    for iu in range(current_col + 1, columns + 1):
        temp += 1
        hvals[f_cid + ig] = temp
        ig += 1
    for iu in range(current_row - 1, 0, -1):
        for ju in range(1, columns + 1):
            hvals[(columns * (iu - 1)) + ju - 1] = 1 + hvals[columns + (columns * (iu - 1)) + ju - 1]
    for iu in range(current_row + 1, rows + 1):
        for ju in range(1, columns + 1):
            hvals[(columns * (iu - 1)) + ju - 1] = 1 + hvals[(columns * (iu - 1)) + ju - 1 - columns]
    return hvals


# This method is used to find the cost of edges from input node ids that are end-points of the edge
def cost_of_edges(n1, n2):
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
            costs = dict_n.get(nn)
            if costs == 'E':
                cost = 2
            elif costs == 'Q':
                cost = 3
            elif costs == 'V':
                cost = 0
            elif costs == 'P':
                cost = 1
        else:
            g1 = 0
            g2 = 0
            costs = dict_n.get(nn)
            costs1 = dict_n.get(nn1)
            if costs == 'E':
                g1 = 2
            elif costs == 'Q':
                g1 = 3
            elif costs == 'V':
                g1 = 0
            elif costs == 'P':
                g1 = 1
            if costs1 == 'E':
                g2 = 2
            elif costs1 == 'Q':
                g2 = 3
            elif costs1 == 'V':
                g2 = 0
            elif costs1 == 'P':
                g2 = 1
            cost = float((g1 + g2) / 2)
    elif n1 - n2 == columns + 1 or n1 - n2 == - columns - 1:
        m = min(n1, n2)
        if m % (columns + 1) == columns:
            nn = m - m // (columns + 1)
            cost1 = dict_n.get(nn)
            if cost1 == 'E':
                cost = 2
            elif cost1 == 'V':
                cost = 0
            elif cost1 == 'P':
                cost = 1
            elif cost1 == 'Q':
                cost = 3
        elif (m + 1) % (columns + 1) == 1:
            nn = (m + 1) - (m + 1) // (columns + 1)
            cost1 = dict_n.get(nn)
            if cost1 == 'E':
                cost = 2
            elif cost1 == 'V':
                cost = 0
            elif cost1 == 'P':
                cost = 1
            elif cost1 == 'Q':
                cost = 3
        else:
            nn = m - m // (columns + 1)
            nn1 = nn + 1
            cost1 = str(dict_n.get(nn))
            cost2 = str(dict_n.get(nn1))
            g1 = 0
            g2 = 0
            if cost1 == 'E':
                g1 = 2
            elif cost1 == 'V':
                g1 = 0
            elif cost1 == 'P':
                g1 = 1
            elif cost1 == 'Q':
                g1 = 3
            if cost2 == 'E':
                g2 = 2
            elif cost2 == 'V':
                g2 = 0
            elif cost2 == 'P':
                g2 = 1
            elif cost2 == 'Q':
                g2 = 3
            cost = (g1 + g2) / 2
    elif n1 - n2 == columns or n2 - n1 == columns:
        u = max(n1, n2)
        v = min(n1, n2)
        c1 = math.sqrt(cost_of_edges(u, u + 1) ** 2 + cost_of_edges(v, u + 1) ** 2)
        c2 = math.sqrt(cost_of_edges(v, v - 1) ** 2 + cost_of_edges(u, v - 1) ** 2)
        cost = max(c1, c2)
    elif n1 - n2 == columns + 2 or n2 - n1 == columns + 2:
        u = max(n1, n2)
        v = min(n1, n2)
        c1 = math.sqrt(cost_of_edges(u, u - 1) ** 2 + cost_of_edges(v, u - 1) ** 2)
        c2 = math.sqrt(cost_of_edges(v, v + 1) ** 2 + cost_of_edges(u, v + 1) ** 2)
        cost = max(c1, c2)
    return float(cost)


def isVaccine(node_id):
    for subb in roleV_goal:
        if node_id in subb:
            return True


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


def in_entered_goal(para):
    for sup in role_V_goal_enter:
        if para in sup:
            return True
    return False


def a_star_V(i_nd, f_nd):
    closed_list = []
    info_ar = [i_nd, 0, 0, [i_nd]]  # [node_id, cost, total cost, path]
    open_list = [info_ar]
    while len(open_list) > 0:
        open_list = sort_open_list(open_list)
        popped_el = open_list[0]
        closed_list.append(popped_el[0])
        del open_list[0]
        if isVaccine(popped_el[0]) and in_entered_goal(popped_el[0]):

            x_values = []
            y_values = []
            if b == 0:
                if final_node_id != popped_el[3][-1]:
                    popped_el[3] += [final_node_id]
            elif b == 1:
                for subr in roleV_goal:
                    if popped_el[0] in subr:
                        popped_el[3] += [subr[2]]
            pathstr = ""
            for value in popped_el[3]:
                x_values.append(ret_x(value)*0.2)
                y_values.append(ret_y(value)*0.1)
            plt.plot(x_values, y_values)
            for loc in popped_el[3]:
                if loc == popped_el[3][-1]:
                    pathstr += str(loc)
                else:
                    pathstr += str(loc)
                    pathstr += "->"
            print("************************")
            print(f"Cost: {popped_el[1]}")
            print(f"Path: {pathstr}")
            print("************************")
            print("Thank You for using our services!")
            plt.show()
            plt.annotate("Start Point", (ret_x(popped_el[3][0]) * 0.2, ret_y(popped_el[3][0]) * 0.1))
            plt.annotate("Goal Point", (ret_x(popped_el[3][-1]) * 0.2, ret_y(popped_el[3][-1]) * 0.1))
            return popped_el[3]
        else:
            adj_arr = implV[popped_el[0]]
            for t in adj_arr:
                if t != -1:
                    cost = popped_el[1] + cost_of_edges(popped_el[0], t)
                    if t not in closed_list and not in_open_list(t, open_list):
                        temp = popped_el[3] + [t]
                        open_list.append([t, cost, hvals_nodes[t] + cost, temp])


def in_open_list(t, ol):
    for iz in range(len(ol)):
        if t == ol[iz][0]:
            return True
    return False


print("!-------------------------------------!")
print("Welcome to the Covid-19 Map Simulation!")
print("!-------------------------------------!")
print("Enter the number of rows and columns to proceed:")
rows = int(input("Rows: "))
columns = int(input("Columns: "))
n = (rows + 1) * (columns + 1)

plt.ylim(-0.1, (rows*0.1) + 0.1)
plt.xlim(-0.1, (columns*0.2) + 0.1)

# implementing the map using a 2D array where each index corresponds to a node id and it stores an array of its
# adjacent node ids
implV = [-1] * n
q1 = 0
for i in range(n):
    j = 0
    yy = [-1] * 8
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
        j += 1
    if 0 <= i % (columns + 1) < columns and 0 <= (i - (columns + 1)) <= (n - 1) - (columns + 1):
        yy[j] = i - columns
        j += 1
    if 0 <= i % (columns + 1) < columns and columns + 1 <= (i + (columns + 1)) <= n - 1:
        yy[j] = i + columns + 2
        j += 1
    if 0 < i % (columns + 1) <= columns and 0 <= (i - (columns + 1)) <= (n - 1) - (columns + 1):
        yy[j] = i - columns - 2
        j += 1
    if 0 < i % (columns + 1) <= columns and columns + 1 <= (i + (columns + 1)) <= n - 1:
        yy[j] = i + columns
    implV[q1] = yy
    q1 += 1

# printing and storing the map as a string for later use
a = 1
map_grid = ""
h: int = rows

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

# creating a dictionary which stores cell id as the key and type of cell (playground, vaccine spot or quarantine place)
# as the value
dict_n = {}
for i in range(1, (rows * columns) + 1):
    dict_n[i] = 'E'

# getting from user the cells ids and editing the map according to those
n_qp = input("How many quarantine cells are on the map?: ")
for i in range(int(n_qp)):
    a = int(input(f"Enter quarantine cell number {i + 1}: "))
    dict_n[a] = 'Q'
    map_grid = map_grid.replace(str('C.' + str(a)), str("Q").center(len(str('C.' + str(a))), ' '), 1)
print("")
roleV_goal = []
n_vs = input("How many vaccine spot cells are on the map?: ")
for i in range(int(n_vs)):
    a = int(input(f"Enter vaccine spot cell number {i + 1}: "))
    sub = []
    hh = (a * (columns + 1)) // columns
    if a % columns == 0:
        sub.append(hh - 1)
        sub.append(hh - 2)
        sub.append(hh + columns - 1)
        sub.append(hh + columns)
    else:
        sub.append(hh)
        sub.append(hh - 1)
        sub.append(hh + columns)
        sub.append(hh + columns + 1)
    roleV_goal.append(sub)
    dict_n[a] = 'V'
    map_grid = map_grid.replace(str('C.' + str(a)), str("V").center(len(str('C.' + str(a))), ' '), 1)
print("")
n_pg = input("How many playground cells are on the map?: ")
for i in range(int(n_pg)):
    a = int(input(f"Enter playground cell number {i + 1}: "))
    dict_n[a] = 'P'
    map_grid = map_grid.replace(str('C.' + str(a)), str("P").center(len(str('C.' + str(a))), ' '), 1)
map_grid = map_grid.replace('C.', '  ')

# editing the map according to user entered cell ids
for ii in range(len(map_grid)):
    if map_grid[ii].isdigit() and map_grid[ii + 2] == '|':
        map_grid = map_grid.replace(map_grid[ii], ' ', 1)

k = 0
for i in range((rows + 1) * (columns + 1)):
    map_grid = map_grid.replace(" + ", str(str(k)).center(3, " "), 1)
    k += 1

# printing the map
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

# getting the start and end point point coordinates from the user and adjusting those coordinates so they correspond to
# the bottom left corner of the cell
print("")
print("Role V has to drive to the Vaccine Spot")
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

sx = math.floor(sx)
sy = math.floor(sy)
gx = math.floor(gx)
gy = math.floor(gy)
if gy == rows:
    gy -= 1
if sy == rows:
    sy -= 1
if sx == columns:
    sx -= 1
if gx == columns:
    gx -= 1
print("")

print(f"According to Role V convention, your start point is ({sx},{sy}) and your goal point is ({gx},{gy}).")
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


role_V_goal_enter = []
for sub in roleV_goal:
    if final_node_id in sub:
        role_V_goal_enter.append(sub)
        final_node_id = sub[2]
ar = ManhattanDistanceofAllNodes(gx, gy)

hvals_nodes = [-1] * (rows + 1) * (columns + 1)

for i in range(0, columns + 1):
    if i < columns:
        hvals_nodes[i] = ar[i]
    elif i % (columns + 1) == columns:
        hvals_nodes[i] = ar[i - 1]
j = columns
for i in range(columns + 1, (rows + 1) * (columns + 1)):
    if i % (columns + 1) == columns:
        hvals_nodes[i] = hvals_nodes[i - 1]
    else:
        j += 1
        hvals_nodes[i] = ar[j - (columns + 1)]

if isVaccine(initial_node_id):
    print("No Path Found because you are already in a Vaccine spot. So, you don't need to move.")
elif not isVaccine(final_node_id):
    b = 1
    role_V_goal_enter = roleV_goal
    print("You did not enter a Vaccine Spot as your end point. However, since you need to get vaccinated, we have "
          "suggested you the nearest Vaccine Spot.")
    a_star_V(initial_node_id, final_node_id)
else:
    a_star_V(initial_node_id, final_node_id)
