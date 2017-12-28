"""
Code to run minsweeper in the terminal

By Victor Lambert
"""

import random

class Board(object):
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
        # Initialize a bomb counter
        mines = 0

        # Set random locations until the number of bombs is met
        while mines < self.mine_count:
            rand_x = random.randint(0, self.size_x - 1)
            rand_y = random.randint(0, self.size_y - 1)
            if self.number_board[rand_y][rand_x] != -1:
                # 1 in the bomb board means bomb
                self.number_board[rand_y][rand_x] = -1
                mines += 1

    def set_numbers(self):
        for j, row in enumerate(self.number_board):
            for i, value in enumerate(row):
                if value == -1:
                    for neighbor in self.get_neighbors((i, j)):
                        n_x, n_y = neighbor
                        if self.number_board[n_y][n_x] >= 0:
                            self.number_board[n_y][n_x] += 1

    def get_neighbors(self, location):
        x, y = location
        res = []
        for j in range(-1, 2):
            for i in range(-1, 2):
                if j == 0 and i == 0:
                    continue
                elif ((x + i >= 0 and x + i < self.size_x) and
                        (y + j >= 0 and y + j < self.size_y)):
                    res.append((x + i, y + j))
        return res

    def display_hidden(self):
        for i, row in enumerate(self.number_board):
            print ' | '.join([str(x) if x >= 0 else 'M' for x in row ])
            if i != len(self.number_board)-1:
                print '--|' + '---|' * (self.size_x - 2) + '--'
def main():
    Board()


if __name__ == '__main__':
    main()
