import os
import shutil
import pandas as pd

# Ajusta estas rutas:
archivo_excel = "pendientes.xlsx"                 # tu archivo de Excel
carpeta_origen = "Imagenes"           # carpeta donde están las imágenes actuales
carpeta_destino = "Fotos_gs1"           # carpeta donde se guardarán con el nuevo nombre

# Crea la carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Lee el Excel
df = pd.read_excel(archivo_excel)

# Recorre cada fila del Excel
for _, fila in df.iterrows():
    barra = str(fila['BARRAS']).strip()
    codigo = str(fila['CODIGO']).strip()

    # Busca el archivo en la carpeta origen (independiente de la extensión)
    for archivo in os.listdir(carpeta_origen):
        nombre, ext = os.path.splitext(archivo)
        if nombre == codigo:  # coincide el nombre con CODIGO
            origen = os.path.join(carpeta_origen, archivo)
            destino = os.path.join(carpeta_destino, barra + ext)
            shutil.copy2(origen, destino)  # copia con metadatos
            print(f"Copiado: {archivo} → {barra + ext}")
            break
