import json

ANCHO_VENTANA = 1200
ALTO_VENTANA = 800
FPS = 120
RUTA_CONFIGURACION = './configs/config.json'
DIRECCION_R = 1
DIRECCION_L = 0

DEBUG = False

RED = (255, 0, 0)
GREEN = (0, 0, 255)
BLUE = (0, 0, 255)

GROUND_LEVEL = 660


def abrir_configuraciones() -> dict:
    with open(RUTA_CONFIGURACION, 'r', encoding='utf-8') as config:
        return json.load(config)
