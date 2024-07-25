import sys
import math
import copy
import numpy as np
import time

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h = [7, 7]
p1, p2, p3, p4, p5, p6, p7 = [649, 1869, 2289, 3507, 5423, 6687, 7926]
min_piece_price = min(p1, p2, p3, p4, p5, p6, p7)
room_input = ['#######',
              '#.....#',
              '#.....#',
              '#..#..#',
              '#.....#',
              '#.....#',
              '#######']
min_cost = np.inf
pos_list = []
pieces_used = ['', 0]
node_counter = 0

def input_to_tab(r_input: list[str]):
    room = []
    for line in r_input:
        row = []
        for char in line:
            if char == '.':
                row.append(0)
            elif char == '#':
                row.append(1)
            else:
                raise RuntimeError
        room.append(row)
    return room

i = {'price': p1,
     0:[[1, 1, 1, 1]],
     1:[[1],
        [1],
        [1],
        [1]]}
o = {'price': p2,
     0: [[1, 1],
         [1, 1]]}
t = {'price': p3,
     0: [[0, 1, 0],
         [1, 1, 1]],
     1: [[1, 1, 1],
         [0, 1, 0]],
     2: [[0, 1],
         [1, 1],
         [0, 1]],
     3: [[1, 0],
         [1, 1],
         [1, 0]],}
l = {'price': p4,
     0: [[1, 1, 1],
         [1, 0, 0]],
     1: [[0, 0, 1],
         [1, 1, 1]],
     2: [[1, 0],
         [1, 0],
         [1, 1]],
     3: [[1, 1],
         [0, 1],
         [0, 1]],}
j = {'price': p5,
     0: [[1, 0, 0],
         [1, 1, 1]],
     1: [[1, 1, 1],
         [0, 0, 1]],
     2: [[0, 1],
         [0, 1],
         [1, 1]],
     3: [[1, 1],
         [1, 0],
         [1, 0]],}
z = {'price': p6,
     0: [[1, 1, 0],
         [0, 1, 1]],
     1: [[0, 1],
         [1, 1],
         [1, 0]],}
s = {'price': p7,
     0: [[0, 1, 1],
         [1, 1, 0]],
     1: [[1, 0],
         [1, 1],
         [0, 1]],}

room_tab = input_to_tab(room_input)

def fit(room:list[list[int]], coord:tuple[int, int], piece:dict, rot:int):
    '''checks if piece[rot] fits in room at coord'''
    if coord[0]+ len(piece[rot]) > h or coord[1]+ len(piece[rot][0]) > w:
        return False
    else:
        for i in range(len(piece[rot])):
            for j in range(len(piece[rot][i])):
                if piece[rot][i][j] and room[coord[0]+i][coord[1]+j]:
                    return False
        return True

def place(room:list[list[int]], coord:tuple[int, int], piece:dict, rot:int):
    '''modifies room to place piece[rot] at coord without checking if it fits and returns price'''
    for i in range(len(piece[rot])):
        for j in range(len(piece[rot][i])):
            if piece[rot][i][j]:
                room[coord[0]+i][coord[1]+j] = 1
    return piece['price']

def pieces():
    return sorted([o, i, t, l, j, z, s], key=lambda piece: piece['price'])

class Node:

    def __init__(self, room=room_tab, piece=None, cost=0, position={}) -> None:
        self.parent = None
        self.child = []
        self.room = room
        self.piece = piece
        self.cost = cost
        self.position = position

def legal_places(room:list[list[int]]):
    leg_places = []
    for piece in pieces():
        for rot in range(len(piece.keys()) - 1):
            for i in range(h):
                for j in range(w):
                    if fit(room, (i, j), piece, rot):
                        leg_places.append(((i, j), piece, rot))
    return leg_places

def is_full(room:list[list[int]]):
    for line in room:
        for ele in line:
            if ele == 0:
                return False
    return True

