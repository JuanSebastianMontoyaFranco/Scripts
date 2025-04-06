import os

def organizar_archivos_consecutivos(carpeta_origen):
    # Extensiones para identificar imágenes y videos
    extensiones_imagenes = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    extensiones_videos = ['.mp4', '.mov', '.avi', '.mkv', '.wmv']

    contador_imagenes = 1
    contador_videos = 1

    # Recorrer los archivos en la carpeta origen
    for archivo in os.listdir(carpeta_origen):
        ruta_completa = os.path.join(carpeta_origen, archivo)
        if os.path.isfile(ruta_completa):
            extension = os.path.splitext(archivo)[1].lower()

            # Renombrar imágenes
            if extension in extensiones_imagenes:
                nuevo_nombre = f"img_{contador_imagenes}{extension}"
                ruta_nueva = os.path.join(carpeta_origen, nuevo_nombre)
                os.rename(ruta_completa, ruta_nueva)
                contador_imagenes += 1

            # Renombrar videos
            elif extension in extensiones_videos:
                nuevo_nombre = f"video_{contador_videos}{extension}"
                ruta_nueva = os.path.join(carpeta_origen, nuevo_nombre)
                os.rename(ruta_completa, ruta_nueva)
                contador_videos += 1

    print("Archivos renombrados consecutivamente.")

# Ejemplo de uso
carpeta_origen = 'Ruta/a/tu/carpeta'  # Cambia esto a la ruta de tu carpeta
organizar_archivos_consecutivos(carpeta_origen)
