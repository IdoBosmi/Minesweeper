# Import necessary modules
import turtle
from GameBoard import GameBoard
from Solver import Solver

# Define constants for the Minesweeper game
num_of_rows = 20
num_of_columns = 32
num_of_mines = 99

CELL_SIZE = 40
SCREEN_WIDTH = num_of_columns * CELL_SIZE
SCREEN_HEIGHT = num_of_rows * CELL_SIZE

# Set up the Turtle screen
wn = turtle.Screen()
wn.title("Minesweeper")
wn.bgcolor("black")
wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
wn.tracer(0)  # Turn off automatic updates to enhance performance

# Function to handle left-click events
def left_click(x, y):
    # Check if the click is within the game board boundaries
    if x > -SCREEN_WIDTH/2 + CELL_SIZE and x < SCREEN_WIDTH/2 - CELL_SIZE and y > -SCREEN_HEIGHT/2 + CELL_SIZE and y < SCREEN_HEIGHT/2 - CELL_SIZE:
        # Convert the click coordinates to row and column indices
        column = int((x + SCREEN_WIDTH/2) // CELL_SIZE)
        row = int((-y + SCREEN_HEIGHT/2) // CELL_SIZE)
        
        # Check if mines are already filled
        if game_board._is_mines_filled:
            # Perform left-click action on the game board cell
            game_board.left_click(row, column)
            
            # If the clicked cell is open and has no neighbors, perform additional checks
            if game_board._board[row][column]._is_open and game_board._board[row][column].get_num_of_neighbors() == 0:
                cells_to_check = [(row, column)]
                
                # Explore neighboring cells with recursion until no more empty cells are found
                while cells_to_check:
                    cell_row, cell_col = cells_to_check.pop(0)
                    for r in range(cell_row-1, cell_row+2):
                        for c in range(cell_col-1, cell_col+2):
                            # Check if the neighboring cell is within the game board boundaries
                            if r > 0 and r < num_of_rows-1 and c > 0 and c < num_of_columns-1 and game_board._board[row][column].get_num_of_neighbors() == 0 and not game_board._board[r][c]._is_open:
                                game_board.left_click(r, c)
                                if game_board._board[r][c].get_num_of_neighbors() == 0:
                                    cells_to_check.append((r, c))
        else:
            # If mines are not filled, fill mines and perform left-click action
            game_board.fill_mines(num_of_mines, row, column)
            left_click(x, y)  # Recursively call the left_click function to handle the initial click

# Function to handle right-click events
def right_click(x, y):
    # Convert the click coordinates to row and column indices
    column = int((x + SCREEN_WIDTH/2) // CELL_SIZE)
    row = int((-y + SCREEN_HEIGHT/2) // CELL_SIZE)
    
    # Perform right-click action on the game board cell
    game_board.right_click(row, column)

# Function to handle moves by the automated Solver
def solver_move(x, y):
    solver.find_next_move()

# Function to highlight the next move by the Solver
def highlight_next_move(x, y):
    solver.highlight_next_move(x, y)



# Create instances of the GameBoard and Solver
game_board = GameBoard(num_of_rows, num_of_columns, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
game_board.draw_board()  # Draw the initial game board
solver = Solver(game_board)  # Create a Solver instance for automated moves


# Set up event handlers for mouse clicks
wn.onclick(left_click, btn=1)  # Left-click
wn.onclick(right_click, btn=3)  # Right-click
wn.onclick(solver_move, btn=2)  # Middle-click
wn.onscreenclick(highlight_next_move, btn=2)  # Middle-click for highlighting next move

# Main game loop for continuously updating the Turtle screen
while True:
    wn.update()
