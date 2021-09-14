"""
chess map

potential map


state action log

adjusted reward chart

policy map

Sorted intersections list


Process: the Gomoku game passes a player (black/white) to the AI and the AI finds the best strategy for that player
and returns a coordinate to the game to place a piece. To save time, the AI needs to have all the intersections sorted
from best to worst for each player, based on its rules, and needs to update and resort the sorted list after each move
(instructed by the game).

FUNCTIONS:

    def check_horizontal(x: int, y: int): # takes a coordinate on the chessboard as parameter, returns an integer value
        ans: int = 0
        for i in

    update_potential() # if a chess is placed at any intersection on the board, the map is updated
"""


class Ai:
    board_size: int = 15
    learning_mode = False
    chess_map: list
    np_map_white: list
    np_map_black: list
    np_map: list
    potential_map: list
    strategy_map_white: list = []
    strategy_map_black: list = []
    strategy_map: list = [strategy_map_white, strategy_map_black]

    policy_map: list = [[]]

    def __init__(self, size, mode: bool):
        self.board_size = size
        self.learning_mode = mode
        # initialize chess map
        self.chess_map = [[-1 for col in range(self.board_size)] for row in range(self.board_size)]

        # initialize the potential map
        directions = 4
        self.potential_map = [[[0 for _ in range(directions)] for _ in range(self.board_size)] for _ in
                              range(self.board_size)]

        # initialize the neighboring pieces maps
        self.np_map_white = [[[0 for _ in range(directions)] for _ in range(self.board_size)] for _ in
                             range(self.board_size)]
        self.np_map_black = [[[0 for _ in range(directions)] for _ in range(self.board_size)] for _ in
                             range(self.board_size)]
        self.np_map = [self.np_map_white, self.np_map_black]

        # initialize strategy maps and update potential maps
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.update_potential((i, j))
                self.strategy_map_white.append((i, j))
                self.strategy_map_black.append((i, j))

    def reset(self):
        # reset chess map
        self.chess_map = [[-1 for col in range(self.board_size)] for row in range(self.board_size)]

        # reset the potential map
        directions = 4
        self.potential_map = [[[0 for _ in range(directions)] for _ in range(self.board_size)] for _ in
                              range(self.board_size)]

        # reset the neighboring pieces maps
        self.np_map_white = [[[0 for _ in range(directions)] for _ in range(self.board_size)] for _ in
                             range(self.board_size)]
        self.np_map_black = [[[0 for _ in range(directions)] for _ in range(self.board_size)] for _ in
                             range(self.board_size)]
        self.np_map = [self.np_map_white, self.np_map_black]

        # reset strategy maps and update potential maps
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.update_potential((i, j))
                self.strategy_map_white.append((i, j))
                self.strategy_map_black.append((i, j))

    def if_win(self, color: int, coordinate: tuple):
        row = coordinate[0]
        col = coordinate[1]
        if self.chess_map[row][col] == 1 - color:
            return False
        for direction in range(4):
            if self.np_map[color][row][col][direction] >= 5:
                return True
        return False

    # NEEDS OPTIMIZATION
    def update_np(self, coordinate: tuple):
        row = coordinate[0]
        col = coordinate[1]
        color = self.chess_map[row][col]
        unoccupied = -1

        # no need to update
        if color == unoccupied:
            return

        white = 0
        black = 1
        lo_bound = 0
        hi_bound = self.board_size - 1
        # directions
        vertical = 0
        diagonal_upper_right = 1
        horizontal = 2
        diagonal_bottom_right = 3

        # if the given color is either black or white
        if color == white or color == black:
            # change np values at the given position in the opposite color np_map to 0
            for direction in range(4):
                self.np_map[1 - color][row][col][direction] = 0

            consecutive = 0
            # starting and ending indices
            starting_row = 0
            ending_row = hi_bound
            # last row position, marking the start of several pieces in a row
            last = starting_row
            # last empty intersection position
            last_empty_i = starting_row
            # vertical direction traverse, for counting np
            for i in range(starting_row, ending_row + 1):
                # reset current intersection's np value
                self.np_map[color][i][col][vertical] = 0
                # current piece color
                current_color = self.chess_map[i][col]
                # count consecutive pieces in 'color'
                if current_color == color:
                    consecutive += 1

                if current_color != color or i == ending_row:
                    # update the np value of the last empty intersection
                    if self.chess_map[last_empty_i][col] == unoccupied:
                        self.np_map[color][last_empty_i][col][vertical] += consecutive
                    last_empty_i = i

                    # update np values so far
                    for r in range(last, i + 1):
                        self.np_map[color][r][col][vertical] = consecutive
                    # the i-th row iteration should be overwritten by the code below

                    if current_color == 1 - color:
                        self.np_map[color][i][col][vertical] = 0
                    # zero out consecutive counts
                    consecutive = 0
                    # update last row position
                    last = i + 1

            # reset consecutive counts
            consecutive = 0
            # upper_right_diagonal direction traverse, for counting np
            s = row + col
            if s < hi_bound:
                starting_row = lo_bound
                ending_row = s
            else:
                starting_row = s - hi_bound
                ending_row = hi_bound
            # set last row position to be the starting row position
            last = starting_row
            # last empty intersection position
            last_empty_i = starting_row
            for i in range(starting_row, ending_row + 1):
                # find current column
                j = s - i
                # current color
                current_color = self.chess_map[i][j]
                # reset current intersection's np value
                self.np_map[color][i][j][diagonal_upper_right] = 0
                # count consecutive pieces in 'color'
                if current_color == color:
                    consecutive += 1
                if current_color != color or i == ending_row:
                    # update the np value of the last empty intersection
                    last_empty_j = s - last_empty_i
                    if self.chess_map[last_empty_i][last_empty_j] == unoccupied:
                        self.np_map[color][last_empty_i][last_empty_j][diagonal_upper_right] += consecutive
                    last_empty_i = i
                    # update np values so far and zero out consecutive counts
                    for r in range(last, i + 1):
                        c = s - r
                        self.np_map[color][r][c][
                            diagonal_upper_right] = consecutive
                        # the i-th row iteration should be overwritten by the code below

                    if current_color == 1 - color:
                        self.np_map[color][i][j][diagonal_upper_right] = 0
                    # zero out consecutive counts
                    consecutive = 0
                    # update last row position
                    last = i + 1

            # reset consecutive counts
            consecutive = 0
            # set last column position to 0
            last = 0
            starting_col = 0
            ending_col = hi_bound
            # last empty intersection position
            last_empty_j = starting_col
            # horizontal direction traverse, for counting np
            for j in range(starting_col, ending_col + 1):
                # current color
                current_color = self.chess_map[row][j]
                # reset current intersection's np value
                self.np_map[color][row][j][horizontal] = 0
                # count consecutive pieces in 'color'
                if current_color == color:
                    consecutive += 1
                if current_color != color or j == ending_col:
                    # update the np value of the last empty intersection
                    if self.chess_map[row][last_empty_j] == unoccupied:
                        self.np_map[color][row][last_empty_j][horizontal] += consecutive
                    last_empty_j = j

                    # update np values so far and zero out consecutive counts
                    for c in range(last, j + 1):
                        self.np_map[color][row][c][
                            horizontal] = consecutive  # the i-th row iteration should be overwritten by the code below

                    if current_color == 1 - color:
                        self.np_map[color][row][j][horizontal] = 0
                    # zero out consecutive counts
                    consecutive = 0
                    # update last row position
                    last = j + 1

            # reset consecutive counts
            consecutive = 0
            # bottom_right_diagonal direction traverse, for counting np
            s = row - col
            if row > col:
                starting_row = row - col
                ending_row = hi_bound
            else:
                starting_row = lo_bound
                ending_row = hi_bound - col + row
            # set last row position to be the starting row position
            last = starting_row
            # last empty intersection position
            last_empty_i = starting_row
            for i in range(starting_row, ending_row + 1):
                # find current column
                j = i - s
                # current color
                current_color = self.chess_map[i][j]
                # reset current intersection's np value
                self.np_map[color][i][j][diagonal_bottom_right] = 0
                # count consecutive pieces in 'color'
                if current_color == color:
                    consecutive += 1
                if current_color != color or i == ending_row:
                    # update the np value of the last empty intersection
                    last_empty_j = last_empty_i - s
                    if self.chess_map[last_empty_i][last_empty_j] == unoccupied:
                        self.np_map[color][last_empty_i][last_empty_j][diagonal_bottom_right] += consecutive
                    last_empty_i = i

                    # update np values so far and zero out consecutive counts
                    for r in range(last, i + 1):
                        c = r - s
                        self.np_map[color][r][c][
                            diagonal_bottom_right] = consecutive
                        # the i-th row iteration should be overwritten by the code below

                    if current_color == 1 - color:
                        self.np_map[color][i][j][diagonal_bottom_right] = 0
                    # zero out consecutive counts
                    consecutive = 0
                    # update last row position
                    last = i + 1

    def update_potential(self, coordinate: tuple):
        # update properties of every intersection in line with the given intersection
        black = 1
        white = 0
        unoccupied = -1
        row = coordinate[0]
        col = coordinate[1]
        if row < 0 or row >= self.board_size:
            raise ValueError("Invalid row input.")
        if col < 0 or col >= self.board_size:
            raise ValueError("Invalid col input.")

        table = self.potential_map
        # directions
        vertical = 0
        diagonal_upper_right = 1
        horizontal = 2
        diagonal_bottom_right = 3
        lo_bound = 0
        hi_bound = self.board_size - 1
        consecutive = 0

        # change potential values at the given position in the potential map to 0
        for d in range(4):
            table[row][col][d] = 0

        # vertical direction double pointers traverse starting from [row][col], for counting potentials
        # starting and ending indices
        direction = vertical
        i1 = row
        i2 = row
        i1 -= 1
        i2 += 1
        while i1 >= lo_bound:
            if self.chess_map[i1][col] == unoccupied:
                consecutive += 1
                i1 -= 1
            else:
                break
        while i2 <= hi_bound:
            if self.chess_map[i2][col] == unoccupied:
                consecutive += 1
                i2 += 1
            else:
                break

        for i in range(i1 + 1, i2):
            table[i][col][direction] = consecutive

        # reset counter
        consecutive = 0
        # END of vertical direction

        # upper-right-diagonal direction double pointers traverse starting from [row][col], for counting potentials
        # starting and ending indices
        direction = diagonal_upper_right
        s = row + col
        if s < hi_bound:
            starting_row = lo_bound
            ending_row = s
        else:
            starting_row = s - hi_bound
            ending_row = hi_bound
        i1 = row
        i2 = row
        i1 -= 1
        i2 += 1
        while i1 >= starting_row:
            j1 = s - i1
            if self.chess_map[i1][j1] == unoccupied:
                consecutive += 1
                i1 -= 1
            else:
                break
        while i2 <= ending_row:
            j2 = s - i2
            if self.chess_map[i2][j2] == unoccupied:
                consecutive += 1
                i2 += 1
            else:
                break

        for i in range(i1 + 1, i2):
            j = s - i
            table[i][j][direction] = consecutive

        # reset counter
        consecutive = 0
        # End of upper-right diagonal direction

        # horizontal direction double pointers traverse starting from [row][col], for counting potentials
        # starting and ending indices
        direction = horizontal
        j1 = col
        j2 = col
        j1 -= 1
        j2 += 1
        while j1 >= lo_bound:
            if self.chess_map[row][j1] == unoccupied:
                consecutive += 1
                j1 -= 1
            else:
                break
        while j2 <= hi_bound:
            if self.chess_map[row][j2] == unoccupied:
                consecutive += 1
                j2 += 1
            else:
                break

        for j in range(j1 + 1, j2):
            table[row][j][direction] = consecutive

        # reset counter
        consecutive = 0
        # END of horizontal direction

        # upper-right-diagonal direction double pointers traverse starting from [row][col], for counting potentials
        # starting and ending indices
        direction = diagonal_bottom_right
        s = row - col
        if row > col:
            starting_row = row - col
            ending_row = hi_bound
        else:
            starting_row = lo_bound
            ending_row = hi_bound + s
        i1 = row
        i2 = row
        i1 -= 1
        i2 += 1
        while i1 >= starting_row:
            j1 = i1 - s
            if self.chess_map[i1][j1] == unoccupied:
                consecutive += 1
                i1 -= 1
            else:
                break
        while i2 <= ending_row:
            j2 = i2 - s
            if self.chess_map[i2][j2] == unoccupied:
                consecutive += 1
                i2 += 1
            else:
                break

        for i in range(i1 + 1, i2):
            j = i - s
            table[i][j][direction] = consecutive
        # End of bottom-right diagonal direction

    # helper function for sorting strategy maps for strategy
    def get_potential(self, coordinate: tuple):
        row = coordinate[0]
        col = coordinate[1]
        ans = 0
        for i in range(4):
            ans += self.potential_map[row][col][i]
        return ans

    # helper function for sorting strategy maps for strategy
    def get_values_white(self, coordinate: tuple):
        row = coordinate[0]
        col = coordinate[1]
        gains = 0
        threats = 0
        for i in range(4):
            current_np = self.np_map[0][row][col][i]
            current_potential = self.potential_map[row][col][i]
            if current_np >= 4:
                gains += current_np * 1000000
            elif current_np == 3:
                if current_potential >= 2:
                    gains += current_np * 20000
            elif current_np == 2:
                if current_potential >= 3:
                    gains += current_np * 2000
            elif current_np == 1:
                if current_potential >= 4:
                    gains += current_np * 200
            else:
                gains += current_potential

        for i in range(4):
            current_np = self.np_map[1][row][col][i]
            current_potential = self.potential_map[row][col][i]
            if current_np >= 4:
                threats += current_np * 100000
            elif current_np == 3:
                if current_potential >= 2:
                    threats += current_np * 10000
            elif current_np == 2:
                if current_potential >= 3:
                    threats += current_np * 1000
            elif current_np == 1:
                if current_potential >= 4:
                    threats += current_np * 100
            else:
                threats += current_potential

        return gains + threats

    def get_values_black(self, coordinate: tuple):
        row = coordinate[0]
        col = coordinate[1]
        gains = 0
        threats = 0
        for i in range(4):
            current_np = self.np_map[1][row][col][i]
            current_potential = self.potential_map[row][col][i]
            if current_np >= 4:
                gains += current_np * 1000000
            elif current_np == 3:
                if current_potential >= 2:
                    gains += current_np * 20000
            elif current_np == 2:
                if current_potential >= 3:
                    gains += current_np * 2000
            elif current_np == 1:
                if current_potential >= 4:
                    gains += current_np * 200
            else:
                gains += current_potential

        for i in range(4):
            current_np = self.np_map[0][row][col][i]
            current_potential = self.potential_map[row][col][i]
            if current_np >= 4:
                threats += current_np * 100000
            elif current_np == 3:
                if current_potential >= 2:
                    threats += current_np * 10000
            elif current_np == 2:
                if current_potential >= 3:
                    threats += current_np * 1000
            elif current_np == 1:
                if current_potential >= 4:
                    threats += current_np * 100
            else:
                threats += current_potential

        return gains + threats

    def update_strategy(self):
        self.strategy_map_black.sort(reverse=True, key=self.get_values_black)
        self.strategy_map_white.sort(reverse=True, key=self.get_values_white)

    def inquire(self, color: int):
        if color != 0 and color != 1:
            raise ValueError("Invalid color input.")
        for i in range(len(self.strategy_map[color])):
            row = self.strategy_map[color][i][0]
            col = self.strategy_map[color][i][1]
            if self.chess_map[row][col] == -1:
                return self.strategy_map[color][i]

    def place(self, coordinate: tuple, color: int):
        if color != 0 and color != 1:
            raise ValueError("Invalid color input.")
        row = coordinate[0]
        col = coordinate[1]
        self.chess_map[row][col] = color
        self.update_np(coordinate)
        self.update_potential(coordinate)
        self.update_strategy()


