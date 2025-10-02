import pandas as pd

def actualizar_titles_por_nombre_y_codigo(input_csv, output_csv):
    # Leer CSV
    df = pd.read_csv(input_csv)

    # Limpiar columnas necesarias
    df['Title'] = df['Title'].fillna('').astype(str).str.strip()
    df['Codigo'] = df['Codigo'].fillna('').astype(str).str.strip()

    # Crear columnas auxiliares para ordenar
    df['Title_lower'] = df['Title'].str.lower()
    df['Codigo_num'] = pd.to_numeric(df['Codigo'], errors='coerce')  # Convierte para ordenar correctamente

    # Ordenar primero por Title alfabético (insensible a mayúsculas), luego por Código numérico
    df_ordenado = df.sort_values(by=['Title_lower', 'Codigo_num']).reset_index(drop=True)

    # Crear Title_Final solo si hay título
    df_ordenado['Title_Final'] = df_ordenado.apply(
        lambda row: f"001.{str(row.name + 1).zfill(3)}.{row['Title']}" if row['Title'] else '',
        axis=1
    )

    # Agregar columna Observacion si no existe
    if 'Observacion' not in df_ordenado.columns:
        df_ordenado['Observacion'] = ''

    # Eliminar columnas auxiliares
    df_ordenado.drop(columns=['Title_lower', 'Codigo_num'], inplace=True)

    # Guardar el archivo con todos los datos originales + nuevas columnas
    df_ordenado.to_csv(output_csv, index=False)
    print(f'Archivo guardado correctamente en: {output_csv}')

# Ejecutar
actualizar_titles_por_nombre_y_codigo('importar.csv', 'archivo_actualizado.csv')
