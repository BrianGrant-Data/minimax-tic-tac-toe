"""
Modeled after: 
- https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py

Note: See references folder
"""

'''Setup Environment
'''

print("hello world!")

from math import inf as infinity
from random import choice
import platform
import time
from os import system


'''Game Objects

HUMAN:
COMP: 
board:
'''

HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


'''Administrative Functions

render()
empty_cells
check_victory()
check_state()
check_valid()
game_over()
clean()
'''

def render(board_state, c_choice, h_choice):
    """

    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in board_state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def empty_cells(board_state):
    """

    """
    cells = []

    for x, row in enumerate(board_state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def check_victory(board_state, player): # based on the original win() function
    """

    """
    win_state = [
        [board_state[0][0], board_state[0][1], board_state[0][2]], # Row Victories
        [board_state[1][0], board_state[1][1], board_state[1][2]],
        [board_state[2][0], board_state[2][1], board_state[2][2]],
        [board_state[0][0], board_state[1][0], board_state[2][0]], # Column Victories
        [board_state[0][1], board_state[1][1], board_state[2][1]],
        [board_state[0][2], board_state[1][2], board_state[2][2]],
        [board_state[0][0], board_state[1][1], board_state[2][2]], # Diagonal Victories
        [board_state[2][0], board_state[1][1], board_state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def check_state(board_state): # based on the original evaluate() function
    """

    """
    if check_victory(board_state, COMP):
        score = +1
    elif check_victory(board_state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def check_valid(x, y): # based on the original valid_move() function
    """

    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def game_over(board_state):
    """

    """
    return check_victory(board_state, HUMAN) or check_victory(board_state, COMP)


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')



'''Artificial Intelligence

minimax()
'''

def minimax(board_state, depth, player):
    """

    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(board_state):
        score = check_state(board_state)
        return [-1, -1, score]

    for cell in empty_cells(board_state):
        x, y = cell[0], cell[1]
        board_state[x][y] = player
        score = minimax(board_state, depth - 1, -player)
        board_state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def minimax1(board_state, depth, player_max, player_min, alpha, beta):
    """
    
    """
    max_score = -infinity # best move/potential boardstate for player1 (thus far found). You start off with infinity in the opposite direction so anything will be better than that
    min_score = +infinity # best move/potential boardstate for player2 (thus far found)

    # For each move available, rerun minimax on the children of those moves but with the opponent as the player

    # 1 Follow the above loop until:
    
    #   - there are no moves available (turn 10) or 
    if depth == 0:
        return board_state
    
    #   - the game has ended
    if game_over(board_state) == True:
        return board_state

    # 2 Score that board state as +1, 0, or -1 using minimax
    score = check_state(board_state)

    # 3a If this is the best option for the opponent save that score and pass it up 
    min_score = (min(min_score, score))

    # 3b If this is the best option for the player save that score and pass it up 
    max_score = (max(max_score, score))


'''Game Actions

take_action()
take_ai_turn()
take_human_turn()
'''

def take_action(x, y, player): # based on the original set_move() function
    """

    """
    if check_valid(x, y):
        board[x][y] = player
        return True
    else:
        print(f"{x}, {y} is an invalid move")
        return False



def take_ai_turn(c_choice, h_choice):
    """

    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    clean() # Why does it run clean() in the middle of this function?
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    take_action(x, y, COMP)
    time.sleep(1)


def take_human_turn(c_choice, h_choice):
    """

    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): ')) # Accepts an turn input from the user
            coord = moves[move] # Checks user's move against the dictionary of valid moves then returns the full coordinates
            can_move = take_action(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
            

'''Main()
'''

def main():
    """
    Main function that calls all functions
    """

    # Setup Game
    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            take_ai_turn(c_choice, h_choice)
            first = ''

        take_human_turn(c_choice, h_choice) # Gathering Player's Move
        take_ai_turn(c_choice, h_choice) # Determine AI's Move

    # Check if Player or AI Won
    if check_victory(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif check_victory(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')

    exit()


'''Press Play
'''

if __name__ == '__main__':
    main()