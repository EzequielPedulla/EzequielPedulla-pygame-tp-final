# models/bullet.py
import pygame
from auxiliar.constantes import DIRECCION_R, ANCHO_VENTANA


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direccion):
        super().__init__()

        self.original_image = pygame.image.load(
            'assets/bullets/Bullet_000.png')
        self.original_image = pygame.transform.scale(
            self.original_image, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.bullet_speed = 2
        self.direccion = direccion

        if self.direccion != DIRECCION_R:
            self.flip_imagen()

    def flip_imagen(self):
        self.image = pygame.transform.flip(self.original_image, True, False)

    def update(self):
        if self.direccion == DIRECCION_R:
            self.rect.x += self.bullet_speed
        else:
            self.rect.x -= self.bullet_speed

        if self.rect.x <= 0 or self.rect.x >= ANCHO_VENTANA:
            self.kill()
