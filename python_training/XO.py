import random


class XoGame:
    """
    Creates a XO game for two players, in any wanted board size (n>2)
    """

    def __init__(self, players, board_size):
        """
        :param players: A list with the player names.
        :param board_size: The length of the boards rows and columns.
        """
        self.players_symbols = ["X", "O"]
        # Create a mapping between the player symbol and name
        self.players = {symbol_and_player[0]: symbol_and_player[1] for symbol_and_player in
                        list(zip(self.players_symbols, players))}
        self.board_size = board_size
        # I Use range so each row would create a different list in the memory
        self.board = [[" "] * board_size for row in range(self.board_size)]
        self.taken_turns = 0
        self.current_player = random.choice(self.players_symbols)

        while not self.has_game_ended():
            self.take_turn()

    def print_board(self):
        """
        Prints the current board of the game
        """
        first_line = '   ' + ' '.join([str(num) for num in range(self.board_size)]) + '\n'
        board_lines = [str(line_index) + ' ' + '|' + '{}|' * self.board_size + '\n' for line_index in
                       range(self.board_size)]
        final_string = first_line + ('  ' + '-' * (3 * self.board_size - (self.board_size - 1)) + '\n').join(
            board_lines)
        print(final_string.format(*[slot for row in self.board for slot in row]))

    def take_turn(self):
        """
        this function performes several actions:
        - switch the player that has the next turn
        - receive a slot from the player and check if it available
        - positions the players symbol on the board
        """""
        self.print_board()

        if not self.taken_turns == 0:
            self.current_player = self.players_symbols[(self.players_symbols.index(self.current_player) + 1) % 2]

        is_slot_available = False
        while not is_slot_available:
            print('OK {}, Its your turn!'.format(self.players[self.current_player]))
            row_index = int(input("Please enter row number >"))
            column_index = int(input("Please enter column number >"))
            if row_index not in range(self.board_size) or column_index not in range(self.board_size):
                print("You have entered invalid slot numbers, please try again.")
                continue
            elif self.board[row_index][column_index] == " ":
                is_slot_available = True
                self.board[row_index][column_index] = self.current_player
            else:
                print("That slot is not available, please choose again.")

        self.taken_turns += 1

    def has_game_ended(self):
        """
        Check whether a player has one/ the game was tied
        :return: True/False
        """

        if self.taken_turns < (self.board_size * 2 - 1):
            return False

        if self.taken_turns == self.board_size ** 2:
            print("The game has ended with a tie!")
            return True

        if any([self._check_for_winning_sequence(row) for row in self.board]):
            return True

        for column_number in range(self.board_size):
            if self._check_for_winning_sequence([row[column_number] for row in self.board]):
                return True

        left_to_right_diagonal = [self.board[index][index] for index in range(self.board_size)]
        if self._check_for_winning_sequence(left_to_right_diagonal):
            return True

        right_to_left_diagonal = [self.board[self.board_size - 1 - index][index] for index in range(self.board_size)]
        if self._check_for_winning_sequence(right_to_left_diagonal):
            return True

    def _check_for_winning_sequence(self, sequence):
        """
        Check if a specific sequence is comprised of a uniform symbol, and indicates a win.
        :param sequence:
        :return: True/False
        """
        if sequence.count(self.current_player) == self.board_size:
            self.print_board()
            print('The winner is {}'.format(self.players[self.current_player]))
            return True


def main():
    player1 = str(input('Please enter the name of player one >'))
    player2 = str(input('Please enter the name of player two >'))
    players = [player1, player2]
    board_size = int(input('Please enter board size'))
    while board_size < 3:
        print('board size must be bigger than 3')
        board_size = input('Please enter board size')

    XoGame(players, board_size)


if __name__ == "__main__":
    main()
