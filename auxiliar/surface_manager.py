import pygame as pg


class SurfaceManager:
    # utilizamos el metodo estatico no hace falta instansciarlo
    @staticmethod
    def get_surface_from_spritesheet(path: str, columna: int, filas: int, flip=False) -> list[pg.surface.Surface]:

        lista_recortada = []

        surface_imagen = pg.image.load(path)

        fotograma_ancho = int(surface_imagen.get_width()/columna)
        fotograma_alto = int(surface_imagen.get_height()/filas)

        x = 0

        for fila in range(filas):
            for columna in range(columna):
                x = columna * fotograma_ancho
                y = fila * fotograma_alto

                surface_fotograma = surface_imagen.subsurface(
                    x, y, fotograma_ancho, fotograma_alto)

                if flip:
                    surface_fotograma = pg.transform.flip(
                        surface_fotograma, True, False)
                lista_recortada.append(surface_fotograma)

        return lista_recortada