def nb_pieces(node:Node):
    res = [0, 0, 0, 0, 0, 0, 0] # I O T L J Z S
    while node.piece != None:
        if node.piece == i:
            res[0] += 1
        elif node.piece == o:
            res[1] += 1
        elif node.piece == t:
            res[2] += 1
        elif node.piece == l:
            res[3] += 1
        elif node.piece == j:
            res[4] += 1
        elif node.piece == z:
            res[5] += 1
        elif node.piece == s:
            res[6] += 1
        else:
            raise RuntimeError
        node = node.parent
    str_res = ''
    for num in res:
        str_res += str(num) + ' '
    return str_res

def neighbours(coord:tuple[int,int]):
    '''Returns an array of neighbouring coordinates, of length 2 to 4.'''
    if coord[0] == 0:
        if coord[1] == 0:
            return [(0,1), (1,0)]
        elif coord[1] == w - 1:
            return [(0,w - 2), (1,w - 1)]
        else:
            return [(0, coord[1]-1),
                    (0, coord[1]+1),
                    (1, coord[1])]
    elif coord[0] == h - 1:
        if coord[1] == 0:
            return [(h - 1, 1), (h - 2, 0)]
        elif coord[1] == w - 1:
            return [(h - 1, w - 2), (h - 2, w - 1)]
        else:
            return [(h - 1, coord[1]-1),
                    (h - 1, coord[1]+1),
                    (h - 2, coord[1])]
    else:
        if coord[1] == 0:
            return [(coord[0]-1, 0), (coord[0]+1, 0), (coord[0], 1)]
        elif coord[1] == w - 1:
            return [(coord[0]-1, w - 1), (coord[0]+1, w - 1), (coord[0], w - 2)]
        else:
            return [(coord[0]-1, coord[1]),
                    (coord[0]+1, coord[1]),
                    (coord[0], coord[1]-1),
                    (coord[0], coord[1]+1)]

def _group_rec(coord, group_list:list, room):
    neighs = neighbours(coord)
    group_list.append(coord)
    for neighb in neighs:
        if (not(neighb in group_list)) and room[neighb[0]][neighb[1]] == 0:
            _group_rec(neighb, group_list, room)
    return

def group(room, coord):
    if room[coord[0]][coord[1]] == 0:
        group_list = []
        _group_rec(coord, group_list, room)
        return group_list
    else:
        raise RuntimeError #group should only be called on 0

def still_solvable(room:list[list[int]]):
    '''returns if every 0 group has a size divisible by 4'''
    visited = []
    for i in range(h):
        for j in range(w):
            if room[i][j] == 0 and not (i, j) in visited:
                grp = group(room, (i, j))
                if len(grp) % 4 != 0:
                    return False
                else:
                    for ele in grp:
                        visited.append(ele)
    return True

def fun_nb_pieces_to_solve(room:list[list[int]]):
    res = 0
    for line in room:
        res += line.count(0)
    return int(res/4)

nb_pieces_to_solve = fun_nb_pieces_to_solve(room_tab)

def parcours(node:Node, depth:int=0):
    global min_cost
    global pos_list
    global pieces_used
    #global node_counter #debug
    if not node.position in pos_list:
        #node_counter += 1 #debug
        leg_places = legal_places(node.room)
        if is_full(node.room):
            pos_list.append(node.position)
            if node.cost == min_cost:
                pieces_used[1] += 1
            elif node.cost < min_cost:
                min_cost = node.cost
                print(min_cost)
                pieces_used[0] = nb_pieces(node)
                pieces_used[1] = 1
        elif still_solvable(node.room) and len(leg_places) > 0 :
            for (coord, piece, rot) in leg_places:
                if node.cost + piece['price'] + (nb_pieces_to_solve - depth - 1)*min_piece_price <= min_cost:
                    new_room = copy.deepcopy(node.room)
                    place(new_room, coord, piece, rot)
                    new_node = Node(new_room, piece, node.cost + piece['price'], copy.deepcopy(node.position))
                    new_node.parent = node
                    new_node.position[coord] = (piece, rot)
                    node.child.append(new_node)
                    parcours(new_node, depth+1)
            pos_list.append(node.position)

def pavages(room:list[list[int]]):
    clock = time.time()
    node = Node(room, None, 0)
    parcours(node)
    print('time: ', time.time() - clock)
    return (min_cost/100, pieces_used[0], pieces_used[1])

print(pavages(room_tab))
print(len(pos_list))