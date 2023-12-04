import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health, width, height):
        super().__init__()

        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        # Actualizar la longitud de la barra de vida
        self.rect.width = int(
            (self.current_health / self.max_health) * self.width)

        # Cambiar el color de la barra de vida según la salud restante
        if self.current_health > self.max_health / 2:
            self.image.fill((0, 255, 0))  # Verde
        elif self.current_health > self.max_health / 4:
            self.image.fill((255, 255, 0))  # Amarillo
        else:
            self.image.fill((255, 0, 0))  # Rojo

    def draw(self, screen):
        screen.blit(self.image, self.rect)
