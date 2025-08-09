import pandas as pd

def extraer_tags_ordenados(csv_path, txt_path):
    # Cargar CSV
    df = pd.read_csv(csv_path)
    
    # Asegurar que la columna existe
    if 'Tags.2' not in df.columns:
        raise ValueError("La columna 'Tags.2' no existe en el archivo CSV.")
    
    # Quitar nulos y limpiar espacios
    tags = df['Tags.2'].dropna().astype(str).str.strip()
    
    # Eliminar duplicados, limpiar espacios, ordenar
    tags_unicos = sorted(set(tags))
    
    # Guardar en .txt, uno por línea
    with open(txt_path, 'w', encoding='utf-8') as f:
        for tag in tags_unicos:
            f.write(tag + '\n')

    print(f'Tags guardados en: {txt_path}')


# Uso
csv_path = 'hola.csv'
txt_path = 'tags_ordenados.txt'
extraer_tags_ordenados(csv_path, txt_path)
