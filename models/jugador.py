from auxiliar.surface_manager import SurfaceManager as sf
import pygame
from auxiliar.constantes import *
from models.healthBar import HealthBar

from models.bullet_player import BulletPlayer


class Jugador(pygame.sprite.Sprite):

    def __init__(self, x, y, player_config) -> None:

        # cargamos las imagenes de las diferentes movimientos ,derecha y invirtiendo las izquierdas

        self.walk_r = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\caminar\caminar.png', 7, 1)
        self.walk_l = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\caminar\caminar.png', 7, 1, True)
        self.stay_r = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\iddle\iddle.png', 7, 1)
        self.stay_l = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\iddle\iddle.png', 7, 1, True)

        self.jump_r = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\caminar\caminar.png', 7, 1)
        self.jump_l = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\caminar\caminar.png', 7, 1, True)
        self.die_r = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\muerte\muerte.png', 7, 1)
        self.die_l = sf.get_surface_from_spritesheet(
            'assets\graphics\movimientos\muerte\muerte.png', 7, 1, True)

        self.frame = 0
        self.animation = self.stay_r
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()

        jugador_configs = player_config.get('jugador', {})

        self.speed_walk = jugador_configs.get('speed_walk')
        self.move_x = x
        self.move_y = y
        self.gravity = jugador_configs.get('gravedad')
        self.jump_power = jugador_configs.get('jump_power')
        self.rect = self.image.get_rect()
        self.direccion = DIRECCION_R
        self.is_jump = False
        self.tiempo_transcurrido_animacion = 0
        self.tiempo_transcurrido_movimiento = 0
        self.frame_rate_ms = jugador_configs.get('frame_rate')
        self.move_rate_ms = jugador_configs.get('move_rate_ms')
        self.y_start_jump = jugador_configs.get('y_start_jump')
        self.jump_height = jugador_configs.get('jump_height')
        self.rect_ground_colliction = pygame.Rect(
            self.rect.x + self.rect.w / 6, self.rect.y + self.rect.h - 10, self.rect.w/3, 5)

        self.is_alive = True
        self.health = 100
        self.health_bar = HealthBar(self.health, width=80, height=10)
        self.health_bar.rect.x = self.rect.x
        self.health_bar.rect.y = self.rect.y - 20
        self.damage = 25
        self.ready = True
        self.fire_time = jugador_configs.get('fire_time')
        self.fire_cooldown = jugador_configs.get('fire_cooldown')
        self.bullet_group = pygame.sprite.Group()
        self.puntaje_total = 0
        self.collected_coins = 0
        self.level_complete = False

        self.reset_counter = 0
        self.respawn_sound = pygame.mixer.Sound(
            'assets\sounds/respawn.mp3')
        self.coin_sound = pygame.mixer.Sound(
            'assets\sounds\coin.mp3')
        self.enemy_hit_sound = pygame.mixer.Sound(
            'assets\sounds\hit.mp3')
        self.heal_sound = pygame.mixer.Sound(
            'assets\sounds\heal.mp3')
        self.shoot_sound = pygame.mixer.Sound('assets\sounds/fire_shoot.mp3')
        self.shoot_sound.set_volume(0.2)
        self.heal_sound.set_volume(9)
        self.coin_sound.set_volume(0.8)
        self.enemy_hit_sound.set_volume(0.7)
        self.respawn_sound.set_volume(9)

    def walk(self, direccion):

        self.direccion = direccion
        if direccion == DIRECCION_R:
            self.move_x = self.speed_walk
            self.animation = self.walk_r

        else:
            self.move_x = -self.speed_walk
            self.animation = self.walk_l
        self.frame = 0

    def jump(self):

        if self.direccion == DIRECCION_R:

            self.y_start_jump = self.rect.y
            self.move_x = self.speed_walk
            self.move_y = -self.jump_power
            self.animation = self.jump_r

        else:
            self.move_x = -self.speed_walk
            self.move_y = -self.jump_power
            self.animation = self.jump_l

        self.frame = 0
        self.is_jump = True

    def stay(self):
        if self.direccion == DIRECCION_R:
            self.animation = self.stay_r
        else:
            self.animation = self.stay_l
        self.move_x = 0
        self.move_y = 0
        self.frame = 0

    def handle_event(self):
        keys = pygame.key.get_pressed()

    # Verifica si alguna tecla está siendo presionada (KEYDOWN)
        if (keys):
            if keys[pygame.K_LEFT]:
                self.walk(DIRECCION_L)
            if keys[pygame.K_RIGHT]:
                self.walk(DIRECCION_R)
            if keys[pygame.K_UP]:
                self.jump()
            if keys[pygame.K_SPACE]:
                self.shoot_fire()

        # Verifica si alguna tecla está siendo liberada (KEYUP)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                self.stay()

    def hacer_movimiento(self, delta_ms, lista_plataformas):

        # actualizamos la posisicon del personaje en pantalla

        self.tiempo_transcurrido_movimiento += delta_ms
        # verificamos si paso el tiempo suficiente
        if self.tiempo_transcurrido_movimiento >= self.move_rate_ms:
            # si la distancia en y es mayor a la altura de salto y no esta saltando
            if abs(self.rect.y) - abs(self.y_start_jump) > self.jump_height and self.is_jump:

                self.move_y = 0
            self.tiempo_transcurrido_movimiento = 0
            self.add_x(self.move_x)
            self.add_y(self.move_y)

        if not (self.is_on_platform(lista_plataformas)):
            # si no esta en la plataforma agregamos gravedad
            self.add_y(self.gravity)
        elif self.is_jump:
            self.is_jump = False

    def is_on_platform(self, lista_plataformas):
        # verificamos si el jugador esta sobre el suelo
        retorno = False
        if self.rect.y >= GROUND_LEVEL:
            retorno = True
        else:
            # verificamos si estamos en contacto con la plataforma
            for plataforma in lista_plataformas:
                if (self.rect_ground_colliction.colliderect(plataforma.rect_ground_colliction)):
                    retorno = True
                    break
        return retorno

    def add_x(self, delta_x):
        # actualizamos la posicion del personaje
        self.rect.x += delta_x
        self.rect_ground_colliction.x += delta_x

    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_colliction.y += delta_y

    def hacer_animacion(self, delta_ms):

        # actualiza la animacion del personaje

        self.tiempo_transcurrido_animacion += delta_ms
        # verificamos si paso el tiempo suficiente
        if self.tiempo_transcurrido_animacion >= self.frame_rate_ms:
            self.tiempo_transcurrido_animacion = 0
        if (self.frame < len(self.animation) - 1):
            self.frame += 1
        else:
            # si el frame es igual al ultimo la reinicia
            self.frame = 0

    def limitar_posicion_pantalla(self):
        # Asegurarse de que el jugador no se salga del lado izquierdo de la pantalla
        if self.rect.x < 0:
            self.rect.x = 0
            self.rect_ground_colliction.x = self.rect.x + self.rect.w / 6

        # Asegurarse de que el jugador no se salga del lado derecho de la pantalla
        if self.rect.x > ANCHO_VENTANA - self.rect.w:
            self.rect.x = ANCHO_VENTANA - self.rect.w
            self.rect_ground_colliction.x = self.rect.x + self.rect.w / 6

        # Asegurarse de que el jugador no se salga del lado superior de la pantalla
        if self.rect.y < 0:
            self.rect.y = 0
            self.rect_ground_colliction.y = self.rect.y + self.rect.h - 10

        # Asegurarse de que el jugador no se salga del lado inferior de la pantalla
        if self.rect.y > ALTO_VENTANA - self.rect.h:
            self.rect.y = ALTO_VENTANA - self.rect.h
            self.rect_ground_colliction.y = self.rect.y + self.rect.h - 10

