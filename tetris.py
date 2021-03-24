from random import choice, randrange
from copy import deepcopy

# CONSTANTS
# user inputs
LEFT = 'a'
RIGHT = 'd'
COUNTERCLOCKWISE = 'w'
CLOCKWISE = 's'
# need to add an option if the user does not want to make a move or quit the game
NO_MOVE = 'e'
QUIT = 'q'

# board
GAME_AREA_SIZE = 20
# board size is bigger than game area because of the walls
BOARD_X_SIZE = 22
BOARD_Y_SIZE = 21
# board coordinates:
# x = 0 at the top left
# y = 0 at the top

# pieces
PIECES = [
    [[1], [1], [1], [1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[0, 1],
     [1, 1],
     [1, 0]],

    [[1, 1],
     [1, 1]]
]


def create_board():
    board = [[0 for _ in range(BOARD_X_SIZE)] for _ in range(BOARD_Y_SIZE)]

    for i in range(BOARD_Y_SIZE):
        board[i][0] = 1
        board[i][-1] = 1
    for index, elem in enumerate(board[-1]):
        board[-1][index] = 1
    return board


def get_piece():
    return choice(PIECES)


def get_piece_pos(piece):
    piece_size = len(piece)
    # the piece is located at the top of the board
    y = 0
    x = randrange(1, BOARD_X_SIZE - piece_size)
    return [x, y]


def print_board(board, piece, position, error=''):
    # the board needs to be copied to prevent the piece from leaving a trace
    # it won't be copied only in the case of merging the piece and board
    copied_board = deepcopy(board)
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            copied_board[position[1] + i][position[0] + j] = piece[i][j] or copied_board[position[1] + i][
                position[0] + j]

    for i in range(BOARD_Y_SIZE):
        for j in range(BOARD_X_SIZE):
            if copied_board[i][j] == 1:
                print("*", end='')
            else:
                print(" ", end='')
        print("")

    print(error)


def fix_piece_on_board(board, piece, position):
    # the function is the same as in printing the board except the board is not copied to fix the piece
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            board[position[1] + i][position[0] + j] = piece[i][j] or board[position[1] + i][position[0] + j]
    # TODO: add the row completion functionality


def print_instructions():
    # function for printing the instruction, to make the play function more clear
    print("GAME CONTROLS:")
    print("• a (return): move piece left")
    print("• d (return): move piece right")
    print("• w (return): rotate piece counter clockwise")
    print("• s (return): rotate piece clockwise")
    print("• e (return): move down")
    print("• q (return): quit game")


# MOVES
def move_left(position):
    # moving left means that the "x" position is decremented
    changed_pos = [position[0] - 1, position[1]]
    return changed_pos


def move_right(position):
    # moving right means that the "x" position is incremented
    changed_pos = [position[0] + 1, position[1]]
    return changed_pos


def move_down(position):
    # moving down means that the "y" position is incremented
    changed_pos = [position[0], position[1] + 1]
    return changed_pos


def clockwise(piece):
    # zipping reversed piece results in the piece being turned clockwise - it is something i found on stack overflow
    copied_piece = deepcopy(piece)
    reversed_piece = zip(*copied_piece[::-1])
    return list(reversed_piece)


def counterclockwise(piece):
    # rotating the piece clockwise three times is the same as turning it counterclockwise
    copied_piece = deepcopy(piece)
    reversed_piece = clockwise(copied_piece)
    reversed_piece = clockwise(reversed_piece)
    return clockwise(reversed_piece)


def overlap(board, piece, position):
    # True if is not overlapping, false if is overlapping
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            if board[position[1] + i][position[0] + j] == 1 and piece[i][j] == 1:
                return False
    return True


# MOVE POSSIBILITY TESTING
# simulate the move and check if the pice will overlap with anything on the board
def left_move_possible(board, piece, position):
    position = move_left(position)
    return overlap(board, piece, position)


def right_move_possible(board, piece, position):
    position = move_right(position)
    return overlap(board, piece, position)


def down_move_possible(board, piece, position):
    position = move_down(position)
    return overlap(board, piece, position)


def clockwise_possible(board, piece, position):
    piece = clockwise(piece)
    return overlap(board, piece, position)


def counterclockwise_possible(board, piece, position):
    piece = counterclockwise(piece)
    return overlap(board, piece, position)


def game_on(board, piece, position):
    if not down_move_possible(board, piece, position) and position[1] == 0:
        return False
    return True


def play():
    print("Welcome to TETRIS - cmd version")
    print_instructions()
    board = create_board()
    piece = get_piece()
    position = get_piece_pos(piece)
    print_board(board, piece, position)

    move = input()

    while game_on(board, piece, position):
        error = ""
        down_move = False
        if move == RIGHT:
            if right_move_possible(board, piece, position):
                position = move_right(position)
                down_move = True
            else:
                error = "Right move not possible"
        elif move == LEFT:
            if left_move_possible(board, piece, position):
                position = move_left(position)
                down_move = True
            else:
                error = "Left move not possible"
        elif move == CLOCKWISE:
            if clockwise_possible(board, piece, position):
                piece = clockwise(piece)
                down_move = True
            else:
                error = "Clockwise turn not possible"
        elif move == COUNTERCLOCKWISE:
            if counterclockwise_possible(board, piece, position):
                piece = counterclockwise(piece)
                down_move = True
            else:
                error = "Counterclockwise turn not possible"
        elif move == NO_MOVE or move == "":
            down_move = True
        elif move == QUIT:
            print('Thank you for playing')
            quit(0)
        else:
            error = "Please enter a valid move"

        if down_move and down_move_possible(board, piece, position):
            position = move_down(position)

        if not down_move_possible(board, piece, position):
            fix_piece_on_board(board, piece, position)
            piece = get_piece()
            position = get_piece_pos(piece)

        print_board(board, piece, position, error=error)

        move = input()
    print('game over')


if __name__ == "__main__":
    play()
