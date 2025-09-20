const axios = require('axios');

async function getCitiesInColombia() {
  const url = 'https://nominatim.openstreetmap.org/search';

  // Consultas para nombres comunes de ciudades en Colombia
  const cities = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena'];

  const citiesData = [];

  for (const city of cities) {
    try {
      const response = await axios.get(url, {
        params: {
          format: 'json',
          q: `${city}, Colombia`,
        },
      });

      // Filtrar solo los lugares que tengan una clasificación de "city"
      const cityResult = response.data.find(place => place.type === 'city');

      if (cityResult) {
        citiesData.push({
          name: cityResult.display_name,
          lat: cityResult.lat,
          lon: cityResult.lon,
        });
      }
    } catch (error) {
      console.error('Error al obtener datos de la ciudad:', city, error.message);
    }
  }

  return citiesData;
}

// Ejemplo de uso
getCitiesInColombia().then(cities => console.log(cities));
