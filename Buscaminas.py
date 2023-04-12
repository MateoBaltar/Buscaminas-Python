import pygame
import random
import pygame_menu

pygame.init()

# Importe de sprites
spr_grillaVacia = pygame.image.load("Sprites/vacio.png")
spr_bandera = pygame.image.load("Sprites/bandera.png")
spr_grilla = pygame.image.load("Sprites/Grilla.png")
spr_grilla1 = pygame.image.load("Sprites/grilla1.png")
spr_grilla2 = pygame.image.load("Sprites/grilla2.png")
spr_grilla3 = pygame.image.load("Sprites/grilla3.png")
spr_grilla4 = pygame.image.load("Sprites/grilla4.png")
spr_grilla5 = pygame.image.load("Sprites/grilla5.png")
spr_grilla6 = pygame.image.load("Sprites/grilla6.png")
spr_grilla7 = pygame.image.load("Sprites/grilla7.png")
spr_grilla8 = pygame.image.load("Sprites/grilla8.png")
spr_grilla7 = pygame.image.load("Sprites/grilla7.png")
spr_mina = pygame.image.load("Sprites/mina.png")
spr_minaClicked = pygame.image.load("Sprites/mina_clicked.png")
spr_minaFalsa = pygame.image.load("Sprites/mina_falsa.png")

grilla = []
minas = []

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

tamaño_grilla = 32
border = 16
top_border = 100

temporizador = pygame.time.Clock()
pygame.display.set_caption("Buscaminas")


def set_dificultad(value, dificultad_juego):
    FACIL = (10, 10, 10)
    MEDIO = (20, 15, 40)
    DIFICIL = (20, 30, 99)
    global dificultad

    if dificultad_juego == 1:
        dificultad = FACIL
    elif dificultad_juego == 2:
        dificultad = MEDIO
    elif dificultad_juego == 3:
        dificultad = DIFICIL
    global display_alto
    global display_ancho
    display_ancho = tamaño_grilla * dificultad[1] + border * 2
    display_alto = tamaño_grilla * dificultad[0] + border + top_border


# Funcion que crea texto
def escribir_texto(text, s, yOff=0):
    if text == "Fin del juego!":
        texto_pantalla = pygame.font.SysFont(
            "Calibri", s, True).render(text, True, (255, 0, 0))
    elif text == "Ganaste!":
        texto_pantalla = pygame.font.SysFont(
            "Calibri", s, True).render(text, True, (0, 255, 0))
    else:
        texto_pantalla = pygame.font.SysFont(
            "Calibri", s, True).render(text, True, (75,0,130))
    rect = texto_pantalla.get_rect()
    rect.center = (dificultad[1] * tamaño_grilla / 2 + border,
                   dificultad[0] * tamaño_grilla / 2 + top_border + yOff)
    displayJuego.blit(texto_pantalla, rect)


# Clase grilla
class Grilla:
    def __init__(self, coordenada_X, coordenada_Y, type):
        self.coordenada_X = coordenada_X
        self.coordenada_Y = coordenada_Y
        self.clicked = False  # Booleano para saber si fue clickeado
        self.minaClicked = False  # Booleano para saber si es una mina y fue clickeada
        self.minaFalse = False  # Booleano para saber si el usuario puso una bandera incorrecta
        self.flag = False  # Booleano para saber si el usuario puso una bandera
        # Crear rectObject para manejar dibujo y coliciones
        self.rect = pygame.Rect(border + self.coordenada_X * tamaño_grilla, top_border +
                                self.coordenada_Y * tamaño_grilla, tamaño_grilla, tamaño_grilla)
        self.valor = type  # Valor de la grilla, -1 es una mina

    def dibujar_grilla(self):
        # Dibuja la grilla con las variables booleanas y los valores de la misma
        if self.minaFalse:
            displayJuego.blit(spr_minaFalsa, self.rect)
        else:
            if self.clicked:
                if self.valor == -1:
                    if self.minaClicked:
                        displayJuego.blit(spr_minaClicked, self.rect)
                    else:
                        displayJuego.blit(spr_mina, self.rect)
                else:
                    if self.valor == 0:
                        displayJuego.blit(spr_grillaVacia, self.rect)
                    elif self.valor == 1:
                        displayJuego.blit(spr_grilla1, self.rect)
                    elif self.valor == 2:
                        displayJuego.blit(spr_grilla2, self.rect)
                    elif self.valor == 3:
                        displayJuego.blit(spr_grilla3, self.rect)
                    elif self.valor == 4:
                        displayJuego.blit(spr_grilla4, self.rect)
                    elif self.valor == 5:
                        displayJuego.blit(spr_grilla5, self.rect)
                    elif self.valor == 6:
                        displayJuego.blit(spr_grilla6, self.rect)
                    elif self.valor == 7:
                        displayJuego.blit(spr_grilla7, self.rect)
                    elif self.valor == 8:
                        displayJuego.blit(spr_grilla8, self.rect)

            else:
                if self.flag:
                    displayJuego.blit(spr_bandera, self.rect)
                else:
                    displayJuego.blit(spr_grilla, self.rect)

    def revelar_grilla(self):
        self.clicked = True
        # Revela automaticamente si el valor es 0
        if self.valor == 0:
            for x in range(-1, 2):
                if self.coordenada_X + x >= 0 and self.coordenada_X + x < dificultad[1]:
                    for y in range(-1, 2):
                        if self.coordenada_Y + y >= 0 and self.coordenada_Y + y < dificultad[0]:
                            if not grilla[self.coordenada_Y + y][self.coordenada_X + x].clicked:
                                grilla[self.coordenada_Y +
                                       y][self.coordenada_X + x].revelar_grilla()
        elif self.valor == -1:
            # Si es una mina revela todas las minas
            for m in minas:
                if not grilla[m[1]][m[0]].clicked:
                    grilla[m[1]][m[0]].revelar_grilla()

    def actualizar_valores(self):
        # Actualiza los valores de la grilla una vez generada
        if self.valor != -1:
            for x in range(-1, 2):
                if self.coordenada_X + x >= 0 and self.coordenada_X + x < dificultad[1]:
                    for y in range(-1, 2):
                        if self.coordenada_Y + y >= 0 and self.coordenada_Y + y < dificultad[0]:
                            if grilla[self.coordenada_Y + y][self.coordenada_X + x].valor == -1:
                                self.valor += 1


