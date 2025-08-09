import pandas as pd

def actualizar_titles_por_grupo_y_codigo(input_csv, output_csv):
    # Leer CSV
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    print("📋 Columnas encontradas:", df.columns.tolist())

    if 'Grupo' not in df.columns:
        print("⚠️ La columna 'Grupo' no existe. Revisa el nombre exacto.")
        return

    # Limpiar columnas necesarias
    df['Grupo'] = df['Grupo'].astype(str).str.strip()
    df['Codigo'] = df['Codigo'].fillna('').astype(str).str.strip()
    df['Title'] = df['Title'].fillna('').astype(str).str.strip()

    # Intentar convertir a número los valores de 'Grupo'
    df['Grupo'] = pd.to_numeric(df['Grupo'], errors='coerce')  # NaN si no es convertible
    df = df.dropna(subset=['Grupo'])  # eliminar filas con Grupo inválido
    df['Grupo'] = df['Grupo'].astype(int)

    if df.empty:
        print("⚠️ No quedan filas válidas con valores numéricos en 'Grupo'.")
        return

    df['Title_Final'] = df['Title']
    df['Observacion'] = ''

    # Procesar cada grupo
    for grupo_num in sorted(df['Grupo'].unique()):
        grupo_df = df[df['Grupo'] == grupo_num].copy()
        grupo_df = grupo_df.sort_values(by='Codigo')
        for subindex, (idx, row) in enumerate(grupo_df.iterrows(), start=1):
            prefix = f"{str(grupo_num).zfill(3)}.{str(subindex).zfill(3)}."
            df.at[idx, 'Title_Final'] = f"{prefix}{row['Title']}"

    # Guardar resultado
    df.to_csv(output_csv, index=False)
    print(f'✅ Archivo guardado correctamente en: {output_csv}')
    print(f"🧾 Filas procesadas: {len(df)}")

# Ejecutar
actualizar_titles_por_grupo_y_codigo('prueba.csv', 'archivo_actualizado.csv')
