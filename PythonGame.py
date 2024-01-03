from typing import Any
import pygame
from pygame.locals import *
import random


pygame.init()

# pantalla
game_width = 800
game_height = 450
screen_size = (game_width, game_height)
game_window = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Star Wars')
padding_y = 50

# colores
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

#tiempo de recarga del laser
bullet_cooldown = 500 

last_bullet_time = pygame.time.get_ticks()

next_asteroid = pygame.time.get_ticks()

# resizing de la imagen
def scale_image(image, new_width):
    image_scale = new_width / image.get_rect().width
    new_height = image.get_rect().height * image_scale
    scaled_size = (new_width, new_height)
    return pygame.transform.scale(image, scaled_size)

# background
bg = pygame.image.load('images/galaxia.jpg').convert_alpha()
bg = scale_image(bg, game_width)
bg_scroll = 0

# x-wing
xwing_images = []
for i in range (2):
    xwing_image = pygame.image.load(f'xwing/xwing{i}.png').convert_alpha()
    xwing_image = scale_image(xwing_image, 150)
    xwing_images.append(xwing_image)
    
heart_images = []
heart_image_index = 0
for i in range(4):
    heart_image = pygame.image.load(f'cora/cora{i}.png').convert_alpha()
    heart_image = scale_image(heart_image, 40)
    heart_images.append(heart_image)
       
asteroid_images = []
for i in range (4):
    asteroid_image = pygame.image.load(f'roca/roca{i}.png').convert_alpha()
    asteroid_image = scale_image(asteroid_image, 70)
    asteroid_image = pygame.transform.flip(asteroid_image, True, False)
    asteroid_images.append(asteroid_image)

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        
        self.lives = 3
        self.score = 0
        
        #index of the image
        self.image_index = 0
        
        #angle of the image
        self.image_angle = 0
        
    def update(self):
        self.image_index += 1
        if self.image_index >= len(xwing_images):
            self.image_index = 0
        
        self.image = xwing_images[self.image_index]
        self.rect = self.image.get_rect()
        
        self.image = pygame.transform.rotate(self.image, self.image_angle)
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if pygame.sprite.spritecollide(self, asteroid_group, True):
            self.lives -= 1

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y 
        self.radius = 5
        
        self.rect = Rect(x, y, 10, 10)
        
    def draw(self):
        pygame.draw.circle(game_window, red, (self.x, self.y), self.radius)
        
    def update(self):
        
        self.x += 2 
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.x > game_width:
            self.kill()
        
class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.x = game_width
        
        self.y = random.randint(padding_y, game_height - padding_y * 2)
        
        self.image_index = 0
        
        self.image = asteroid_images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def update(self):
        
        self.x -= 2
        
        self.image_index += 0.25
        if self.image_index >= len(asteroid_images):
            self.image_index = 0
            
        self.image = asteroid_images[int(self.image_index)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.kill()
            player.score += 1

        if self.x < 0:
            self.kill()

# creacion de los grupos sprite
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

# player 
player_x = 30
player_y = game_height // 2
player = Player(player_x, player_y)
player_group.add(player)

# loop del juego
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False 
    
    keys =  pygame.key.get_pressed()     
   
    if keys[K_UP] and player.rect.top > padding_y:
        player.y -= 2
        player.image_angle = 15
    elif keys[K_DOWN] and player.rect.bottom < game_height - padding_y:
        player.y += 2
        player.image_angle = -15
    else:
        player.image_angle = 0
    
    # disparo con espacio
    if keys[K_SPACE] and last_bullet_time + bullet_cooldown < pygame.time.get_ticks():
        bullet_x = player.x + player.image.get_width()
        bullet_y = player.y + player.image.get_height() // 2
        bullet = Bullet(bullet_x, bullet_y)
        bullet_group.add(bullet)
        last_bullet_time = pygame.time.get_ticks()
        
    if next_asteroid < pygame.time.get_ticks():
        asteroid = Asteroid()
        asteroid_group.add(asteroid)
        
        next_asteroid = random.randint(pygame.time.get_ticks(), pygame.time.get_ticks() + 3000)
    
    # draw the background
    game_window.blit(bg, (0 - bg_scroll, 0))
    game_window.blit(bg, (game_width - bg_scroll, 0))
    bg_scroll += 1
    if bg_scroll == game_width:
        bg_scroll = 0
        
    player_group.update()
    player_group.draw(game_window)
    
    bullet_group.update()
    for bullet in bullet_group:
        bullet.draw()
        
    asteroid_group.update()
    asteroid_group.draw(game_window)
    
    for i in range(player.lives):
        heart_image = heart_images[int(heart_image_index)]
        heart_x = 5 + i * (heart_image.get_width() + 5)
        heart_y = 5
        game_window.blit(heart_image, (heart_x, heart_y))
    heart_image_index += 0.1
    if heart_image_index >= len(heart_images):
        heart_image_index = 0
    
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {player.score}', True, white)   
    text_rect = text.get_rect()
    text_rect.center = (200,20)
    game_window.blit(text, text_rect)
            
    pygame.display.update()
    
    while player.lives == 0:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                
        gameover_str = f'Game over. ¿Jugar otra vez? (y o n)'
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        text = font.render(gameover_str, True, red)
        text_rect = text.get_rect()
        text_rect.center = (game_width / 2, game_height / 2)
        game_window.blit(text, text_rect)
        
        keys = pygame.key.get_pressed()
        if keys[K_y]:
            
            player_group.empty()
            bullet_group.empty()
            asteroid_group.empty()
            
            player = Player(player_x, player_y)
            player_group.add(player)
        
        elif keys[K_n]:
            running = False
            break
        
        pygame.display.update()
    
pygame.quit()