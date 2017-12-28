"""
Code to run minsweeper in the terminal

By Victor Lambert
"""

import random

class Board(object):
    """
    This class holds the functions for generating and displaying a minesweeper
    board, but not the full game.
    """
    def __init__(self, mines = 10, size = (10,10)):
        # extract the size for use later
        self.size_x = size[0]
        self.size_y = size[1]

        # save the number of bombs
        self.mine_count = mines

        # initialize a board to hold the square numbers
        self.number_board = [[0 for _ in range(self.size_x)]
                                                    for _ in range(self.size_y)]
        # Set the bomb locations
        self.set_mines()
        self.set_numbers()
        self.display_hidden()

    def set_mines(self):
        """
        Function chooses the locations for the mines on the board, mines are -1
        on the board.
        """
        # Initialize a bomb counter
        mines = 0

        # Set random locations until the number of bombs is met
        while mines < self.mine_count:

            # Choose a random x and y
            rand_x = random.randint(0, self.size_x - 1)
            rand_y = random.randint(0, self.size_y - 1)

            # add the bomb only if it isn't already added
            if self.number_board[rand_y][rand_x] != -1:

                # 1 in the bomb board means bomb
                self.number_board[rand_y][rand_x] = -1
                # Count the number of mines added
                mines += 1

    def set_numbers(self):
        """
        Uses the mines to set the number of adjacent mines on the non-mine
        squares.
        """
        # Iterate through each space on the board
        for j, row in enumerate(self.number_board):
            for i, value in enumerate(row):
                # If you find a bomb
                if value == -1:
                    # go through each neighbor
                    for neighbor in self.get_neighbors((i, j)):
                        n_x, n_y = neighbor # extract neighbor

                        # if the neighbor isn't a bomb, add 1
                        if self.number_board[n_y][n_x] >= 0:
                            self.number_board[n_y][n_x] += 1

    def get_neighbors(self, location):
        """
        Given a location on the board, returns a list of the neighboring (x,y)
        pairs.
        """
        # Extract the location
        x, y = location
        res = []

        # Iterate through different pairs of (-1, 0, 1) to choose the neighbors
        for j in range(-1, 2):
            for i in range(-1, 2):
                # Skip if it is the original element
                if j == 0 and i == 0:
                    continue

                # Check if it will be out of bounds, otherwise attach it to res
                elif ((x + i >= 0 and x + i < self.size_x) and
                        (y + j >= 0 and y + j < self.size_y)):
                    res.append((x + i, y + j))
        return res

    def display_hidden(self):
        """
        Print the full board with numbers and all, includes gridlines for ease
        of viewing. This function shouldn't be called during gameplay, it will
        give everything away!
        """
        for i, row in enumerate(self.number_board):
            print ' | '.join([str(x) if x >= 0 else 'M' for x in row ])
            if i != len(self.number_board)-1:
                print '--|' + '---|' * (self.size_x - 2) + '--'
def main():
    Board()


if __name__ == '__main__':
    main()
