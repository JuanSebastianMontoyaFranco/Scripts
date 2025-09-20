import pandas as pd
import os

def exportar_vendors_con_imagen(csv_path, txt_imagenes_path, output_txt_path):
    # Leer CSV
    df = pd.read_csv(csv_path)

    # Leer TXT y extraer códigos antes del primer punto
    with open(txt_imagenes_path, 'r') as file:
        nombres_imagenes = file.readlines()
    codigos_imagen = {line.strip().split('.')[0] for line in nombres_imagenes if line.strip()}

    # Asegurar que 'Vendor' es string
    df['Vendor'] = df['Vendor'].astype(str)

    # Filtrar Vendors que están en la lista de códigos
    vendors_en_csv = set(df['Vendor'])
    vendors_con_imagen = sorted(vendors_en_csv.intersection(codigos_imagen))

    # Encontrar imágenes sin vendor asociado
    imagenes_sin_vendor = sorted(codigos_imagen.difference(vendors_en_csv))

    # Guardar resultado en un TXT
    if vendors_con_imagen:
        with open(output_txt_path, 'w') as output_file:
            for vendor in vendors_con_imagen:
                output_file.write(f"{vendor}\n")
        print(f"✅ Se guardó el archivo con Vendors que tienen imágenes en: {output_txt_path}")
    else:
        print("⚠️ No se encontró ningún Vendor con imagen.")
        if os.path.exists(output_txt_path):
            os.remove(output_txt_path)

    # Mostrar imágenes que no tienen vendor
    if imagenes_sin_vendor:
        print("\n🔍 Imágenes que no tienen Vendor asociado en el CSV:")
        for codigo in imagenes_sin_vendor:
            print(f"- {codigo}")
    else:
        print("\n✅ Todas las imágenes tienen Vendor asociado en el CSV.")

# Uso
csv_path = 'productos-dos.csv'
txt_imagenes_path = 'nombres_imagenes.txt'
output_txt_path = 'vendors_con_imagen.txt'

exportar_vendors_con_imagen(csv_path, txt_imagenes_path, output_txt_path)
