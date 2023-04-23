import pygame as pg
import serial
import time
from pygame.locals import *
from test import Player
from threading import Thread   

pg.init()
window = pg.display.set_mode((800, 600))
clock = pg.time.Clock()

SURFACE_COLOR = (167, 255, 100)
class Player(pg.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
  
        self.image = pg.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        pg.draw.rect(self.image, color, pg.Rect(0, 0, width, height))
        
        self.rect = self.image.get_rect()
# BACKGROUND = pg.image.load("maze.png")
vel = 0.001

# def draw_maze():
#     for row in range(len(maze)):
#         for col in range(len(maze[0])):
#             if maze[row][col] == 1:
#                 rect = pg.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE)
#                 pg.draw.rect(window, (255, 255, 255), rect)
#             else:
#                 x = col*TILE_SIZE
#                 y = row*TILE_SIZE
#                 pg.draw.line(window, (255, 255, 255), (x, y), (x+TILE_SIZE, y))
#                 pg.draw.line(window, (255, 255, 255), (x+TILE_SIZE, y), (x+TILE_SIZE, y+TILE_SIZE))
#                 pg.draw.line(window, (255, 255, 255), (x+TILE_SIZE, y+TILE_SIZE), (x, y+TILE_SIZE))
#                 pg.draw.line(window, (255, 255, 255), (x, y+TILE_SIZE), (x, y))
# draw_maze()

speed_a = 0.51
#Spawn player
all_sprites_list = pg.sprite.Group()
COLOR = (255,0,0) # red
player = Player(COLOR, 30, 30)
player.rect.x = 0
player.rect.y = 0
player_rect = Rect(400, 300, 50, 50)
all_sprites_list.add(player)

def arduino_read(data_from_arduino):
    
    arduino = serial.Serial('COM4', 115200, timeout=.1)

    try:
        arduino.open()
        if arduino.is_open:
            print('CONNECTED')
    except:
        pass
    time.sleep(1)
    while True:
        arduino.readline = lambda: arduino.read_until(b'\n').rstrip(b'\n') # get rid of \n in serial
        raw = arduino.readline()

        try:
            pos = raw.decode('utf-8').split(",")
            data_from_arduino[0] = float(pos[0])
            data_from_arduino[1] = float(pos[1])
            arduino.flush()
            # print(x_ar, y_ar)
        except:
            pass
        
pos = [0, 0]
t = Thread(target=arduino_read, args=(pos,), daemon=True)
t.start()

run = True
while run:
    print(f"x_ar: {pos[0]}, y_ar: {pos[1]}")
    # clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            READ = False
        # if event.type == pg.KEYDOWN:
        #     print(keys[pg.K_RIGHT] - keys[pg.K_LEFT])

    # keys = pg.key.get_pressed()
    player_rect.bottom += speed_a
    player_rect.top += speed_a
    player_rect.left += 0
    player_rect.right += 0
    # rect.x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * vel
    player.rect.x += pos[0]* vel
    player.rect.y += pos[1]* vel
        
    # rect.clamp_ip(window.get_rect())
    # window.fill(0)
    # window.blit(BACKGROUND, (0, 0))
    window.fill(0)
    all_sprites_list.update()
    all_sprites_list.draw(window)
    collide = pg.Rect.colliderect(player_rect,
                                      player)
    if collide:
        speed_a *= -1
        # arduino.write(b'1')
    if player_rect.top <= 0 or player_rect.bottom >= 600 or player_rect.left <= 0 or player_rect.right >= 800:
        speed_a *= -1
    player_rect.clamp_ip(window.get_rect())
    pg.draw.rect(window, (0,   255,   0),
                    player_rect)
    pg.display.flip()
    clock.tick(60)

pg.quit()
exit()