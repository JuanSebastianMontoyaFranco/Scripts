import pandas as pd
import re

def split_tags_respetando_parentesis(texto):
    return [tag.strip() for tag in re.split(r',\s*(?![^()]*\))', texto)]

def construir_modelos_validos(df):
    posibles_modelos = set()
    for fila in df['Tags'].fillna(''):
        tags = split_tags_respetando_parentesis(fila)
        for tag in tags:
            matches = re.findall(r'\b[A-Z]{1,4}\b', tag.upper())
            posibles_modelos.update(matches)
    return sorted(posibles_modelos)

def extraer_info_tag(tag, modelos_validos):
    marca = modelo = cilindraje = ''
    tag_upper = tag.upper()

    marca_match = re.search(r'\b[A-Z]{3,}\b', tag_upper)
    if marca_match:
        marca = marca_match.group(0).capitalize()

    cilindro_match = re.findall(r'\b\d{2,3}\b', tag)
    if cilindro_match:
        cilindraje = '/'.join(cilindro_match)

    for modelo_opcion in modelos_validos:
        if re.search(rf'\b{modelo_opcion}\b', tag_upper):
            modelo = modelo_opcion
            break

    return marca, modelo, cilindraje

def procesar_tags_y_generar_archivos(csv_path, salida_csv, salida_txt):
    df = pd.read_csv(csv_path)
    if 'Tags' not in df.columns:
        raise ValueError("El archivo CSV no contiene una columna llamada 'Tags'.")

    modelos_validos = construir_modelos_validos(df)

    marcas_usadas, modelos_usadas, cilindrajes_usadas, detalles_por_tag = [], [], [], []
    marcas_global, modelos_global, cilindrajes_global = set(), set(), set()

    for fila in df['Tags'].fillna(''):
        tags = split_tags_respetando_parentesis(fila)

        marcas, modelos, cilindrajes = set(), set(), set()
        detalles_combinados = []

        for tag in tags:
            marca, modelo, cilindraje = extraer_info_tag(tag, modelos_validos)

            if marca:
                marcas.add(marca)
                marcas_global.add(marca)
                detalles_combinados.append(marca)

            if modelo:
                modelos.add(modelo)
                modelos_global.add(modelo)
                detalles_combinados.append(modelo)

            if cilindraje:
                for cil in cilindraje.split('/'):
                    cil = cil.strip()
                    cilindrajes.add(cil)
                    cilindrajes_global.add(cil)
                    detalles_combinados.append(cil)

        marcas_usadas.append(', '.join(sorted(marcas)))
        modelos_usadas.append(', '.join(sorted(modelos)))
        cilindrajes_usadas.append(', '.join(sorted(cilindrajes)))
        detalles_por_tag.append(', '.join(detalles_combinados))

    df['Marcas usadas'] = marcas_usadas
    df['Modelos usados'] = modelos_usadas
    df['Cilindrajes usados'] = cilindrajes_usadas
    df['Detalles por tag'] = detalles_por_tag

    df.to_csv(salida_csv, index=False, encoding='utf-8-sig')
    print(f"Archivo CSV generado: {salida_csv}")

    with open(salida_txt, 'w', encoding='utf-8') as f:
        f.write("🔹 Marcas usadas:\n")
        for marca in sorted(marcas_global):
            f.write(f"- {marca}\n")
        f.write("\n🔹 Modelos usados:\n")
        for modelo in sorted(modelos_global):
            f.write(f"- {modelo}\n")
        f.write("\n🔹 Cilindrajes usados:\n")
        for cil in sorted(cilindrajes_global, key=int):
            f.write(f"- {cil}\n")

    print(f"Archivo TXT generado: {salida_txt}")

# Uso:
procesar_tags_y_generar_archivos('importar.csv', 'productos_enriquecido.csv', 'listado_tags.txt')
