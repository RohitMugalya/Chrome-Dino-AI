import pygame
import os
import math

pygame.init()

# -------------------------------------------------
# Adjustable parameters (BLOG CONTROL)
# -------------------------------------------------
TAKE_OFF_DISTANCE = 255.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# -------------------------------------------------
# Screen
# -------------------------------------------------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Jump Decision Visualization")

BG_COLOR = (0, 0, 0)
GROUND_COLOR = "brown"
LINE_COLOR = (0, 220, 220)
PATH_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)

GROUND_THICKNESS = 10

# -------------------------------------------------
# Dimensions
# -------------------------------------------------
DINO_SIZE = 100
CACTUS_SIZE = (50, 100)

# -------------------------------------------------
# Paths
# -------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BLOG_ASSETS_DIR = os.path.join(PROJECT_ROOT, "rehearsal", "blog_assets")
os.makedirs(BLOG_ASSETS_DIR, exist_ok=True)

# -------------------------------------------------
# Assets
# -------------------------------------------------
dino_img = pygame.image.load(os.path.join(ASSETS_DIR, "dinoai_left.png")).convert_alpha()
cactus_img = pygame.image.load(os.path.join(ASSETS_DIR, "green_cactus.png")).convert_alpha()

dino_img = pygame.transform.smoothscale(dino_img, (DINO_SIZE, DINO_SIZE))
cactus_img = pygame.transform.smoothscale(cactus_img, CACTUS_SIZE)

# -------------------------------------------------
# Ground
# -------------------------------------------------
GROUND_Y = int(0.68 * SCREEN_HEIGHT)
ground = pygame.Rect(
    0,
    GROUND_Y + DINO_SIZE // 2,
    SCREEN_WIDTH,
    GROUND_THICKNESS
)

# -------------------------------------------------
# Jump physics
# -------------------------------------------------
JUMP_HEIGHT = int(0.5 * SCREEN_HEIGHT)

def jump_y(x, x0, x1, y0, h):
    t = (x - x0) / (x1 - x0)
    return y0 - 4 * h * t * (1 - t)

# -------------------------------------------------
# Logical CENTER positions
# -------------------------------------------------
dino_takeoff_center = (160, GROUND_Y)
GROUND_TOP_Y = ground.top

cactus_center = (
    int(dino_takeoff_center[0] + TAKE_OFF_DISTANCE),
    GROUND_TOP_Y - CACTUS_SIZE[1] // 2
)

mid_x = int(dino_takeoff_center[0] + TAKE_OFF_DISTANCE / 2)
mid_y = jump_y(
    mid_x,
    dino_takeoff_center[0],
    cactus_center[0],
    dino_takeoff_center[1],
    JUMP_HEIGHT
)

dino_midair_center = (mid_x, int(mid_y))
dino_crash_center = (
    cactus_center[0] - 40,
    GROUND_TOP_Y - DINO_SIZE // 2
)

# -------------------------------------------------
# Center → top-left helper
# -------------------------------------------------
def topleft_from_center(center, size):
    return (
        int(center[0] - size // 2),
        int(center[1] - size // 2)
    )

# -------------------------------------------------
# Fonts
# -------------------------------------------------
font_path = pygame.font.match_font("DejaVu Serif")
label_font = pygame.font.Font(font_path, 22)
legend_font = pygame.font.Font(font_path, 18)

# -------------------------------------------------
# Render
# -------------------------------------------------
screen.fill(BG_COLOR)

# Ground
pygame.draw.rect(screen, GROUND_COLOR, ground)

# Cactus
screen.blit(
    cactus_img,
    topleft_from_center(cactus_center, CACTUS_SIZE[0])
)

# Dinos
screen.blit(
    dino_img,
    topleft_from_center(dino_takeoff_center, DINO_SIZE)
)

screen.blit(
    dino_img,
    topleft_from_center(dino_midair_center, DINO_SIZE)
)

screen.blit(
    dino_img,
    topleft_from_center(dino_crash_center, DINO_SIZE)
)

# -------------------------------------------------
# Distance line
# -------------------------------------------------
line_y = dino_takeoff_center[1]

pygame.draw.line(
    screen,
    LINE_COLOR,
    (dino_takeoff_center[0] + DINO_SIZE // 2, line_y),
    (cactus_center[0] - CACTUS_SIZE[0] // 2, line_y),
    3
)

distance_label = label_font.render(f"{TAKE_OFF_DISTANCE}", True, TEXT_COLOR)
screen.blit(
    distance_label,
    distance_label.get_rect(
        center=(
            (dino_takeoff_center[0] + cactus_center[0]) // 2,
            line_y - 22
        )
    )
)

# -------------------------------------------------
# Dotted jump trajectory
# -------------------------------------------------
for i in range(120):
    t = i / 120
    x = dino_takeoff_center[0] + t * TAKE_OFF_DISTANCE
    y = jump_y(
        x,
        dino_takeoff_center[0],
        cactus_center[0],
        dino_takeoff_center[1],
        JUMP_HEIGHT
    )
    pygame.draw.circle(screen, PATH_COLOR, (int(x), int(y)), 2)

# -------------------------------------------------
# Legend (top-right)
# -------------------------------------------------
legend_x = SCREEN_WIDTH - 200
legend_y = 25

# d : take-off distance
screen.blit(
    legend_font.render(f"d : {TAKE_OFF_DISTANCE}", True, TEXT_COLOR),
    (legend_x, legend_y)
)

# Solid line visual + label
pygame.draw.line(
    screen,
    LINE_COLOR,
    (legend_x, legend_y + 30),
    (legend_x + 60, legend_y + 30),
    3
)
screen.blit(
    legend_font.render("distance", True, TEXT_COLOR),
    (legend_x + 70, legend_y + 22)
)

# Dotted curve visual + label
for i in range(12):
    pygame.draw.circle(
        screen,
        PATH_COLOR,
        (legend_x + i * 5, legend_y + 60),
        2
    )

screen.blit(
    legend_font.render("jump trajectory", True, TEXT_COLOR),
    (legend_x + 70, legend_y + 52)
)

pygame.display.flip()

# -------------------------------------------------
# Save screenshot
# -------------------------------------------------
pygame.image.save(
    screen,
    os.path.join(BLOG_ASSETS_DIR, "dino_jump_phases.png")
)

pygame.time.wait(1500)
pygame.quit()
