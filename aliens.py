# This is my own recreation of aliens example of Pygame
# TODO: should've used spritecollide, didn't know it
# TODO: should've separated debug logic into another class
# so i can use it on UI as well.
# TODO: UI module can be better. For now it works
# This is my first python project so please don't judge
# I'm still a beginner.

import pygame
from main_menu import MainMenu
from util import load_image, load_sound, save_score, load_score, resource_path
from entity import Player, Bullet, Alien, AlienLaser, Explosion
import random

SCORE = 0
DEBUG = False

class GameState:
    MAIN_MENU = 1
    PLAYING = 2
    END = 3

class Score(pygame.sprite.Sprite):
    containers = None
    def __init__(self, pos):
        super().__init__(self.containers)
        self.font = pygame.Font(None, 30)
        self.lastscore = -1
        self.color = "yellow"
        self.update()
        self.rect = self.image.get_rect(bottomleft=pos)

    def update(self):
        global SCORE
        if self.lastscore != SCORE:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, False, self.color)

class Game:
    WIN_SIZE = (800, 600)
    WIN_TITLE = "My Imperfect Aliens"
    
    def __init__(self, screen):
        self.clock = pygame.Clock()
        self.main_screen = screen
        self.game_state = GameState.MAIN_MENU
        self.font_Default30px = pygame.Font(None, 30)
        self.main_menu = MainMenu(self)
        
        # containers
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.alien_sprites = pygame.sprite.Group()
        self.alien_laser_sprites = pygame.sprite.Group()
        self.particle_sprites = pygame.sprite.Group()
        
        # setting up player
        Player.containers = self.all_sprites
        Player.image = load_image("images/air_defense.png")
        self.player = Player(self, 300)
        # setting up bullet
        Bullet.containers = self.bullet_sprites, self.all_sprites
        Bullet.image = load_image("images/bullet.png")
        # setting up alien
        Alien.containers = self.alien_sprites, self.all_sprites
        Alien.image = load_image("images/aliens.png")
        Alien(self)
        # setting up alien laser
        AlienLaser.containers = self.alien_laser_sprites, self.all_sprites
        AlienLaser.image = load_image("images/alien_laser.png")
        # setting up explosion
        Explosion.containers = self.particle_sprites, self.all_sprites
        img = load_image("images/explosion1.gif")
        Explosion.images = [img, pygame.transform.flip(img, True, True)]
        
        Score.containers = self.all_sprites
        self.score = Score(self.main_screen.get_rect().bottomleft)
        
        # Setup background
        bg_image = load_image("images/background.png")
        self.background = pygame.Surface(self.main_screen.get_rect().size)
        for x in range(0, screen.get_rect().width, bg_image.get_width()):
            self.background.blit(bg_image, (x, 0))
        pygame.display.flip()
        
        # load sound and music
        self.boom_sound = load_sound("sounds/boom.wav")
        self.shot_sound = load_sound("sounds/car_door.wav")
        music = pygame.mixer_music.load(resource_path("sounds/house_lo.wav"))
        pygame.mixer_music.play(-1)
        
        # Misc
        self.alien_spawn_cooldown = random.randint(1, 2)
        self.alien_spawn_timer = 0
    
    def __debug_rect(self, rect, color):
        global DEBUG
        if not DEBUG:
            return
        pygame.draw.rect(
            self.main_screen,
            color,
            rect,
            width=1
        )
    
    def gameplay(self, dt):
        global SCORE
        self.alien_spawn_timer += dt
        keystate = pygame.key.get_pressed()

        # Shooting and bullet
        space_pressed = keystate[pygame.K_SPACE]
        if self.player.can_fire and space_pressed:
            self.player.can_fire = False
            self.shot_sound.play()
            Bullet((self.player.rect.centerx, self.player.rect.centery - 30))
        
        # Can only shoot if not on cooldown
        if not self.player.can_fire:
            self.player.fire_cooldown_timer -= dt
            if self.player.fire_cooldown_timer <= 0:
                self.player.fire_cooldown_timer = self.player.fire_cooldown 
                self.player.can_fire = True
        
        for bullet in self.bullet_sprites:
            bullet.update(dt)
            self.__debug_rect(bullet.rect, "blue")
        
        # Aliens
        if self.alien_spawn_timer >= self.alien_spawn_cooldown:
            Alien(self)
            self.alien_spawn_timer = 0
            self.alien_spawn_cooldown = random.randint(1, 2)
        
        for alien in self.alien_sprites:
            alien.update(dt)
            if alien.can_fire:
                AlienLaser(self, alien.rect.midbottom)
                alien.can_fire = False
            if not alien.can_fire:
                alien.fire_cooldown_timer -= dt
                if alien.fire_cooldown_timer <= 0:
                    alien.can_fire = True
                    alien.fire_cooldown_timer = alien.fire_cooldown
            idx = alien.rect.collidelist([b.rect for b in self.bullet_sprites])
            if idx > -1:
                alien.kill()
                Explosion(alien)
                Explosion(self.bullet_sprites.sprites()[idx])
                self.boom_sound.play()
                self.bullet_sprites.sprites()[idx].kill()
                SCORE += 1
            self.__debug_rect(alien.rect, "green")
        
        for laser in self.alien_laser_sprites:
            laser.update(dt)
            self.__debug_rect(laser.rect, "black")
        
        for particle in self.particle_sprites:
            particle.update(dt)
        
        # Player
        direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        self.player.move(direction, dt)
        self.__debug_rect(self.player.rect, "red")
        if self.player.rect.collidelist([a.rect for a in self.alien_sprites]) > -1 \
            or self.player.rect.collidelist([l.rect for l in self.alien_laser_sprites]) > -1:
            self.player.kill()
            self.boom_sound.play()
            self.game_state = GameState.MAIN_MENU
            if SCORE > load_score():
                save_score(SCORE)
            SCORE = 0
            self.__init__(self.main_screen)
        
        self.score.update()

        self.all_sprites.draw(self.main_screen)
    
    def run(self):
        deltatime = 0
        while self.game_state != GameState.END:
            self.main_screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = GameState.END

            if self.game_state == GameState.MAIN_MENU:
                self.main_menu.render()
            elif self.game_state == GameState.PLAYING:
                self.gameplay(deltatime)
            else:
                break
            pygame.display.flip()
            # divide by 1000 because self.clock.tick returns in ms
            deltatime = self.clock.tick(60) / 1000
        pygame.quit()
    
    def set_state_play(self):
        self.game_state = GameState.PLAYING

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(Game.WIN_TITLE)
    game = Game(pygame.display.set_mode(Game.WIN_SIZE))
    game.run()
