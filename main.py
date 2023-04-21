import pygame as pg
import serial
import time
from pygame.locals import *
from test import maze, Player

arduino = serial.Serial('COM4', 115200, timeout=.1)
x_ar = 0
y_ar = 0
try:
    arduino.open()
    if arduino.is_open:
        print('CONNECTED')
except:
    pass
time.sleep(1)


pg.init()
window = pg.display.set_mode((800, 600))
clock = pg.time.Clock()


BACKGROUND = pg.image.load("maze.png")
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

run = True
while run:
    arduino.readline = lambda: arduino.read_until(b'\n').rstrip(b'\n') # get rid of \n in serial
    raw = arduino.readline()

    try:
        pos = raw.decode('utf-8').split(",")
        x_ar = float(pos[0])
        y_ar = float(pos[1])
        arduino.flush()
    except:
        pass
    # clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # if event.type == pg.KEYDOWN:
        #     print(keys[pg.K_RIGHT] - keys[pg.K_LEFT])

    # keys = pg.key.get_pressed()
    player_rect.bottom += speed_a
    player_rect.top += speed_a
    player_rect.left += 0
    player_rect.right += 0
    # rect.x += (keys[pg.K_RIGHT] - keys[pg.K_LEFT]) * vel
    player.rect.x += x_ar * vel
    player.rect.y += y_ar * vel
        
    # rect.clamp_ip(window.get_rect())
    # window.fill(0)
    # window.blit(BACKGROUND, (0, 0))
    window.fill(0)
    player.update()
    all_sprites_list.draw(window)
    collide = pg.Rect.colliderect(player_rect,
                                      player)
    if collide:
        speed_a *= -1
        arduino.write(b'1')
    if player_rect.top <= 0 or player_rect.bottom >= 600 or player_rect.left <= 0 or player_rect.right >= 800:
        speed_a *= -1
    player_rect.clamp_ip(window.get_rect())
    pg.draw.rect(window, (0,   255,   0),
                    player_rect)
    pg.display.flip()

pg.quit()
exit()