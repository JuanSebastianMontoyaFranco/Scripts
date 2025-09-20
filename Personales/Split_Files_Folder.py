import os
import shutil

def dividir_archivos_en_carpetas(carpeta_origen, max_archivos=198):
    # Obtener la lista de archivos en la carpeta origen
    archivos = [f for f in os.listdir(carpeta_origen) if os.path.isfile(os.path.join(carpeta_origen, f))]
    
    # Contador de carpetas
    num_carpeta = 1
    index = 0
    
    while index < len(archivos):
        # Crear el nombre de la subcarpeta
        carpeta_destino = os.path.join(carpeta_origen, f'lote_{num_carpeta}')
        os.makedirs(carpeta_destino, exist_ok=True)
        
        # Obtener el subconjunto de archivos para esta subcarpeta
        archivos_lote = archivos[index:index + max_archivos]
        
        # Mover los archivos a la subcarpeta
        for archivo in archivos_lote:
            shutil.move(os.path.join(carpeta_origen, archivo), os.path.join(carpeta_destino, archivo))
        
        # Actualizar contadores
        index += max_archivos
        num_carpeta += 1

# Uso
dividir_archivos_en_carpetas(r"C:\Users\jsm21\Downloads\archivos")
