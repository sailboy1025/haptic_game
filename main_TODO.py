import pygame, sys, random, math
from pygame.locals import *
from haptic_helper import HapkitCommute, normalize_vector
import threading
class Player(pygame.sprite.Sprite):
    def __init__(self, img, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fire_sound = pygame.mixer.Sound('art/SHOOT011.mp3')
    def fire(self):
        self.fire_sound.play()
        return Bullet(bullet_src, self.rect.center[0], self.rect.center[1])
    def update(self) -> None:
        self.rect.center = [self.pos_x, self.pos_y]
        r = math.sqrt((player.rect.x - blackhole.rect.x) ** 2 + (player.rect.y - blackhole.rect.y) ** 2)
        r_to_earth = math.sqrt((player.rect.x - earth.rect.x) ** 2 + (player.rect.y - earth.rect.y) ** 2)
        #vector between player and blackhole
        hor_bh = player.rect.x - blackhole.rect.x
        ver_bh = player.rect.y - blackhole.rect.y
        k = 1000
        force_bh = normalize_vector([hor_bh, ver_bh])
        force_bh[0] = -force_bh[0] * k / (r ** 2)
        force_bh[1] = -force_bh[1] * k / (r ** 2)
        # vector between player and enemy
        hor_en = player.rect.x - blackhole.rect.x
        ver_en = player.rect.y - blackhole.rect.y
        v_en = normalize_vector([hor_en, ver_en])
        # haptic effect
        # with ufo
        if (pygame.sprite.spritecollide(player, enemy_group, False)):
            hc.arduino_write(v_en[0],  v_en[1])
            # print(f"Collision detected--Vector: {v_en}") 
        # with blackhole
        if r < 200:
            hc.arduino_write(force_bh[0],  force_bh[1])
            # print(f"force produced by blackhole: {force_bh}")
        # with earth
        if r_to_earth < 200:
            hc.arduino_write(damp = 1.5)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed_x, speed_y):
        super().__init__()
        self.sprites = []
        img_0 = pygame.transform.scale(pygame.image.load('art/UfoGrey.png'), (32, 32))
        img_1 = pygame.transform.scale(pygame.image.load('art/UfoGrey1.png'), (32, 32))
        self.sprites.append(img_0)
        self.sprites.append(img_1)
        self.curr_index = 0
        self.image = self.sprites[self.curr_index]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.speed_x = speed_x
        self.speed_y = speed_y


    def update(self) -> None:
        self.curr_index += 0.05
        if self.curr_index > len(self.sprites) - 1:
            self.curr_index = 0
        self.image = self.sprites[round(self.curr_index)] 
        collision_forgive = 10
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #TODO limited inside screen
        if self.rect.right >= screen_w - 100 or self.rect.left <= 1:
            self.speed_x *= -1
        if self.rect.bottom >= screen_h - 100 or self.rect.top <= 1:
            self.speed_y *= -1
        if pygame.sprite.spritecollide(player, enemy_group, False):    
            if abs(self.rect.right - player.rect.left) < collision_forgive and self.speed_x > 0\
            or abs(self.rect.left - player.rect.right) < collision_forgive and self.speed_x < 0:
                self.speed_x *= -1

            if abs(self.rect.top - player.rect.bottom) < collision_forgive and self.speed_y < 0\
            or abs(self.rect.bottom - player.rect.top) < collision_forgive and self.speed_y > 0:
                self.speed_y *= -1
                    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(img)
        # self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    
    
    def update(self):
        self.rect.y -= 5
        if self.rect.y <= 0 + 10 or pygame.sprite.spritecollide(bullet, enemy_group, True):
            self.kill()

class Blackhole(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprites = []
        img_0 = pygame.transform.scale(pygame.image.load('art/Hurricane.png'), (128, 128))
        img_1 = pygame.transform.scale(pygame.image.load('art/Hurricane_1.png'), (128, 128))
        self.sprites.append(img_0)
        self.sprites.append(img_1)
        self.curr_index = 0
        self.image = self.sprites[self.curr_index]
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]


    def update(self):
        self.curr_index += 0.05
        if self.curr_index > len(self.sprites) - 1:
            self.curr_index = 0
        self.image = self.sprites[round(self.curr_index)] 


class Earth(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sprites = []
        img_0 = pygame.transform.scale(pygame.image.load('art/Earth.png'), (128, 128))
        # img_1 = pygame.transform.scale(pygame.image.load('art/Hurricane_1.png'), (128, 128))
        self.sprites.append(img_0)
        # self.sprites.append(img_1)
        self.curr_index = 0
        self.image = self.sprites[self.curr_index]
        self.rect = self.image.get_rect()
        self.rect.center = [self.pos_x, self.pos_y]


    def update(self):
        pass

player_src = 'art/RocketWhite.png'
# enemy_src = 'art/UfoBlue.png' 
bullet_src = 'art/bullet.png'   
SIZE = (32, 32)

pygame.init()
clock = pygame.time.Clock()
#background music
pygame.mixer.music.load('art/Battle in the winter.mp3')
pygame.mixer_music.play()
screen_w = 1024
screen_h = 1024
screen = pygame.display.set_mode((screen_w, screen_h))
background = pygame.image.load('art/space_up.png')
# Hide cursor
pygame.mouse.set_visible(False)


#spawn player
pos_ar = [512, 512, 0]
player = Player(player_src, pos_ar[0], pos_ar[1])
player_group = pygame.sprite.Group()
player_group.add(player)

#spawn enemy
enemy_group = pygame.sprite.Group()
for i in range(15):
    enemy = Enemy(random.randrange(0, screen_w), random.randrange(0, screen_h),
                  0.5* random.randrange(-5, 5), 0.5* random.randrange(-5, 5))
    enemy_group.add(enemy)
#spawn bullet
bullet_group = pygame.sprite.Group()
#spawn blackhole
blackhole = Blackhole(200, 800)
blackhole_group = pygame.sprite.Group()
blackhole_group.add(blackhole)
earth = Earth(800, 800)
earth_group = pygame.sprite.Group()
earth_group.add(earth)
hc = HapkitCommute('COM5', 115200)
#Thread for serial
def main():
    global bullet
    t = threading.Thread(target=hc.arduino_read, args=(pos_ar,), daemon=True)
    t.start()
    #main loop
    while True:
        # Uncomment this for position control
        player.pos_x = pos_ar[0]
        player.pos_y = pos_ar[1] - 500 # Some offset to match the screen

        # print(f'x: {pos_ar[0]}, y:{pos_ar[1]}')
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if even.type == pygame.MOUSEBUTTONDOWN:
                bullet = player.fire()
                bullet_group.add(bullet)
        # trigger effect
        if pos_ar[2] == 1:
            bullet = player.fire()
            bullet_group.add(bullet)
        screen.blit(background, (0,0))
        blackhole_group.draw(screen)
        earth_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        bullet_group.draw(screen)
        blackhole_group.update()
        earth_group.update()
        player_group.update()
        enemy_group.update()
        bullet_group.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
