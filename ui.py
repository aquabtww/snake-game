import pygame.mouse


class Button:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.Font, callback=None):
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback

    def render(self, display):
        text = self.font.render(self.text, True, (255, 255, 255))
        pygame.draw.rect(display, (255, 255, 255), self.rect, 2)
        display.blit(text, (self.rect.x + 12, self.rect.y + self.rect.height // 6))

    def check_input(self, call=True) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if call and self.callback:
                self.callback()
            return True
        return False

    def update_text(self, text):
        self.text = text
