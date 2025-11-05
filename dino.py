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
        animation_delay=150
    ):
        assert jump_speed < 0 and jump_height > 0, "jump_speed * t^2 + jump_height must be a downward opening parabola"
        
        self.costume_paths = costume_paths
        self.dimension = (width, height)
        self.x = initial_x
        self.y = initial_y
        self.jump_speed = jump_speed
        self.jump_height = jump_height
        self.animation_delay = animation_delay

        self.costumes = self.load_costumes()
        self.costume_index = 0
        self.last_switch_time = 0
    
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
    
    @property
    def current_costume(self):
        return self.costumes[self.costume_index]
    
    @property
    def coordinates(self):
        return self.x, self.y