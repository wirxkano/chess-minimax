from constants import *
from Minimax import Minimax
from RandomAgent import RandomAgent

class Engine:
  def __init__(self, method, depth):
    self.method = method
    self.depth = depth
  
  def move(self, board, color):
    if type(self.method) is Minimax:
      move, _ = self.method.minimax(board, self.depth, -CHECKMATE, CHECKMATE, color)
      return move
    
    elif type(self.method) is RandomAgent:
      return self.method.get_move(board, color)
      