import pandas as pd

# Cargar el archivo de Excel
file_path = r'C:\\Users\\jsm21\\Downloads\\anserra.xlsx'  # Asegúrate de que la ruta sea correcta
df = pd.read_excel(file_path)

# Filtrar las filas con 'status' igual a 'archived'
filtered_df = df[df['status'] == 'archived']

# Guardar el archivo filtrado en un nuevo archivo
filtered_df.to_excel(r'C:\\Users\\jsm21\\Downloads\\archived_products.xlsx', index=False)  # Guardar como archivo nuevo
