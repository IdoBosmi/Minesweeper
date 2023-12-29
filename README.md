# Minesweeper Game

Minesweeper is a classic single-player puzzle game where the objective is to clear a rectangular board containing hidden mines without detonating any of them. The game is won when all safe cells are revealed, and it is lost if a mine is uncovered.

## Features

- Classic Minesweeper gameplay with left-click to reveal cells and right-click to flag mines.
- Mines are randomly placed on the board, and the game ensures a safe initial click.
- Implement a solver that can provide hints based on computer logic.

## Installation

1. Make sure you have Python installed on your system.
2. Clone this repository:

    ```bash
    git clone https://github.com/your-username/Minesweeper.git
    ```

3. Navigate to the project directory:

    ```bash
    cd Minesweeper
    ```

4. Run the Minesweeper game:

    ```bash
    python MineSweeper.py
    ```

## How to Play

- **Left-Click:** Reveal a cell.
- **Right-Click:** Flag or unflag a mine.
- **Middle-Click (Solver):** Request a hint based on computer logic.
- **Press 'R':** Restart the game at any time.

## Solver

The Minesweeper game includes a solver that provides hints based on computer thinking. By middle-clicking, you can request a hint, and the solver will respond with a blinking green cell for a safe move or an orange cell for a mine.

The solver doesn't cheat by accessing real mines but relies on accurate computer logic for making educated guesses.



