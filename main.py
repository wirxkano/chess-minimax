import sys
import copy
import pygame as pg
from Gui import Gui
from Board import Board
from Engine import Engine
from Minimax import Minimax
from constants import *

def printUsage():
    print("Person vs Agent run command: python main.py 1 0 <difficulty>")
    print("Person vs Person run command: python main.py 1 1")
    print("Difficulty options: easy, medium, hard")

def chess_label(pos):
    row, col = pos
    letters = 'abcdefgh'
    numbers = '12345678'
    column_label = letters[col]
    row_label = numbers[7 - row]
    return f"{row_label}{column_label}"

def main(argv):
    if len(argv) < 2:
        printUsage()
        return
    if argv[1] == '0' and len(argv) < 3:
        print("Please specify difficulty: easy, medium, or hard")
        printUsage()
        return

    difficulty = None
    if argv[1] == '0':
        difficulty = argv[2].lower()
        if difficulty not in DIFFICULTY_LEVELS:
            print("Invalid difficulty. Choose: easy, medium, hard")
            return
        depth = DIFFICULTY_LEVELS[difficulty]
    else:
        depth = DIFFICULTY_LEVELS['medium']  # Default for Agent vs Agent

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Chess Ranger")
    clock = pg.time.Clock()
    screen.fill("black")
    font = pg.font.Font('freesansbold.ttf', 12)

    print("Press space to find next step, press 'N' to start new game!")

    current_player = 'w' if argv[1] == '0' else 'b'
    selected = None
    running = True

    gui = Gui()
    gui.load_images()  # Load images once after Gui is created
    board = Board(current_player)
    engine = Engine(Minimax())
    state = STATE

    valid_moves = []  # To store valid moves for highlighting
    king_in_check = None  # To store king's position when in check

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # AGENT MOVE
            if current_player == 'b' and argv[1] == '0':
                virtual_board = copy.deepcopy(board)
                agent_move = engine.ai_move(virtual_board, current_player)
                if agent_move is None:
                    if board.gameOver:
                        print(board.gameOver)
                        running = False
                    continue
                state = board.make_move(agent_move[0], agent_move[1])
                row, col = agent_move[1]
                # Handle pawn promotion for agent
                if board.state[row][col][1] == 'p' and (row == 0 or row == 7):
                    state = board.promotion(row, col, current_player, player_choice=False)
                print(f'Agent performs move from {chess_label(agent_move[0])} to {chess_label(agent_move[1])}')
                current_player = 'w'

            elif event.type == pg.MOUSEBUTTONDOWN:
                # PERSON MOVE
                pos = pg.mouse.get_pos()
                row, col = pos[1] // CELL_SZ, pos[0] // CELL_SZ

                if selected:
                    moves = board.get_piece_moves(selected[0], selected[1])

                    if (row, col) in moves:
                        state = board.make_move(selected, (row, col), player_choice=True)
                        piece = board.state[row][col]
                        # Handle pawn promotion via GUI for human player
                        if piece[1] == 'p' and (row == 0 or row == 7):
                            choice = gui.promote_pawn(screen, row, col, current_player)
                            board.state[row][col] = current_player + choice
                        current_player = 'b' if current_player == 'w' else 'w'
                        print(f"{'White' if current_player == 'w' else 'Black'}'s turn")
                        if board.gameOver:
                            print(board.gameOver)
                            running = False
                        selected = None
                        valid_moves = []
                    else:
                        # If clicking another piece of the same player, reselect
                        if state[row][col] != "--" and state[row][col][0] == current_player:
                            selected = (row, col)
                            valid_moves = board.get_piece_moves(row, col)
                        else:
                            selected = None
                            valid_moves = []
                else:
                    if state[row][col] != "--" and state[row][col][0] == current_player:
                        selected = (row, col)
                        valid_moves = board.get_piece_moves(row, col)
                    else:
                        selected = None
                        valid_moves = []

        # Check if the current player's king is in check
        if board.in_check(current_player):
            king_pos = board.whiteKingPos if current_player == 'w' else board.blackKingPos
            king_in_check = king_pos
        else:
            king_in_check = None

        # RENDER GAME
        gui.draw_board(screen, selected, valid_moves, king_in_check)
        gui.draw_pieces(screen)
        gui.draw_labels(screen, font)
        pg.display.flip()

        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main(sys.argv[1:])
