import pandas as pd

def procesar_productos_csv(ruta_entrada: str, ruta_salida: str):
    df = pd.read_csv(ruta_entrada)

    columnas_necesarias = ["Handle", "Variant Barcode", "Image Position", "Image Src"]
    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f"❌ Falta la columna: {col}")

    if "Procesado" not in df.columns:
        df["Procesado"] = ""

    columnas_finales = list(df.columns)
    nuevas_filas = []

    for _, fila in df.iterrows():
        if fila["Procesado"] == "Sí":
            continue

        handle = fila["Handle"]
        barcode = str(fila["Variant Barcode"]).strip()

        fila_dict = fila.to_dict()
        fila_dict["Image Position"] = 1
        fila_dict["Procesado"] = "Sí"

        # Si Image Src está vacío, asignar imagen .1 a la fila original
        if not str(fila_dict["Image Src"]).strip():
            fila_dict["Image Src"] = f"https://raw.githubusercontent.com/JuanSebastianMontoyaFranco/Imagenes/main/Todas/{barcode}.1.jpg"
            nuevas_filas.append(fila_dict)

            # Crear solo 4 adicionales: .2 a .5
            for i in range(2, 6):
                nueva_fila = {col: "" for col in columnas_finales}
                nueva_fila["Handle"] = handle
                nueva_fila["Image Position"] = i
                nueva_fila["Image Src"] = f"https://raw.githubusercontent.com/JuanSebastianMontoyaFranco/Imagenes/main/Todas/{barcode}.{i}.jpg"
                nueva_fila["Procesado"] = "Sí"
                nuevas_filas.append(nueva_fila)
        else:
            # Ya tiene una imagen, crear 5 nuevas: .1 a .5
            nuevas_filas.append(fila_dict)
            for i in range(1, 6):
                nueva_fila = {col: "" for col in columnas_finales}
                nueva_fila["Handle"] = handle
                nueva_fila["Image Position"] = i + 1
                nueva_fila["Image Src"] = f"https://raw.githubusercontent.com/JuanSebastianMontoyaFranco/Imagenes/main/Todas/{barcode}.{i}.jpg"
                nueva_fila["Procesado"] = "Sí"
                nuevas_filas.append(nueva_fila)

    df_final = pd.DataFrame(nuevas_filas, columns=columnas_finales)
    df_final.to_csv(ruta_salida, index=False)
    print(f"✅ Archivo generado correctamente: {ruta_salida}")

# Ejecutar
procesar_productos_csv("productos.csv", "productos_procesados.csv")
