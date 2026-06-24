import pygame
import random

class Player(pygame.sprite.Sprite):
    image = None
    containers = None

    def __init__(self, game, speed):
        super().__init__(self.containers)
        self.game = game
        self.can_fire = True
        self.fire_cooldown = 1
        self.fire_cooldown_timer = self.fire_cooldown
        self.rect = self.image.get_rect(midbottom=self.game.main_screen.get_rect().midbottom)
        self.speed = speed
        
    def move(self, direction, dt):
        self.rect.move_ip(direction * self.speed * dt, 0)
        self.rect.clamp_ip(self.game.main_screen.get_rect())

class Bullet(pygame.sprite.Sprite):
    speed = 400
    image = None
    containers = None
    
    def __init__(self, pos):
        super().__init__(self.containers)
        self.rect = self.image.get_rect(midbottom=pos)
    
    def update(self, dt):
        self.rect.move_ip(0, -self.speed * dt)
        if self.rect.top <= 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    image = None
    containers = None
    speed = 500
    
    def __init__(self, game):
        super().__init__(self.containers)
        self.screenrect = game.main_screen.get_rect()
        rect = (
            self.image.get_rect(),
            self.image.get_rect(topright=self.screenrect.topright)
        )
        self.can_fire = False
        self.fire_cooldown = random.randint(1, 3)
        self.fire_cooldown_timer = self.fire_cooldown
        self.rect = random.choice(rect)
        self.main_screen = game.main_screen
        self.direction = 0
    
    def update(self, dt):
        if self.rect.right >= self.screenrect.right:
            self.direction = -1
        elif self.rect.left <= self.screenrect.left:
            self.direction = 1

        self.rect.move_ip(self.direction * self.speed * dt, 0)
        
        if self.rect.right >= self.screenrect.right or \
            self.rect.left <= self.screenrect.left:
            self.rect.move_ip(0, self.image.get_height())

class AlienLaser(pygame.sprite.Sprite):
    image = None
    containers = None
    speed = 380
    
    def __init__(self, game, pos):
        self.game = game
        super().__init__(self.containers)
        self.rect = self.image.get_rect(midtop=pos)
    
    
    def update(self, dt):
        self.rect.move_ip(0, self.speed * dt)
        if self.rect.bottom >= self.game.main_screen.get_rect().bottom:
            self.kill()
            Explosion(self)

class Explosion(pygame.sprite.Sprite):
    containers = None
    images = []
    defaultlife = 12  # total duration of animation
    animcycle = 3  # how many updates one frame last
    
    def __init__(self, actor):
        super().__init__(self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife
    
    def update(self, dt):
        self.life -= 1
        frame = (self.life // self.animcycle) % len(self.images)
        self.image = self.images[frame]
        if self.life <= 0:
            self.kill()
