import random

class RandomAgent:
  def get_move(self, board, color):
    valid_moves = board.get_all_moves(color)
    if not valid_moves:
        return None
    return random.choice(valid_moves)
