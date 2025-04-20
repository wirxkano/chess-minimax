from constants import *

class Minimax:
  def __init__(self):
    pass
  
  def evaluate(self, board, color):
    if board.gameOver:
      if board.gameOver[0] == 'Checkmate':
        winner = board.gameOver[1]
        if (winner == 'WHITE' and color == 'w') or (winner == 'BLACK' and color == 'b'):
          return CHECKMATE  # color win
        else:
          return -CHECKMATE  # color lose
      return 0  # Stalemate

    return board.score(color)
    
  def minimax(self, board, depth, alpha, beta, color):
    if depth == 0 or board.gameOver:
      return None, self.evaluate(board, color)
    
    valid_moves = board.get_all_moves(color)
    
    if not valid_moves:
      if board.in_check(color):
        return None, -CHECKMATE
      return None, 0
      
    best_move = None
    best_value = -CHECKMATE
    
    for move in valid_moves:
      board.make_move(move[0], move[1], auto_promotion=True)
      _, value = self.minimax(board, depth-1, -beta, -alpha, 'w' if color == 'b' else 'b')
      value = - value
      board.unmake_move()
      
      if value > best_value:
        best_value = value
        best_move = move
      
      alpha = max(alpha, best_value)
      if alpha >= beta:
        break
          
    return best_move, best_value
  