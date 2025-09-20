import os
from PIL import Image

def convertir_imagenes_a_jpg(carpeta):
    extensiones_validas = ['.png', '.bmp', '.tif', '.tiff', '.webp', '.heic', '.gif', '.jpg', '.jpeg']

    for archivo in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, archivo)

        if not os.path.isfile(ruta_completa):
            continue

        archivo = archivo.strip()  # limpia espacios
        nombre_base, extension = os.path.splitext(archivo)
        extension = extension.lower()

        if extension not in extensiones_validas:
            print(f"Ignorado (extensión no válida): {archivo}")
            continue

        try:
            with Image.open(ruta_completa) as img:
                img = img.convert("RGB")

                if " (1)" in nombre_base:
                    # Quitar " (1)" y el posible sufijo .1, .2, etc.
                    base = nombre_base.replace(" (1)", "")
                    if '.' in base:
                        base = base.rsplit('.', 1)[0]
                    nuevo_nombre = base + ".5.jpg"
                else:
                    nuevo_nombre = nombre_base + ".jpg"

                ruta_salida = os.path.join(carpeta, nuevo_nombre)

                img.save(ruta_salida, "JPEG")
                print(f"✅ Convertido: {archivo} → {nuevo_nombre}")

        except Exception as e:
            print(f"❌ Error al convertir {archivo}: {e}")

# Ejecutar
carpeta = "C:\\Users\\jsm21\\Downloads\\Imagenes\\Todas"
convertir_imagenes_a_jpg(carpeta)
