import pygame as p
from constants import *

class Gui:
  def __init__(self):
    self.state = STATE
    
  def load_images(self):
    pieces = ['bb', 'bk', 'bn', 'bp', 'bq', 'br', 'wb', 'wk', 'wn', 'wp', 'wq', 'wr']
    for piece in pieces:
      IMAGES[piece] = p.transform.scale(p.image.load('pieces/' + piece + '.png'), (CELL_SZ, CELL_SZ))
  
  def draw_board(self, screen, selected=None):
    cnt = 0
    for i in range(DIMENSION):
      for j in range(DIMENSION):
        if cnt % 2 == 0:
          p.draw.rect(screen, p.Color(238,238,210,255),[CELL_SZ * j, CELL_SZ * i, CELL_SZ, CELL_SZ])
        else:
          p.draw.rect(screen, p.Color(118,150,86,255), [CELL_SZ * j, CELL_SZ * i, CELL_SZ, CELL_SZ])
        cnt +=1

      cnt-=1
        
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
