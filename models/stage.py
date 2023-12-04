from auxiliar.constantes import abrir_configuraciones
import pygame
from models.jugador import Jugador
from auxiliar.constantes import ANCHO_VENTANA, ALTO_VENTANA, FPS
from auxiliar.biblioteca import *
import sys


class Stage:
    def __init__(self, screen: pygame.surface.Surface, stage_name: str):
        self.stage_name = stage_name
        self.game_timer = 180

        self.configs = abrir_configuraciones().get(stage_name)
        self.jugador = Jugador(0, 0, self.configs)
        self.jugador.reset(0, 0)
        self.screen = screen
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(cargar_enemigos(self.configs))
        self.plataforma_group = pygame.sprite.Group()
        self.plataforma_group.add(cargar_plataformas(self.configs))
        self.plataforma_trampa_group = pygame.sprite.Group()
        self.plataforma_trampa_group.add(
            cargar_plataformas_trampas(self.configs))
        self.coin_group = pygame.sprite.Group()
        self.coin_group.add(cargar_monedas(self.configs))
        self.healt_coins_group = pygame.sprite.Group()
        self.healt_coins_group.add(cargar_vidas(self.configs))

    def cargar_imagen_fondo(self):
        imagen_fondo_path = self.configs.get("background_img")
        imagen_fondo = pygame.image.load(imagen_fondo_path)
        return pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))

    def is_level_complete(self):
        return self.jugador.level_complete

    def run(self, delta_ms):
        imagen_fondo = self.cargar_imagen_fondo()
        self.screen.blit(imagen_fondo, imagen_fondo.get_rect())

        self.coin_group.update()
        self.coin_group.draw(self.screen)
        self.healt_coins_group.draw(self.screen)
        self.jugador.check_coin_collision(self.coin_group)
        self.jugador.check_life_consumable_collision(
            self.healt_coins_group)
        for plataforma in self.plataforma_group:
            plataforma.draw(self.screen)
        for plataforma in self.plataforma_trampa_group:
            plataforma.draw(self.screen)

        for enemy in self.enemy_group:
            enemy.draw(self.screen)
            for bullet in enemy.get_bullets:
                hits = pygame.sprite.spritecollide(
                    bullet, [self.jugador], False)
                for hit_player in hits:
                    hit_player.reduce_health()
                    self.jugador.enemy_hit_sound.play()
                    bullet.kill()
                bullet.update()
                bullet.draw(self.screen)
            enemy.update(delta_ms, self.screen)

        for plataforma_trampa in self.plataforma_trampa_group:
            if self.jugador.rect.colliderect(plataforma_trampa.rect_ground_colliction):
                current_time = pygame.time.get_ticks()
                if current_time - self.jugador.last_damage_time >= self.jugador.damage_cooldown:
                    self.jugador.enemy_hit_sound.play()
                    self.jugador.reduce_health_trampa()

        self.jugador.update(delta_ms, self.plataforma_group,
                            self.screen, self.coin_group)
        self.jugador.draw(self.screen)
        self.jugador.health_bar.draw(self.screen)

        for bullet in self.jugador.get_bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemy_group, False)
            for hit_enemy in hits:
                hit_enemy.reduce_health()
                bullet.kill()
                self.jugador.add_score(200)
            bullet.update()
            bullet.draw(self.screen)
        font = pygame.font.Font(None, 36)
        puntaje_surface = font.render(
            f"Puntaje: {self.jugador.puntaje_total}", True, (255, 255, 255))
        self.screen.blit(puntaje_surface, (10, 10))
        tiempo_transcurrido = pygame.time.get_ticks()//1000

        if tiempo_transcurrido >= self.game_timer:
            pygame.quit()
            sys.exit()
        text_tiempo_restante = font.render(
            f'Tiempo restante: {self.game_timer - tiempo_transcurrido}', True, (255, 255, 255))
        self.screen.blit(text_tiempo_restante, (500, 10))
        reset_font = pygame.font.Font(None, 24)
        reset_text = reset_font.render(
            f"Resets: {self.jugador.reset_counter}", True, (255, 255, 255))
        self.screen.blit(reset_text, (10, 40))

        self.enemy_group.update(delta_ms, self.screen)
