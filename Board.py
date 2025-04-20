from constants import *
import random

class Board:
  def __init__(self, turn):
    self.state = STATE
    self.whiteKingPos = (7, 4)
    self.blackKingPos = (0, 4)
    
    self.whiteKingMoved = False
    self.blackKingMoved = False
    self.leftWhiteRookMoved = False
    self.rightWhiteRookMoved = False
    self.leftBlackRookMoved = False
    self.rightBlackRookMoved = False
    
    self.moveLog = []
    self.turn = turn
    self.gameOver = None
  
  def score(self, color):
    """
    Returns score of specified player

    Args:
        color (String): color of chess
    
    """
    score = 0
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        piece = self.state[r][c]
        if piece == '--': continue
        
        piece_color, piece_type = piece[0], piece[1]
        piece_score = PIECESCORE[piece_type]
        position_score = 0

        if piece_type == 'p':
            position_score = PIECE_POSITIONS_SCORE[piece_color + 'p'][r][c] * WEIGHT_SCORE['p']
        elif piece_type != 'k':
            position_score = PIECE_POSITIONS_SCORE[piece_type][r][c] * WEIGHT_SCORE[piece_type]

        if piece_color == color:
            score += piece_score + position_score
        else:
            score -=piece_score + position_score
    
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for r, c in center_squares:
      piece = self.state[r][c]
      if piece != '--' and piece[0] == color:
          score += CENTER_CONTROL_BONUS
      elif piece != '--' and piece[0] != color:
          score -= CENTER_CONTROL_BONUS
          
    player_moves = 0
    opponent_moves = 0
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        if self.state[r][c] != '--':
          moves = self.get_piece_moves(r, c)
          if self.state[r][c][0] == color:
            player_moves += len(moves)
          else:
            opponent_moves += len(moves)
    score += player_moves * MOBILITY_BONUS
    score -= opponent_moves * MOBILITY_BONUS
    
    if self.in_check(color):
      score -= CHECK_BONUS
    if self.in_check('b' if color == 'w' else 'w'):
      score += CHECK_BONUS
        
    king_pos = self.whiteKingPos if color == 'w' else self.blackKingPos
    if king_pos:
      r, c = king_pos
      if 2 <= r <= 5 and 2 <= c <= 5:
        score += KING_SAFETY_PENALTY
      if (r in [0, 7] and c in [0, 7]):
        score -= KING_SAFETY_PENALTY
        
    return score
  
  def rules(self, piece):
    """
    Returns possible directions of each piece (just capture move for pawns)

    Args:
        piece (String): type of piece

    """
    directions = []
    
    if piece in ['wp']: # White Pawn
      directions = [(-1, -1), (-1, 1)]
      
    elif piece in ['bp']: # Black Pawn
      directions = [(1, -1), (1, 1)]
      
    elif piece in ['wb', 'bb']:  # Bishop
      directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
      
    elif piece in ['wn', 'bn']: # Knight
      directions = [
        (-1, 2), (-2, 1), (1, 2), (2, 1),
        (-1, -2), (-2, -1), (1, -2), (2, -1)
      ]
      
    elif piece in ['wr', 'br']:  # Rook
      directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
      
    elif piece in ['wk', 'bk', 'wq', 'bq']:  # King, Queen
      directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0),   (1, 1)
      ]
      
    return directions
  
  def random_promote(self, promote_to=None):
    """
    Returns random promoted piece if not specified

    Args:
        promote_to (String, optional): type of piece. Defaults to None.

    """
    if promote_to is not None and promote_to not in ['q', 'n', 'r', 'b']:
      return self.random_promote('q')
    return ['q', 'n', 'r', 'b'][random.randint(0, 3)] if promote_to is None else promote_to
  
  def promotion(self, row, col, color, player_choice=False):
    """
    Returns new state of the board after promote pawn

    Args:
        row (Int): row
        col (Int): column
        color (String): color of chess
        player_choice (bool, optional): True if it is the player's turn. Defaults to False.

    """
    if (row == 0 or row == 7) and self.state[row][col][1] == 'p':
      choice = 'q'
      
      if player_choice:
        choice = input("Promote pawn to: Queen (q), Knight (n), Rook (r), Bishop (b)")
        if choice not in ['q', 'n', 'r', 'b']:
          choice = self.random_promote()
        
      self.state[row][col] = color + choice
        
    return self.state
  
  def is_square_attacked(self, r, c, player):
    """
    Kiểm tra xem ô (r, c) có bị quân địch tấn công không.
    """
    opponent = 'b' if player == 'w' else 'w'
    for row in range(DIMENSION):
      for col in range(DIMENSION):
        if self.state[row][col][0] == opponent:
          moves = self.get_piece_moves(row, col)
          if (r, c) in moves:
            return True
    return False
  
  def can_castling(self, side, player):
    # CHECK IS MOVED
    if player == "w":
      if self.whiteKingMoved:
        return False
      if side == "left" and self.leftWhiteRookMoved:
        return False
      if side == "right" and self.rightWhiteRookMoved:
        return False
    else:
      if self.blackKingMoved:
        return False
      if side == "left" and self.leftBlackRookMoved:
        return False
      if side == "right" and self.rightBlackRookMoved:
        return False

    if self.in_check(player):
        return False
    
    # CHECK ANY PIECE IN BETWEEN
    if player == "w":
      king_pos = self.whiteKingPos
      if side == "right":
        if any(self.state[7][i] != '--' for i in range(5, 7)):
          return False
      else:
        if any(self.state[7][i] != '--' for i in range(1, 4)):
          return False
    else:
      king_pos = self.blackKingPos
      if side == "right":
        if any(self.state[0][i] != '--' for i in range(5, 7)):
          return False
      else:
        if any(self.state[0][i] != '--' for i in range(1, 4)):
          return False
        
    if side == "right":
      squares_to_check = [(king_pos[0], 5), (king_pos[0], 6)]
    else:
      squares_to_check = [(king_pos[0], 3), (king_pos[0], 2)]
    for square in squares_to_check:
      if self.is_square_attacked(square[0], square[1], player):
        return False
    
    return True
  
  def castling(self, r1, c1, r2, c2):
    piece = self.state[r1][c1]
    player = piece[0]
    
    if piece[1] != 'k':
      return False
    
    if player == 'w':
      if self.whiteKingMoved:
        return False
      if c2 == 2:
        self.state[7][2] = 'wk'
        self.state[7][4] = '--'
        self.state[7][3] = 'wr'
        self.state[7][0] = '--'
        self.whiteKingMoved = True
        self.leftWhiteRookMoved = True
        self.whiteKingPos = (7, 2)
        self.next_turn()
        return True
      elif c2 == 6:
        self.state[7][6] = 'wk'
        self.state[7][4] = '--'
        self.state[7][5] = 'wr'
        self.state[7][7] = '--'
        self.whiteKingMoved = True
        self.rightWhiteRookMoved = True
        self.whiteKingPos = (7, 6)
        self.next_turn()
        return True
    elif player == 'b':
      if self.blackKingMoved:
        return False
      if c2 == 2:
        self.state[0][2] = 'bk'
        self.state[0][4] = '--'
        self.state[0][3] = 'br'
        self.state[0][0] = '--'
        self.blackKingMoved = True
        self.leftBlackRookMoved = True
        self.blackKingPos = (0, 2)
        self.next_turn()
        return True
      elif c2 == 6:
        self.state[0][6] = 'bk'
        self.state[0][4] = '--'
        self.state[0][5] = 'br'
        self.state[0][7] = '--'
        self.blackKingMoved = True
        self.rightBlackRookMoved = True
        self.blackKingPos = (0, 6)
        self.next_turn()
        return True
    
    return False
  
  def get_piece_moves(self, r, c):
    """
    Returns all posible moves of specified piece.

    Args:
        r (Int): row
        c (Int): column

    """
    piece = self.state[r][c]
    moves = []
    
    if piece == '--':
      return moves
    
    piece_color = piece[0]
    piece_type = piece[1]
    
    # FORWARD MOVE FOR PAWNS
    if piece_type == 'p':
      dr = -1 if piece_color == 'w' else 1
      
      new_r = r + dr
      if 0 <= new_r < DIMENSION and self.state[new_r][c] == '--':
        moves.append((new_r, c))
        
        # START POSITION OF WHITE & BLACK PAWNS
        start_rank = 6 if piece_color == 'w' else 1
        if r == start_rank:
          new_r = r + 2*dr
          if 0 <= new_r < DIMENSION and self.state[new_r][c] == '--':
            moves.append((new_r, c))
    
    directions = self.rules(piece)
        
    for dr, dc in directions:
      new_r, new_c = dr + r, dc + c
      if (new_r < 0 or new_r >= DIMENSION) or (new_c < 0 or new_c >= DIMENSION):
        continue
      
      captured_piece = self.state[new_r][new_c]
      
      if piece_type in ['n', 'k']:
        if captured_piece == '--' or captured_piece[0] != piece_color:
          moves.append((new_r, new_c))
          
      elif piece_type == 'p':
        if captured_piece != '--' and captured_piece[0] != piece_color:
          moves.append((new_r, new_c))
      
      else:
        while 0 <= new_r < DIMENSION and 0 <= new_c < DIMENSION:
          if self.state[new_r][new_c] == '--':
            moves.append((new_r, new_c))
          
          elif self.state[new_r][new_c][0] != piece_color:
            moves.append((new_r, new_c))
            break
          
          else: break
          
          new_r += dr
          new_c += dc
    
    return moves
  
  def get_all_moves(self, player):
    """
    Returns all possible move of specified player (include not in check after move)

    Args:
        player (String): color of chess

    """
    valid_moves = []
    raw_moves = []
    
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        if self.state[r][c][0] == player:
          for move in self.get_piece_moves(r, c):
            raw_moves.append(((r, c), move))
    
    for move in raw_moves:
      if not self.in_check_after_move(move[0], move[1], player):
        valid_moves.append(move)
          
    return valid_moves
  
  def next_turn(self):
    self.turn = 'b' if self.turn == 'w' else 'w'
  
  def make_move(self, from_pos, to_pos, auto_promotion=False, flag=True):
    """
    Makes specified piece move from current position to new position.

    Args:
        from_pos (Tuple): current position (row, column)
        to_pos (Tuple): new position (row, column)
        player_choice (bool, optional): Player choose pawn in order to promote to new piece. Defaults to False.
        flag (bool, optional): check game over. Defaults to True.
        
    """
    r1, c1 = from_pos
    r2, c2 = to_pos
    piece = self.state[r1][c1]
    
    move_info = {
      'from': (r1, c1),
      'to': (r2, c2),
      'piece': piece,
      'captured': self.state[r2][c2],
      'turn': self.turn,
      'whiteKingPos': self.whiteKingPos,
      'blackKingPos': self.blackKingPos
    }
    self.moveLog.append(move_info)
    
    if auto_promotion and piece[1] == 'p' and r2 in [0, 7]:
      self.state[r2][c2] = piece[0] + 'q'
    else:
      self.state[r2][c2] = piece
    self.state[r1][c1] = '--'
    
    if self.state[r2][c2][1] == 'k':
      if self.state[r2][c2][0] == 'w':
        self.whiteKingPos = (r2, c2)
      else:
        self.blackKingPos = (r2, c2)
    
    self.next_turn()
    if flag: self.game_over()
    
    return self.state
  
  def unmake_move(self):
    """
    Restores the current move.

    Args:
        from_pos (Tuple): old position (row, column)
        to_pos (_type_): current position (row, column)

    """
    move_info = self.moveLog.pop()
    r1, c1 = move_info['from']
    r2, c2 = move_info['to']
    
    self.state[r1][c1] = move_info['piece']
    self.state[r2][c2] = move_info['captured']
    
    self.whiteKingPos = move_info['whiteKingPos']
    self.blackKingPos = move_info['blackKingPos']
    
    self.turn = move_info['turn']
    self.gameOver = None
    
    return self.state
  
  def enemy_at_pos(self, pos, player):
    """
    Returns: True if enemy in the position else False

    Args:
        pos (Tuple): the selected position
        player (String): color of chess

    """
    r, c = pos[0], pos[1]
    piece = self.state[r][c]
    
    if 0 <= r < DIMENSION and 0 <= c < DIMENSION and piece != '--' and piece[0] != player:
      return True
    return False
  
  def in_check(self, player):
    """
    Returns: True if player of specified color is in check

    Args:
        player (String): color of chess

    """
    king_pos = self.blackKingPos if player == 'b' else self.whiteKingPos
    
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        if not self.enemy_at_pos((r, c), player): continue
        
        for move in self.get_piece_moves(r, c):
          if move[0] == king_pos[0] and move[1] == king_pos[1]:
            return True
          
    return False
        
  def in_check_after_move(self, from_pos, to_pos, player):
    """
    Returns True if player of specified color is in check after a move from source to dest

    Args:
        from_pos (Tuple): source position
        to_pos (Tuple): destination position
        player (String): color of chess
        
    """
    self.make_move(from_pos, to_pos, flag=False)
    in_check = self.in_check(player)
    self.unmake_move()
    
    return in_check
  
  def game_over(self):
    """
    Checks for checkmate or stalemate status of board
    
    """
    legal_moves = 0
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        piece = self.state[r][c]
        if piece != '--' and piece[0] == self.turn:
          moves = self.get_piece_moves(r, c)
          for move in moves:
            if not self.in_check_after_move((r, c), move, self.turn):
              legal_moves += 1
              
    opponent = 'BLACK' if self.turn == 'w' else 'WHITE'
    if legal_moves == 0 and not self.in_check(self.turn):
      self.gameOver = ("Stalemate", None)
    elif legal_moves == 0:
      self.gameOver = ("Checkmate", opponent)
    
    insufficent_mate = self.insufficient_material()
    if insufficent_mate is not None:
      self.gameOver = insufficent_mate
  
  def insufficient_material(self):
    piece_counts = {"wminor": 0, "bminor": 0, "king": 0, "wknight": 0, "bknight": 0}
    for r in range(8):
      for c in range(8):
        piece = self.state[r][c]
        if piece:
        # if a Queen is present, insufficient material is impossible
          if piece[1] == 'q':
            return None
          if piece[1] == 'k':
            piece_counts["king"] += 1
          elif piece[1] == 'n' and piece[0] == 'w':
            piece_counts["wknight"] += 1
          elif piece[1] == 'n' and piece[0] == 'b':
            piece_counts["bknight"] += 1
          else:
            if piece[0] == 'w':
              piece_counts["wminor"] += 1
            elif piece[0] == 'b':
              piece_counts["bminor"] += 1

    # King vs King
    if piece_counts["wminor"] == piece_counts["bminor"] == piece_counts["wknight"] == piece_counts["bknight"] == 0 and piece_counts["king"] == 2:
      return ("Insufficient Material", None)
    # King + minor piece vs King
    elif ((piece_counts["wminor"] == 1 and piece_counts["bminor"] == 0) or (piece_counts["bminor"] == 1 and piece_counts["wminor"] == 0)) and piece_counts["king"] == 2 and piece_counts["bknight"] == piece_counts["wknight"] == 0:
      return ("Insufficient Material", None)
    # King + two Knights vs King
    elif (piece_counts["wknight"] == 2 and piece_counts["king"] == 2 and piece_counts["wminor"] == piece_counts["bminor"] == 0) or (piece_counts["bknight"] == 2 and piece_counts["king"] == 2 and piece_counts["wminor"] == piece_counts["bminor"] == 0):
      return ("Insufficient Material", None)
    elif (piece_counts["wminor"] == 1 and piece_counts["king"] == 2 and piece_counts["bminor"] == 0) or (piece_counts["bminor"] == 1 and piece_counts["king"] == 2 and piece_counts["wminor"] == 0):
      return ("Insufficient Material", None)
      
    return None