import pygame as pg
import sys
import random
from tetris_container import *
from constants import *
from pygame.locals import QUIT

class Tetris:
  def __init__(self):
    pg.init() 
    self.font = pg.font.SysFont('arial', 10, bold = True)
    self.clock = pg.time.Clock()
  def run(self):
    #Intro Screen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pg.display.set_caption("Tetris")
      
    win.fill((0,0,0))
    label = self.font.render("Welcome to Tetris", 1, (255,255,255))
    win.blit(label, (TOP_LEFT[0] + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT[1] + GRID_HEIGHT/2 - label.get_height()))
    pg.display.update()
    
    pg.time.delay(3000)
    win.fill((30,30,30))
    label = self.font.render("Use the Down, Left, and Right arrow keys to move your tetrimino around.", 1, (255,255,255))
    win.blit(label, (TOP_LEFT[0] + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT[1] + GRID_HEIGHT/2 - label.get_height()))
    pg.display.update()

    pg.time.delay(3000)
    win.fill((20,20,20))
    label = self.font.render("Use the Up arrow key to rotate your Tetrimino", 1, (255,255,255))
    win.blit(label, (TOP_LEFT[0] + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT[1] + GRID_HEIGHT/2 - label.get_height()))
    pg.display.update()
      
    pg.time.delay(3000)
    win.fill((10,10,10))
    label = self.font.render("Use Space to instantly place your Tetrimino", 1, (255,255,255))
    win.blit(label, (TOP_LEFT[0] + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT[1] + GRID_HEIGHT/2 - label.get_height()))
      
    pg.display.update()
    pg.time.delay(4500)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    
    while True:
      self.clock.tick(40)
      win.fill((0,0,0))
      
      label = pg.font.SysFont('arial', 20, bold = True).render("Press any key to play, press 'T' to enter testing mode", 1, (255,255,255))
      win.blit(label, (TOP_LEFT[0] + GRID_WIDTH /2 - (label.get_width()/2), TOP_LEFT[1] + GRID_HEIGHT/2 - label.get_height()))

      for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_t:
                run(win,True)
            else:
              print("Game Ran successfully")
              run(win)
        pg.display.update()

  
if __name__ == "__main__":
  Tetris().run()
  