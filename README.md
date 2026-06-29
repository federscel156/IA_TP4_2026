# Transformada de Hough - Implementación Manual (TP4)

Este directorio contiene los prototipos de la Transformada de Hough desarrollados para el Trabajo Práctico 4, los algoritmos centrales de votación matemática han sido implementados **desde cero** en Python utilizando matrices de NumPy.

## Requisitos

Para ejecutar estos scripts necesitas tener instalado Python 3 y las siguientes librerías estándar de procesamiento matricial y graficación:

```bash
pip install numpy matplotlib
```

## Archivos

### 1. `hough_rectas.py`
Este script implementa el algoritmo de detección de líneas rectas:
- Genera una imagen sintética en escala de grises con una recta diagonal ($y = x + 20$).
- Aplica la Transformada de Hough utilizando el espacio paramétrico polar ($\rho$ y $\theta$).
- Itera sobre todos los píxeles de borde y vota en una matriz acumuladora de Hough.
- Encuentra el pico (el punto con más intersecciones/votos) que define la línea principal.
- Exporta una imagen `resultado_hough_rectas.png` mostrando la imagen original y el espacio acumulador con el pico destacado.

**Ejecución:**
```bash
python hough_rectas.py
```

### 2. `hough_circulos.py`
Este script implementa el algoritmo de detección del centro de circunferencias cuando el **radio es conocido**, como se requiere en el caso industrial del motor:
- Genera una imagen sintética de prueba con una circunferencia completa dibujada a partir de un centro aleatorio conocido.
- Recibe el radio conocido por parámetro.
- Por cada píxel del borde de la imagen de entrada, "dibuja" una circunferencia en el espacio acumulador con el mismo radio conocido (buscando los posibles centros $a$ y $b$).
- Encuentra la celda con más votos en la matriz resultante, la cual representa las coordenadas ($x, y$) del centro buscado.
- Exporta una imagen `resultado_hough_circulos.png` demostrando el proceso y marcando el centro detectado en el plano de los posibles centros.

**Ejecución:**
```bash
python hough_circulos.py
```

## Relación con el Caso de Estudio

La solución `hough_circulos.py` demuestra que, disponiendo del radio del aro "C" del block del motor (y habiendo pasado la imagen capturada por la cámara por un filtro de bordes previamente), el robot puede encontrar matemáticamente el punto central "A" en milisegundos con altísima precisión (resolución a nivel de píxel), resistiendo ruido y oclusiones parciales sin necesidad de entrenamiento previo.
