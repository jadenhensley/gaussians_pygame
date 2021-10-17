import pygame
pygame.font.init()

normal_font = pygame.font.SysFont('Bauhuas 93', 30)
small_font = pygame.font.SysFont('Bauhaus 93', 26)

def draw_text(surface, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surface.blit(img,(x, y))