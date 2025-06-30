import pygame
from pygame.locals import *
import random

pygame.init()

# screen setup
width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Car Game')

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# road details
road_width = 300
marker_width = 10
marker_height = 50
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# movement
lane_marker_move_y = 0

# player setup
player_x = 250
player_y = 400
player_img = pygame.image.load('car.png')
player_img = pygame.transform.scale(player_img, (45, int(player_img.get_rect().height * (45 / player_img.get_rect().width))))
player_rect = player_img.get_rect()
player_rect.center = [player_x, player_y]

# game state
clock = pygame.time.Clock()
fps = 120
run = True  # changed to True so the game starts running
speed = 2
score = 0
game_over = False  # added this to control game over state separately

# vehicles
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [pygame.image.load(name) for name in image_filenames]
for i in range(len(vehicle_images)):
    vehicle_images[i] = pygame.transform.scale(vehicle_images[i], (45, int(vehicle_images[i].get_rect().height * (45 / vehicle_images[i].get_rect().width))))

vehicles = []

# crash image
crash = pygame.image.load('crash.png')
crash_rect = crash.get_rect()

running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if not game_over and event.type == KEYDOWN:
            if event.key == K_LEFT and player_rect.centerx > left_lane:
                player_rect.x -= 100
            elif event.key == K_RIGHT and player_rect.centerx < right_lane:
                player_rect.x += 100

            for vehicle in vehicles:
                if player_rect.colliderect(vehicle['rect']):
                    game_over = True
                    run = False  # stop game running when game over
                    if event.key == K_LEFT:
                        player_rect.left = vehicle['rect'].right
                        crash_rect.center = [player_rect.left, (player_rect.centery + vehicle['rect'].centery) / 2]
                    elif event.key == K_RIGHT:
                        player_rect.right = vehicle['rect'].left
                        crash_rect.center = [player_rect.right, (player_rect.centery + vehicle['rect'].centery) / 2]

    # draw background
    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(-marker_height * 2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # draw player
    screen.blit(player_img, player_rect)

    if not game_over:
        # add vehicles
        if len(vehicles) < 2:
            add_vehicle = True
            for vehicle in vehicles:
                if vehicle['rect'].top < vehicle['rect'].height * 1.5:
                    add_vehicle = False
            if add_vehicle:
                lane = random.choice(lanes)
                image = random.choice(vehicle_images)
                rect = image.get_rect()
                rect.center = [lane, -rect.height]
                vehicles.append({'image': image, 'rect': rect})

        # move and draw vehicles
        for vehicle in vehicles[:]:
            vehicle['rect'].y += speed
            screen.blit(vehicle['image'], vehicle['rect'])

            if vehicle['rect'].top >= height:
                vehicles.remove(vehicle)
                score += 1
                if score > 0 and score % 5 == 0:
                    speed += 1

    # score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    screen.blit(text, (50, 400))

    # check for head-on collision
    for vehicle in vehicles:
        if player_rect.colliderect(vehicle['rect']):
            game_over = True
            run = False
            crash_rect.center = [player_rect.centerx, player_rect.top]
            vehicles.remove(vehicle)
            break

    if game_over:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect(center=(width / 2, 100))
        screen.blit(text, text_rect)

    pygame.display.update()

    while game_over:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    game_over = False
                    run = True
                    speed = 2
                    score = 0
                    vehicles.clear()
                    player_rect.center = [player_x, player_y]
                elif event.key == K_n:
                    game_over = False
                    running = False

pygame.quit()
