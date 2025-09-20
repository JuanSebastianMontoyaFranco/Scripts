import pandas as pd

def actualizar_titles_por_tags_y_codigo(input_csv, output_csv):
    # Leer CSV
    df = pd.read_csv(input_csv)

    # Lista de grupos
    tags_list = [
        'ANILLOS', 'ARANDELAS Y TUERCA CIGÜEÑAL', 'ARAÑAS DE CLUTCH', 'ARBOLES DE LEVAS',
        'AUTOMATICO TRASERO', 'BALANCINES (ADM/ESC, INFERIOR, SUPERIOR)', 'BALINERAS (CIGÙENAL, DE CLUTCH)',
        'BARRA TELESCOPICA', 'BOBINAS (ALTA, ENCENDIDO, PULSORA)', 'BOMBAS (ACEITE, FRENO)',
        'BRAZOS (OSCILANTES, TENSORES)', 'BUJES (ARBOL DE LEVAS, CLUTCH, PORTACATALINA)', 'C.D.I.',
        'CADENAS', 'CADENILLAS', 'CAJAS DE CAMBIO', 'CALIPER FRENO', 'CANASTILLA (CAJA, CLUTCH, PISTON)',
        'CAPUCHONES BUJIA', 'CARBURADORES', 'CAUCHOS (CAMPANA, POSAPIES, SELECTOR, TORQUE)',
        'CENTROS Y PLATO EMBRAGUE', 'CIGÜEÑAL', 'CLUTCH (UNA VIA, AUTOMATICO, PRIMARIO)', 'CONDENSADORES',
        'CONECTORES FILTRO AIRE', 'CONJUNTOS PIÑON VELOCIMETRO', 'CORONAS ARAÑA CLUTCH', 'CORREA DISTRIBUCION',
        'CUCHARA DE  CAMBIOS', 'EJES (DELANTERO, TRASERO)', 'EJES ABREBANDAS', 'EJES CAJA',
        'EJES CAMBIOS', 'EJES PEDAL ARRANQUE', 'EJES PIÑON (BOMBA,CAJA, SALIDA)', 'ESCOBILLAS',
        'ESTATORES BOBINA', 'FILTROS (ACEITE, AIRE)', 'FLASHER', 'FLAUTA',
        'GUIAS (CADENILLA, CILINDRO, LUBRICACION, VALVULA ADM/ESC)', 'HORQUILLAS', 'INSTALACION ELECTRICA',
        'KIT BIELAS', 'KIT CILINDROS', 'KIT CUNAS DIRECCION', 'KIT DISCOS CLUTCH', 'KIT DISTRIBUCION',
        'KIT FLOTA Y AGUJA', 'KIT GUIAS TENSOR CADENILLA', 'KIT PERNOS PORTACATALINA', 'KIT PISTONES',
        'KIT REPARACION', 'KIT RETENES', 'KIT TIJERAS', 'LEVAS (CLUCH, FRENO)', 'LLAVES GASOLINA',
        'MANGO ACELERADOR', 'MANIGUETAS', 'MEDIDORES COMBUSTIBLE', 'MOTORES DE ARRANQUE', 'MUÑON DE CRANK',
        'O-RING', 'PASTILLAS DE FRENO', 'PATA LATERAL', 'PEDALES (ARRANQUE, CAMBIOS, FRENO)',
        'PIÑONES (ARBOL DE LEVAS ,CAJA, CIGÜEÑAL TIEMPO, CONDUCTOR, CRANK, FUERZA, VELOCIMETRO,TENSOR)',
        'PORTA SPROCKET', 'PORTABANDAS', 'REGULADORES', 'RELAY', 'REPOSAPIES', 'RETENES', 'ROLDANAS',
        'SEGURO TAPA LATERAL', 'SELECTOR DE CAMBIOS', 'SELLOS VALVULA', 'SENSOR VELOCIDAD', 'SOCKET FAROLA',
        'SOPORTES (ESTRIBO, MANIGUETA)', 'SWITCHES (ARRANQUE, CLUTCH, ENCENDIDO,FRENO,INDICADOR CAMBIOS, NEUTRO)',
        'TAPA VAVULA', 'TAPAS GASOLINA', 'TENSORES CADENA', 'TENSORES HIDRAHULICOS', 'TORQUES INDUCCION',
        'VALVULAS PLUS'
    ]

    # Crear mapa de orden
    tags_dict = {tag: idx + 1 for idx, tag in enumerate(tags_list)}

    # Limpiar columnas
    df['Tags.2'] = df['Tags.2'].fillna('').str.strip().str.upper()
    df['Codigo'] = df['Codigo'].fillna('').astype(str).str.strip()
    df['Title'] = df['Title'].fillna('').astype(str).str.strip()

    df['Title_Final'] = df['Title']
    df['Observacion'] = ''

    # Procesar cada grupo
    for tag in tags_list:
        grupo = df[df['Tags.2'] == tag].copy()
        if grupo.empty:
            continue
        grupo = grupo.sort_values(by='Codigo')
        for subindex, (idx, row) in enumerate(grupo.iterrows(), start=1):
            prefix = f"{str(tags_dict[tag]).zfill(3)}.{str(subindex).zfill(3)}."
            df.at[idx, 'Title_Final'] = f"{prefix}{row['Title']}"

    # Marcar los que no tienen coincidencia
    df.loc[~df['Tags.2'].isin(tags_list), 'Observacion'] = 'NO ASIGNADO'

    # Guardar resultado
    df.to_csv(output_csv, index=False)
    print(f'Archivo guardado correctamente en: {output_csv}')


# Ejecutar
actualizar_titles_por_tags_y_codigo('hola.csv', 'archivo_actualizado.csv')
