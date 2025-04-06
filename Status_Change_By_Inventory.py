import pandas as pd

# Cargar el archivo de Excel
file_path = 'C:\\Users\\jsm21\\Downloads\\anserra.xlsx'  # Sustituye con la ruta de tu archivo
df = pd.read_excel(file_path)

# Comprobar los valores en la columna 'Variant Inventory Qty' y actualizar 'status'
df['status'] = df['Variant Inventory Qty'].apply(lambda x: 'archived' if x <= 0 else 'active')

# Guardar los cambios en un nuevo archivo o sobrescribir el original
df.to_excel('C:\\Users\\jsm21\\Downloads\\archivo_actualizado.xlsx', index=False)  # Puedes cambiar el nombre de salida
