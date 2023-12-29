import turtle
import time

class Cell:
    def __init__(self, i, j, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE) -> None:
        # Initialize a Cell with its properties

        self._is_open = False
        self._is_flaged = False
        self._is_mine = False
        self.num_of_neighbors = 0
        self._row = i
        self._column = j
        self._SCREEN_WIDTH = SCREEN_WIDTH
        self._SCREEN_HEIGHT = SCREEN_HEIGHT
        self._CELL_SIZE = CELL_SIZE
        self.cover = turtle.Turtle()
        self.flag = turtle.Turtle()
        self.label = turtle.Turtle()

        self.flag.hideturtle()
        self.label.hideturtle()
        self.cover.hideturtle()
        

    def draw_cell(self):
        # Draw the cover of the cell

        self.cover.penup()
        self.cover.goto(self._column*self._CELL_SIZE - self._SCREEN_WIDTH/2 + self._CELL_SIZE/2, -(self._row*self._CELL_SIZE - self._SCREEN_HEIGHT/2 + self._CELL_SIZE/2))
        self.cover.speed(0)
        self.cover.shape("square")
        self.cover.color("white")
        self.cover.shapesize(stretch_wid= (self._CELL_SIZE*0.9)/20, stretch_len=(self._CELL_SIZE*0.9)/20)
        self.cover.showturtle()

    def set_num_of_neighbors(self, num_of_neighbors):
        # Set the number of neighboring mines

        self.num_of_neighbors = num_of_neighbors

    def openCell(self):
        # Open the cell and draw label if it's not a mine

        self.cover.hideturtle()
        self._is_open = True

        # Draw label if there are neighboring mines
        if self.num_of_neighbors > 0:
            self.label.penup()
            self.label.goto(self._column*self._CELL_SIZE - self._SCREEN_WIDTH/2 + self._CELL_SIZE/2, -(self._row*self._CELL_SIZE - self._SCREEN_HEIGHT/2 + self._CELL_SIZE/1.25))
            self.label.speed(0)
            self.label.color("white")
            self.label.write(self.num_of_neighbors, move=False, align='center', font=('Arial', self._CELL_SIZE//3, 'normal'))

    def inc(self):
        # Increment the number of neighboring mines

        self.num_of_neighbors += 1

    def set_as_mine(self):
        # Set the cell as a mine

        self._is_mine = True

    def draw_flag(self):
        # Draw a flag on the cell

        self.flag.penup()
        self.flag.goto(self._column*self._CELL_SIZE - self._SCREEN_WIDTH/2 + self._CELL_SIZE/2, -(self._row*self._CELL_SIZE - self._SCREEN_HEIGHT/2 + self._CELL_SIZE/2))
        self.flag.speed(0)
        self.flag.shape("square")
        self.flag.color("red")
        self.flag.shapesize(stretch_wid=(self._CELL_SIZE*0.6)/20, stretch_len=(self._CELL_SIZE*0.6)/20)
        self.flag.showturtle()
        self.cover.hideturtle()
        self._is_flaged = True

    def erase_flag(self):
        # Erase the flag and show the cover

        self.flag.hideturtle()
        self.cover.showturtle()
        self._is_flaged = False

    def get_num_of_neighbors(self):
        # Get the number of neighboring mines

        return self.num_of_neighbors

    def is_open(self):
        # Check if the cell is open

        return self._is_open

    def is_flagged(self):
        # Check if the cell is flagged

        return self._is_flaged

    def green_cover(self):
        # Flash the cover in green to indicate a safe move

        self.cover.color("green")
        self.cover.update()
        time.sleep(1)  # Adjust the sleep duration as needed
        self.cover.color("white")
        self.cover.update()

    def orange_cover(self):
        # Flash the cover in orange to indicate a mine move

        self.cover.color("orange")
        self.cover.update()
        time.sleep(1)  # Adjust the sleep duration as needed
        self.cover.color("white")
        self.cover.update()

    def white_cover(self):
        # Reset the cover color to white

        self.cover.color("white")

    def draw_free_hint(self):
        # Draw a hint for a safe move

        self.cover.color("green")

        for i in range(5):
            turtle.ontimer(self.green_cover, 400 * (i + 1))
            turtle.ontimer(self.white_cover, 400 * (i + 1))

    def draw_mine_hint(self):
        # Draw a hint for a mine move

        self.cover.color("orange")

        for i in range(5):
            turtle.ontimer(self.orange_cover, 400 * (i + 1))
            turtle.ontimer(self.white_cover, 400 * (i + 1))
