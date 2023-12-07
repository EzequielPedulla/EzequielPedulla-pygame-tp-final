import pygame
import random as rd
from auxiliar.surface_manager import SurfaceManager as sf
from auxiliar.constantes import *
from models.bullet_enemy import BulletEnemy
from models.bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, game_configs_dict):
        pygame.sprite.Sprite.__init__(self)
        self.enemigo = self.seleccionar_enemigo()
        self.walk_r = sf.get_surface_from_spritesheet(
            f'assets\graphics\movimientos\enemigo-caminar\{self.enemigo}-caminar.png', 5, 1)
        self.walk_l = sf.get_surface_from_spritesheet(
            f'assets\graphics\movimientos\enemigo-caminar\{self.enemigo}-caminar.png', 5, 1, True)

        self.frame = 0
        self.animation = self.walk_r
        self.image = self.animation[self.frame]

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        enemigo_configs = game_configs_dict.get('enemigo')
        self.gravity = enemigo_configs.get('gravedad')
        self.damage = 50
        self.frame_rate_ms = enemigo_configs.get('frame_rate')
        self.time_move = 0
        self.move_right = True
        self._porcentaje_shoot = enemigo_configs.get('porcentaje_shoot')
        self.mirando_derecha = True
        self.bullet_group = pygame.sprite.Group()

        self.move_direction = 1
        self.move_counter = 0
        self.health = 100

        self.rect_ground_colliction = pygame.Rect(
            self.rect.x + self.rect.w / 6, self.rect.y + self.rect.h - 10, self.rect.w/3, 5)
        self.enemy_dead_sound = pygame.mixer.Sound(
            'assets\sounds\enemy-dead.mp3')
        self.enemy_dead_sound.set_volume(0.2)
        self.clock = pygame.time.Clock()

    def seleccionar_enemigo(self):
        enemigo = rd.choice(['troll1', 'troll2', 'troll3'])
        return enemigo

    def limits_screen(self, direccion):

        # controlamos los limites de pantalla del enemigo
        self.direccion = direccion
        self.rect.x += self.move_direction
        self.move_counter += 1

        if direccion == self.mirando_derecha and self.move_counter > 100:

            self.move_direction *= -1  # se invierte la direccion de movimiento
            self.animation = self.walk_l
            self.move_counter = 0
            self.mirando_derecha = False
        elif self.mirando_derecha == False and self.move_counter > 100:
            self.move_direction *= 1
            self.animation = self.walk_r
            self.mirando_derecha = True
            self.move_counter = 0

    @property
    def get_bullets(self):
        return self.bullet_group

    def reduce_health(self):
        self.health -= 50
        if self.health <= 0:
            self.enemy_dead_sound.play()
            self.kill()

    def create_bullet(self):

        return BulletEnemy(self.rect.centerx, self.rect.centery, DIRECCION_R if self.mirando_derecha else DIRECCION_L)

    def shoot_laser(self):
        self.bullet_group.add(self.create_bullet())

    def can_shoot(self) -> bool:
        return rd.random() * 600 <= self._porcentaje_shoot

    def is_shooting(self) -> bool:
        return self.can_shoot()

    def do_movement(self, delta_ms):
        self.time_move += delta_ms
        if self.time_move >= self.frame_rate_ms:
            self.limits_screen(DIRECCION_R)

    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.do_movement(delta_ms)
        if self.is_shooting():
            self.shoot_laser()
        self.draw(screen)
        self.bullet_group.draw(screen)
        self.bullet_group.update()

    def draw(self, screen: pygame.surface.Surface):
        if (DEBUG):
            pass

        screen.blit(self.image, self.rect)
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(
            self.image, (100, 100))
