import pandas as pd
import requests
import time

# Cargar el archivo de Excel
excel_file = "C:\\Users\\jsm21\\Downloads\\Direcciones 200.xlsx"  # Reemplaza con la ruta de tu archivo
df = pd.read_excel(excel_file)

# Iterar sobre cada fila del DataFrame
for index, row in df.iterrows():
    direccion = row['billing_address_1']
    ciudad = row['billing_city']
    key = 'AIzaSyAdmK1VOx3h8sXPhHsk8JtleSRC_-cQtWE'
    
    # Construir la URL de la API de Google Maps
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={key}&components=locality:{ciudad}country:CO"
    
    try:
        # Hacer la solicitud GET a la API
        response = requests.get(url)
        data = response.json()
        
        print("Respuesta de la API:", data)
        print("****************************************")
        
        # Verificar si la solicitud fue exitosa y si hay resultados
        if response.status_code == 200:
            # Extraer latitud y longitud de la respuesta JSON
            latitud = data['results'][0]['geometry']['location']['lat']
            longitud = data['results'][0]['geometry']['location']['lng']
            
            # Imprimir los valores de latitud y longitud
            print(f"Latitud: {latitud}, Longitud: {longitud}")
            # Colocar los valores de latitud y longitud en el DataFrame
            df.at[index, 'Latitud'] = latitud
            df.at[index, 'Longitud'] = longitud
        else:
            print(f"No se pudieron obtener las coordenadas para la dirección: {direccion}, ciudad: {ciudad}")
    except Exception as e:
        print(f"Error al procesar la solicitud para la dirección: {direccion}, ciudad: {ciudad}. Error: {e}")


# Guardar el DataFrame actualizado en un nuevo archivo de Excel
df.to_excel("C:\\Users\\jsm21\\Downloads\\Direcciones 200V1.xlsx", index=False)
