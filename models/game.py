import pygame
import sys
from models.stage import Stage
from auxiliar.constantes import *
from models.jugador import Jugador
from auxiliar.biblioteca import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.clock = pygame.time.Clock()
        self.stage_number = 1
        self.stage = None
        cancion = pygame.mixer.music.load("assets/sounds/musica_fondo.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    def run_stage(self, stage_name: str):
        while True:
            if not self.stage or self.stage.is_level_complete():
                if self.stage_number <= 3:
                    self.stage = Stage(
                        self.screen, f'stage_{self.stage_number}')
                    self.stage_number += 1
                else:
                    print("Has completado el tercer nivel. ¡Juego completado!")
                    break
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            delta_ms = self.clock.tick(FPS)
            self.stage.run(delta_ms)
            pygame.display.flip()
