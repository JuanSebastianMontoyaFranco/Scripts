import pandas as pd
import re

def split_tags_respetando_parentesis(texto):
    # Divide los tags por comas que están fuera de paréntesis
    return [tag.strip() for tag in re.split(r',\s*(?![^()]*\))', texto)]

def extraer_tags_unicos(csv_path, salida_txt):
    # Leer CSV
    df = pd.read_csv(csv_path)

    if 'Tags' not in df.columns:
        raise ValueError("El archivo CSV no contiene una columna llamada 'Tags'.")

    tags = []
    for lista in df['Tags'].dropna():
        tags.extend(split_tags_respetando_parentesis(lista))

    # Eliminar duplicados y ordenar alfabéticamente
    tags_unicos = sorted(set(tags))

    # Guardar en archivo TXT
    with open(salida_txt, 'w', encoding='utf-8') as f:
        for tag in tags_unicos:
            f.write(tag + '\n')

    print(f"Se han guardado {len(tags_unicos)} tags únicos en '{salida_txt}'.")

# Ejemplo de uso:
extraer_tags_unicos('importar.csv', 'tags_unicos.txt')
