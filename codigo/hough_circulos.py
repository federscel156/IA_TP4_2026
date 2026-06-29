import numpy as np
import matplotlib.pyplot as plt
import math
import os

def crear_imagen_prueba(radio):
    """Crea una imagen sintética de prueba con una circunferencia."""
    img = np.zeros((100, 100), dtype=np.uint8)
    centro_x, centro_y = 60, 40
    
    # Dibujar una circunferencia de radio conocido
    for theta in np.arange(0, 360, 1):
        x = int(centro_x + radio * math.cos(math.radians(theta)))
        y = int(centro_y + radio * math.sin(math.radians(theta)))
        if 0 <= x < 100 and 0 <= y < 100:
            img[y, x] = 255
            
    return img, (centro_x, centro_y)

def transformada_hough_circulos(img, radio):
    """
    Implementación de la Transformada de Hough para circunferencias de radio conocido.
    Basado en la ecuación: (x - a)^2 + (y - b)^2 = R^2
    Para un punto (x, y) del borde, los posibles centros (a, b) forman un círculo de radio R.
    """
    height, width = img.shape
    
    # Matriz acumuladora de votos para los posibles centros (a, b)
    # Su tamaño es igual al de la imagen
    accumulator = np.zeros((height, width), dtype=np.uint64)
    
    # Resoluciones angulares para generar los círculos en el acumulador
    thetas = np.deg2rad(np.arange(0, 360, 1))
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    
    # Obtener los píxeles que son "bordes" (valor > 0)
    y_idxs, x_idxs = np.nonzero(img)
    
    # Proceso de votación
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]
        
        for t_idx in range(len(thetas)):
            # Calcular posibles coordenadas del centro (a, b)
            a = int(round(x - radio * cos_t[t_idx]))
            b = int(round(y - radio * sin_t[t_idx]))
            
            # Sumar un voto si el centro está dentro de los límites de la imagen
            if 0 <= a < width and 0 <= b < height:
                accumulator[b, a] += 1
                
    return accumulator

def main():
    print("Iniciando prototipo de Transformada de Hough para Circunferencias...")
    radio_conocido = 25
    
    # 1. Obtener imagen de prueba
    img, centro_real = crear_imagen_prueba(radio_conocido)
    print(f"Centro real de la circunferencia: {centro_real}")
    
    # 2. Aplicar transformada
    print(f"Calculando espacio de Hough para radio = {radio_conocido}...")
    acc = transformada_hough_circulos(img, radio_conocido)
    
    # 3. Encontrar el pico (el centro más evidente)
    idx = np.argmax(acc)
    b_idx, a_idx = np.unravel_index(idx, acc.shape)
    
    print(f"Centro detectado: x = {a_idx}, y = {b_idx}")
    print(f"Votos: {acc[b_idx, a_idx]}")
    
    # 4. Visualización
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    # Imagen original
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Imagen con circunferencia original')
    
    # Espacio acumulador
    axes[1].imshow(acc, cmap='jet')
    axes[1].set_title('Espacio Acumulador (Posibles centros)')
    axes[1].plot(a_idx, b_idx, 'rx', markersize=12, markeredgewidth=2)
    
    output_path = "resultado_hough_circulos.png"
    plt.savefig(output_path)
    print(f"Resultado guardado en {output_path}")

if __name__ == "__main__":
    main()