# almacenamos las balas del jugador
    @property
    def get_bullets(self):
        return self.bullet_group

    def reduce_health_trampa(self):
        self.health_bar.current_health -= 1

        if self.health_bar.current_health <= 0:

            self.is_alive = False
            self.reset(0, 0)

    def reduce_health(self):

        self.health_bar.current_health -= self.damage
        if self.health_bar.current_health <= 0:

            self.is_alive = False
            self.reset(0, 0)
            self.respawn_sound.play()

    def shoot_fire(self):
        if self.ready:
            self.shoot_sound.play()
            bullet = self.create_bullet()
            self.bullet_group.add(bullet)
            self.ready = False
            self.fire_time = pygame.time.get_ticks()

    def create_bullet(self):

        return BulletPlayer(self.rect.centerx, self.rect.top, self.direccion)

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            # agregamos un cooldown para disparar
            if current_time - self.fire_time >= self.fire_cooldown:
                self.ready = True

    def check_coin_collision(self, coin_group):

        hits = pygame.sprite.spritecollide(self, coin_group, True)

        for hit_coin in hits:

            self.add_score(500)
            self.check_coin_collected()

    def check_coin_collected(self):
        self.coin_sound.play()
        self.collected_coins += 1
        if self.collected_coins >= 3:
            self.level_complete = True

    def add_score(self, points):
        self.puntaje_total += points

    def check_life_consumable_collision(self, healt_coins_group):
        hits = pygame.sprite.spritecollide(self, healt_coins_group, True)
        for hit_health_coin in hits:
            self.heal(50)

    def heal(self, health):
        self.heal_sound.play()
        self.health_bar.current_health += health

        if self.health_bar.current_health > 100:
            self.health_bar.current_health = 100

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.health_bar.current_health = 100
        self.is_alive = True
        self.level_complete = False
        self.last_damage_time = pygame.time.get_ticks()
        self.ready = True
        self.rect_ground_colliction = pygame.Rect(
            self.rect.x + self.rect.w / 6, self.rect.y + self.rect.h - 10, self.rect.w/3, 5)
        self.reset_counter += 1
        self.respawn_sound.play()

    def update(self, delta_ms, lista_plataformas, screen, coin_group):
        self.handle_event()
        self.hacer_movimiento(delta_ms, lista_plataformas)
        self.hacer_animacion(delta_ms)
        self.limitar_posicion_pantalla()
        self.recharge()
        self.health_bar.rect.x = self.rect.x

        self.health_bar.rect.y = self.rect.y - 20
        self.bullet_group.draw(screen)
        self.bullet_group.update()
        self.health_bar.update()
        self.bullet_group.draw(screen)
        self.bullet_group.update()

        # el delta obtenemos el tiempo que transcurrio desde que llamos al a funcion clock tick

    def draw(self, screen: pygame.surface.Surface):
        if (DEBUG):
            pygame.draw.rect(screen, RED, self.rect)
            pygame.draw.rect(screen, GREEN, self.rect_ground_colliction)
            print("Player Position:", self.rect.x, self.rect.y)

        self.image = self.animation[self.frame]
        screen.blit(self.image, self.rect)
        self.health_bar.draw(screen)
