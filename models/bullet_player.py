
from models.bullet import Bullet
import pygame


class BulletPlayer(Bullet):
    def __init__(self, pos_x, pos_y, direccion):
        super().__init__(pos_x, pos_y, direccion)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
