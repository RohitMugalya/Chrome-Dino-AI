import pygame
import sys

from utils import check_collision

pygame.init()

DIMENSION = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
SCREEN_BACKGROUND_COLOR = (0, 0, 0)

DINO_DIMENSION = DINO_WIDTH, DINO_HEIGHT = 100, 100
DINO_COORDINATES = DINO_X, DINO_Y = int(0.1 * SCREEN_WIDTH), int(0.6 * SCREEN_HEIGHT)
cactus_x, CACTUS_Y = int(0.8 * SCREEN_WIDTH), int(0.6 * SCREEN_HEIGHT) + 11
CACTUS_DIMENSION = CACTUS_WIDTH, CACTUS_HEIGHT = 50, 100

GROUND_COLOR = (0, 139, 139)
GROUND_THICKNESS = 10
RUN_SPEED = 5

ground = pygame.Rect(0, DINO_Y + DINO_HEIGHT, SCREEN_WIDTH, GROUND_THICKNESS)

screen = pygame.display.set_mode(DIMENSION)
pygame.display.set_caption("Chrome Dino AI")

dino_left = pygame.image.load("assets/dino_left.png").convert_alpha()
dino_right = pygame.image.load("assets/dino_right.png").convert_alpha()
cactus_image = pygame.image.load("assets/cactus.png").convert_alpha()

dino_left = pygame.transform.scale(dino_left, DINO_DIMENSION)
dino_right = pygame.transform.scale(dino_right, DINO_DIMENSION)
cactus_image = pygame.transform.scale(cactus_image, CACTUS_DIMENSION)

dino_images = [dino_left, dino_right]
dino_index = 0
last_switch_time = 0
ANIMATION_DELAY = 150

running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_time - last_switch_time > ANIMATION_DELAY:
        dino_index = (dino_index + 1) % len(dino_images)
        last_switch_time = current_time

    screen.fill(SCREEN_BACKGROUND_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, ground)
    screen.blit(dino_images[dino_index], DINO_COORDINATES)
    screen.blit(cactus_image, (cactus_x, CACTUS_Y))
    
    if check_collision(dino_images[dino_index], DINO_COORDINATES, cactus_image, (cactus_x, CACTUS_Y)):
        print("Collision detected!")
    else:
        cactus_x = (cactus_x - RUN_SPEED) % SCREEN_WIDTH

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
