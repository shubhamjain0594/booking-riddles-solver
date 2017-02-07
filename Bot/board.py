import copy
import sys

PLAYER1, PLAYER2, EMPTY, BLOCKED, BUG, WEAPON, CODE = [0, 1, 2, 3, 4, 5, 6]

S_PLAYER1, S_PLAYER2, S_EMPTY, S_BLOCKED, S_BUG, S_WEAPON, S_CODE = ['0', '1', '.', 'x', 'E', 'W', 'C']

CHARTABLE = [(PLAYER1, S_PLAYER1), (PLAYER2, S_PLAYER2), (EMPTY, S_EMPTY), (BLOCKED, S_BLOCKED), (BUG, S_BUG), (WEAPON, S_WEAPON), (CODE, S_CODE)]

DIRS = [
    ((-1, 0), "up"),
    ((0, 1), "right"),
    ((1, 0), "down"),
    ((0, -1), "left")
]

class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell = [[[EMPTY] for col in range (0, width)] for row in range(0, height)]

    def parse_cell_char(self, players, row, col, char):
        result = -1
        if char == S_PLAYER1:
            players[0].row = row;
            players[0].col = col;
        elif char == S_PLAYER2:
            players[1].row = row;
            players[1].col = col;
        for (i, symbol) in CHARTABLE:
            if symbol == char:
                result = i
                break
        return result

    def parse_cell(self, players, row, col, data):
        cell = []
        for char in data:
            cell.append(self.parse_cell_char(players, row, col, char))
        return cell

    def parse(self, players, data):
        cells = data.split(',')
        #sys.stderr.write("num cells in field = " + str(len(cells)) + "\n")
        #sys.stderr.write("width = " + str(self.width) + "\n")
        #sys.stderr.write("height = " + str(self.height) + "\n")
        col = 0
        row = 0
        for cell in cells:
            if (col >= self.width):
                col = 0
                row +=1
            self.cell[row][col] = self.parse_cell(players, row, col, cell)
            col += 1

    def in_bounds (self, row, col):
        return row > 0 and col > 0 and col < self.width and row < self.height

    def legal_moves(self, my_id, players):
        my_player = players[my_id]
        #sys.stderr.write("my player loc = " + str(my_player.row) + ", " + str(my_player.col) + "\n")
        result = []
        for ((o_row, o_col), order) in DIRS:
            t_row = my_player.row + o_row
            t_col = my_player.col + o_col
            #sys.stderr.write("Testing " + str(t_row) + ", " + str(t_col) + "\n")
            if (self.in_bounds(t_row, t_col)) and (not BLOCKED in self.cell[t_row][t_col]):
                #sys.stderr.write("legal\n")
                result.append(((o_row, o_col), order))
            else:
                pass
                #sys.stderr.write("illegal\n")
        return result

    def output_cell(self, cell):
        done = False
        for (i, symbol) in CHARTABLE:
            if i in cell:
                if not done:
                    sys.stderr.write(symbol)
                done = True
                break
        if not done:
            sys.stderr.write("!")
            done = True
                

    def output(self):
        for row in self.cell:
            sys.stderr.write("\n")
            for cell in row:
                self.output_cell(cell)
        sys.stderr.write("\n")
        sys.stderr.flush()

