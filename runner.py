import pygame
import sys

from cactus import Cactus
from dino import Dino
from dinoai import DinoAI
from utils import check_collision, has_jump_over, show_message, show_restart_prompt, get_horizontal_distance

pygame.init()

DIMENSION = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
SCREEN_BACKGROUND_COLOR = (0, 0, 0)

DINO_DIMENSION = DINO_WIDTH, DINO_HEIGHT = 100, 100
DINO_COORDINATES = DINO_X, DINO_Y = int(0.1 * SCREEN_WIDTH), int(0.6 * SCREEN_HEIGHT)
CACTUS_Y = int(0.6 * SCREEN_HEIGHT) + 11
CACTUS_DIMENSION = CACTUS_WIDTH, CACTUS_HEIGHT = 50, 100

RESTART_PROMPT_Y = int(0.4 * SCREEN_HEIGHT)

GROUND_COLOR = (0, 139, 139)
GROUND_THICKNESS = 10
RUN_SPEED = 8

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
    jump_speed=2e-3,
    jump_height=int(0.5 * SCREEN_HEIGHT),
)

dino_ai = DinoAI()

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
    estimated_distance = get_horizontal_distance(dino, cactus)
    has_collided = check_collision(dino.current_costume, dino.coordinates, cactus.image, cactus.coordinates)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not dino.is_jumping:
                take_off_distance = estimated_distance
                dino.jump_time = current_time

    
    if not cactus.passed and has_jump_over(dino, cactus) and not has_collided:
        dino_ai.record_observation(take_off_distance, dino_ai.jump_successful)
        cactus.passed = True
    if has_collided:
        if dino.is_jumping:
            dino_ai.record_observation(take_off_distance, dino_ai.jump_failed)
        else:
            dino_ai.record_observation(estimated_distance, dino_ai.jump_successful)

        show_message(screen, "Re-training AI on new obervations...")
        running = show_restart_prompt(screen, RESTART_PROMPT_Y)
        dino.reset()
        cactus.reset()
    else:
        if dino.is_jumping:
            dino.update_y(current_time)
        cactus.move()
        dino.switch_costume(current_time)

        screen.fill(SCREEN_BACKGROUND_COLOR)
        pygame.draw.rect(screen, GROUND_COLOR, ground)
        screen.blit(dino.current_costume, dino.coordinates)
        screen.blit(cactus.image, cactus.coordinates)
        pygame.display.flip()

    clock.tick(60)

pygame.quit()
dino_ai.save_observations()
sys.exit()