def gameLoop():
    gameState = "Jugando"
    minas_restantes = dificultad[2]
    global grilla
    grilla = []
    global minas
    tiempo = 0

    # Generador de minas
    minas = [[random.randrange(0, dificultad[1]),
              random.randrange(0, dificultad[0])]]

    for c in range(dificultad[2] - 1):
        pos = [random.randrange(0, dificultad[1]),
               random.randrange(0, dificultad[0])]
        same = True
        while same:
            for i in range(len(minas)):
                if pos == minas[i]:
                    pos = [random.randrange(
                        0, dificultad[1]), random.randrange(0, dificultad[0])]
                    break
                if i == len(minas) - 1:
                    same = False
        minas.append(pos)

    # Generar toda la grilla
    for j in range(dificultad[0]):
        linea = []
        for i in range(dificultad[1]):
            if [i, j] in minas:
                linea.append(Grilla(i, j, -1))
            else:
                linea.append(Grilla(i, j, 0))
        grilla.append(linea)

    # Grilla actualizada
    for i in grilla:
        for j in i:
            j.actualizar_valores()

    # Loop principal
    while gameState != "Salir":
        # Reset de pantalla
        displayJuego.fill(bg_color)

        # Inputs de usuario
        for event in pygame.event.get():
            # Verificar si el usuario cerro la ventana y vuelve al menu principal
            if event.type == pygame.QUIT:
                gameState = "Salir"
                global surface
                surface = pygame.display.set_mode((600, 400))
            # Verifica si se reinicia el juego
            if gameState == "Fin del juego" or gameState == "Ganaste":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Salir"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grilla:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # Click izquierdo
                                    j.revelar_grilla()
                                    # Toggle flag off
                                    if j.flag:
                                        minas_restantes += 1
                                        j.flag = False
                                    # Si es una mina
                                    if j.valor == -1:
                                        gameState = "Fin del juego"
                                        j.minaClicked = True
                                elif event.button == 3:
                                    # Click derecho
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            minas_restantes += 1
                                        else:
                                            j.flag = True
                                            minas_restantes -= 1

        # Verificar si gano
        w = True
        for i in grilla:
            for j in i:
                j.dibujar_grilla()
                if j.valor != -1 and not j.clicked:
                    w = False
        if w and gameState != "Salir":
            gameState = "Ganaste"

        # Dibujar texto
        if gameState != "Fin del juego" and gameState != "Ganaste":
            tiempo += 1
        elif gameState == "Fin del juego":
            escribir_texto("Fin del juego!", 50)
            escribir_texto("R para reiniciar", 35, 50)
            for i in grilla:
                for j in i:
                    if j.flag and j.valor != -1:
                        j.minaFalse = True
        else:
            escribir_texto("Ganaste!", 50)
            escribir_texto("R para reiniciar", 35, 50)
        # Dibujar tiempo
        s = str(tiempo // 15)
        texto_pantalla = pygame.font.SysFont(
            "Calibri", 50).render(s, True, (0, 0, 0))
        displayJuego.blit(texto_pantalla, (border, border))
        # Dibujar minas restantes
        texto_pantalla = pygame.font.SysFont("Calibri", 50).render(
            minas_restantes.__str__(), True, (0, 0, 0))
        displayJuego.blit(
            texto_pantalla, (display_ancho - border - 50, border))

        pygame.display.update()

        temporizador.tick(15)


def iniciar_juego():
    global displayJuego
    displayJuego = pygame.display.set_mode((display_ancho, display_alto))
    gameLoop()


global surface
surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu('Bienvenid@', 400, 300,
                        theme=pygame_menu.themes.THEME_DARK)

menu.add.button('Jugar', iniciar_juego)
menu.add.selector('Dificultad :', [
                  ('Facil', 1), ('Medio', 2), ('Dificil', 3)], onchange=set_dificultad, default=1)
menu.add.button('Salir', pygame_menu.events.EXIT)
menu.mainloop(surface)

pygame.quit()
quit()
