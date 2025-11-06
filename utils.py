import pygame


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
