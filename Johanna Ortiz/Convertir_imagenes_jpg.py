import os
import shutil
import itertools
from PIL import Image, ImageFile

# Permite cargar imágenes truncadas o parcialmente corruptas
ImageFile.LOAD_TRUNCATED_IMAGES = True

def _ensure_unique_path(path_sin_ext):
    """
    Si path_sin_ext.jpg existe, genera path_sin_ext_1.jpg, _2, ... hasta que no exista.
    """
    base = path_sin_ext
    candidate = base + ".jpg"
    if not os.path.exists(candidate):
        return candidate
    for i in itertools.count(1):
        candidate = f"{base}_{i}.jpg"
        if not os.path.exists(candidate):
            return candidate

def _to_rgb_on_white(img):
    """
    Convierte a RGB. Si tiene alfa (RGBA/P), compone sobre fondo blanco para evitar fondos negros.
    """
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        # Convertir a RGBA para asegurar canal alfa
        return Image.alpha_composite(bg.convert("RGBA"), img.convert("RGBA")).convert("RGB")
    # Algunos escáneres generan CMYK/YCbCr; convertimos a RGB
    return img.convert("RGB")

def convertir_todo_a_jpg(
    carpeta_entrada: str,
    carpeta_salida: str,
    calidad_jpg: int = 95,
    mantener_estructura: bool = True,
):
    """
    Convierte (o copia si ya es JPG) TODAS las imágenes de carpeta_entrada (recursivo) a .jpg en carpeta_salida.

    - mantener_estructura=True replica la estructura de subcarpetas en la salida.
      Si False, guarda todo plano en carpeta_salida (con nombres únicos para evitar choques).
    - Evita sobrescrituras generando sufijos _1, _2, ...
    """

    soportadas_para_abrir = {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff",
        ".webp", ".ico", ".jfif", ".heic", ".heif"  # heic/heif funciona si tu Pillow tiene soporte
    }
    # Nota: Igual intentamos abrir cualquier cosa; esta lista solo optimiza el filtrado.

    convertidos = 0
    copiados = 0
    saltados = 0
    errores = []

    for raiz, _, archivos in os.walk(carpeta_entrada):
        for archivo in archivos:
            ruta_in = os.path.join(raiz, archivo)
            nombre, ext = os.path.splitext(archivo)
            ext_low = ext.lower()

            # Definir ruta base de salida
            if mantener_estructura:
                rel_dir = os.path.relpath(raiz, carpeta_entrada)
                out_dir = os.path.join(carpeta_salida, rel_dir)
                os.makedirs(out_dir, exist_ok=True)
                base_sin_ext = os.path.join(out_dir, nombre)
            else:
                os.makedirs(carpeta_salida, exist_ok=True)
                base_sin_ext = os.path.join(carpeta_salida, nombre)

            try:
                if ext_low in (".jpg", ".jpeg"):
                    # Solo copiar, con nombre único para no pisar
                    ruta_out = _ensure_unique_path(base_sin_ext)
                    shutil.copy2(ruta_in, ruta_out)
                    copiados += 1
                    print(f"📂 Copiado: {ruta_in} → {ruta_out}")
                    continue

                # Intentar abrir como imagen (aunque no esté en la lista)
                with Image.open(ruta_in) as img:
                    img = _to_rgb_on_white(img)
                    ruta_out = _ensure_unique_path(base_sin_ext)
                    img.save(ruta_out, "JPEG", quality=calidad_jpg, optimize=True, progressive=True)
                    convertidos += 1
                    print(f"✅ Convertido: {ruta_in} → {ruta_out}")

            except Exception as e:
                # Si no es una imagen o falló, lo registramos
                saltados += 1
                errores.append((ruta_in, str(e)))
                print(f"⚠️ No procesado: {ruta_in} → {e}")

    print("\n———— Resumen ————")
    print(f"✅ Convertidos: {convertidos}")
    print(f"📂 Copiados (JPG): {copiados}")
    print(f"⚠️ Saltados/Errores: {saltados}")
    if errores:
        print("\nDetalles de errores:")
        for ruta, err in errores[:50]:  # muestra primeros 50 por brevedad
            print(f" - {ruta}: {err}")
        if len(errores) > 50:
            print(f"... y {len(errores) - 50} más.")

# Uso:
convertir_todo_a_jpg("Fotos", "Fotos2", calidad_jpg=95, mantener_estructura=True)
