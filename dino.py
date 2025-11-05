import pygame


class Dino:
    def __init__(
        self,
        costume_paths,
        width,
        height,
        initial_x,
        initial_y,
        jump_speed,
        jump_height,
        animation_delay=150,
    ):
        assert jump_speed > 0 and jump_height > 0
        
        self.costume_paths = costume_paths
        self.dimension = (width, height)
        self.x = initial_x
        self.y = initial_y
        self.initial_y = initial_y
        self.jump_speed = jump_speed
        self.jump_height = -jump_height
        self.animation_delay = animation_delay

        self.costumes = self.load_costumes()
        self.costume_index = 0
        self.last_switch_time = 0
        
        self.jump_time = None
        self.take_off_time, self.landing_time = self.get_jump_duration()
    
    def load_costumes(self):
        costumes = []
        for path in self.costume_paths:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, self.dimension)
            costumes.append(image)
        
        return costumes
    
    def switch_costume(self, current_time):
        if current_time - self.last_switch_time > self.animation_delay:
            self.costume_index = (self.costume_index + 1) % len(self.costumes)
            self.last_switch_time = current_time
    
    def jump_distance(self, time_elapsed):
        return self.jump_speed * (time_elapsed ** 2) + self.jump_height
    
    def get_jump_duration(self):
        a = self.jump_speed
        b = 0
        c = self.jump_height

        discriminant = b**2 - 4*a*c

        root1 = (-b + discriminant**0.5) / (2*a)
        root2 = (-b - discriminant**0.5) / (2*a)

        return sorted([root1, root2])
    
    def update_y(self, current_time):
        time_elapsed = current_time - self.jump_time + self.take_off_time
        
        if time_elapsed >= self.landing_time:
            self.jump_time = None
            self.y = self.initial_y
        else:
            self.y = int(self.jump_distance(time_elapsed) + self.initial_y)

    @property
    def is_jumping(self):
        return self.jump_time is not None

    @property
    def current_costume(self):
        return self.costumes[self.costume_index]
    
    @property
    def coordinates(self):
        return self.x, self.y


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 400))

    dino_costume_paths = ["assets/dino_left.png", "assets/dino_right.png"]

    dino = Dino(
        costume_paths=dino_costume_paths,
        width=100,
        height=100,
        initial_x=0,
        initial_y=10,
        jump_speed=1,
        jump_height=5,
    )
    
    dino.jump_time = 12
    print(dino.take_off_time, dino.landing_time)
    for t in range(12, 21, 1):
        if dino.is_jumping:
            dino.update_y(t)
            print(f"Time: {t} ms, Dino Y: {dino.y}")
    
    print(dino.y)
