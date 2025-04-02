import sys
import copy
from Gui import *
from Board import Board
from Engine import Engine
from Minimax import Minimax

def printUsage():
  print("Person vs Agent run command: python main.py 0")
  print("Agent vs Agent run command: python main.py 1")

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
  
  p.init()
  screen = p.display.set_mode((WIDTH, HEIGHT))
  p.display.set_caption("Chess Ranger")
  clock = p.time.Clock()
  screen.fill("black")
  font = p.font.Font('freesansbold.ttf', 12)
    
  print("Press space to find next step, press 'N' to start new game!")
  
  current_player = 'w' if argv[1] == '0' else 'b'
  selected = None
  running = True
   
  gui = Gui()
  board = Board(current_player)
  engine = Engine(Minimax())
  state = STATE
    
  while running:
    for event in p.event.get():
      if event.type == p.QUIT:
        running = False
      
      # AGENT
      if current_player == 'b' and argv[0] == '0':
        virtual_board = copy.deepcopy(board)
        agent_move = engine.ai_move(virtual_board, current_player)
        if agent_move is None:
          if board.gameOver:
            print(board.gameOver)
            running = False
            return
        state = board.make_move(agent_move[0], agent_move[1])
        state = board.promotion(agent_move[1][0], agent_move[1][1], current_player)
        print(f'Agent perform move from {agent_move[0]} to {agent_move[1]}')
        
        current_player = 'w'
      elif event.type == p.MOUSEBUTTONDOWN:
        # PERSON
        pos = p.mouse.get_pos()
        row, col = pos[1] // CELL_SZ, pos[0] // CELL_SZ
        
        if selected:
          moves = board.get_piece_moves(selected[0], selected[1])
          
          if (row, col) in moves and not board.in_check_after_move(selected, (row, col), current_player):
            state = board.make_move(selected, (row, col), player_choice=True)
            state = board.promotion(row, col, current_player, player_choice=True)
              
            current_player = 'b' if current_player == 'w' else 'w'
            print(f"{'White' if current_player == 'w' else 'Black'}'s turn")
              
            if board.gameOver:
              print(board.gameOver)
              running = False
              
            selected = None
              
          elif state[row][col] != "--" and state[row][col][0] == current_player:
            selected = (row, col)
            
          else: selected = None
          
        elif state[row][col] != "--":
          piece_color = state[row][col][0]
            
          if piece_color == current_player:
            if board.in_check(current_player):
              possible_move = board.get_all_moves(current_player)
              if (row, col) not in possible_move:
                print("You are in check")
              else:
                selected = (row, col)
            
            selected = (row, col)
          else:
            print(f"It's {'White' if current_player == 'w' else 'Black'}'s turn")

      # RENDER GAME
      gui.load_images()
      gui.draw_board(screen, selected)
      gui.draw_pieces(screen)
      p.display.flip()

      clock.tick(60)

if __name__ == '__main__':
  main(sys.argv[1:])