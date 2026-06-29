import numpy as np
import matplotlib.pyplot as plt
import math
import os

def crear_imagen_prueba():
    """Crea una imagen sintética de prueba con una recta."""
    img = np.zeros((100, 100), dtype=np.uint8)
    # Dibujar una recta (y = x + 20)
    for x in range(100):
        y = x + 20
        if 0 <= y < 100:
            img[y, x] = 255
    return img

def transformada_hough_rectas(img):
    """
    Implementación de la Transformada de Hough para rectas desde cero.
    Basado en la formulación polar: rho = x * cos(theta) + y * sin(theta)
    """
    height, width = img.shape
    
    # Rango máximo de rho: la diagonal de la imagen
    diag_len = int(np.ceil(np.sqrt(width**2 + height**2)))
    
    # Resoluciones
    thetas = np.deg2rad(np.arange(-90, 90, 1))
    rhos = np.arange(-diag_len, diag_len, 1)
    
    # Matriz acumuladora de votos
    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)
    
    # Precomputar senos y cosenos para optimización
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    
    # Obtener los píxeles que son "bordes" (valor > 0)
    y_idxs, x_idxs = np.nonzero(img)
    
    # Proceso de votación
    for i in range(len(x_idxs)):
        x = x_idxs[i]
        y = y_idxs[i]
        
        for t_idx in range(len(thetas)):
            # Calcular rho
            rho = int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
            
            # Encontrar el índice de rho en nuestro arreglo de rhos
            rho_idx = rho + diag_len
            
            # Sumar un voto
            accumulator[rho_idx, t_idx] += 1
            
    return accumulator, thetas, rhos

def main():
    print("Iniciando prototipo de Transformada de Hough para Rectas...")
    
    # 1. Obtener imagen de prueba
    img = crear_imagen_prueba()
    
    # 2. Aplicar transformada
    print("Calculando espacio de Hough...")
    acc, thetas, rhos = transformada_hough_rectas(img)
    
    # 3. Encontrar el pico (la recta más evidente)
    idx = np.argmax(acc)
    rho_idx, theta_idx = np.unravel_index(idx, acc.shape)
    
    mejor_rho = rhos[rho_idx]
    mejor_theta = thetas[theta_idx]
    
    print(f"Mejor recta detectada: rho = {mejor_rho}, theta = {np.rad2deg(mejor_theta):.2f} grados")
    print(f"Votos: {acc[rho_idx, theta_idx]}")
    
    # 4. Visualización
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    # Imagen original
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Imagen con recta original')
    
    # Espacio acumulador
    axes[1].imshow(acc, cmap='jet', extent=[np.rad2deg(thetas[0]), np.rad2deg(thetas[-1]), rhos[-1], rhos[0]], aspect='auto')
    axes[1].set_title('Espacio Acumulador de Hough')
    axes[1].set_xlabel('Theta (grados)')
    axes[1].set_ylabel('Rho (píxeles)')
    axes[1].plot(np.rad2deg(mejor_theta), mejor_rho, 'ro', markersize=10, mfc='none')
    
    output_path = "resultado_hough_rectas.png"
    plt.savefig(output_path)
    print(f"Resultado guardado en {output_path}")

if __name__ == "__main__":
    main()
