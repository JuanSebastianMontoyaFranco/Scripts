import os
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageOps

def apply_gs1_web_format(
    input_dir: str,
    output_dir: str,
    filename_pattern: str = "{codigo}_C1C1.jpg",  # e.g. CODIGO_C1C1.jpg
    codigo_from_filename: bool = True,            # True: usa el nombre base como CODIGO
    target_size: int = 2400,                      # 2400x2400 px
    dpi: int = 300,                               # 300 ppi
    max_bytes: int = 2 * 1024 * 1024,             # ≤ 2 MB
    min_quality: int = 70,                        # calidad mínima aceptable
    initial_quality: int = 92                     # calidad inicial para JPG
):
    """
    Aplica formato GS1 (versión web) a todas las imágenes de input_dir:
    - Lienzo cuadrado blanco RGB 2400x2400
    - Reescalado sin deformar, centrado
    - Salida JPG a 300 ppi y ≤ 2 MB (ajusta calidad)
    - Renombra con patrón {codigo}_C1C1.jpg (por defecto toma CODIGO del nombre base)
    """
    in_dir = Path(input_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    exts = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
    count_ok, count_fail = 0, 0

    for p in in_dir.iterdir():
        if not p.is_file() or p.suffix.lower() not in exts:
            continue

        try:
            # 1) Abrir y normalizar orientación + convertir a RGB
            im = Image.open(p)
            im = ImageOps.exif_transpose(im)
            im = im.convert("RGB")  # RGB requerido

            # 2) Reescalar manteniendo proporciones para encajar en 2400x2400
            w, h = im.size
            scale = min(target_size / w, target_size / h)
            new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
            im_resized = im.resize((new_w, new_h), Image.LANCZOS)

            # 3) Lienzo blanco cuadrado (fondo #FFFFFF)
            canvas = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            paste_x = (target_size - new_w) // 2
            paste_y = (target_size - new_h) // 2
            canvas.paste(im_resized, (paste_x, paste_y))

            # 4) Definir nombre de salida (CODIGO)
            codigo = p.stem if codigo_from_filename else p.stem  # ajusta si lo lees de otra fuente
            out_name = filename_pattern.format(codigo=codigo)
            out_path = out_dir / out_name

            # 5) Guardar ajustando calidad para cumplir ≤ 2 MB
            quality = initial_quality
            while quality >= min_quality:
                buf = BytesIO()
                canvas.save(
                    buf,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                    progressive=True,
                    dpi=(dpi, dpi),
                )
                size_bytes = buf.tell()
                if size_bytes <= max_bytes:
                    with open(out_path, "wb") as f:
                        f.write(buf.getvalue())
                    break
                quality -= 5

            if not out_path.exists():
                # Si no se logró ≤2MB con la calidad mínima, guardamos el último intento igualmente
                canvas.save(
                    out_path,
                    format="JPEG",
                    quality=max(min_quality, quality),
                    optimize=True,
                    progressive=True,
                    dpi=(dpi, dpi),
                )

            print(f"OK → {out_path.name}")
            count_ok += 1

        except Exception as e:
            print(f"ERROR con {p.name}: {e}")
            count_fail += 1

    print(f"\nHecho. Correctas: {count_ok} | Fallidas: {count_fail} | Carpeta: {out_dir.resolve()}")

# Ejemplo de uso:
apply_gs1_web_format("Fotos_gs1", "fotos_gs1_1", filename_pattern="0{codigo}_A1N1.jpg")
