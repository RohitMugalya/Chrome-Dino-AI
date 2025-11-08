import pygame
import sys


def show_message(
    screen,
    message,
    font_size=32,
    text_color=(255, 255, 255),
    box_color=(50, 50, 50),
    padding=30,
    border_radius=12
):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=screen.get_rect().center)

    box_rect = text_rect.inflate(padding * 2, padding)

    pygame.draw.rect(screen, box_color, box_rect, border_radius=border_radius)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()


def show_restart_prompt(
    screen,
    y_position,
    message="Press ENTER to restart the game",
    font_size=36,
    text_color=(255, 255, 255),
):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(message, True, text_color)
    
    screen_rect = screen.get_rect()
    text_rect = text_surface.get_rect(center=(screen_rect.centerx, y_position))

    waiting = True
    clock = pygame.time.Clock()

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(30)
    
    return True


def check_collision(sprite1, pos1, sprite2, pos2):
    """
    Returns True if two images (with transparency) collide pixel-perfectly.
    sprite1, sprite2: pygame.Surface
    pos1, pos2: (x, y) top-left coordinates
    """
    rect1 = sprite1.get_rect(topleft=pos1)
    rect2 = sprite2.get_rect(topleft=pos2)

    if not rect1.colliderect(rect2):
        return False

    mask1 = pygame.mask.from_surface(sprite1)
    mask2 = pygame.mask.from_surface(sprite2)

    offset = (rect2.x - rect1.x, rect2.y - rect1.y)

    overlap_point = mask1.overlap(mask2, offset)

    return overlap_point is not None


def get_horizontal_distance(sprite1, sprite2):
    sprite1_center = sprite1.x + sprite1.dimension[0] / 2
    sprite2_center = sprite2.x + sprite2.dimension[0] / 2
    return sprite2_center - sprite1_center


def has_jump_over(dino, cactus):
    cactus_right = cactus.x + cactus.dimension[0]
    dino_left = dino.x
    return cactus_right < dino_left
