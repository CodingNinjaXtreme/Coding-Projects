import pygame
from sys import exit
from random import  choice

# Initialize Pygame and mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Set up screen and clock
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Platform Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Pixeltype.ttf', 50)

# Game state
game_active = False
start_time = 0
score = 0

# Load audio
jump_sound = pygame.mixer.Sound('jump.mp3')
jump_sound.set_volume(0.7)
pygame.mixer.music.load('music.wav')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)  # Loop music

# Background and ground
Sky_surface = pygame.image.load('Sky.png').convert()
ground_surface = pygame.image.load('ground.png').convert()

# Snail animation
snail_1 = pygame.image.load('snail1.png').convert_alpha()
snail_2 = pygame.image.load('snail1.png').convert_alpha()
snail_frames = [snail_1, snail_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly animation
fly_1 = pygame.image.load("Fly1.png").convert_alpha()
fly_2 = pygame.image.load("Fly2.png").convert_alpha()
fly_frames = [fly_1, fly_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Obstacles
obstacle_rect_list = []

# Player animation and position
player_walk_1 = pygame.image.load('player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('jump.png').convert_alpha()

player_surf = player_walk[player_index]
# Fix player x position near left side (e.g. x=80), only allow vertical movement
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Player idle graphic
player_stand = pygame.image.load('player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# UI text
game_name = test_font.render('Platform Game', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to Run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 150)

# World scroll speed (speed at which obstacles and background move left)
world_scroll_speed = 5

# Functions
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision(player, obstacles):
    for _, obstacle_rect in obstacles:
        if player.colliderect(obstacle_rect):
            return False
    return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

# Variables to help with background scrolling
ground_scroll_x = 0
sky_scroll_x = 0
SKY_WIDTH = Sky_surface.get_width()
GROUND_WIDTH = ground_surface.get_width()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()

            if event.type == obstacle_timer:
                obstacle_type = choice(['snail', 'fly1', 'fly2'])
                if obstacle_type == 'snail':
                    obstacle_rect = snail_surf.get_rect(bottomright=(900, 300))
                else:
                    obstacle_rect = fly_surf.get_rect(bottomright=(900, 210))
                obstacle_rect_list.append((obstacle_type, obstacle_rect))

            if event.type == snail_animation_timer:
                snail_frame_index = (snail_frame_index + 1) % len(snail_frames)
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                fly_frame_index = (fly_frame_index + 1) % len(fly_frames)
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                obstacle_rect_list.clear()
                player_rect.midbottom = (80, 300)
                player_gravity = 0
                ground_scroll_x = 0
                sky_scroll_x = 0

    if game_active:
        # Scroll sky and ground
        sky_scroll_x -= world_scroll_speed / 4  # slower scroll for parallax effect
        ground_scroll_x -= world_scroll_speed

        # Loop sky background
        if abs(sky_scroll_x) > SKY_WIDTH:
            sky_scroll_x = 0
        # Loop ground background
        if abs(ground_scroll_x) > GROUND_WIDTH:
            ground_scroll_x = 0

        # Draw sky twice for continuous scrolling
        screen.blit(Sky_surface, (sky_scroll_x, 0))
        screen.blit(Sky_surface, (sky_scroll_x + SKY_WIDTH, 0))

        # Draw ground twice for continuous scrolling
        screen.blit(ground_surface, (ground_scroll_x, 300))
        screen.blit(ground_surface, (ground_scroll_x + GROUND_WIDTH, 300))

        score = display_score()

        # Obstacles move left by scroll speed
        for obstacle_type, obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= world_scroll_speed
            if obstacle_type == 'snail':
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        # Remove obstacles off-screen left
        obstacle_rect_list = [(t, r) for (t, r) in obstacle_rect_list if r.right > 0]

        # Player physics and vertical movement only
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()

        # Draw player fixed at ~x=80 horizontally
        # So player x pos doesn't change; only y changes
        player_rect.x = 80
        screen.blit(player_surf, player_rect)

        # Collision detection
        game_active = collision(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            score_message = test_font.render(f'Score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)