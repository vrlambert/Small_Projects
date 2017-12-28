"""
Code to run minsweeper in the terminal

By Victor Lambert
"""

"""
to do
board generation
board output
making moves
updating board based on moves
winning

steps of game
spread bombs
assign values
show board
accept moves
play to win or lose
"""
import random

class Board(object):
    def __init__(self, bombs = 10, size = (10,10)):
        self.size_x = size[0]
        self.size_y = size[1]
        self.bomb_count = bombs
        self.bomb_board = [[0 for _ in range(self.size_x)]
                                                    for _ in range(self.size_y)]

        self.set_bombs()
        self.display()

    def set_bombs(self):
        bombs = 0
        while bombs < self.bomb_count:
            rand_x = random.randint(0, self.size_x - 1)
            rand_y = random.randint(0, self.size_y - 1)
            if self.bomb_board[rand_y][rand_x] != 1:
                self.bomb_board[rand_y][rand_x] = 1
                bombs += 1

    def display(self):
        for row in self.bomb_board:
            print row
def main():
    Board()


if __name__ == '__main__':
    main()
