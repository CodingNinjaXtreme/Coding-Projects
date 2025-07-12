import pygame
import time

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cookie Clicker with Buttons")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('comicsans', 30)

cookie = pygame.image.load('Cookie.png').convert_alpha()
cookie = pygame.transform.scale(cookie, (200, 200))
cookie_rect = cookie.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

click_sound = pygame.mixer.Sound('click-151673.mp3')

cookie_count = 0
cookies_per_click = 1
cookies_per_second = 0

# Upgrade costs and ownership counts
grandma_cost = 50
cursor_cost = 15
grandma_owned = 0
cursor_owned = 0

# Define button properties
button_width = 260
button_height = 60
button_margin = 20
bottom_y = SCREEN_HEIGHT - button_height - 30

# Define buttons as rects
grandma_button_rect = pygame.Rect(20, bottom_y, button_width, button_height)
cursor_button_rect = pygame.Rect(20 + button_width + button_margin, bottom_y, button_width, button_height)
reset_button_rect = pygame.Rect(20 + 2 * (button_width + button_margin), bottom_y, button_width, button_height)

def format_cookies(num):
    return f"{num:,}"

running = True
while running:
    screen.fill((255, 255, 255))

    current_time = time.time()
    delta = current_time - last_tick if 'last_tick' in locals() else 0
    if delta >= 1:
        cookie_count += cookies_per_second
        last_tick = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if cookie_rect.collidepoint(pygame.mouse.get_pos()):
                cookie_count += cookies_per_click
                click_sound.play()
            elif grandma_button_rect.collidepoint(pygame.mouse.get_pos()):
                if cookie_count >= grandma_cost:
                    cookie_count -= grandma_cost
                    grandma_owned += 1
                    grandma_cost = int(grandma_cost * 1.3)
            elif cursor_button_rect.collidepoint(pygame.mouse.get_pos()):
                if cookie_count >= cursor_cost:
                    cookie_count -= cursor_cost
                    cursor_owned += 1
                    cursor_cost = int(cursor_cost * 1.3)
            elif reset_button_rect.collidepoint(pygame.mouse.get_pos()):
                cookie_count = 0
                grandma_owned = 0
                cursor_owned = 0
                grandma_cost = 50
                cursor_cost = 15
                cookies_per_click = 1
                cookies_per_second = 0

    cookies_per_second = grandma_owned
    cookies_per_click = 1 + cursor_owned

    screen.blit(cookie, cookie_rect)

    count_text = FONT.render(f"Cookies: {format_cookies(cookie_count)}", True, (0, 0, 0))
    screen.blit(count_text, (20, 20))

    cpc_text = FONT.render(f"Cookies per click: {format_cookies(cookies_per_click)}", True, (0, 0, 0))
    screen.blit(cpc_text, (20, bottom_y - 110))

    cps_text = FONT.render(f"Cookies per second: {format_cookies(cookies_per_second)}", True, (0, 0, 0))
    screen.blit(cps_text, (20, bottom_y - 75))

    mouse_pos = pygame.mouse.get_pos()
    buttons = [
        (grandma_button_rect, f"Grandma ({format_cookies(grandma_owned)}) - {format_cookies(grandma_cost)}"),
        (cursor_button_rect, f"Cursor ({format_cookies(cursor_owned)}) - {format_cookies(cursor_cost)})"),
        (reset_button_rect, "Reset")
    ]
    for rect, text in buttons:
        color = (170, 170, 170) if rect.collidepoint(mouse_pos) else (200, 200, 200)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        text_surf = FONT.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.midleft = (rect.x + 15, rect.y + rect.height // 2)
        screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
