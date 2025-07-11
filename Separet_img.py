import os
import shutil
import math

def dividir_en_cuatro_grupos(carpeta_origen, carpeta_destino_base):
    archivos = [f for f in os.listdir(carpeta_origen) if os.path.isfile(os.path.join(carpeta_origen, f))]
    total = len(archivos)
    tamanio_grupo = math.ceil(total / 4)  # Reparte equitativamente

    for i in range(4):
        carpeta_grupo = os.path.join(carpeta_destino_base, f"Grupo_{i+1}")
        os.makedirs(carpeta_grupo, exist_ok=True)

        inicio = i * tamanio_grupo
        fin = min(inicio + tamanio_grupo, total)

        for archivo in archivos[inicio:fin]:
            ruta_origen = os.path.join(carpeta_origen, archivo)
            ruta_destino = os.path.join(carpeta_grupo, archivo)
            shutil.copy2(ruta_origen, ruta_destino)

    print("Imágenes divididas en 4 grupos.")

# Ejecutar con tus rutas
dividir_en_cuatro_grupos(
    "C:\\Users\\jsm21\\Downloads\\fotos\\Descartadas",
    "C:\\Users\\jsm21\\Downloads\\fotos\\Bloques"
)
