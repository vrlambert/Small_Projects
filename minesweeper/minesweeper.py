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
    def __init__(self, mines = 10, size = (10,10), show = False):
        # extract the size for use later
        self.size_x = size[0]
        self.size_y = size[1]

        # save the number of mines
        self.mine_count = mines

        # Set the bomb locations
        self.generate_board()
        if show == True:
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

    def generate_board(self):
        """
        Call this to generate the board
        """
        # initialize a board to hold the square numbers
        self.number_board = [[0 for _ in range(self.size_x)]
                                                    for _ in range(self.size_y)]
        self.set_mines()
        self.set_numbers()

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

class Game(Board):
    """
    Game class inherits from board to allow for use of the board generation
    functions. Also adds input reading, board updating, and game running
    functionality.
    """
    def __init__(self, difficulty = 'E'):
        if difficulty == 'E':
            self.size_x = 10
            self.size_y = 10
            self.mine_count = 10

        self.revealed = [[0 for _ in range(self.size_x)]
                                                    for _ in range(self.size_y)]

        self.generate_board() # generate the underlying board
        self.display()
        initial  = self.read_move()
        _, init_x, init_y = initial
        while self.number_board[init_y][init_x] == -1:
            print 'regenerating'
            self.generate_board()

        self.update(initial)

    def read_move(self):
        """
        Read a move into an x y pair, with a flag add or remove option if
        necessary.
        """
        move = raw_input("""Enter your move in format m x y.
m is the type of move, c for click, f for flag, r for remove flag.
x and y should be numbers.
Enter here:""")
        m, x_str, y_str = move.split() # need to change this to avoid crashes
        try:
            x = int(x_str)
            y = int(y_str)
        except:
            print 'invalid integers entered'
            return self.read_move()

        if m in ['c', 'f', 'r', 'cheat']:
            return (m, x, y)
        else:
            print 'invalid move entered'
            return self.read_move()

    def update(self, move):
        """
        Given a move, update the state of the game board based on the given
        move.
        """
        m, x, y = move
        if m == 'c':
            if self.revealed[y][x] == 2:
                print 'That cell is flagged, choose again or unflag with r'
                self.read_move()
                return
            elif self.number_board[y][x] == -1:
                print 'BOOM'
                return False

            elif self.revealed[y][x] == 1:
                print 'Already chose that cell'
                self.read_move()
                return
            else:
                print x, y, 'revealed'
                self.revealed[y][x] = 1

        elif m == 'f':
            self.revealed[y][x] = 2
            print 'ok'
        elif m == 'r':
            self.revealed[y][x] = 0

        elif m == 'cheat' and x == 9 and y == 9:
            self.display_hidden()

    def reveal_mines(self):
        """Called when the game is lost, reveals all the mines only"""
        for j, row in enumerate(self.number_board):
            for i, item in enumerate(row):
                if item == -1:
                    self.revealed[j][i] = 1

    def run(self):
        while True:
            self.display()
            move = self.read_move()
            state = self.update(move)
            if state == False:
                self.reveal_mines()
                self.display()
                print 'OH NO, YOU LOSE'
                print 'BOOM'
                break

    def display(self):
        """
        Display the non hidden items of the board, this is what the player
        should see as they reveal squares.
        """
        for j, row in enumerate(self.number_board):
            to_show = []
            for i, item in enumerate(row):
                if self.revealed[j][i] == 1:
                    if item >= 0:
                        to_show.append(str(item))
                    else:
                        to_show.append('M')
                elif self.revealed[j][i] == 2:
                    to_show.append('F')
                else:
                    to_show.append(' ')
            print ' | '.join(to_show)
            if j != len(self.number_board)-1:
                print '--|' + '---|' * (self.size_x - 2) + '--'

def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
