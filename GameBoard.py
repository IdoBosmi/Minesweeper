
import random
from Cell import Cell
import turtle

# Initialize turtle
turtle.speed(0)
turtle.hideturtle()

class GameBoard:

    def __init__(self, num_of_rows, num_of_columns, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE) -> None:
        # Initialize the GameBoard with the specified dimensions and cell size

        self._num_of_rows = num_of_rows
        self._num_of_columns = num_of_columns
        self._SCREEN_WIDTH = SCREEN_WIDTH
        self._SCREEN_HEIGHT = SCREEN_HEIGHT
        self._CELL_SIZE = CELL_SIZE
        self._is_mines_filled = False
        
        # Create a 2D array to represent the game board with cells
        self._board = []
        for i in range(num_of_rows):
            row = []
            for j in range(num_of_columns):
                row.append(Cell(i, j, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE))
            self._board.append(row)
        
    def fill_mines(self, num_of_mines, current_row, current_column):
        # Fill the board with mines, ensuring a safe initial click location

        not_options = list(range((current_row-1)*self._num_of_columns + current_column-1, (current_row-1)*self._num_of_columns + current_column+2))
        not_options = not_options + list(range(current_row*self._num_of_columns + current_column-1, current_row*self._num_of_columns + current_column+2))
        not_options = not_options + list(range((current_row+1)*self._num_of_columns + current_column-1, (current_row+1)*self._num_of_columns + current_column+2))

        not_options = not_options + list(range(0, self._num_of_columns))  # add first demo row
        not_options = not_options + list(range((self._num_of_rows-1)* self._num_of_columns, self._num_of_rows*self._num_of_columns))  # add last demo row
        not_options = not_options + list(range(0, (self._num_of_rows-1)* self._num_of_columns, self._num_of_columns))  # add first demo column
        not_options = not_options + list(range(self._num_of_columns - 1, self._num_of_rows*self._num_of_columns, self._num_of_columns))  # add last demo column
        mines_locations_options = [k for k in range(self._num_of_columns*self._num_of_rows) if k not in not_options]

        x = random.sample(mines_locations_options, num_of_mines)

        for i in range(self._num_of_rows):
            for j in range(self._num_of_columns):
                if (self._num_of_columns*(i) + j) in x:
                    self._board[i][j].set_as_mine()
                    self._board[i-1][j-1].inc()
                    self._board[i-1][j].inc()
                    self._board[i-1][j+1].inc()
                    self._board[i][j-1].inc()
                    self._board[i][j+1].inc()
                    self._board[i+1][j-1].inc()
                    self._board[i+1][j].inc()
                    self._board[i+1][j+1].inc()
          
        self._is_mines_filled = True

    def draw_board(self):
        # Draw the game board with cells

        for i in range(1, self._num_of_rows-1):
            for j in range(1, self._num_of_columns-1):
                self._board[i][j].draw_cell()

    def left_click(self, i, j):
        # Handle left-click events on cells

        if not self._board[i][j]._is_open and not self._board[i][j]._is_mine:
            self._board[i][j].openCell() 
        elif self._board[i][j]._is_mine:
            self.game_over()

    def right_click(self, i, j):
        # Handle right-click events on cells

        if not self._board[i][j]._is_flaged and not self._board[i][j]._is_open:
            self._board[i][j].draw_flag()
        elif self._board[i][j]._is_flaged:
            self._board[i][j].erase_flag()

    def show_next_move(self, cell_index, type):
        # Show the next move based on the type of move (safe or mine)

        if type == "safe":
            print(cell_index)
            self._board[cell_index[0]][cell_index[1]].draw_free_hint()
        elif type == "mine":
            self._board[cell_index[0]][cell_index[1]].draw_mine_hint()

    def __str__(self) -> str:
        # Print the game board in a human-readable format

        print(len(self._board))
        print(len(self._board[0]))
        for i in range(len(self._board)):
            row = ""
            for j in range(len(self._board[0])):
                row = row + str(self._board[i][j].get_num_of_neighbors()) + ","
            print(row)
    
    def draw_free_hint(self, row, column):
        # Draw a hint for a safe move in the specified cell

        self._board[row][column].draw_free_hint()
    
    def draw_mine_hint(self, row, column):
        # Draw a hint for a mine in the specified cell

        self._board[row][column].draw_mine_hint()
            
    def game_over(self):
        self.clear_board()
        turtle.penup()
        turtle.color("red")
        turtle.goto(0, 0)
        turtle.write("GAME OVER", align="center", font=("Arial", 24, "normal"))
        turtle.goto(0, -50)
        turtle.write("Press 'R' to restart", align="center", font=("Arial", 16, "normal"))
        turtle.hideturtle()
        
        # Remove the previous 'R' key binding if it exists
        turtle.onkey(None, "r")
        
        # Add the 'R' key binding to restart the game
        turtle.onkey(self.restart_game, "r")
        turtle.listen()

    def clear_board(self):
        turtle.clear()
        turtle.resetscreen()

    def restart_game(self):
        self.clear_board()
        self.__init__(self._num_of_rows, self._num_of_columns, self._SCREEN_WIDTH, self._SCREEN_HEIGHT, self._CELL_SIZE)
        self.draw_board()

