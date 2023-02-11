import pygame
from pygame.locals import *
import sys 
import random
import time

pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450  #Cap variables are used to avoid change
WIDTH = 400
ACC = 0.5    #Acceleration 
FRIC = -0.12 #Friction
FPS = 50  #Frames Per Second

FramePerSec = pygame.time.Clock()
displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
background = pygame.image.load("background.png")

#player class below
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("player.png")#image here
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 385))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0: 
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
      hits = pygame.sprite.spritecollide(self, platforms, False)
      if hits and not self.jumping:
        self.jumping = True
        self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
      hits = pygame.sprite.spritecollide(player_one, platforms, False)
      if player_one.vel.y > 0:
        if hits:
            if self.pos.y < hits[0].rect.bottom:
                if hits[0].point == True:
                    hits[0].point = False
                    self.score += 1
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0
                self.jumping = False
          
#player class ends, platform class starts
          
class platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

            self.image = pygame.image.load("platform.png")
    
            self.surf = pygame.transform.scale(self.image, (width, height))
            self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT-30)))
            
        
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.point = True


    def move(self):
        hits = self.rect.colliderect(player_one.rect)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if hits:
                player_one.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        if(self.speed == 0):
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(player_one.rect):
            player_one.score += 5
            self.kill()

#check platform function for collision

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if(abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top)<40):
                return True
        c = False


def plat_gen():
  while len(platforms) < 7:
    width = random.randrange(50, 100)
    p = None
    C = True

    while C:
        p = platform()
        p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
        C = check(p, platforms)

    p.generateCoin()
    platforms.add(p)
    all_sprites.add(p)

PT = platform()
player_one = Player()

PT.surf = pygame.Surface((WIDTH, 20))
PT.surf.fill((255, 0, 0))
PT.rect = PT.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT.moving = False
PT.point = False

all_sprites = pygame.sprite.Group()
all_sprites.add(PT)
all_sprites.add(player_one)

platforms = pygame.sprite.Group()
platforms.add(PT)

coins = pygame.sprite.Group()

for x in range(random.randint(4, 5)):
    C = True
    plat = platform()
    while C:
        plat = platform()
        C = check(plat, platforms)
    plat.generateCoin()
    platforms.add(plat)
    all_sprites.add(plat)
    
while True:
    player_one.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            player_one.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_one.cancel_jump()

    if player_one.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaySurface.fill((255, 0, 0))
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()

    if player_one.rect.top <= HEIGHT/3:
      player_one.pos.y += abs(player_one.vel.y)
      for plat in platforms:
          plat.rect.y += abs(player_one.vel.y)
          if plat.rect.top >= HEIGHT:
            plat.kill()

      for coin in coins:
          coin.rect.y += abs(player_one.vel.y)
          if coin.rect.top >= HEIGHT:
              coin.kill()
              self.score += 1
        

    plat_gen()
    displaySurface.blit(background, (0,0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(player_one.score), True, (123, 244, 0))
    displaySurface.blit(g, (WIDTH/2, 10))

    for entity in all_sprites:
        displaySurface.blit(entity.surf, entity.rect)
        entity.move()

    for coin in coins:
        displaySurface.blit(coin.image, coin.rect)
        coin.update()

    pygame.display.update()
    FramePerSec.tick(FPS)
