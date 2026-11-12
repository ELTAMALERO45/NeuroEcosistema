# NeuroEcosistema - Simulador 2D de Depredador-Presa con Redes Neuronales

Simulador ecológico en 2D de tipo depredador-presa desarrollado en **Python** utilizando **Pygame**, **NumPy** y un gestor de entornos basado en **`uv`**. El proyecto implementa inteligencia artificial mediante redes neuronales multicapa entrenadas con datos expertos de búsqueda óptima (BFS/A*), combinadas con comportamientos de evasión táctica y gestión de recursos en mapas laberínticos estilo selva (15x15).

---

## 🌲 Características Principales

* **Ecosistema Dinámico:** Simulación interactiva con 5 presas (conejos), 1 depredador (lobo) y recursos de alimento (zanahorias) distribuidos en mapas de 15x15 celdas.
* **Cerebro Neuronal (`RedLaberinto`):** Red neuronal multicapa que procesa entradas espaciales y emite probabilidades Softmax para la toma de decisiones de navegación.
* **Comportamiento Táctico e Inteligente:** 
  * Los conejos buscan comida y cuentan con un radio de alerta para huir en dirección contraria cuando el lobo se acerca.
  * Sistema de memoria de celdas recientes para evitar bucles de movimiento.
  * Restricción de casillas únicas (evita que los agentes se superpongan).
* **Control de Velocidad Asimétrico:** El lobo se desplaza en cada turno, mientras que las presas descansan 1 de cada 4 turnos, otorgando ventaja táctica al depredador.
* **Panel de Control y Métricas en Tiempo Real:** Visualización gráfica de épocas entrenadas, pérdida (*Loss*), exactitud de prueba, barras Softmax de probabilidad y gráfica de evolución del entrenamiento.

---

## 🛠️ Estructura del Proyecto

```text
NeuroEcosistema/
│
├── src/
│   └── neuroecosistema/
│       ├── __init__.py
│       ├── main.py             # Controlador principal, bucle de juego y UI de Pygame
│       ├── entorno.py          # Gestor del ecosistema, colisiones y turnos
│       ├── agentes.py          # Lógica de agentes (presas, depredador, comida)
│       ├── red_neuronal.py     # Arquitectura de la red neuronal y datos expertos
│       └── laberinto_mundo.py  # Mapas de 15x15 y algoritmos de búsqueda BFS/A*
│
├── src/assets/                 # Sprites en alta resolución (.png)
├── pyproject.toml              # Configuración de dependencias y proyecto
└── README.md

📦 Dependencias y Prerrequisitos
El proyecto utiliza uv para la gestión ultra rápida de entornos virtuales y dependencias en Python.

Python >= 3.12

Pygame (Renderizado gráfico y sprites)

NumPy (Operaciones tensoriales y procesamiento de la red neuronal)

🚀 Instrucciones de Ejecución
Sigue estos pasos para clonar, configurar y ejecutar el proyecto en tu entorno local (compatible con PowerShell en Windows):

Clonar el repositorio:

PowerShell
git clone [https://github.com/ELTAMALERO45/NeuroEcosistema.git](https://github.com/ELTAMALERO45/NeuroEcosistema.git)
cd NeuroEcosistema
Ejecutar la simulación directamente con uv:uv se encargará de crear el entorno virtual y descargar las librerías necesarias de forma automática la primera vez que lo ejecutes.

PowerShell
uv run .\src\neuroecosistema\main.py
🎮 Controles del Simulador
Durante la ejecución de la simulación, puedes utilizar las siguientes teclas para controlar el entrenamiento y el flujo del entorno:

1: Entrena la red neuronal por +1 época.

2: Entrena la red neuronal en bloques de +10 épocas.

3: Activa / Pausa el entrenamiento continuo en segundo plano.

P: Alterna entre modo Automático y modo Paso a Paso.

ESPACIO: Avanza un turno manual (cuando está en modo paso a paso).

N: Cambia al siguiente diseño de mapa (1 al 3).

G: Reinicia el reto actual manteniendo el cerebro entrenado.

R: Reinicia completamente el cerebro neuronal y los contadores.

ESC: Sale del simulador.