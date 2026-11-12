import pygame
import random
from entorno import Entorno
from red_neuronal import RedLaberinto, generar_datos
from laberinto_mundo import NOMBRES

ANCHO, ALTO = 1080, 690
TAM = 34
ORIGEN_X, ORIGEN_Y = 25, 95

FONDO = (242, 247, 240)
TEXTO = (45, 60, 45)
COLOR_GRAFICA = (100, 160, 100)
COLOR_BARRA_FONDO = (220, 235, 220)
COLOR_BARRA_LLENA = (85, 140, 90)

def texto(superficie, fuente, contenido, x, y, color=TEXTO):
    superficie.blit(fuente.render(str(contenido), True, color), (x, y))

def barras_probabilidad(pantalla, fuente, probs, x, y):
    if probs is None: return
    for k, nombre in enumerate(NOMBRES):
        yy = y + k * 30
        texto(pantalla, fuente, f'{nombre}: {probs[k]:.1%}', x, yy)
        pygame.draw.rect(pantalla, COLOR_BARRA_FONDO, (x + 140, yy + 4, 130, 12), border_radius=5)
        pygame.draw.rect(pantalla, COLOR_BARRA_LLENA, (x + 140, yy + 4, int(130 * probs[k]), 12), border_radius=5)

def grafica(pantalla, historial, area):
    pygame.draw.rect(pantalla, (230, 240, 230), area, border_radius=11)
    if len(historial) < 2: return
    salto = max(1, len(historial) // 180)
    datos = historial[::salto]
    ymax = max(0.2, max(datos))
    puntos = [
        (int(area.left + 10 + i * (area.width - 20) / (len(datos) - 1)),
         int(area.bottom - 10 - v / ymax * (area.height - 20)))
        for i, v in enumerate(datos)
    ]
    pygame.draw.lines(pantalla, COLOR_GRAFICA, False, puntos, 3)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('NeuroEcosistema - Control de Épocas y Movimiento Suave')
    reloj = pygame.time.Clock()
    
    grande = pygame.font.SysFont("segoeui", 26, bold=True)
    normal = pygame.font.SysFont("segoeui", 16, bold=True)
    pequeno = pygame.font.SysFont("segoeui", 13)
    
    red = RedLaberinto()
    (X, y), (Xt, yt), _ = generar_datos()
    ecosistema = Entorno(0)
    
    activo = True
    automatico = True
    continuo = False
    alerta_lobo = False
    ultima_probabilidad = [0.25, 0.25, 0.25, 0.25]
    ultimo_tick = pygame.time.get_ticks()

    while activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                activo = False
            elif evento.type == pygame.KEYDOWN:
                tecla = evento.key
                if tecla == pygame.K_ESCAPE:
                    activo = False
                elif tecla == pygame.K_1:
                    red.entrenar_epoca(X, y)
                elif tecla == pygame.K_2:
                    for _ in range(10): red.entrenar_epoca(X, y)  # Cambiado de 100 a 10 épocas
                elif tecla == pygame.K_3:
                    continuo = not continuo
                elif tecla == pygame.K_p:
                    automatico = not automatico
                elif tecla == pygame.K_n:
                    ecosistema = Entorno(ecosistema.indice_mapa + 1)
                    alerta_lobo = False
                elif tecla == pygame.K_g:
                    ecosistema = Entorno(ecosistema.indice_mapa)
                    alerta_lobo = False
                elif tecla == pygame.K_r:
                    red.reiniciar()
                    continuo = False
                    ecosistema = Entorno(0)
                    alerta_lobo = False
                elif tecla == pygame.K_SPACE and not automatico:
                    ultimo_tick = 0

        if continuo:
            red.entrenar_epoca(X, y)

        ahora = pygame.time.get_ticks()
        # Aumentado a 350ms para que vayan más lentos y se aprecie mejor la estrategia
        dar_paso = (automatico and ahora - ultimo_tick >= 350) or (not automatico and ultimo_tick == 0)
        
        if dar_paso:
            ultimo_tick = ahora
            probs, todas_muertas = ecosistema.actualizar(red)
            if probs is not None:
                ultima_probabilidad = probs
            if todas_muertas:
                alerta_lobo = True

        # === DIBUJADO DE LA INTERFAZ ===
        pantalla.fill(FONDO)
        
        texto(pantalla, grande, 'NEUROECOSISTEMA - CONTROL TÁCTICO', 25, 12, (30, 80, 40))
        texto(pantalla, pequeno, f'Mapa {ecosistema.indice_mapa+1}/3  |  Estrategia: Movimiento Lento y Enfoque Fijo', 25, 46)

        ecosistema.dibujar(pantalla, ORIGEN_X, ORIGEN_Y)

        if alerta_lobo:
            srf_alerta = pygame.Surface((450, 90))
            srf_alerta.set_alpha(230)
            srf_alerta.fill((200, 50, 50))
            pantalla.blit(srf_alerta, (ORIGEN_X + 50, ORIGEN_Y + 180))
            texto(pantalla, grande, "¡EL LOBO CAZÓ A LAS 5 PRESAS!", ORIGEN_X + 70, ORIGEN_Y + 195, (255, 255, 255))
            texto(pantalla, pequeno, "Presiona 'G' para reiniciar o 'N' para otro mapa.", ORIGEN_X + 85, ORIGEN_Y + 235, (255, 255, 255))

        x_panel = ORIGEN_X + (ecosistema.cols * TAM) + 25
        presas_vivas = sum(1 for p in ecosistema.presas if p.vivo)
        
        texto(pantalla, normal, f'Épocas entrenadas: {red.epocas}', x_panel, 75)
        texto(pantalla, normal, f'Pérdida (Loss): {red.historial[-1]:.4f}' if red.historial else 'Pérdida: sin entrenar', x_panel, 105)
        texto(pantalla, normal, f'Exactitud: {red.exactitud(Xt, yt):.1%}', x_panel, 135)
        texto(pantalla, normal, f'Presas Vivas: {presas_vivas} / {len(ecosistema.presas)}', x_panel, 165)
        texto(pantalla, normal, f'Simulación: {"AUTOMÁTICA" if automatico else "PASO A PASO"}', x_panel, 195)
        texto(pantalla, normal, f'Entreno Continuo: {"ACTIVADO" if continuo else "PAUSADO"}', x_panel, 225)
        
        texto(pantalla, normal, 'SALIDAS SOFTMAX', x_panel, 270)
        barras_probabilidad(pantalla, pequeno, ultima_probabilidad, x_panel, 298)
        
        texto(pantalla, normal, 'EVOLUCIÓN DE LA PÉRDIDA', x_panel, 435)
        grafica(pantalla, red.historial, pygame.Rect(x_panel, 468, 335, 95))

        franja_rect = pygame.Rect(0, 605, ANCHO, 85)
        pygame.draw.rect(pantalla, (225, 235, 222), franja_rect)
        pygame.draw.line(pantalla, (200, 215, 195), (0, 605), (ANCHO, 605), 2)

        texto(pantalla, pequeno, '1: +1 época    2: +10 épocas    3: entrenamiento continuo (toggle)', 25, 615, (40, 70, 40))
        texto(pantalla, pequeno, 'P: automático/pasos    ESPACIO: avanzar    N: otro mapa    G: nuevo reto', 25, 638, (40, 70, 40))
        texto(pantalla, pequeno, 'R: reiniciar cerebro y contadores     ESC: salir', 25, 660, (40, 70, 40))

        pygame.display.flip()
        reloj.tick(60)

pygame.quit()

if __name__ == '__main__':
    main()