"""
Obsolete codes:

    if top:
        if left:
            self.np_map[color][row][col + 1][horizontal] += 1
            self.np_map[color][row + 1][col][vertical] += 1
            self.np_map[color][row + 1][col + 1][diagonal_bottom_right] += 1
        elif right:
            self.np_map[color][row][col - 1][horizontal] += 1
            self.np_map[color][row + 1][col][vertical] += 1
            self.np_map[color][row + 1][col - 1][diagonal_upper_right] += 1
        else:
            self.np_map[color][row][col - 1][horizontal] += 1
            self.np_map[color][row][col + 1][horizontal] += 1
            self.np_map[color][row + 1][col - 1][diagonal_upper_right] += 1
            self.np_map[color][row + 1][col][vertical] += 1
            self.np_map[color][row + 1][col + 1][diagonal_bottom_right] += 1

    elif bottom:
        if left:
            self.np_map[color][row - 1][col][vertical] += 1
            self.np_map[color][row - 1][col + 1][diagonal_upper_right] += 1
            self.np_map[color][row][col + 1][horizontal] += 1
        elif right:
            self.np_map[color][row - 1][col - 1][diagonal_bottom_right] += 1
            self.np_map[color][row - 1][col][vertical] += 1
            self.np_map[color][row][col - 1][horizontal] += 1
        else:
            self.np_map[color][row - 1][col - 1][diagonal_bottom_right] += 1
            self.np_map[color][row - 1][col][vertical] += 1
            self.np_map[color][row - 1][col + 1][diagonal_upper_right] += 1
            self.np_map[color][row][col - 1][horizontal] += 1
            self.np_map[color][row][col + 1][horizontal] += 1

    else:
        self.np_map[color][row - 1][col - 1][diagonal_bottom_right] += 1
        self.np_map[color][row - 1][col][vertical] += 1
        self.np_map[color][row - 1][col + 1][diagonal_upper_right] += 1
        self.np_map[color][row][col - 1][horizontal] += 1
        self.np_map[color][row][col + 1][horizontal] += 1
        self.np_map[color][row + 1][col - 1][diagonal_upper_right] += 1
        self.np_map[color][row + 1][col][vertical] += 1
        self.np_map[color][row + 1][col + 1][diagonal_bottom_right] += 1
"""