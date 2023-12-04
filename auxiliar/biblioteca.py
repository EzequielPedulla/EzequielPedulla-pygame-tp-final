import pygame

from models.plataforma import Plataforma
from models.enemy import Enemy
from models.coin import Coin
from models.health_coin import HealthCoin
from models.plataforma_trampa import PlataformaTrampa


def cargar_plataformas(config):
    plataformas = []

    for plataforma_config in config.get("plataformas", []):

        x = plataforma_config.get("x", 0)
        y = plataforma_config.get("y", 0)
        height = plataforma_config.get("height", 60)
        width = plataforma_config.get("width", 60)

        plataformas.append(Plataforma(x, y, height, width))

    return plataformas


def cargar_enemigos(config):

    enemigos = []

    for enemigo_config in config.get('enemigo', []).get('enemigos_coords'):

        x = enemigo_config.get('x')

        y = enemigo_config.get('y')

        enemigos.append(Enemy(x, y, config))

    return enemigos


def cargar_monedas(config):
    coins = []

    for coins_config in config.get("coins", []):

        x = coins_config.get("x", 0)
        y = coins_config.get("y", 0)

        coins.append(Coin(x, y))

    return coins


def cargar_vidas(config):
    healt_coins = []

    for healt_coin in config.get("health_coin", []):

        x = healt_coin.get("x", 0)
        y = healt_coin.get("y", 0)

        healt_coins.append(HealthCoin(x, y))

    return healt_coins


def cargar_plataformas_trampas(config):
    plataformas_trampas = []

    for plataforma_config in config.get('plataformas_trampa', []):

        x = plataforma_config.get("x", 0)
        y = plataforma_config.get("y", 0)
        height = plataforma_config.get("height", 60)
        width = plataforma_config.get("width", 60)

        plataformas_trampas.append(PlataformaTrampa(x, y, height, width))

    return plataformas_trampas
