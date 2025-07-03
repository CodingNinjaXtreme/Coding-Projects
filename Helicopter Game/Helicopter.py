import random
import pygame

pygame.init()

HEIGHT = 600
WIDTH = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Helicopter in Python!')
font = pygame.font.Font('freesansbold.ttf', 20)
fps = 60
timer = pygame.time.Clock()
new_map = True
map_rects = []
rect_width = 10
total_rects = WIDTH // rect_width
spacer = 10
player_x = 100
player_y = 300
flying = False
y_speed = 0
gravity = 0.3
map_speed = 2
score = 0
high_score = 0
active = True
heli = pygame.transform.scale(pygame.image.load('helicopter.png'), (60, 60))
pygame.mixer_music = pygame.mixer.Sound('mixkit-air-traffic-ambience-with-helicopter-2714.wav')
pygame.mixer_music.play(-1)





def generate_new():
    global player_y
    rects = []
    top_height = random.randint(0, 300)
    player_y = top_height + 150
    for i in range(total_rects):
        top_height = random.randint(top_height - spacer, top_height + spacer)
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300
        top_rect = pygame.Rect(i * rect_width, 0, rect_width, top_height)
        bot_rect = pygame.Rect(i * rect_width, top_height + 300, rect_width, HEIGHT)
        rects.append(top_rect)
        rects.append(bot_rect)
    return rects


def draw_map(rects):
    for rect in rects:
        pygame.draw.rect(screen, (0, 0, 139), rect)  # dark blue obstacles
    pygame.draw.rect(screen, 'dark gray', [0, 0, WIDTH, HEIGHT], 12)


def draw_player():
    # Remove the hitbox circle, just draw helicopter image
    screen.blit(heli, (player_x - 40, player_y - 30))
    # Return player rect for collision detection instead of circle
    return pygame.Rect(player_x - 20, player_y - 20, 40, 40)



def move_player(y_pos, speed, fly):
    if fly:
        speed += gravity
    else:
        speed -= gravity
    y_pos -= speed
    return y_pos, speed


def move_rects(rects):
    global score
    for i in range(len(rects)):
        rects[i] = pygame.Rect(rects[i].x - map_speed, rects[i].y, rect_width, rects[i].height)
    # Remove off-screen rects and add new ones
    while rects and rects[0].right < 0:
        rects.pop(0)
        rects.pop(0)
        if rects:
            last_top_height = rects[-2].height
        else:
            last_top_height = random.randint(0, 300)
        top_height = random.randint(last_top_height - spacer, last_top_height + spacer)
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300
        new_top = pygame.Rect(rects[-2].x + rect_width if rects else WIDTH, 0, rect_width, top_height)
        new_bot = pygame.Rect(new_top.x, top_height + 300, rect_width, HEIGHT)
        rects.append(new_top)
        rects.append(new_bot)
        score += 1
    return rects


def check_collision(rects, circle, act):
    for rect in rects:
        if circle.colliderect(rect):
            act = False
    return act


run = True
while run:
    screen.fill((135, 206, 250))  # light blue background


    timer.tick(fps)
    if new_map:
        map_rects = generate_new()
        new_map = False
    draw_map(map_rects)
    player_circle = draw_player()
    if active:
        player_y, y_speed = move_player(player_y, y_speed, flying)
        map_rects = move_rects(map_rects)
    active = check_collision(map_rects, player_circle, active)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying = True
            if event.key == pygame.K_RETURN:
                if not active:
                    new_map = True
                    active = True
                    y_speed = 0
                    map_speed = 2
                    if score > high_score:
                        high_score = score
                    score = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flying = False

    map_speed = 2 + score // 50
    spacer = 10 + score // 100

    screen.blit(font.render(f'Score: {score}', True, 'black'), (20, 15))
    screen.blit(font.render(f'High Score: {high_score}', True, 'black'), (20, 565))
    if not active:
        screen.blit(font.render('Press Enter to Restart', True, 'black'), (300, 15))


    pygame.display.flip()

pygame.quit()
