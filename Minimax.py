from constants import *

class Minimax:
  def __init__(self):
    pass
  
  def evaluate(self, board, player):
    bscore = board.score('b')
    wscore = board.score('w')
    return bscore - wscore if player == 'b' else wscore - bscore
    
  def minimax(self, board, depth, alpha, beta, player):
    if depth == 0 or board.gameOver:
      return None, self.evaluate(board, player)
    
    valid_moves = board.get_all_moves(player)
    
    if not valid_moves:
      if board.in_check(player):
        return None, MIN
      return None, 0
      
    best_move = None
    best_value = MIN
    
    for move in valid_moves:
      board.make_move(move[0], move[1])
      _, value = self.minimax(board, depth-1, -beta, -alpha, 'w' if player == 'b' else 'b')
      value = - value
      board.unmake_move(move[0], move[1])
      
      if value > best_value:
        best_value = value
        best_move = move
      
      alpha = max(alpha, best_value)
      if alpha >= beta:
        break
          
    return best_move, best_value
  