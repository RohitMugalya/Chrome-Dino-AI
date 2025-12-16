import pygame
import os

pygame.init()

# -----------------------------
# Screen configuration
# -----------------------------
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino–Cactus Distance Illustration")

BG_COLOR = (0, 0, 0)
LINE_COLOR = (0, 220, 220)
TEXT_COLOR = (255, 255, 255)
GROUND_COLOR = (0, 139, 139)
GROUND_THICKNESS = 10

# -----------------------------
# Resolve project root
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# Asset paths
# -----------------------------
DINO_IMG_PATH = os.path.join(PROJECT_ROOT, "assets", "dino_left.png")
CACTUS_IMG_PATH = os.path.join(PROJECT_ROOT, "assets", "cactus.png")

dino_img = pygame.image.load(DINO_IMG_PATH).convert_alpha()
cactus_img = pygame.image.load(CACTUS_IMG_PATH).convert_alpha()

# Resize for clarity
dino_img = pygame.transform.smoothscale(dino_img, (100, 100))
cactus_img = pygame.transform.smoothscale(cactus_img, (50, 100))

# -----------------------------
# Positions (consistent with runner.py)
# -----------------------------
DINO_X = int(0.1 * SCREEN_WIDTH)
DINO_Y = int(0.6 * SCREEN_HEIGHT)
CACTUS_Y = int(0.6 * SCREEN_HEIGHT) + 11

dino_pos = (DINO_X, DINO_Y)
cactus_pos = (580, CACTUS_Y)

# Ground
ground = pygame.Rect(
    0,
    DINO_Y + dino_img.get_height(),
    SCREEN_WIDTH,
    GROUND_THICKNESS
)

# -----------------------------
# Distance line
# -----------------------------
line_y = DINO_Y + dino_img.get_height() // 2
line_start_x = dino_pos[0] + dino_img.get_width()
line_end_x = cactus_pos[0]

# -----------------------------
# Font (LaTeX-style fallback)
# -----------------------------
font_candidates = [
    "Computer Modern",
    "Latin Modern Math",
    "DejaVu Serif",
    "Times New Roman",
    "Arial"
]

font_path = None
for f in font_candidates:
    font_path = pygame.font.match_font(f)
    if font_path:
        break

label_font = pygame.font.Font(font_path, 26)
legend_font = pygame.font.Font(font_path, 20)

# -----------------------------
# Render scene
# -----------------------------
screen.fill(BG_COLOR)

# Ground
pygame.draw.rect(screen, GROUND_COLOR, ground)

# Sprites
screen.blit(dino_img, dino_pos)
screen.blit(cactus_img, cactus_pos)

# Distance line
pygame.draw.line(
    screen,
    LINE_COLOR,
    (line_start_x, line_y),
    (line_end_x, line_y),
    3
)

# Arrowheads
arrow = 8
pygame.draw.polygon(
    screen,
    LINE_COLOR,
    [
        (line_start_x, line_y),
        (line_start_x + arrow, line_y - arrow),
        (line_start_x + arrow, line_y + arrow),
    ],
)

pygame.draw.polygon(
    screen,
    LINE_COLOR,
    [
        (line_end_x, line_y),
        (line_end_x - arrow, line_y - arrow),
        (line_end_x - arrow, line_y + arrow),
    ],
)

# Distance label
d_label = label_font.render("d", True, TEXT_COLOR)
d_rect = d_label.get_rect(
    center=((line_start_x + line_end_x) // 2, line_y - 18)
)
screen.blit(d_label, d_rect)

# Legend (top-right)
legend_text = "d : distance (Dino → Cactus)"
legend_surface = legend_font.render(legend_text, True, TEXT_COLOR)
legend_rect = legend_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
screen.blit(legend_surface, legend_rect)

pygame.display.flip()

# -----------------------------
# Save screenshot
# -----------------------------
BLOG_ASSETS_DIR = os.path.join(PROJECT_ROOT, "rehearsal", "blog_assets")
os.makedirs(BLOG_ASSETS_DIR, exist_ok=True)

pygame.image.save(
    screen,
    os.path.join(BLOG_ASSETS_DIR, "dino_distance_visual.png")
)

pygame.time.wait(1500)
pygame.quit()
