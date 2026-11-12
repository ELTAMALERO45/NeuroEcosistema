import pygame
import random
from laberinto_mundo import MAPAS, libres
from agentes import Agente

class Entorno:
    def __init__(self, indice_mapa=0):
        self.indice_mapa = indice_mapa % len(MAPAS)
        self.mapa = MAPAS[self.indice_mapa]
        self.filas = len(self.mapa)
        self.cols = len(self.mapa[0])
        self.tam_celda = 34
        self.turnos_totales = 0 
        
        celdas = libres(self.mapa)
        rutas_presa = ['src/assets/presa1.png', 'src/assets/presa2.png']
        rutas_depredador = ['src/assets/depredador1.png', 'src/assets/depredador2.png']
        ruta_comida = 'src/assets/comida.png'
        
        self.presas = []
        self.depredadores = []
        self.plantas = []
        
        posiciones_iniciales = random.sample(celdas, min(7, len(celdas)))
        
        for i in range(5):
            p = posiciones_iniciales[i]
            celdas.remove(p)
            self.presas.append(Agente(p, rutas_presa, 'presa'))
            
        pos_dep = posiciones_iniciales[5]
        celdas.remove(pos_dep)
        self.depredadores.append(Agente(pos_dep, rutas_depredador, 'depredador'))
            
        for _ in range(min(6, len(celdas))):
            p = random.choice(celdas)
            celdas.remove(p)
            self.plantas.append(Agente(p, ruta_comida, 'comida'))

    def actualizar(self, red):
        self.turnos_totales += 1
        ultima_prob = None
        lobo = self.depredadores[0] if self.depredadores else None
        
        # 1. MOVER PRESAS (Solo se mueven el 75% del tiempo, van más lento que el lobo)
        mover_presas = (self.turnos_totales % 4 != 0) 
        
        if mover_presas:
            posiciones_ocupadas = {(p.fila, p.col) for p in self.presas if p.vivo}
            for idx, presa in enumerate(self.presas):
                if presa.vivo:
                    comida_objetivo = self.plantas[idx % len(self.plantas)] if self.plantas else None

                    posiciones_ocupadas.discard((presa.fila, presa.col))
                    _, probs = presa.tomar_decision_inteligente(comida_objetivo, lobo, self.mapa, red, self.indice_mapa, posiciones_ocupadas)
                    posiciones_ocupadas.add((presa.fila, presa.col))
                    ultima_prob = probs
                    
                    for planta in self.plantas:
                        if planta.vivo and presa.fila == planta.fila and presa.col == planta.col:
                            presa.energia = min(100, presa.energia + 30)
                            planta.vivo = False

        # 2. MOVER LOBO (Se mueve SIEMPRE en cada turno)
        for dep in self.depredadores:
            presas_vivas = [p for p in self.presas if p.vivo]
            if dep.vivo and presas_vivas:
                if not hasattr(dep, 'objetivo_actual') or dep.objetivo_actual not in presas_vivas or not dep.objetivo_actual.vivo:
                    dep.objetivo_actual = min(presas_vivas, key=lambda p: abs(p.fila - dep.fila) + abs(p.col - dep.col))
                
                dep.tomar_decision_inteligente(dep.objetivo_actual, None, self.mapa, red, self.indice_mapa, set())
                
                for presa in self.presas:
                    if presa.vivo and dep.fila == presa.fila and dep.col == presa.col:
                        presa.vivo = False
                        if hasattr(dep, 'objetivo_actual'):
                            dep.objetivo_actual = None

        self.plantas = [p for p in self.plantas if p.vivo]
        celdas_libres = libres(self.mapa)
        if len(self.plantas) < 6 and celdas_libres and random.random() < 0.15:
            p = random.choice(celdas_libres)
            self.plantas.append(Agente(p, 'src/assets/comida.png', 'comida'))

        todas_muertas = all(not p.vivo for p in self.presas)
        return ultima_prob, todas_muertas

    def dibujar(self, pantalla, offset_x, offset_y):
        COLOR_ARBOL = (45, 90, 50)
        COLOR_PASTO = (210, 230, 200)
        
        for f, fila in enumerate(self.mapa):
            for c, celda in enumerate(fila):
                rect = pygame.Rect(offset_x + c * self.tam_celda, offset_y + f * self.tam_celda, self.tam_celda - 1, self.tam_celda - 1)
                color_celda = COLOR_ARBOL if celda == '#' else COLOR_PASTO
                pygame.draw.rect(pantalla, color_celda, rect, border_radius=4)

        for planta in self.plantas: planta.dibujar(pantalla, offset_x, offset_y)
        for presa in self.presas: presa.dibujar(pantalla, offset_x, offset_y)
        for dep in self.depredadores: dep.dibujar(pantalla, offset_x, offset_y)