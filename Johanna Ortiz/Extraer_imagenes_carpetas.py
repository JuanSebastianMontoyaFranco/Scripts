import os
from PIL import Image

def extraer_y_renombrar_imagenes(carpeta_raiz, carpeta_destino):
    """
    Recorre las subcarpetas de `carpeta_raiz`, busca imágenes y las copia en `carpeta_destino`
    renombradas según la última carpeta donde estaban.
    Todas las imágenes se convierten a JPG.
    FRONT siempre será -1, y el resto se numera en orden.
    """

    os.makedirs(carpeta_destino, exist_ok=True)

    extensiones = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    for root, dirs, files in os.walk(carpeta_raiz):
        if not files:
            continue

        nombre_carpeta = os.path.basename(root)

        imagenes = [f for f in files if os.path.splitext(f)[1].lower() in extensiones]
        if not imagenes:
            continue

        # Ordenar: primero las que contengan "FRONT"
        imagenes.sort(key=lambda x: (not "front" in x.lower(), x.lower()))

        for i, img in enumerate(imagenes, start=1):
            nuevo_nombre = f"{nombre_carpeta}-{i}.jpg"
            origen = os.path.join(root, img)
            destino = os.path.join(carpeta_destino, nuevo_nombre)

            try:
                with Image.open(origen) as im:
                    # Convertir a RGB (quita transparencias y asegura compatibilidad con JPG)
                    if im.mode in ("RGBA", "P"):
                        # Fondo blanco para imágenes con transparencia
                        fondo = Image.new("RGB", im.size, (255, 255, 255))
                        fondo.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
                        im = fondo
                    else:
                        im = im.convert("RGB")

                    im.save(destino, "JPEG", quality=95)
                print(f"Convertido: {origen} -> {destino}")
            except Exception as e:
                print(f"Error al procesar {origen}: {e}")


extraer_y_renombrar_imagenes("D:\\Fotos", "D:\\Finales")
