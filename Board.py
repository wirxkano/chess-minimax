from constants import *

class Board:
  def __init__(self, turn):
    self.state = STATE
    self.whiteKingPos = (7, 4)
    self.blackKingPos = (0, 4)
    self.prevPiece = '--'
    self.turn = turn
    self.gameOver = None
  
  def score(self, player):
    score = 0
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        piece = self.state[r][c]
        if piece[0] != player: continue
        
        piece_position_score = 0
        if piece[1] == 'p':
          piece_position_score = PIECE_POSITIONS_SCORE[player + 'p'][r][c] * WEIGHT_SCORE['p']
        elif piece[1] != 'k':
          piece_position_score = PIECE_POSITIONS_SCORE[piece[1]][r][c] * WEIGHT_SCORE[piece[1]]
          
        score += PIECESCORE[piece[1]] + piece_position_score
        
    return score
  
  def rules(self, piece):
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
  
  def get_piece_moves(self, r, c):
    piece = self.state[r][c]
    moves = []
    
    if piece == '--':
      return moves
    
    piece_color = piece[0]
    piece_type = piece[1]
    
    # forward move for pawns
    if piece_type == 'p':
      dr = -1 if piece_color == 'w' else 1
      
      new_r = r + dr
      if 0 <= new_r < DIMENSION and self.state[new_r][c] == '--':
        if new_r == 0 or new_r == 7:
          moves.extend([(new_r, c, promo) for promo in ['q', 'r', 'b', 'n']])
        else:
          moves.append((new_r, c))
        
        # position of white and black pawns
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
    all_moves = []
    
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        if self.state[r][c][0] == player:
          for move in self.get_piece_moves(r, c):
            if not self.in_check_after_move((r, c), move, player):
              all_moves.append(((r, c), move))
           
    return all_moves
  
  def next_turn(self):
    self.turn = 'b' if self.turn == 'w' else 'w'
  
  def make_move(self, from_pos, to_pos, flag=True):
    r1, c1 = from_pos
    if len(to_pos) == 3:
      r2, c2, special = to_pos
    else:
      r2, c2 = to_pos
      special = None
    
    self.prevPiece = self.state[r2][c2]
    piece = self.state[r1][c1]
    
    if special in ['q', 'r', 'b', 'n']:
      self.state[r2][c2] = piece[0] + special
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
  
  def unmake_move(self, from_pos, to_pos):
    r1, c1 = from_pos
    if len(to_pos) == 3:
      r2, c2, special = to_pos
    else:
      r2, c2 = to_pos
      special = None
    
    self.state[r1][c1] = self.state[r2][c2]
    self.state[r2][c2] = self.prevPiece
    
    if self.state[r1][c1][1] == 'k':
      if self.state[r1][c1][0] == 'w':
        self.whiteKingPos = (r1, c1)
      else:
        self.blackKingPos = (r1, c1)
    
    self.next_turn()
    
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
    self.unmake_move(from_pos, to_pos)
    
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
    piece_counts = {"wk": 0, "bk": 0, "wn": 0, "bn": 0, "wb": 0, "bb": 0, "wr": 0, "br": 0, "wq": 0, "bq": 0, "wp": 0, "bp": 0}
    
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        piece = self.state[r][c]
        if piece != '--':
          piece_counts[piece] += 1
    
    total_pieces = sum(piece_counts.values())
    if total_pieces == 2 and piece_counts["wk"] == 1 and piece_counts["bk"] == 1:
      return ("Insufficient Material", None)  # King vs King
    if total_pieces == 3 and piece_counts["wk"] == 1 and piece_counts["bk"] == 1 and (piece_counts["wn"] == 1 or piece_counts["bn"] == 1 or piece_counts["wb"] == 1 or piece_counts["bb"] == 1):
      return ("Insufficient Material", None)  # King vs King + minor piece
    
    return None