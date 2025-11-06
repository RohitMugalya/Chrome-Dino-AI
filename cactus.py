import pygame


class Cactus:
    def __init__(
        self,
        image_path,
        width,
        height,
        initial_x,
        initial_y,
        run_speed,
        screen_width
    ):
        self.image_path = image_path
        self.dimension = (width, height)
        self.x = initial_x
        self.y = initial_y
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.run_speed = run_speed
        self.screen_width = screen_width

        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.dimension)
    
    def move(self):
        self.x -= self.run_speed
        self.x %= self.screen_width
    
    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y
    
    def reset(self):
        self.reset_position()

    @property
    def coordinates(self):
        return self.x, self.y
    
    def __str__(self) -> str:
        outputs = [
            "Cactus(",
            f"  image_path={self.image_path!r},",
            f"  dimension={self.dimension!r},",
            f"  coordinates={self.coordinates!r},",
            f"  run_speed={self.run_speed!r},",
            ")",
        ]
        return "\n".join(outputs)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    
    cactus = Cactus(
        image_path="assets/cactus.png",
        width=50,
        height=100,
        initial_x=100,
        initial_y=200,
        run_speed=5,
        screen_width=800
    )
    
    print(cactus)