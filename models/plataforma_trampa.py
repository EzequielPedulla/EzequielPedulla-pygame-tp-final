from auxiliar.constantes import *
import pygame
from auxiliar.surface_manager import SurfaceManager as sf


class PlataformaTrampa(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'assets\graphics/bloques\plataforma_trampa.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_ground_colliction = pygame.Rect(
            self.rect.x, self.rect.y, self.rect.w, 10)

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, RED, self.rect)
        screen.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, GREEN, self.rect_ground_colliction)
