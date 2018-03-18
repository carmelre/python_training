import random

PLAYER1_SYMBOL = "X"
PLAYER2_SYMBOL = "O"


class XOGame:
    """
    Creates a XO game for two players, in any wanted board size (n>2).
    """

    def __init__(self, player1, player2, board_size):
        """
        Initiates the XO game.

        :param player1: The name of the first player
        :param player2: The name of the second player
        :param board_size: The length of the boards rows and columns.
        """
        # Create a mapping between the player representation and name
        self.players = [player1, player2]
        # Create mapping between player representation and printable symbol
        self.symbols_mapping = [PLAYER1_SYMBOL, PLAYER2_SYMBOL]
        self.board_size = board_size
        # Range is used so each row would create a different list in the memory
        self.board = [[None] * board_size for row in range(self.board_size)]
        self.turns_counter = 0
        self.current_player = random.choice([0, 1])

    def start_game(self):
        """
        Calls for turns to be taken until the game is over.
        """
        self.print_board()
        while not self.has_game_ended():
            self.take_turn()
            self.print_board()

    def print_board(self):
        """
        Prints the current board of the game.
        """
        # Prints the first line that looks like this (for n = 3):
        #   0 1 2
        print('   {}'.format(' '.join([str(num) for num in range(self.board_size)])))
        # Creates a line that separates the board rows (calculated according to the number of slots)
        # Eventually the line would look like this -------------
        separator_line = '  {}'.format('-' * (3 * self.board_size - (self.board_size - 1)))
        for row_number in range(self.board_size):
            # Create a list of printable values according to our mapping.
            printable_values = [self.symbols_mapping[value] if value is not None else ' '
                                for value in self.board[row_number]]
            # Create a template string as this one (for n=3):
            # 0 |{}|{}|{}|
            # And format the printable values into it.
            # 0 | |X|O|
            print(f'{row_number} |' + ('{}|' * self.board_size).format(*printable_values))
            # Print a separator line if we haven`t reached the last line.
            if row_number < self.board_size - 1:
                print(separator_line)

    def take_turn(self):
        """
        Performs several actions:
        - Switch the player that has the next turn
        - Receive a slot from the player and check if it available
        - Positions the players symbol on the board
        """""
        if self.turns_counter > 0:
            self.current_player = (self.current_player + 1) % 2

        print('OK {}, its your turn!'.format(self.players[self.current_player]))

        row_index, column_index = self._get_validated_slot_number_input()
        self.board[row_index][column_index] = self.current_player
        self.turns_counter += 1

    def has_game_ended(self) -> bool:
        """
        Check whether a player has won/the game was tied.
        """

        if self.turns_counter < (self.board_size * 2 - 1):
            return False

        if any([self._check_for_winning_sequence(row) for row in self.board]):
            return True

        columns_list = [[row[column_number] for row in self.board] for column_number in range(self.board_size)]
        if any([self._check_for_winning_sequence(column) for column in columns_list]):
            return True

        left_to_right_diagonal = [self.board[index][index] for index in range(self.board_size)]
        if self._check_for_winning_sequence(left_to_right_diagonal):
            return True

        right_to_left_diagonal = [self.board[self.board_size - 1 - index][index] for index in range(self.board_size)]
        if self._check_for_winning_sequence(right_to_left_diagonal):
            return True

        if self.turns_counter == self.board_size ** 2:
            print("The game has ended with a tie!")
            return True

        return False

    def _check_for_winning_sequence(self, sequence) -> bool:
        """
        Check if a specific sequence is comprised of a uniform symbol, and indicates a win.

        :param sequence: The sequence that should be checked.
        """
        if sequence.count(self.current_player) == self.board_size:
            print('The winner is {}'.format(self.players[self.current_player]))
            return True

        return False

    def _get_validated_slot_number_input(self):
        """
        Get a valid slot number input from the user.

        :return: a tuple with two items: (row index, column index)
        """
        is_slot_number_valid = False

        while not is_slot_number_valid:
            row_index = input("Please enter row number >")
            column_index = input("Please enter column number >")
            if not row_index.isnumeric() or not column_index.isnumeric():
                print("Slot locations must be numbers, please try again")
                continue
            row_index = int(row_index)
            column_index = int(column_index)
            if row_index not in range(self.board_size) or column_index not in range(self.board_size):
                print("Make sure the slot numbers you have entered are within the range of the board.")
            elif self.board[row_index][column_index] in [0, 1]:
                print("That slot is already taken, choose again")
            else:
                is_slot_number_valid = True

        return row_index, column_index


def get_validated_board_size() -> int:
    """
    Validates that the user has given a numeric board size that is bigger than 2.

    :return: A board size after validation.
    """
    is_board_size_valid = False
    while not is_board_size_valid:
        board_size_input = input('Please enter board size')
        if not board_size_input.isnumeric():
            print("invalid input, please enter a number")
            continue
        board_size_input = int(board_size_input)
        if board_size_input < 3:
            print('board size must be bigger than 3')
        else:
            is_board_size_valid = True

    return board_size_input


def main():
    player1 = input('Please enter the name of player one >')
    player2 = input('Please enter the name of player two >')
    board_size = get_validated_board_size()

    game = XOGame(player1, player2, board_size)
    game.start_game()


if __name__ == '__main__':
    main()
