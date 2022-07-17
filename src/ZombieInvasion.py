"""

This file contains the Menu game loop

"""

import pickle

import pygame
import sys
from pygame import mixer

pygame.init()
inst = False
screen = pygame.display.set_mode((1306, 526))
clock = pygame.time.Clock()
pygame.mouse.set_visible(True)
screen_home = pygame.image.load('resources/images/world/HomeScreen.png')
screen_home = pygame.transform.scale(screen_home, (1306, 526))

mixer.music.load('resources/sounds/MainMenu.wav')
mixer.music.play(-1)

while True:

    font1 = pygame.font.Font('resources/fonts/Starjedi.ttf', 40)
    game1 = font1.render("Play", True, (255, 255, 255))
    game1_rect = game1.get_rect(center=(640, 300))

    font2 = pygame.font.Font('resources/fonts/Starjedi.ttf', 25)
    title1 = font2.render("(i) for instructions", True, (255, 255, 255))
    title1_rect = title1.get_rect(center=(150, 500))

    font3 = pygame.font.Font('resources/fonts/Chernobyl.ttf', 70)
    title2 = font3.render("Zombie Invasion!", True, (255, 255, 255))
    title2_rect = title2.get_rect(center=(315, 80))

    with open("top_scores.pickle", "rb") as scores:
        highscore = pickle.load(scores)

    font4 = pygame.font.Font('resources/fonts/Starjedi.ttf', 30)
    title3 = font4.render(f"High Score: {highscore}", True, (255, 255, 255))
    title3_rect = title3.get_rect(center=(1150, 500))
    title3_rect.right = 1290

    fontN = pygame.font.Font('resources/fonts/Oswald.ttf', 35)
    fontI = pygame.font.Font('resources/fonts/Oswald.ttf', 20)

    screen.blit(screen_home, (0, 0))
    screen.blit(game1, game1_rect)
    screen.blit(title1, title1_rect)
    screen.blit(title2, title2_rect)
    screen.blit(title3, title3_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game1_rect.collidepoint(event.pos):
                import MainGame
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                inst = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_i:
                inst = False

    if inst:
        instructions_rect = pygame.draw.rect(screen, (57, 61, 71), (0, 200, 550, 400))
        instructions = fontN.render("Welcome to Zombie Invasion!", True, (255, 255, 255))
        instructions1 = fontI.render("Press 'Play' to start the game", True, (255, 255, 255))
        instructions2 = fontI.render("To play again, press anywhere on the 'Game Over' screen", True, (255, 255, 255))
        instructions3 = fontI.render("To exit the game, press 'Escape' or close the window", True, (255, 255, 255))
        instructions4 = fontI.render("Press 'Space' to shoot, 'Left' and 'Right' to move and 'Up' to jump", True,
                                     (255, 255, 255))
        instructions5 = fontI.render("Keep Sky alive as long as you can!", True, (255, 255, 255))
        instructions6 = fontI.render("Have Fun!", True, (255, 255, 255))

        screen.blit(instructions, (10, 220))
        screen.blit(instructions1, (15, 280))
        screen.blit(instructions2, (15, 320))
        screen.blit(instructions3, (15, 360))
        screen.blit(instructions4, (15, 400))
        screen.blit(instructions5, (15, 440))
        screen.blit(instructions6, (15, 480))

    programIcon = pygame.image.load('resources/images/world/icon.png')
    pygame.display.set_icon(programIcon)
    pygame.display.set_caption("Zombie Invasion!")
    pygame.display.update()
    clock.tick(30)
