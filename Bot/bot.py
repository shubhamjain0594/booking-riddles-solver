import random
import sys
import queue
import Bot.points as points

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
        self.my_id = self.game.my_botid
        self.opponent_id = 1 - self.my_id
        self.numrows = self.game.field_height
        self.numcols = self.game.field_width

    def do_turn(self):
        self.get_opponents_distance_to_snippets()
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            move = self.get_best_move(legal)
            if move is None:
                (_, chosen) = random.choice(legal)
            else:
                (_, chosen) = move
            self.game.issue_order(chosen)
        # sys.stderr.flush()

    def get_best_move(self, legal_moves):
        self.opponent_dist = self.get_opponents_distance_to_snippets()
        # print(self.opponent_dist)
        best_score = -2000
        best_move = None
        for move in legal_moves:
            score = self.get_scores_move(move)
            if score > best_score:
                best_move = move
                best_score = score

        # print(moves_value)
        return best_move

    def get_score_helper(self, dist, vals):
        if dist > vals[3]:
            return 0
        score = vals[0] + max(dist - 1, 0) * vals[1]
        if vals[1] < 0:
            score = max(score, vals[2])
        else:
            score = min(score, vals[2])
        return score

    def get_scores_move(self, move):
        done_vert = self.get_graph(None)  # tracking parents of each node
        dist_vert = self.get_graph(0)  # tracking distances from start pos
        field = self.game.field.cell

        start_pos = self.game.field.bot_pos[self.my_id]
        done_vert[start_pos[0]][start_pos[1]] = (-1, -1)
        done_vert[start_pos[0]][start_pos[1]] = 0
        current_pos = (start_pos[0] + move[0][0], start_pos[1] + move[0][1])
        dist_vert[current_pos[0]][current_pos[1]] = dist_vert[start_pos[0]][start_pos[1]] + 1

        q = queue.Queue()
        q.put(current_pos)
        while not q.empty():
            front = q.get()
            cell = field[front[0]][front[1]]

            for direc in DIRS:
                row_num = front[0] + direc[0][0]
                col_num = front[1] + direc[0][1]

                if row_num < 0 or row_num >= self.numrows or col_num < 0 or col_num >= self.numcols:
                    continue
                elif done_vert[row_num][col_num] is not None:
                    continue
                elif BLOCKED in cell:
                    continue
                else:
                    done_vert[row_num][col_num] = front
                    dist_vert[row_num][col_num] = dist_vert[front[0]][front[1]] + 1
                    q.put((row_num, col_num))

        score = 0
        for bug in self.game.field.bugs:
            score += self.get_score_helper(dist_vert[bug[0]][bug[1]], points.POINTS[0])

        for snippet in self.game.field.snippets:
            if snippet not in self.opponent_dist or (dist_vert[snippet[0]][snippet[1]] + self.my_id <= self.opponent_dist[snippet] + self.opponent_id):
                score += self.get_score_helper(dist_vert[snippet[0]][snippet[1]],
                                               points.POINTS[1])
            else:
                score += self.get_score_helper(dist_vert[snippet[0]][snippet[1]],
                                              points.POINTS[1]) / 2.0

        for weapon in self.game.field.weapons:
            if weapon not in self.opponent_dist or (dist_vert[weapon[0]][weapon[1]] + self.my_id <= self.opponent_dist[weapon] + self.opponent_id):
                score += self.get_score_helper(dist_vert[weapon[0]][weapon[1]],
                                               points.POINTS[2])
            else:
                score += self.get_score_helper(dist_vert[weapon[0]][weapon[1]],
                                               points.POINTS[2]) / 2.0

        if self.game.players[self.opponent_id].has_weapon and not self.game.players[self.my_id].has_weapon:
            pos = self.game.field.bot_pos[self.opponent_id]
            score += self.get_score_helper(dist_vert[pos[0]][pos[1]], points.POINTS[3])

        if not self.game.players[self.opponent_id].has_weapon and self.game.players[self.my_id].has_weapon:
            pos = self.game.field.bot_pos[self.opponent_id]
            score += self.get_score_helper(dist_vert[pos[0]][pos[1]], points.POINTS[4])

        return score

    def get_graph(self, val):
        # define graph
        graph = [None] * self.numrows
        for i in range(self.numrows):
            graph[i] = [val] * self.numcols

        return graph

    def get_opponents_distance_to_snippets(self):
        """
        Checks the snippets closest to and in same path of opponent's closest
        snippet and returns that distances
        """
        start_pos = self.game.field.bot_pos[self.opponent_id]
        done_vert = self.get_graph(None)
        field = self.game.field.cell

        q = queue.Queue()
        q.put(start_pos)
        snippet_pos = None
        done_vert[start_pos[0]][start_pos[1]] = (-1, -1)

        while not q.empty():
            front = q.get()
            cell = field[front[0]][front[1]]
            if CODE in cell or WEAPON in cell:
                snippet_pos = front
                break
            for direc in DIRS:
                row_num = front[0] + direc[0][0]
                col_num = front[1] + direc[0][1]

                if row_num < 0 or row_num >= self.numrows or col_num < 0 or col_num >= self.numcols:
                    continue
                elif done_vert[row_num][col_num] is not None:
                    continue
                elif BLOCKED in cell:
                    continue
                else:
                    done_vert[row_num][col_num] = front
                    q.put((row_num, col_num))

        if not snippet_pos:
            return {}

        current_pos = snippet_pos
        vert_seen = self.get_graph(None)
        length = 0
        while current_pos != (-1, -1):
            vert_seen[current_pos[0]][current_pos[1]] = done_vert[current_pos[0]][current_pos[1]]
            current_pos = done_vert[current_pos[0]][current_pos[1]]
            length += 1

        vert_seen[snippet_pos[0]][snippet_pos[1]] = length
        snippet_dist = {}
        snippet_dist[snippet_pos] = length

        return snippet_dist

        # q = queue.Queue()
        # q.put(snippet_pos)
        # while q.empty():
        #     front = q.get()
        #     cell = field[front[0]][front[1]]
        #     if CODE in cell or WEAPON in cell:
        #         snippet_pos = front
        #         snippet_dist[snippet_pos] = vert_seen[front[0]][front[1]]
        #     for direc in DIRS:
        #         row_num = front[0] + direc[0][0]
        #         col_num = front[1] + direc[0][1]
        #
        #         if row_num < 0 or row_num >= numrows or col_num < 0 or col_num >= numcols:
        #             continue
        #         elif vert_seen[row_num][col_num] is not None:
        #             continue
        #         elif BLOCKED in cell:
        #             continue
        #         else:
        #             vert_seen[row_num][col_num] = vert_seen[front[0]][front[1]] + 1
        #             q.put((row_num, col_num))
        #
        # return snippet_dist

    def select_least_distance_move(self):
        """
        Select the move with least distance
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
                if EMPTY in cell or (BUG in cell and self.game.players[my_id].has_weapon) or  (self.game.other_botid in cell and not self.game.players[self.game.other_botid].has_weapon):
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
