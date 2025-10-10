import os

def guardar_nombres_imagenes(
    carpeta_raiz: str,
    archivo_txt: str = "imagenes.txt",
    incluir_subcarpetas: bool = True,
    incluir_extension: bool = False,
):
    """
    Recorre `carpeta_raiz` (opcionalmente subcarpetas) y guarda en un .txt
    los nombres de todos los archivos de imagen encontrados.
    - Un nombre por línea.
    - Por defecto SIN extensión.
    - No copia ni convierte imágenes.
    """
    extensiones = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

    nombres = []

    if incluir_subcarpetas:
        walker = os.walk(carpeta_raiz)
        for root, _, files in walker:
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in extensiones:
                    nombre = f if incluir_extension else os.path.splitext(f)[0]
                    nombres.append(nombre)
    else:
        # Solo la carpeta raíz, sin descender
        for f in os.listdir(carpeta_raiz):
            if os.path.isfile(os.path.join(carpeta_raiz, f)):
                ext = os.path.splitext(f)[1].lower()
                if ext in extensiones:
                    nombre = f if incluir_extension else os.path.splitext(f)[0]
                    nombres.append(nombre)

    # Orden alfabético y sin duplicados (manteniendo orden)
    vistos = set()
    nombres_ordenados = []
    for n in sorted(nombres, key=lambda s: s.lower()):
        if n not in vistos:
            vistos.add(n)
            nombres_ordenados.append(n)

    ruta_salida = os.path.join(carpeta_raiz, archivo_txt)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        for n in nombres_ordenados:
            f.write(n + "\n")

    print(f"Se guardaron {len(nombres_ordenados)} nombres en: {ruta_salida}")


# Ejemplo de uso (ajusta la ruta de la carpeta):
guardar_nombres_imagenes(
    carpeta_raiz=r"C:\\Users\\smontoya\\Documents\\Scripts\\Johanna Ortiz\\Fotos",
    archivo_txt="C:\\Users\\smontoya\\Documents\\Scripts\\Johanna Ortiz\\imagenes.txt",
    incluir_subcarpetas=True,   # True = recorre subcarpetas
    incluir_extension=False     # False = sin extensión
)
