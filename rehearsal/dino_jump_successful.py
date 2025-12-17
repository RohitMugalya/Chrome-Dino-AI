import pygame
import os
import math

pygame.init()

# -------------------------------------------------
# Parameters
# -------------------------------------------------
TAKE_OFF_DISTANCE = 135.0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# -------------------------------------------------
# Screen
# -------------------------------------------------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Successful Jump Visualization")

BG_COLOR = (0, 0, 0)
GROUND_COLOR = (0, 139, 139)
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
dino_img = pygame.image.load(os.path.join(ASSETS_DIR, "dino_left.png")).convert_alpha()
cactus_img = pygame.image.load(os.path.join(ASSETS_DIR, "cactus.png")).convert_alpha()

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
GROUND_TOP_Y = ground.top

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
dino1_center = (160, GROUND_Y)

cactus_center = (
    int(dino1_center[0] + TAKE_OFF_DISTANCE),
    GROUND_TOP_Y - CACTUS_SIZE[1] // 2
)

# Successful landing AFTER cactus
dino3_center = (
    cactus_center[0] + 120,
    GROUND_Y
)

# Mid-air dino (halfway between takeoff and landing)
mid_x = int((dino1_center[0] + dino3_center[0]) / 2)
mid_y = jump_y(
    mid_x,
    dino1_center[0],
    dino3_center[0],
    dino1_center[1],
    JUMP_HEIGHT
)
dino2_center = (mid_x, int(mid_y))

# -------------------------------------------------
# Center → top-left helper
# -------------------------------------------------
def topleft(center, size):
    return (int(center[0] - size // 2), int(center[1] - size // 2))

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

# Assets
screen.blit(cactus_img, topleft(cactus_center, CACTUS_SIZE[0]))
screen.blit(dino_img, topleft(dino1_center, DINO_SIZE))
screen.blit(dino_img, topleft(dino2_center, DINO_SIZE))
screen.blit(dino_img, topleft(dino3_center, DINO_SIZE))

# -------------------------------------------------
# Solid distance line (dino → cactus)
# -------------------------------------------------
line_y = dino1_center[1]

pygame.draw.line(
    screen,
    LINE_COLOR,
    (dino1_center[0] + DINO_SIZE // 2, line_y),
    (cactus_center[0] - CACTUS_SIZE[0] // 2, line_y),
    3
)

distance_text = label_font.render(f"{TAKE_OFF_DISTANCE}", True, TEXT_COLOR)
screen.blit(
    distance_text,
    distance_text.get_rect(
        center=((dino1_center[0] + cactus_center[0]) // 2, line_y - 22)
    )
)

# -------------------------------------------------
# Dotted jump trajectory (DINO 1 → DINO 3)
# -------------------------------------------------
for i in range(140):
    t = i / 140
    x = dino1_center[0] + t * (dino3_center[0] - dino1_center[0])
    y = jump_y(
        x,
        dino1_center[0],
        dino3_center[0],
        dino1_center[1],
        JUMP_HEIGHT
    )
    pygame.draw.circle(screen, PATH_COLOR, (int(x), int(y)), 2)

# -------------------------------------------------
# Legend (top-right)
# -------------------------------------------------
legend_x = SCREEN_WIDTH - 200
legend_y = 25

# d value
screen.blit(
    legend_font.render(f"d : {TAKE_OFF_DISTANCE}", True, TEXT_COLOR),
    (legend_x, legend_y)
)

# Solid line legend
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

# Dotted legend
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
    os.path.join(BLOG_ASSETS_DIR, "dino_jump_successful.png")
)

pygame.time.wait(1500)
pygame.quit()
