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
        # difficulty sets the size and number of bombs
        if difficulty == 'E':
            self.size_x = 10
            self.size_y = 10
            self.mine_count = 10

        # Reveal count decreases until all non mine cells are revealed
        # Then you win the game
        self.reveal_count = self.size_x * self.size_y - self.mine_count

        # Initialize a 2D list to show which cells have been revealed
        self.revealed = [[0 for _ in range(self.size_x)]
                                                    for _ in range(self.size_y)]

        self.generate_board() # generate the underlying board
        self.display() # Display the first board

        # Accept the first move
        initial  = self.read_move()
        _, init_x, init_y = initial

        # Check if the first move is a bomb, and regenerate until it isn't
        while self.number_board[init_y][init_x] == -1:
            self.generate_board()

        # Process the first move
        self.update(initial)

    def new_move(self):
        """
        Gets a new move. This function helps when a repeat move is needed,
        this function can be called to restart the process.
        """
        move = self.read_move()
        result = self.update(move)
        return result

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

        # Check if x an y are ints
        try:
            x = int(x_str)
            y = int(y_str)

        # If they aren't try to read another move after a warning
        except:
            print 'invalid integers entered'
            return self.read_move()

        # If the move is valid, return the move
        if m in ['c', 'f', 'r', 'cheat']:
            return (m, x, y)

        # If the move isn't valid, get another move
        else:
            print 'invalid move entered'
            return self.read_move()

    def update(self, move):
        """
        Given a move, update the state of the game board based on the given
        move.
        """
        m, x, y = move
        # If the move is a choice, process on
        if m == 'c':
            # If it's flagged, warn them and accept another move
            if self.revealed[y][x] == 2:
                self.display()
                print 'That cell is flagged, choose again or unflag with r'
                return self.new_move()

            # If it's a bomb, return and lose the game
            elif self.number_board[y][x] == -1:
                return False

            # If it's already revealed, try again
            elif self.revealed[y][x] == 1:
                self.display()
                print 'Already chose that cell'
                return self.new_move()

            # Otherwise, reveal the chosen cell
            else:
                self.revealed[y][x] = 1
                self.reveal_count -= 1
                if self.number_board[y][x] == 0:
                    self.reveal_zeros((x, y))

        # If the move is flag, flag the target
        elif m == 'f':
            if self.revealed[y][x] == 1:
                self.display()
                print 'Cell already revealed, choose again'
                return self.new_move()
            # Otherwise, flag it
            else:
                self.revealed[y][x] = 2

        # If the move is remove flag, hide the cell
        elif m == 'r':
            # if it's not a flag, skip
            if self.revealed[y][x] != 2:
                self.display()
                print 'You did not choose a flag, make another move'
                self.new_move()

            # If it is a flag, remove
            else:
                self.revealed[y][x] = 0

        # cheat is cheating, it shows the whole board
        elif m == 'cheat' and x == 9 and y == 9:
            self.display_hidden()
        elif m == 'cheat' and x == 1 and y == 1:
            self.reveal_mines(flag = True)

    def reveal_mines(self, flag = False):
        """Called when the game is lost, reveals all the mines only"""
        for j, row in enumerate(self.number_board):
            for i, item in enumerate(row):
                if item == -1:
                    if flag is True:
                        self.revealed[j][i] = 2
                    else:
                        self.revealed[j][i] = 1

    def reveal_zeros(self, location):
        """
        Called when a zero is clicked. Reveals all adjacent zeros and their
        adjacent numbers. This just removes the boring part of the game where
        zeros can be clicked without any thought.

        Runs using a depth first search.
        """
        visited =[]
        to_check = [location]

        while to_check:
            # Take the last element in the queue
            current = to_check.pop()
            # Mark it as visited
            visited.append(current)

            x, y = current

            # Set it to revealed and drop the revealed counter
            if self.revealed[y][x] == 0:
                self.revealed[y][x] = 1
                self.reveal_count -= 1

            # Add the next elements if they are 0, not visited, and not in queue
            if self.number_board[y][x] == 0:
                for neigh in self.get_neighbors(current):
                    if neigh not in visited and neigh not in to_check:
                        to_check.append(neigh)

    def run(self):
        """The main function of the Game. Loops continuously accepting a move
        each loop. The only time the loop ends is if you lose or if you win."""
        while True:
            # Start by showing the board
            self.display()

            # Get a new move
            state = self.new_move()
            print self.reveal_count
            # If the state is False, a mine was clicked
            if state == False:
                self.reveal_mines()
                self.display()
                print 'OH NO, YOU LOSE'
                print 'BOOM'
                break
            elif self.reveal_count == 0:
                self.reveal_mines()
                self.display()
                print 'YOU WIN'
                print '8)'
                break

    def display(self):
        """
        Display the non hidden items of the board, this is what the player
        should see as they reveal squares.
        """

        for j, row in enumerate(self.number_board):

            # For each row, compile a list of symbols to show
            to_show = []

            for i, item in enumerate(row):
                # If its revealed but not flagged, show a symbol
                if self.revealed[j][i] == 1:
                    # If it's greater than 0 it's a number, show it
                    if item >= 0:
                        to_show.append(str(item))
                    # Otherwise it's a mine, display M
                    else:
                        to_show.append('M')
                # If revealed is a 2, it's a flag
                elif self.revealed[j][i] == 2:
                    to_show.append('F')
                # Else it's hidden, show a blank
                else:
                    to_show.append(' ')

            # Combine all the to show with vertical grids
            print ' | '.join(to_show)

            # Print a horizontal grid for all but the last line
            if j != len(self.number_board)-1:
                print '--|' + '---|' * (self.size_x - 2) + '--'

def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
