import pygame
import os
pygame.font.init()  # fonts
pygame.mixer.init()  # sounds

WIDTH = 1000
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game!")

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound("files/Assets_Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("files/Assets_Gun+Silencer.mp3")

HEALTH_FONT = pygame.font.SysFont("comisans", 40)
WINNER_FONT = pygame.font.SysFont("comisans", 100)

COLOUR = (78, 48, 87)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
SPEED = 5
BULLET_SPEED = 8
MAX_BULLETS = 3

SHUTTLE_WIDTH = 60
SHUTTLE_HEIGHT = 40

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

RED_SHUTTLE_IMAGE = pygame.image.load(os.path.join("files", "spaceship_red.png"))
YELLOW_SHUTTLE_IMAGE = pygame.image.load(os.path.join("files", "spaceship_yellow.png"))

RED_SHUTTLE = pygame.transform.rotate(pygame.transform.scale(RED_SHUTTLE_IMAGE, (SHUTTLE_WIDTH, SHUTTLE_HEIGHT)), 90)
YELLOW_SHUTTLE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHUTTLE_IMAGE, (SHUTTLE_WIDTH, SHUTTLE_HEIGHT)),
                                         270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("files", "space.png")), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Health {str(red_health)}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health {str(yellow_health)}", 1, WHITE)
    WINDOW.blit(red_health_text, (10, 10))
    WINDOW.blit(yellow_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WINDOW.blit(RED_SHUTTLE, (red.x, red.y))
    WINDOW.blit(YELLOW_SHUTTLE, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()


def red_movement(keys_present, red):
    if keys_present[pygame.K_a] and red.x - SPEED > 0:  # LEFT
        red.x -= SPEED
    if keys_present[pygame.K_d] and red.x + red.height + SPEED < BORDER.x:  # RIGHT
        red.x += SPEED
    if keys_present[pygame.K_w] and red.y - SPEED > 0:  # UP
        red.y -= SPEED
    if keys_present[pygame.K_s] and red.y + red.height + SPEED < HEIGHT - 15:  # DOWN
        red.y += SPEED


def yellow_movement(keys_present, yellow):
    if keys_present[pygame.K_LEFT] and yellow.x - SPEED > BORDER.x + BORDER.width:  # LEFT
        yellow.x -= SPEED
    if keys_present[pygame.K_RIGHT] and yellow.x + yellow.width + SPEED < WIDTH + 15:  # RIGHT
        yellow.x += SPEED
    if keys_present[pygame.K_UP] and yellow.y - SPEED > 0:  # UP
        yellow.y -= SPEED
    if keys_present[pygame.K_DOWN] and yellow.y + yellow.height + SPEED < HEIGHT - 15:  # DOWN
        yellow.y += SPEED


def hand_bullets(red, yellow, red_bullets, yellow_bullets):
    for bullet in red_bullets:
        bullet.x += BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x < 0:
            yellow_bullets.remove(bullet)


def winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(6000)


def main():
    red = pygame.Rect(100, 100, SHUTTLE_WIDTH, SHUTTLE_HEIGHT)
    yellow = pygame.Rect(800, 100, SHUTTLE_WIDTH, SHUTTLE_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + yellow.height // 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height // 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        if yellow_health <= 0:
            winner_text = "Red wins!"
        if winner_text != "":
            winner(winner_text)
            break

        keys_present = pygame.key.get_pressed()
        red_movement(keys_present, red)
        yellow_movement(keys_present, yellow)

        hand_bullets(red, yellow, red_bullets, yellow_bullets)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()

if __name__ == "__main__":
    main()
