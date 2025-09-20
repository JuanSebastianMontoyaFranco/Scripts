import requests

def obtener_vendedores_y_guardar_txt():
    url = "https://apis.serpi.com.co/api/v1/Tercero"
    token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiI4MDUwMjYzODYiLCJ1bmlxdWVfbmFtZSI6IklNUE9SVEFET1JBIEFORElOQSBERSBSRVBVRVNUT1MgU0FTIiwiU3RrZW1wcmVzYWlkIjoiMTMiLCJnZHRlbXByZXNhaWQiOiIxIiwiZ2R0dXN1YXJpb2lkIjoiNjQiLCJ1c2VyIjoiR0xPUklBIEFNUEFSTyBIRU5BTyBBTkdFTCIsInVybCI6Imh0dHBzOi8vYW5kaW5hcmVwLnNlcnBpLmNvbS5jby8iLCJzY2hlbWUiOiJzZXJwaV9hbmRpbmF8MTcyLjMxLjMzLjEzOSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjkvMy8yMDI1IDExOjU5OjQ3IFBNIiwibmJmIjoxNzU0MzM5NTY3LCJleHAiOjE3NTY5NjE5ODcsImlhdCI6MTc1NDMzOTU2N30.tYoMZh1uwUG62DGZtc6UfDSKMkAqH23-qonhqho_ItAojc3wqVqa3lN__FW9xEpN3zj8apkBlc1aXAy6MATcmQ"
    secretkey = "af2002659f5ef4c96d35a614239e3da7"

    headers = {
        "Authorization": f"Bearer {token}",
        "secretkey": secretkey
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        vendedores = []

        for item in data.get("result", []):
            if item.get("esvendedor", False):
                identificacion = item.get("identificacion", "")
                email = item.get("email", "")
                vendedores.append(f"{identificacion} - {email}")

        # Guardar en un archivo .txt
        with open("vendedores.txt", "w", encoding="utf-8") as file:
            for linea in vendedores:
                file.write(linea + "\n")

        print(f"{len(vendedores)} registros guardados en 'vendedores.txt'.")

    else:
        print(f"Error al consultar la API: {response.status_code} - {response.text}")

# Ejecutar función
obtener_vendedores_y_guardar_txt()
