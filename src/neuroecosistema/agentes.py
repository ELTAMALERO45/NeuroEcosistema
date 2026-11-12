import pygame
import numpy as np
import random

class Agente:
    def __init__(self, pos, rutas_imagenes, tipo):
        self.fila, self.col = pos
        self.tipo = tipo  # 'presa', 'depredador', 'comida'
        self.energia = 100
        self.vivo = True
        self.tam_celda = 34
        self.historial_posiciones = []
        
        # Tamaños ajustados para alta resolución
        if self.tipo == 'depredador':
            self.tam_imagen = 32  
        elif self.tipo == 'presa':
            self.tam_imagen = 28  
        else:
            self.tam_imagen = 22  

        self.imagenes = []
        rutas = rutas_imagenes if isinstance(rutas_imagenes, list) else [rutas_imagenes]
        for ruta in rutas:
            # Cargar imagen y limpiar cualquier máscara o canal residual
            img = pygame.image.load(ruta).convert_alpha()
            
            # Escalar conservando la transparencia nativa del PNG
            img = pygame.transform.smoothscale(img, (self.tam_imagen, self.tam_imagen))
            
            self.imagenes.append(img)

    def tomar_decision_inteligente(self, objetivo_principal, amenaza, mapa, red, mapa_idx, ocupadas):
        if not self.vivo:
            return 0, np.array([0.25, 0.25, 0.25, 0.25])

        movimientos = ((-1, 0), (1, 0), (0, -1), (0, 1))
        ff, fc = self.fila, self.col
        
        if objetivo_principal is not None:
            try:
                probs_red = red.probabilidades(mapa_idx, (ff, fc), (objetivo_principal.fila, objetivo_principal.col))
            except:
                probs_red = np.array([0.25, 0.25, 0.25, 0.25])
        else:
            probs_red = np.array([0.25, 0.25, 0.25, 0.25])

        puntajes = probs_red.copy()

        for i, (df, dc) in enumerate(movimientos):
            nf, nc = ff + df, fc + dc
            
            if not (0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]) and mapa[nf][nc] != '#'):
                puntajes[i] -= 1000
                continue
                
            if (nf, nc) in ocupadas and self.tipo != 'depredador':
                puntajes[i] -= 1000
                continue

            if (nf, nc) in self.historial_posiciones:
                puntajes[i] -= 1.0

            if self.tipo == 'presa' and amenaza is not None and amenaza.vivo:
                dist_amenaza_actual = abs(ff - amenaza.fila) + abs(fc - amenaza.col)
                if dist_amenaza_actual <= 5: 
                    dist_futura = abs(nf - amenaza.fila) + abs(nc - amenaza.col)
                    if dist_futura > dist_amenaza_actual:
                        puntajes[i] += 2.0 
                    else:
                        puntajes[i] -= 2.0 

        mejor_accion = int(puntajes.argmax())
        
        if puntajes[mejor_accion] <= -500:
            nf, nc = ff, fc
        else:
            df, dc = movimientos[mejor_accion]
            nf, nc = ff + df, fc + dc

        self.fila, self.col = nf, nc
        self.historial_posiciones.append((ff, fc))
        if len(self.historial_posiciones) > 2:
            self.historial_posiciones.pop(0)

        self.energia -= 0.3
        if self.energia <= 0:
            self.vivo = False

        return mejor_accion, probs_red

    def dibujar(self, superficie, offset_x=0, offset_y=0):
        if self.vivo:
            if len(self.imagenes) > 1 and self.tipo != 'comida':
                tiempo = pygame.time.get_ticks()
                frame = (tiempo // 250) % len(self.imagenes)
                imagen_actual = self.imagenes[frame]
            else:
                imagen_actual = self.imagenes[0]
            
            ajuste_x = (self.tam_celda - self.tam_imagen) // 2
            ajuste_y = (self.tam_celda - self.tam_imagen) // 2
            
            x = offset_x + (self.col * self.tam_celda) + ajuste_x
            y = offset_y + (self.fila * self.tam_celda) + ajuste_y
            superficie.blit(imagen_actual, (x, y))