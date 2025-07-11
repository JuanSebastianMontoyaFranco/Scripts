import os

def guardar_nombres_imagenes_en_txt(carpeta, archivo_salida):
    # Filtrar solo archivos con extensiones comunes de imagen
    extensiones_imagen = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    # Obtener todos los archivos en la carpeta
    nombres_imagenes = [
        archivo for archivo in os.listdir(carpeta)
        if archivo.lower().endswith(extensiones_imagen)
    ]
    
    # Guardar en un archivo .txt
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for nombre in nombres_imagenes:
            f.write(nombre + '\n')

    print(f"Se guardaron {len(nombres_imagenes)} nombres en '{archivo_salida}'.")

# Ejemplo de uso:
guardar_nombres_imagenes_en_txt("C:\\Users\\jsm21\\Downloads\\Imagenes\\Originales2", "nombres_imagenes.txt")
