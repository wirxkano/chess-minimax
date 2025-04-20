import pygame as p
from constants import *

class Gui:
  def __init__(self):
    self.state = STATE
    
  def load_images(self):
    pieces = ['bb', 'bk', 'bn', 'bp', 'bq', 'br', 'wb', 'wk', 'wn', 'wp', 'wq', 'wr']
    for piece in pieces:
      IMAGES[piece] = p.transform.scale(p.image.load('pieces/' + piece + '.png'), (CELL_SZ, CELL_SZ))
  
  def draw_board(self, screen, selected=None, valid_moves=None, king_in_check=None):
    """
    Draws the chessboard with highlights for selected squares, valid moves,
    and king in check.

    Args:
        screen: Pygame screen object.
        selected (tuple, optional): (row, col) of the selected piece.
        valid_moves (list, optional): List of (row, col) tuples for valid moves.
        king_in_check (tuple, optional): (row, col) of the king in check.
    """
    if valid_moves is None:
        valid_moves = []
    
    # Draw the checkered board
    cnt = 0
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if cnt % 2 == 0:
                p.draw.rect(screen, p.Color(238, 238, 210, 255),
                           [CELL_SZ * j, CELL_SZ * i, CELL_SZ, CELL_SZ])
            else:
                p.draw.rect(screen, p.Color(118, 150, 86, 255),
                           [CELL_SZ * j, CELL_SZ * i, CELL_SZ, CELL_SZ])
            cnt += 1
        cnt -= 1
    
    # Highlight valid moves in yellowish
    for move in valid_moves:
        row, col = move
        highlight_rect = p.Rect(col * CELL_SZ, row * CELL_SZ, CELL_SZ, CELL_SZ)
        p.draw.rect(screen, p.Color(255, 255, 100, 100), highlight_rect)
    
    # Highlight king in check in reddish
    if king_in_check:
        row, col = king_in_check
        highlight_rect = p.Rect(col * CELL_SZ, row * CELL_SZ, CELL_SZ, CELL_SZ)
        p.draw.rect(screen, p.Color(255, 100, 100, 100), highlight_rect)
    
    # Highlight selected square in yellow (drawn last to stay on top)
    if selected:
        sr, sc = selected
        highlight_rect = p.Rect(sc * CELL_SZ, sr * CELL_SZ, CELL_SZ, CELL_SZ)
        p.draw.rect(screen, p.Color(255, 255, 0, 100), highlight_rect)
  
  def draw_pieces(self, screen):
    for i in range(DIMENSION):
      for j in range(DIMENSION):
        piece = self.state[i][j]
        if piece != '--':
          screen.blit(IMAGES[piece], p.Rect(j * CELL_SZ, i * CELL_SZ, CELL_SZ, CELL_SZ))
          
  def draw_labels(self, screen, font):
    letters = 'abcdefgh'
    numbers = '12345678'

    for col in range(DIMENSION):
      text = font.render(letters[col], True, p.Color('black'))
      x = col * CELL_SZ + CELL_SZ // 2 - text.get_width() // 2
      y = HEIGHT - text.get_height()
      screen.blit(text, (x, y))

    for row in range(DIMENSION):
      text = font.render(numbers[7 - row], True, p.Color('black'))
      x = WIDTH - text.get_width()
      y = row * CELL_SZ + CELL_SZ // 2 - text.get_height() // 2
      screen.blit(text, (x, y))
      
  def promote_pawn(self, screen, row, col, color):
    """
    Displays a GUI menu for pawn promotion and returns the chosen piece type.

    Args:
        screen: Pygame screen object.
        row (int): Row where the pawn is promoted.
        col (int): Column where the pawn is promoted.
        color (str): 'w' or 'b' for the player’s color.

    Returns:
        str: 'q', 'r', 'n', or 'b' representing the chosen piece.
    """
    # Semi-transparent overlay
    overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Promotion options
    pieces = ['q', 'r', 'n', 'b']  # Queen, Rook, Knight, Bishop
    piece_images = [f'{color}{piece}' for piece in pieces]
    box_width = CELL_SZ * 4
    box_height = CELL_SZ
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2
    
    # Draw promotion menu
    p.draw.rect(screen, p.Color('white'), (box_x, box_y, box_width, box_height))
    for i, piece in enumerate(piece_images):
        screen.blit(IMAGES[piece], (box_x + i * CELL_SZ, box_y))
    
    p.display.flip()
    
    # Wait for user selection
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                exit()
            if event.type == p.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if box_y <= mouse_y <= box_y + box_height and box_x <= mouse_x < box_x + box_width:
                    index = (mouse_x - box_x) // CELL_SZ
                    if 0 <= index < 4:
                        return pieces[index]
                      
  def render(self, screen, board, current_player, selected, valid_moves, font):
    if board.in_check(current_player):
        king_pos = board.whiteKingPos if current_player == 'w' else board.blackKingPos
    else:
        king_pos = None

    self.draw_board(screen, selected, valid_moves, king_pos)
    self.draw_pieces(screen)
    self.draw_labels(screen, font)
    p.display.flip()         
