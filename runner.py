import pygame
import sys

from cactus import Cactus
from dino import Dino
from utils import check_collision

pygame.init()

DIMENSION = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
SCREEN_BACKGROUND_COLOR = (0, 0, 0)

DINO_DIMENSION = DINO_WIDTH, DINO_HEIGHT = 100, 100
DINO_COORDINATES = DINO_X, DINO_Y = int(0.1 * SCREEN_WIDTH), int(0.6 * SCREEN_HEIGHT)
CACTUS_Y = int(0.6 * SCREEN_HEIGHT) + 11
CACTUS_DIMENSION = CACTUS_WIDTH, CACTUS_HEIGHT = 50, 100

GROUND_COLOR = (0, 139, 139)
GROUND_THICKNESS = 10
RUN_SPEED = 5

ground = pygame.Rect(0, DINO_Y + DINO_HEIGHT, SCREEN_WIDTH, GROUND_THICKNESS)

screen = pygame.display.set_mode(DIMENSION)
pygame.display.set_caption("Chrome Dino AI")

dino_costume_paths = ["assets/dino_left.png", "assets/dino_right.png"]

dino = Dino(
    costume_paths=dino_costume_paths,
    width=DINO_WIDTH,
    height=DINO_HEIGHT,
    initial_x=DINO_X,
    initial_y=DINO_Y,
    jump_speed=-1,
    jump_height=50,
)

cactus = Cactus(
    image_path="assets/cactus.png",
    width=CACTUS_WIDTH,
    height=CACTUS_HEIGHT,
    initial_x=SCREEN_WIDTH,
    initial_y=CACTUS_Y,
    run_speed=RUN_SPEED,
    screen_width=SCREEN_WIDTH
)

running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dino.switch_costume(current_time)

    screen.fill(SCREEN_BACKGROUND_COLOR)
    pygame.draw.rect(screen, GROUND_COLOR, ground)
    screen.blit(dino.current_costume, dino.coordinates)
    screen.blit(cactus.image, cactus.coordinates)

    if check_collision(dino.current_costume, dino.coordinates, cactus.image, cactus.coordinates):
        print("Collision detected!")
    else:
        cactus.move()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
