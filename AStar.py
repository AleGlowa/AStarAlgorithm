from graphics import *
from math import sqrt
from random import random

WIDTH = 600
HEIGHT = WIDTH + 20
squares_amount_on_every_row_and_column = int(input('Enter amount of squares for every row and column: '))
squares_width = WIDTH // squares_amount_on_every_row_and_column
button_posx, button_posy = WIDTH / 2, 10

start_pos = tuple(int(x.strip()) for x in input('Enter start point position: ').split())
end_pos = tuple(int(x.strip()) for x in input('Enter end point position: ').split())

class Node:
    def __init__(self, pos):
        self.weight = 0
        self.heuristic = 0
        self.distance = 0
        self.f_cost = 0
        self.pos = pos
        self.is_obstacle = True if random() < 0.2 else False  # chance for obstacle
        self.neighbours = []
        self.parent = None

    def __str__(self):
        return 'Node in ' + str(self.pos)

    def __repr__(self):
        return 'Node in ' + str(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

    def add_neighbours(self):
        (x, y) = self.pos
        if x > 1:
            self.neighbours.append(Node((x - 1, y)))
            self.weight = 1
        if x < squares_amount_on_every_row_and_column:
            self.neighbours.append(Node((x + 1, y)))
            self.weight = 1
        if y > 1:
            self.neighbours.append(Node((x, y - 1)))
            self.weight = 1
        if y < squares_amount_on_every_row_and_column:
            self.neighbours.append(Node((x, y + 1)))
            self.weight = 1
        if x < squares_amount_on_every_row_and_column and y < squares_amount_on_every_row_and_column:
            self.neighbours.append(Node((x + 1, y + 1)))
            self.weight = sqrt(2)
        if x < squares_amount_on_every_row_and_column and y > 1:
            self.neighbours.append(Node((x + 1, y - 1)))
            self.weight = sqrt(2)
        if x > 1 and y < squares_amount_on_every_row_and_column:
            self.neighbours.append(Node((x - 1, y + 1)))
            self.weight = sqrt(2)
        if x > 1 and y > 1:
            self.neighbours.append(Node((x - 1, y - 1)))
            self.weight = sqrt(2)

class Button:
    def __init__(self, win, center, width, height, label):
        w, h = width / 2, height / 2
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.label = Text(center, label)
        self.rect.draw(win)
        self.label.draw(win)

    def clicked(self, p):
        return self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax


blocks = [[] for i in range(squares_amount_on_every_row_and_column)]
nodes = [[] for i in range(squares_amount_on_every_row_and_column)]
open_nodes = []
closed_nodes = []
path = []
start = None
end = None

win = GraphWin('A* algorithm', WIDTH, HEIGHT)
button = Button(win, Point(button_posx, button_posy), 90, 20, 'Search!')

# GRID CONSTRUCTOR
i, j = 0, 0
for cut in range(squares_width, WIDTH + 1, squares_width):
    j += 1
    for cut2 in range(squares_width + 20, HEIGHT + 1, squares_width):
        i += 1
        point1 = Point(cut, cut2)
        point2 = Point(cut - squares_width, cut2 - squares_width)
        block = Rectangle(point1, point2)
        block.draw(win)
        blocks[j - 1].append(block)
        if start_pos[0] == i and start_pos[1] == j:
            nodes[j - 1].append(Node((j, i)))
            start = nodes[j - 1][i - 1]
            blocks[j - 1][i - 1].setFill('green')
        elif end_pos[0] == i and end_pos[1] == j:
            nodes[j - 1].append(Node((j, i)))
            end = nodes[j - 1][i - 1]
            blocks[j - 1][i - 1].setFill('red')
        else:
            nodes[j - 1].append(Node((j, i)))
            if nodes[j - 1][i - 1].is_obstacle:
                blocks[j - 1][i - 1].setFill('black')
    i = 0

if start.is_obstacle:
    start.is_obstacle = False
    blocks[start.pos[0] - 1][start.pos[1] - 1].setFill('green')
if end.is_obstacle:
    end.is_obstacle = False
    blocks[end.pos[0] - 1][end.pos[1] - 1].setFill('red')

for i in nodes:
    for j in i:
        j.add_neighbours()

def search(start, end):
    current = start
    open_nodes.append(current)

    while open_nodes:
        current = min(open_nodes, key=lambda o: o.f_cost)

        if current == end:
            temp = current
            path.append(temp)
            blocks[temp.pos[0] - 1][temp.pos[1] - 1].setFill('red')
            while temp.parent:
                path.append(temp.parent)
                temp = temp.parent
                blocks[temp.pos[0] - 1][temp.pos[1] - 1].setFill('red')
            return path

        open_nodes.remove(current)
        closed_nodes.append(current)
        blocks[current.pos[0] - 1][current.pos[1] - 1].setFill('orange')

        for n in current.neighbours:
            if n not in closed_nodes and not n.is_obstacle:
                temp_distance = current.distance + n.weight
                new_path = False

                if n in open_nodes:
                    if temp_distance < n.distance:
                        n.distance = temp_distance
                        new_path = True
                else:
                    n.distance = temp_distance
                    new_path = True
                    open_nodes.append(n)
                    blocks[n.pos[0] - 1][n.pos[1] - 1].setFill('yellow')

                if new_path:
                    n.heuristic = sqrt((n.pos[0] - end.pos[0])**2 + (n.pos[1] - end.pos[1])**2)
                    n.f_cost = n.distance + n.heuristic
                    n.parent = current

    raise ValueError('There is no path to the destination!')


point = win.getMouse()
if button.clicked(point):
    path = search(start, end)

print(path)
win.getMouse()
win.close()
