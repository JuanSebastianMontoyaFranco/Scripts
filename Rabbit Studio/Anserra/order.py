import pandas as pd

# Cargar CSV original
df = pd.read_csv("orden.csv")

# Asegurar tipos
df["Handle"] = df["Handle"].astype(str)
df["Tags"] = df["Tags"].astype(str)
df["Vendor"] = df["Vendor"].astype(str)
df["Title"] = df["Title"].astype(str)

# Lista ordenada de tags
ordered_tags = [
    "Aislador Carburador", "Anillos", "Arandela y Tuerca Cigüeñal", "Araña de Clutch", "Árboles de levas",
    "Automático Trasero", "Balancines", "Balineras", "Barra Telescópica", "Bobinas", "Bombas", "Brazos",
    "Bujes", "C.D.I", "Cadenas", "Cadenillas", "Cajas de Cambio", "Caliper Freno", "Campana Clutch", "Canastilla",
    "Capuchones Bujía", "Carburadores", "Cauchos", "Centro y Plato Embrague Completo", "Centro y Plato Embrague",
    "Cigüeñal", "Clutch", "Comando", "Conectores Filtro Aire", "Conjunto Piñón", "Correa Distribución", 
    "Cuchara de Cambios", "Ejes Abrebandas", "Ejes Caja", "Ejes Cambios", "Ejes", "Ejes Pedal", "Ejes Piñón",
    "Escobillas", "Estatores Bobinas", "Filtros", "Flasher", "Flauta", "Guías", "Horquillas", "Instalación Eléctrica",
    "Kit Bielas", "Kit Cilindros", "Kit Cunas", "Kit Discos", "Kit Distribución", "Kit Flota y Aguja", "Kit Guías Tensor",
    "Kit Pernos", "Kit Pistones", "Kit Reparación", "Kit Retenes", "Kit Tijeras", "Levas", "Llaves Gasolina",
    "Mango Acelerador", "Maniguetas", "Medidor de Combustible", "Motor de Arranque", "Muñón de Crank", "O-Ring",
    "Pastillas de Freno", "Pata Lateral", "Pedales", "Piñones", "Portabandas", "Porta Sprocket", "Reguladores",
    "Relay", "Reposapie", "Retenes", "Roldanas", "Rotor", "Seguro Tapa Lateral", "Selector de Cambios",
    "Sellos Válvula", "Sensor Velocidad", "Socket Farola", "Soportes", "Switches", "Tapa Gasolina", "Tapa Válvula",
    "Tensor Cadena", "Tensor Hidráulico", "Torque Inducción", "Válvulas Plus", "Varilla Impulsora"
]

# Paso 1: obtener el índice del tag (X)
def get_tag_index(tags):
    for i, tag in enumerate(ordered_tags):
        if tag in tags:
            return i + 1
    return None

# Asignar índice de tag
df["tag_index"] = df["Tags"].apply(get_tag_index)

# Crear vendor_prefix con primeros 6 dígitos
df["vendor_prefix"] = df["Vendor"].str[:6]

# Crear vendor_prefix → tag_index para los que sí tienen tag válido y título
vendor_group_map = {}
for _, row in df[df["tag_index"].notna() & df["Title"].str.strip().ne("")].iterrows():
    prefix = row["vendor_prefix"]
    if prefix not in vendor_group_map:
        vendor_group_map[prefix] = row["tag_index"]

# Asignar título final
def asignar_title(row):
    if row["Title"].strip() == "":
        return row["Title"]
    tag_index = row["tag_index"]
    if tag_index is None:
        tag_index = vendor_group_map.get(row["vendor_prefix"], 999)
    return f"{tag_index}.{row['Vendor']} {row['Title']}"

# Aplicar
df["Title"] = df.apply(asignar_title, axis=1)

# Limpiar columnas auxiliares
df.drop(columns=["tag_index", "vendor_prefix"], inplace=True)

# Guardar
df.to_csv("shopify_listing_titles_con_vendor_grupo.csv", index=False)
