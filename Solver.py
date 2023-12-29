class Solver:

    def __init__(self, game_board) -> None:
        # Initialize the Solver with a reference to the game board
        self._board = game_board
        self.safe_cells = []  # List to store safe cells
        self._mines = []  # List to store identified mines

    def get_neigbors(self, r, c):
        # Return neighbors of a cell (r, c) that are within the game board boundaries
        return [(x, y) for (x, y) in [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)] if x > 0 and x < self._board._num_of_rows-1 and y > 0 and y < self._board._num_of_columns-1]
    
    @staticmethod
    def get_sub_groups(group):
        # Return all possible subsets of a group
        n = len(group)
        power_set_size = 2 ** n
        result = []
        for i in range(power_set_size):
            subset = [group[j] for j in range(n) if i & (1 << j)]
            result.append(subset)
        return result

    def find_next_move(self):
        # Logic to find the next move based on various rules

        # Get a list of open cells in the game board
        open_cells = [(cell._row, cell._column) for x in self._board._board for cell in x if cell._is_open]

        # Find mines with basic rule
        for (r, c) in open_cells:
            closed_neighbors = [x for x in self.get_neigbors(r, c) if x not in open_cells]
            if len(closed_neighbors) != 0 and len(closed_neighbors) == self._board._board[r][c].get_num_of_neighbors():
                if len([x for x in self.get_neigbors(r, c) if (x not in open_cells and not self._board._board[x[0]][x[1]].is_flagged())]) > 0:
                    row, column = [x for x in self.get_neigbors(r, c) if (x not in open_cells and not self._board._board[x[0]][x[1]].is_flagged())][0]
                    print(row, column, "basic")
                    self._board.right_click(row, column)
                    return

        # Find safe cells with basic rule
        for (r, c) in open_cells:
            flaged_neighbors = [(row, column) for (row, column) in self.get_neigbors(r, c) if self._board._board[row][column]._is_flaged]
            if len(flaged_neighbors) == self._board._board[r][c].get_num_of_neighbors():
                self.safe_cells += [x for x in self.get_neigbors(r, c) if (x not in flaged_neighbors and x not in self.safe_cells and x not in open_cells)]
                if len([x for x in self.get_neigbors(r, c) if (x not in flaged_neighbors and x not in open_cells)]) > 0:
                    row, column = [x for x in self.get_neigbors(r, c) if (x not in flaged_neighbors and x not in open_cells)][0]
                    print(row, column, "basic")
                    self._board.left_click(row, column)
                    return
        
        groups = []
        # Find safe and mines with groups
        for (r, c) in open_cells: 
            flaged_neighbors = [(row, column) for (row, column) in self.get_neigbors(r, c) if self._board._board[row][column]._is_flaged]
            unflaged_neighbors = [(row, column) for (row, column) in self.get_neigbors(r, c) if not self._board._board[row][column]._is_flaged and not self._board._board[row][column]._is_open]
            if len(unflaged_neighbors) > 0:
                groups += [(unflaged_neighbors, self._board._board[r][c].get_num_of_neighbors() - len(flaged_neighbors))]

        for (x_group, x_num) in groups:
            for (y_group, y_num) in groups:
                if all(item in y_group for item in x_group):
                    if x_num == y_num:
                        self.safe_cells += [x for x in y_group if x not in x_group]
                        if len([x for x in y_group if x not in x_group]) > 0: 
                            row, column = [x for x in y_group if x not in x_group][0]
                            print(row, column, "groups")
                            self._board.left_click(row, column)
                            return
                    if x_num + 1 == y_num and len(x_group) + 1 == len(y_group):
                        self._mines += [x for x in y_group if x not in x_group]
                        if len([x for x in y_group if x not in x_group]) > 0:
                            row, column = [x for x in y_group if x not in x_group][0]
                            print(row, column, "groups")
                            self._board.right_click(row, column)
                            return

        sub_groups = []
        # Creating subgroups
        for group in groups:
            sub_groups += [(self.get_sub_groups(group[0]), group[1])]

        # Find using subgroups
        for (group, x_num) in groups:
            for (sub_group, y_num) in sub_groups:
                if all(item in group for item in sub_group):
                    if x_num == y_num:
                        self.safe_cells += [x for x in group if x not in sub_group]
                        if len([x for x in group if x not in sub_group]) > 0: 
                            row, column = [x for x in group if x not in sub_group][0]
                            print(row, column, "subgroup")
                            self._board.left_click(row, column)
                            return 
                    if y_num < x_num:
                        self._mines += [x for x in group if x not in sub_group]
                        if len([x for x in group if x not in sub_group]) > 0:
                            row, column = [x for x in group if x not in sub_group][0]
                            print(row, column, "subgroup")
                            self._board.right_click(row, column)
                            return
                        
    def highlight_next_move(self, x, y):
        # Highlight the next move based on the Solver's strategy
        next_safe_cell, next_mine_cell = self.find_next_safe_and_mine()

        if next_safe_cell:
            self._board.draw_free_hint(*next_safe_cell)

        if next_mine_cell:
            row, column = next_mine_cell
            self._board.draw_mine_hint(row, column)

    def find_next_safe_and_mine(self):
        # Find the next safe cell and mine based on the Solver's strategy
        open_cells = [(cell._row, cell._column) for x in self._board._board for cell in x if cell._is_open]

        for (r, c) in open_cells:
            closed_neighbors = [x for x in self.get_neigbors(r, c) if x not in open_cells]
            if len(closed_neighbors) != 0 and len(closed_neighbors) == self._board._board[r][c].get_num_of_neighbors():
                if len([x for x in self.get_neigbors(r, c) if (x not in open_cells and not self._board._board[x[0]][x[1]].is_flagged())]) > 0:
                    return None, [x for x in self.get_neigbors(r, c) if (x not in open_cells and not self._board._board[x[0]][x[1]].is_flagged())][0]

        for (r, c) in open_cells:
            flaged_neighbors = [(row, column) for (row, column) in self.get_neigbors(r, c) if self._board._board[row][column]._is_flaged]
            if len(flaged_neighbors) == self._board._board[r][c].get_num_of_neighbors():
                if len([x for x in self.get_neigbors(r, c) if (x not in flaged_neighbors and x not in open_cells)]) > 0:
                    return [x for x in self.get_neigbors(r, c) if (x not in flaged_neighbors and x not in open_cells)][0], None

        return None, None
