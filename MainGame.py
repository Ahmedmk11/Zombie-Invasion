import pygame
import math
import random
import sys
import pickle
from pygame import mixer 

pygame.init()
vec = pygame.math.Vector2

# Constants

WIDTH = 1306
HEIGHT = 526 
FPS_INGAME = 60
FULL_SCREEN = (0,0)

#mixer.music.load('sounds/background.wav')
#mixer.music.play(-1)

bullet_img = pygame.image.load('Bullet.png')
jump = False

bullet_timer = 0
score = 0

moving_left = False
moving_right = False
shoot = False
acceleration = 0.7
friction = -0.12
gravity = 9.8
platform_color = (150,59,230)

# Classes and Sprites


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.shoot_cooldown = 0
        self.anime = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0

        temp_list = []
        for i in range(12,14):
            img = pygame.image.load(f'{i}.png')
            temp_list.append(img)
        self.anime.append(temp_list)

        temp_list = []
        for i in range(1,9):
            img = pygame.image.load(f'{i}.png')
            temp_list.append(img)
        self.anime.append(temp_list)

        self.direction = 1
        self.flip = False 
        

        self.image = self.anime[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        

        # vectors and sprite constants
        
        self.health = 100
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel_vec = vec(0,0)
        self.acc_vec = vec(0,0)


    def jump(self):
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(player_group.sprite, platform_group,False)
        self.rect.y -= -1
        if hits:
            jump_sound = mixer.Sound('Jump.wav')
            jump_sound.play()
            self.vel_vec.y = -15

    def screen_edge(self):
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

    def get_damage(self,damage_mag):
        self.health -= damage_mag
        hit_sound = mixer.Sound('Hit.wav')
        hit_sound.play()

    def update(self):

        animation_cooldown = 75
        self.image = self.anime[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.anime[self.action]):
            self.frame_index = 0

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def move(self,moving_left,moving_right):
        self.acc_vec = vec(0,acceleration)
        if moving_left:
            self.acc_vec.x = -(acceleration)
            self.direction = 1
            self.flip = False

        if moving_right:
            self.acc_vec.x = acceleration
            self.direction = -1
            self.flip = True

        self.acc_vec.x += self.vel_vec.x * friction
        self.vel_vec += self.acc_vec
        self.pos += self.vel_vec + 0.5 * self.acc_vec
        self.rect.midbottom = self.pos
        hits = pygame.sprite.spritecollide(player_group.sprite, platform_group,False)
        if hits:
            self.pos.y = hits[0].rect.top
            self.vel_vec.y = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
 

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
            super().__init__()
            self.image = pygame.Surface((w,h))
            self.image.fill(platform_color)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


class Hostiles(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,speed):
        super(Hostiles,self).__init__()

        self.images = []
        self.images.append(pygame.image.load('go_1L.png'))
        self.images.append(pygame.image.load('go_2L.png'))
        self.images.append(pygame.image.load('go_3L.png'))
        self.images.append(pygame.image.load('go_4L.png'))
        self.images.append(pygame.image.load('go_5L.png'))
        self.images.append(pygame.image.load('go_6L.png'))
        self.images.append(pygame.image.load('go_7L.png'))
        self.images.append(pygame.image.load('go_8L.png'))
        self.images.append(pygame.image.load('go_9L.png'))
        self.images.append(pygame.image.load('go_10L.png'))
        self.index = 0
        self.image = self.images[self.index]

        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.speed = speed

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.rect.centerx += self.speed
        if self.rect.centerx >= 1350 or self.rect.centerx <= -50:
            self.kill()

class Hostiles2(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,speed):
        super(Hostiles2,self).__init__()

        self.images2 = []
        self.images2.append(pygame.image.load('go_1.png'))
        self.images2.append(pygame.image.load('go_2.png'))
        self.images2.append(pygame.image.load('go_3.png'))
        self.images2.append(pygame.image.load('go_4.png'))
        self.images2.append(pygame.image.load('go_5.png'))
        self.images2.append(pygame.image.load('go_6.png'))
        self.images2.append(pygame.image.load('go_7.png'))
        self.images2.append(pygame.image.load('go_8.png'))
        self.images2.append(pygame.image.load('go_9.png'))
        self.images2.append(pygame.image.load('go_10.png'))
        self.index = 0
        self.image = self.images2[self.index]

        self.rect = self.image.get_rect(center = (x_pos,y_pos))
        self.speed = speed

    def update(self):
        self.index += 1
        if self.index >= len(self.images2):
            self.index = 0
        self.image = self.images2[self.index]
        self.rect.centerx += self.speed
        if self.rect.centerx >= 1350 or self.rect.centerx <= -50:
            self.kill()

class Bullets(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__()
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (x,y))
        self.direction = direction

    def update(self):
        self.rect.x -= (self.direction * self.speed)

        if self.rect.left >= WIDTH or self.rect.right <= 0:  
            self.kill()

        screen.blit(self.image,self.rect)

# Functions

def make_text(font_type,font_size,text,color,position):
    font = pygame.font.Font(font_type, font_size)
    title = font.render(text,True,(color))
    title_rect = title.get_rect(center = (position))
    screen.blit(title,title_rect)

def main_game():
    
    pygame.draw.rect(screen,(255,0,0),(22,20,200,10))
    pygame.draw.rect(screen,platform_color,(22,20,2 * player_group.sprite.health,10))
    screen.blit(heart,(0,2))

    bullet_group.draw(screen)  
    player.draw() 
    hostiles_group.draw(screen)
    platform_group.draw(screen)

    bullet_group.update()
    player_group.update()
    hostiles_group.update()
    player_group.update()

    player.screen_edge()
    
    if shoot:
        if player.shoot_cooldown == 0:
            Fireball_sound = mixer.Sound('Fireball.wav')
            Fireball_sound.play()
            bullet = Bullets(player.rect.centerx - (0.5 * player.direction * player.rect.size[0]),player.rect.centery - 7,player.direction)
            bullet_group.add(bullet)
            player.shoot_cooldown = 37

    if moving_left or moving_right:
        player.update_action(1)

    else:
        player.update_action(0)
    player.move(moving_left,moving_right)


    if pygame.sprite.spritecollide(player_group.sprite,hostiles_group,True):
        player_group.sprite.get_damage(10)



    if pygame.sprite.groupcollide(hostiles_group, bullet_group,True,True):
        zombie_die = mixer.Sound('Zombie.wav')
        zombie_die.play()
    return 2

def game_over():
    screen.fill((0,0,0))
    text = gamefont.render("GAME OVER",True,(255,255,255))
    text_rect = text.get_rect(center = (653,243))
    screen.blit(text,text_rect)

    with open("top_scores.pickle", "rb") as scores:
        highscore = pickle.load(scores)
        if score > highscore:
            highscore = score
            with open("top_scores.pickle", "wb") as scores:
                pickle.dump(highscore, scores)


    scoresurface = gamefont.render(f"Score: {score}",True,(255,255,255))
    score_rect = scoresurface.get_rect(center = (653,283))
    screen.blit(scoresurface,score_rect)

    scoresurface1 = gamefont.render(f"High Score: {highscore}",True,(255,255,255))
    score_rect1 = scoresurface1.get_rect(center = (653,323))
    screen.blit(scoresurface1,score_rect1)

    
# Creating window

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Zombie Invasion!")
clock = pygame.time.Clock()

# Groups and objects

gamefont = pygame.font.Font('Chernobyl.ttf',40)

player = Player()


platform = Platform(0,HEIGHT-96,WIDTH,100)

platform_group = pygame.sprite.GroupSingle()
platform_group.add(platform)

player_group = pygame.sprite.GroupSingle()
player_group.add(player)

hostiles_group = pygame.sprite.Group()
hostile_event = pygame.USEREVENT
pygame.time.set_timer(hostile_event,275)


bullet_group = pygame.sprite.Group()

pygame.mouse.set_visible(True)

sky = pygame.image.load('SkyNight.png')
wallpaper = pygame.image.load('GamePlatform.png')
heart = pygame.image.load('Heart.png')

# Game loop

running = True
while running:
    # Events (Inputs)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mixer.music.stop()
            running = False
        
        if event.type == hostile_event:
            random_xpos = [-40,-20]
            random_xpos2 = [1340,1360]
            random_hs = [-2,2]
            hostile_left = Hostiles2(random.choice(random_xpos),400,random.choice(random_hs))
            hostile_right = Hostiles(random.choice(random_xpos2),400,random.choice(random_hs))
            hostiles_group.add(hostile_left,hostile_right)
        
        if event.type == pygame.MOUSEBUTTONDOWN and player_group.sprite.health <= 0:
            player_group.sprite.health = 100
            hostiles_group.empty()
            score  = 0
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                mixer.music.stop()

                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_group.sprite.jump()


    if player_group.sprite.health > 0:
        score += main_game()

        fontscore = pygame.font.Font('Starjedi.ttf',20)
        scoretext = fontscore.render(f"Score: {score}",True,(255,255,255))
        scoretextrect = scoretext.get_rect(center = (1200,40))
        screen.blit(scoretext,scoretextrect)

  
    else:
        game_over()

    pygame.display.update()
    screen.blit(sky,FULL_SCREEN)
    screen.blit(wallpaper,FULL_SCREEN)
    programIcon = pygame.image.load('icon.png')
    pygame.display.set_icon(programIcon)
    clock.tick(FPS_INGAME)