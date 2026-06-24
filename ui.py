import pygame

class Button:
    def __init__(self, font, text, rect, color, bg_color, antialias=True):
        self.font = font
        self.text = text
        self.rect = rect
        self.color = color
        self.bg_color = bg_color
        self.antialias = antialias
        
        self.was_click = False
    
    def is_hover(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)
    
    def is_click(self):
        if self.is_hover() and pygame.mouse.get_pressed()[0] and not self.was_click:
            self.was_click = True
            return True
        return False

    def set_bg_color(self, color):
        self.bg_color = color
    
    def render(self, surface):
        button_text = self.font.render(self.text, self.antialias, self.color)
        button = pygame.draw.rect(
            surface,
            self.bg_color,
            self.rect
        )
        button_text_rect = button_text.get_rect(center=button.center)
        surface.blit(button_text, button_text_rect)

class Label:
    def __init__(self, text, color, bg_color, font_px, pos):
        self.font = pygame.Font(None, font_px)
        self.label = self.font.render(
            text,
            False,
            color
            )
        self.bg_color = bg_color
        self.pos = pos
        self.label_rect = self.label.get_rect(center=self.pos)
    
    def render(self, surface):
        pygame.draw.rect(
            surface,
            self.bg_color,
            self.label_rect
        )
        surface.blit(self.label, self.label_rect)
        
