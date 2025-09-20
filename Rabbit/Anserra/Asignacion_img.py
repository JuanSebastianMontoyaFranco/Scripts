import pandas as pd
import re
from pathlib import Path
import urllib.parse


def cargar_imagenes_existentes(ruta_txt):
    with open(ruta_txt, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def procesar_productos_con_imagenes(ruta_entrada, ruta_txt, ruta_salida):
    df = pd.read_csv(ruta_entrada)

    columnas_necesarias = ["Handle", "Variant Barcode"]
    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f"❌ Falta la columna: {col}")

    imagenes = cargar_imagenes_existentes(ruta_txt)

    base_url = "https://raw.githubusercontent.com/JuanSebastianMontoyaFranco/Imagenes/main/Originales2"

    imagenes_dict = {}
    for img in imagenes:
        match = re.match(r"(\d+)", Path(img).stem)
        if match:
            codigo = match.group(1)
            if codigo not in imagenes_dict:
                imagenes_dict[codigo] = []
            imagenes_dict[codigo].append(img)

    columnas_finales = df.columns.tolist()
    if "Image Src" not in columnas_finales:
        columnas_finales.append("Image Src")
    if "Image Position" not in columnas_finales:
        columnas_finales.append("Image Position")

    nuevas_filas = []
    for _, fila in df.iterrows():
        handle = fila["Handle"]
        barcode = str(fila["Variant Barcode"]).strip()

        if barcode not in imagenes_dict:
            continue

        imagenes_asociadas = sorted(imagenes_dict[barcode])  # opcional: ordena alfabéticamente
        for i, nombre_imagen in enumerate(imagenes_asociadas, start=1):
            nueva_fila = {col: "" for col in columnas_finales}
            
            nueva_fila["Handle"] = handle
            if i == 1:
                for col in df.columns:
                    nueva_fila[col] = fila[col]
            nombre_imagen_url = urllib.parse.quote(nombre_imagen)
            nueva_fila["Image Src"] = f"{base_url}/{nombre_imagen_url}"
            nueva_fila["Image Position"] = i
            nuevas_filas.append(nueva_fila)

    if not nuevas_filas:
        print("⚠️ No se encontraron coincidencias entre los barcodes y las imágenes.")
    else:
        df_final = pd.DataFrame(nuevas_filas)
        df_final.to_csv(ruta_salida, index=False)
        print(f"✅ Archivo generado correctamente: {ruta_salida}")

# USO LOCAL
if __name__ == "__main__":
    procesar_productos_con_imagenes(
        ruta_entrada="productos.csv",
        ruta_txt="nombres_imagenes.txt",
        ruta_salida="productos_procesados.csv"
    )
