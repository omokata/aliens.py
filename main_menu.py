import pygame
from ui import Button, Label
from util import load_score

class MainMenu:
    def __init__(self, game):
        self.game = game
        surface = self.game.main_screen
        self.font_Default30px = pygame.Font(None, 30)
        
        # setup play button
        play_button_size = (60, 40)
        play_button_pos = (
            (surface.get_width() - play_button_size[0]) / 2,
            (surface.get_height() - play_button_size[1]) / 2
        )
        self.play_button = Button(
            self.game.font_Default30px,
            "PLAY",
            pygame.Rect(
                play_button_pos,
                play_button_size
            ),
            "white",
            "pink"
        )
        self.score = load_score()
        label = f"Best Score: {self.score}"
        score_label_pos = (
            surface.get_width() / 2,
            (surface.get_height() / 2) - play_button_size[1]
        )
        self.score_label = Label(
            label,
            "black",
            "yellow",
            25,
            score_label_pos,
        )
        
    
    def render(self):
        self.score_label.render(self.game.main_screen)
        self.play_button.render(self.game.main_screen)
        if self.play_button.is_hover():
            self.play_button.set_bg_color("red")
        else:
            self.play_button.set_bg_color("pink")
        
        if self.play_button.is_click():
            self.game.set_state_play()
            

