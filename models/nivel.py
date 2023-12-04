from auxiliar.constantes import *
import pygame


from models.jugador import Jugador


class Nivel:
    def __init__(self, screen: pygame.surface.Surface, limite_w, limite_h, nombre_nivel) -> None:

        self.__configs = abrir_configuraciones().get(nombre_nivel)
        self.jugador_sprite = Jugador(0, 0, self.__configs)

        self.jugador = pygame.sprite.GroupSingle(self.jugador_sprite)

        background_path = self.__configs['background_img']
        self.nivel_background = pygame.image.load(background_path).convert()

        self.nivel_background = pygame.transform.scale(
            self.nivel_background, (ANCHO_VENTANA, ALTO_VENTANA))

        self.limit_w = limite_w
        self.limit_h = limite_h

        self.__main_screen = screen

    def run(self, delta_ms):
        self.jugador.m
        self.__main_screen.blit(self.nivel_background,
                                self.nivel_background.get_rect())
        self.jugador.draw(self.__main_screen)
        self.jugador.update()
