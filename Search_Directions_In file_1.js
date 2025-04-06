const fs = require('fs');
const axios = require('axios');
const ExcelJS = require('exceljs');
const XLSX = require('xlsx');

// Ruta del archivo de Excel de entrada y salida
const excelFilePathInput = "C:\\Users\\jsm21\\Downloads\\Direcciones 200.xlsx";
const excelFilePathOutput = "C:\\Users\\jsm21\\Downloads\\Direcciones 200V2.xlsx";

// Leer el archivo de Excel
const workbook = XLSX.readFile(excelFilePathInput);
const sheet_name_list = workbook.SheetNames;
const jsonData = XLSX.utils.sheet_to_json(workbook.Sheets[sheet_name_list[0]]);

// Crear un nuevo libro de Excel
const workbookOutput = new ExcelJS.Workbook();
const worksheetOutput = workbookOutput.addWorksheet('Direcciones');

// Agregar encabezados a la hoja de cálculo de salida
worksheetOutput.addRow(['Dirección', 'Ciudad', 'Latitud', 'Longitud']);

// Iterar sobre cada fila del objeto JSON
(async () => {
    for (const [index, row] of jsonData.entries()) {
        const direccion = row['billing_address_1'];
        const ciudad = row['billing_city'];
        const key = 'AIzaSyBhS2uKnMaLfRVVCjcByt2kLs_sJG30epE';
        
        // Construir la URL de la API de Google Maps
        const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${direccion}&key=${key}&components=locality:${ciudad}|country:CO`;
        
        try {
            // Hacer la solicitud GET a la API con axios
            const response = await axios.get(url);
            const data = response.data;
            
            console.log("Respuesta de la API:", data);
            console.log("****************************************");
            
            // Verificar si la solicitud fue exitosa y si hay resultados
            if (response.status === 200 && data.results.length > 0) {
                // Extraer latitud y longitud de la respuesta JSON
                const latitud = data.results[0].geometry.location.lat;
                const longitud = data.results[0].geometry.location.lng;
                
                // Agregar la fila con los resultados a la hoja de cálculo de salida
                worksheetOutput.addRow([direccion, ciudad, latitud, longitud]);
            } else {
                console.log(`No se pudieron obtener las coordenadas para la dirección: ${direccion}, ciudad: ${ciudad}`);
                // Agregar una fila con valores nulos a la hoja de cálculo de salida
                worksheetOutput.addRow([direccion, ciudad, null, null]);
            }
        } catch (error) {
            console.log(`Error al procesar la solicitud para la dirección: ${direccion}, ciudad: ${ciudad}. Error: ${error.message}`);
            // Agregar una fila con valores nulos a la hoja de cálculo de salida
            worksheetOutput.addRow([direccion, ciudad, null, null]);
        }
        
        // Esperar 30 segundos antes de la próxima solicitud
        await new Promise(resolve => setTimeout(resolve, 30000));
    }
    
    // Guardar el libro de Excel de salida en un archivo
    await workbookOutput.xlsx.writeFile(excelFilePathOutput);
    console.log(`Archivo de Excel exportado a: ${excelFilePathOutput}`);
})();
