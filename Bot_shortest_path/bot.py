import random
import sys
import queue

# sys.stderr = open('/home/users/shubham/projects/hack-man-engine/error', 'w+')
# sys.stderr = open('/home/users/shubham/projects/booking-riddle/error', 'w+')

PLAYER1, PLAYER2, EMPTY, BLOCKED, BUG, WEAPON, CODE = [0, 1, 2, 3, 4, 5, 6]

DIRS = [
    ((-1, 0), "up"),
    ((1, 0), "down"),
    ((0, 1), "right"),
    ((0, -1), "left")
]


class Bot:
    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            move = self.select_least_distance_move()
            if move is None:
                self.game.issue_order_pass()
            else:
                (_, chosen) = move
                self.game.issue_order(chosen)
        # sys.stderr.flush()

    def select_least_distance_move(self):
        """
        Selects the move with least distance
        """
        numrows = self.game.field_height
        numcols = self.game.field_width
        my_id = self.game.my_botid

        # define graph
        graph = [None] * numrows
        for i in range(numrows):
            graph[i] = [0] * numcols

        field = self.game.field.cell
        row_num = 0
        start = None
        # print(str(field))
        for row in field:
            # sys.stderr.write(str(field))
            # sys.stderr.flush()
            column_num = 0
            for cell in row:
                if EMPTY in cell or (BUG in cell and self.game.players[my_id].has_weapon) or (self.game.other_botid in cell and not self.game.players[self.game.other_botid].has_weapon):
                    graph[row_num][column_num] = 0
                elif WEAPON in cell or CODE in cell:
                    graph[row_num][column_num] = 2
                elif my_id in cell:
                    graph[row_num][column_num] = 1
                    start = (row_num, column_num)
                else:
                    # print(cell, row_num, column_num)
                    graph[row_num][column_num] = -1
                column_num += 1
            row_num += 1
        # print(graph)

        # bfs
        # sys.stderr.write(str(start) + '\n')
        # sys.stderr.flush()

        # track vertices done by storing their parent
        done_vert = [None] * numrows
        for i in range(numrows):
            done_vert[i] = [None] * numcols

        done_vert[start[0]][start[1]] = start
        q = queue.Queue()
        q.put(start)
        front = None
        while not q.empty():
            front = q.get()
            # sys.stderr.write(str(front) + '\n')
            # sys.stderr.flush()
            if graph[front[0]][front[1]] == 2:
                break
            elif graph[front[0]][front[1]] == -1:
                pass
            else:
                for direc in DIRS:
                    row_num = front[0] + direc[0][0]
                    col_num = front[1] + direc[0][1]
                    if row_num < 0 or row_num >= numrows or col_num < 0 or col_num >= numcols or graph[row_num][col_num] == -1:
                        continue
                    elif done_vert[row_num][col_num] is not None:
                        continue
                    else:
                        # sys.stderr.write(str(row_num) + str(col_num) + str(done_vert[row_num][col_num]) + '\n')
                        # sys.stderr.flush()
                        done_vert[row_num][col_num] = front
                        q.put((row_num, col_num))
            front = None
        sys.stderr.write(str(front) + '\n\n')
        sys.stderr.flush()
        if front is None:
            return None
        else:
            vert_from = done_vert[front[0]][front[1]]
            while not (vert_from[0] == start[0] and vert_from[1] == start[1]):
                front = vert_from
                vert_from = done_vert[front[0]][front[1]]

            row_dir = front[0] - start[0]
            col_dir = front[1] - start[1]
            for direc in DIRS:
                if row_dir == direc[0][0] and col_dir == direc[0][1]:
                    return direc
            return None
