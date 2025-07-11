import os
import re
from PIL import Image

def procesar_imagenes(carpeta_entrada, carpeta_salida, carpeta_descartadas, formato='.jpg'):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    if not os.path.exists(carpeta_descartadas):
        os.makedirs(carpeta_descartadas)

    codigos_vistos = set()

    for archivo in os.listdir(carpeta_entrada):
        ruta_archivo = os.path.join(carpeta_entrada, archivo)

        if not os.path.isfile(ruta_archivo):
            continue

        nombre, _ = os.path.splitext(archivo)

        # Detecta si contiene .1, .2, .3 o (1), (2), etc.
        if re.search(r'\.\d$|\(\d+\)', nombre):
            ruta_destino = os.path.join(carpeta_descartadas, archivo)
            os.rename(ruta_archivo, ruta_destino)
            continue

        # Extrae solo el número inicial
        match = re.match(r"(\d+)", nombre)
        if not match:
            continue

        codigo = match.group(1)

        if codigo in codigos_vistos:
            continue

        try:
            with Image.open(ruta_archivo) as img:
                img = img.convert("RGB")
                nuevo_nombre = f"{codigo}{formato}"
                ruta_salida = os.path.join(carpeta_salida, nuevo_nombre)
                img.save(ruta_salida)
                codigos_vistos.add(codigo)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

    print("Procesamiento completado.")

# Ejecutar con tus rutas
procesar_imagenes(
    "C:\\Users\\jsm21\\Downloads\\fotos\\Originales",
    "C:\\Users\\jsm21\\Downloads\\fotos\\Nuevas",
    "C:\\Users\\jsm21\\Downloads\\fotos\\Descartadas"
)
