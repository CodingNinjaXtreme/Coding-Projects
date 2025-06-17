import math
import random

import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Load background image
background = pygame.image.load("image/background1.png")
# Background Music
mixer.music.load("image/background (1).wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("image/ship.png")
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load("image/ship.png")
PlayerX = 370
PlayerY = 480
PlayerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("image/Space-Invader-Enemy-1--Streamline-Cyber.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(10)

# Bullet
bulletImg = pygame.image.load("image/laserBullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 24)
textX = 10
textY = 10

# Game Over font
over_font = pygame.font.Font("freesansbold.ttf", 48)

# Timer
start_ticks = pygame.time.get_ticks()

# Functions
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER : " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_timer(x, y):
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    timer = font.render("Time : " + str(seconds), True, (255, 255, 255))
    screen.blit(timer, (x, y))

def player(x, y):
    screen.blit(PlayerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x - 60, y - 120))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < 27

# Game Loop
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    PlayerX_change = -2
                if event.key == pygame.K_RIGHT:
                    PlayerX_change = 2
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_Sound = mixer.Sound('image/laser.wav')
                    bullet_Sound.play()
                    bulletX = PlayerX
                    fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    PlayerX_change = 0

    if not game_over:
        # Player movement
        PlayerX += PlayerX_change
        if PlayerX <= 0:
            PlayerX = 0
        elif PlayerX >= 736:
            PlayerX = 736

        # Enemy movement
        for i in range(num_of_enemies):
            if enemyY[i] > 200:
                game_over = True
                break

            enemyX[i] += enemyX_change[i]

            if enemyX[i] <= 0:
                enemyX_change[i] = 1
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -1
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_Sound = mixer.Sound('image/laser.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    # Draw player, score, timer
    player(PlayerX, PlayerY)
    show_score(textX, textY)
    show_timer(680, 10)

    if game_over:
        game_over_text()

    pygame.display.update()