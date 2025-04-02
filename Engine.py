from constants import *
from Minimax import Minimax

class Engine:
  def __init__(self, method):
    self.method = method
  
  def ai_move(self, board, player):
    if type(self.method) is Minimax:
      move, _ = self.method.minimax(board, DEPTH, MIN, MAX, player)
      return move
      