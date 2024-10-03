import pygame
import random
import math

pygame.init()

ANCHO, ALTO = 800, 600
TAMANO_CUADRICULA = 20
ANCHO_CUADRICULA = ANCHO // TAMANO_CUADRICULA
ALTO_CUADRICULA = ALTO // TAMANO_CUADRICULA
FPS = 10
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 120, 255)
MORADO = (128, 0, 128)
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Serpiente")
reloj = pygame.time.Clock()

controles = {
    "arriba": pygame.K_UP,
    "abajo": pygame.K_DOWN,
    "izquierda": pygame.K_LEFT,
    "derecha": pygame.K_RIGHT,
    "pausa": pygame.K_ESCAPE,
}


class Serpiente:
    def __init__(self):
        self.cuerpo = [(ANCHO_CUADRICULA // 2, ALTO_CUADRICULA // 2)]
        self.direccion = (1, 0)
        self.crecer = False
        self.color_cuerpo = VERDE
        self.color_cabeza = (0, 100, 0)

    def mover(self):
        cabeza = self.cuerpo[0]
        nueva_cabeza = (
            (cabeza[0] + self.direccion[0]) % ANCHO_CUADRICULA,
            (cabeza[1] + self.direccion[1]) % ALTO_CUADRICULA,
        )
        self.cuerpo.insert(0, nueva_cabeza)
        if not self.crecer:
            self.cuerpo.pop()
        else:
            self.crecer = False

    def cambiar_direccion(self, nueva_direccion):
        if (nueva_direccion[0] * -1, nueva_direccion[1] * -1) != self.direccion:
            self.direccion = nueva_direccion

    def verificar_colision(self):
        return len(self.cuerpo) != len(set(self.cuerpo))

    def dibujar(self):
        for i, segmento in enumerate(self.cuerpo):
            x, y = segmento[0] * TAMANO_CUADRICULA, segmento[1] * TAMANO_CUADRICULA
            if i == 0:
                self.dibujar_cabeza(x, y)
            else:
                if i == len(self.cuerpo) - 1:
                    prev_segment = self.cuerpo[i - 1]
                    dx = prev_segment[0] - segmento[0]
                    dy = prev_segment[1] - segmento[1]
                    angle = math.atan2(dy, dx)
                    points = [
                        (x + TAMANO_CUADRICULA // 2, y + TAMANO_CUADRICULA // 2),
                        (
                            x
                            + int(
                                TAMANO_CUADRICULA * 0.7 * math.cos(angle - math.pi / 6)
                            ),
                            y
                            + int(
                                TAMANO_CUADRICULA * 0.7 * math.sin(angle - math.pi / 6)
                            ),
                        ),
                        (
                            x
                            + int(
                                TAMANO_CUADRICULA * 0.7 * math.cos(angle + math.pi / 6)
                            ),
                            y
                            + int(
                                TAMANO_CUADRICULA * 0.7 * math.sin(angle + math.pi / 6)
                            ),
                        ),
                    ]
                    pygame.draw.polygon(pantalla, self.color_cuerpo, points)
                else:
                    pygame.draw.ellipse(
                        pantalla,
                        self.color_cuerpo,
                        (x + 2, y + 2, TAMANO_CUADRICULA - 4, TAMANO_CUADRICULA - 4),
                    )

    def dibujar_cabeza(self, x, y):
        pygame.draw.ellipse(
            pantalla, self.color_cabeza, (x, y, TAMANO_CUADRICULA, TAMANO_CUADRICULA)
        )
        ojo_size = TAMANO_CUADRICULA // 4
        pygame.draw.ellipse(pantalla, BLANCO, (x + 3, y + 3, ojo_size, ojo_size))
        pygame.draw.ellipse(
            pantalla,
            BLANCO,
            (x + TAMANO_CUADRICULA - ojo_size - 3, y + 3, ojo_size, ojo_size),
        )
        pupila_size = ojo_size // 2
        pygame.draw.ellipse(pantalla, NEGRO, (x + 4, y + 4, pupila_size, pupila_size))
        pygame.draw.ellipse(
            pantalla,
            NEGRO,
            (x + TAMANO_CUADRICULA - pupila_size - 4, y + 4, pupila_size, pupila_size),
        )
        lengua_color = (255, 50, 50)
        lengua_width = TAMANO_CUADRICULA // 8
        lengua_length = TAMANO_CUADRICULA // 2
        if self.direccion == (1, 0):
            pygame.draw.line(
                pantalla,
                lengua_color,
                (x + TAMANO_CUADRICULA, y + TAMANO_CUADRICULA // 2),
                (x + TAMANO_CUADRICULA + lengua_length, y + TAMANO_CUADRICULA // 2),
                lengua_width,
            )
        elif self.direccion == (-1, 0):
            pygame.draw.line(
                pantalla,
                lengua_color,
                (x, y + TAMANO_CUADRICULA // 2),
                (x - lengua_length, y + TAMANO_CUADRICULA // 2),
                lengua_width,
            )
        elif self.direccion == (0, -1):
            pygame.draw.line(
                pantalla,
                lengua_color,
                (x + TAMANO_CUADRICULA // 2, y),
                (x + TAMANO_CUADRICULA // 2, y - lengua_length),
                lengua_width,
            )
        elif self.direccion == (0, 1):
            pygame.draw.line(
                pantalla,
                lengua_color,
                (x + TAMANO_CUADRICULA // 2, y + TAMANO_CUADRICULA),
                (x + TAMANO_CUADRICULA // 2, y + TAMANO_CUADRICULA + lengua_length),
                lengua_width,
            )


class Comida:
    def __init__(self):
        self.posicion = self.posicion_aleatoria()

    def posicion_aleatoria(self):
        return (
            random.randint(0, ANCHO_CUADRICULA - 1),
            random.randint(0, ALTO_CUADRICULA - 1),
        )

    def dibujar(self):
        x, y = (
            self.posicion[0] * TAMANO_CUADRICULA,
            self.posicion[1] * TAMANO_CUADRICULA,
        )
        pygame.draw.ellipse(
            pantalla, ROJO, (x, y, TAMANO_CUADRICULA, TAMANO_CUADRICULA)
        )
        pygame.draw.circle(
            pantalla,
            BLANCO,
            (x + TAMANO_CUADRICULA // 2, y + TAMANO_CUADRICULA // 4),
            5,
        )


def mostrar_mensaje(texto, y):
    fuente = pygame.font.Font(None, 74)
    texto_renderizado = fuente.render(texto, True, BLANCO)
    pantalla.blit(
        texto_renderizado, (ANCHO // 2 - texto_renderizado.get_width() // 2, y)
    )


def menu_principal():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Jugar", "Personalizar Controles", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente.render("Serpiente", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        juego()
                    elif seleccion == 1:
                        personalizar_controles()
                    elif seleccion == 2:
                        pygame.quit()
                        return
        pygame.display.flip()


def personalizar_controles():
    fuente = pygame.font.Font(None, 36)
    fuente_Titulo = pygame.font.Font(None, 46)
    fuente_instrucciones = pygame.font.Font(None, 26)
    controles_orden = ["arriba", "abajo", "izquierda", "derecha", "pausa"]
    seleccion = 0
    esperando_tecla = False
    gris_claro = (200, 200, 200)
    while True:
        pantalla.fill(NEGRO)
        texto_titulo = fuente_Titulo.render("Personalizar Controles", True, BLANCO)
        pantalla.blit(
            texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 6)
        )
        for i, control in enumerate(controles_orden):
            color = AZUL if i == seleccion else BLANCO
            texto = f"{control.capitalize()}: {pygame.key.name(controles[control])}"
            if esperando_tecla and i == seleccion:
                texto = f"{control.capitalize()}: Presiona una tecla..."
            texto_renderizado = fuente.render(texto, True, color)
            pantalla.blit(
                texto_renderizado,
                (ANCHO // 2 - texto_renderizado.get_width() // 2, ALTO // 3 + i * 50),
            )
        texto_instruccion = fuente_instrucciones.render(
            "Presiona ENTER para personalizar", True, gris_claro
        )
        pantalla.blit(
            texto_instruccion,
            (ANCHO // 2 - texto_instruccion.get_width() // 2, ALTO - 100),
        )
        texto_volver = fuente_instrucciones.render(
            "Presiona ESC para volver", True, gris_claro
        )
        pantalla.blit(
            texto_volver, (ANCHO // 2 - texto_volver.get_width() // 2, ALTO - 60)
        )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if esperando_tecla:
                    controles[controles_orden[seleccion]] = evento.key
                    esperando_tecla = False
                else:
                    if evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(controles_orden)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(controles_orden)
                    elif evento.key == pygame.K_RETURN:
                        esperando_tecla = True
                    elif evento.key == pygame.K_ESCAPE:
                        return
        pygame.display.flip()


def pausar():
    fuente = pygame.font.Font(None, 74)
    fuente_pequeña = pygame.font.Font(None, 36)
    seleccion = 0
    opciones = ["Continuar", "Reiniciar", "Salir"]
    while True:
        pantalla.fill(NEGRO)
        texto_pausa = fuente.render("Pausa", True, BLANCO)
        pantalla.blit(
            texto_pausa, (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 4)
        )
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (150, 150, 150)
            texto_opcion = fuente_pequeña.render(opcion, True, color)
            pantalla.blit(
                texto_opcion,
                (ANCHO // 2 - texto_opcion.get_width() // 2, ALTO // 2 + i * 50),
            )
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                if evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                if evento.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return
                    elif seleccion == 1:
                        return "reiniciar"
                    elif seleccion == 2:
                        return "salir"
        pygame.display.flip()


def juego():
    serpiente = Serpiente()
    comida = Comida()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == controles["arriba"]:
                    serpiente.cambiar_direccion((0, -1))
                elif evento.key == controles["abajo"]:
                    serpiente.cambiar_direccion((0, 1))
                elif evento.key == controles["izquierda"]:
                    serpiente.cambiar_direccion((-1, 0))
                elif evento.key == controles["derecha"]:
                    serpiente.cambiar_direccion((1, 0))
                elif evento.key == controles["pausa"]:
                    seleccion = pausar()
                    if seleccion == "reiniciar":
                        return juego()
                    elif seleccion == "salir":
                        return menu_principal()
        serpiente.mover()
        if serpiente.cuerpo[0] == comida.posicion:
            serpiente.crecer = True
            comida.posicion = comida.posicion_aleatoria()
        if serpiente.verificar_colision():
            mostrar_mensaje("Perdiste", ALTO // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            return
        pantalla.fill(NEGRO)
        serpiente.dibujar()
        comida.dibujar()
        pygame.display.flip()
        reloj.tick(FPS)


menu_principal()
pygame.quit()
