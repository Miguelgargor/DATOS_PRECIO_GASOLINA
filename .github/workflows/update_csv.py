import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import io


# URL de la página web que contiene el precio del diésel
url = 'https://plenoil.es/estacion/plenoil-avila?lang=es'

# URL del archivo CSV en GitHub (URL cruda)
github_csv_url = 'https://raw.githubusercontent.com/Miguelgargor/DATOS_PRECIO_GASOLINA/main/PRECIO%20GASOLINA.csv'

# Realizar una solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar el elemento que contiene el precio del diésel
    precio_element_diesel= soup.select_one('#imagen-fondo > div > section > div > div.elementor-column.elementor-col-50.elementor-inner-column.elementor-element.elementor-element-b5f06b3 > div > div.elementor-element.elementor-element-732af91.elementor-widget.elementor-widget-heading > div > h2')
    precio_element_gasolina= soup.select_one('#imagen-fondo > div > section > div > div.elementor-column.elementor-col-50.elementor-inner-column.elementor-element.elementor-element-3769b81 > div > div.elementor-element.elementor-element-20e92a9.elementor-widget.elementor-widget-heading > div > h2')

    if precio_element_diesel:
        precio_diesel = precio_element_diesel.text.strip('€')
        precio_gasolina = precio_element_gasolina.text.strip('€')

        # Obtener la fecha actual:
        fecha_actual = pd.to_datetime(datetime.now(), format='%d/%m/%Y')

        # Crear un nuevo DataFrame con la fecha y precio del diésel
        nuevo_registro = pd.DataFrame({'Fecha':[fecha_actual], 'Precio Diesel':[float(precio_diesel)], 'Precio Gasolina 95':[float(precio_gasolina)]})


        # Cargar los datos desde el archivo CSV en GitHub
        csv_data = requests.get(github_csv_url)
        df = pd.read_csv(io.StringIO(csv_data.text), sep=';')

        # Agregar el nuevo registro al DataFrame
        df = pd.concat([df, nuevo_registro], ignore_index=True)

        # ELIMINAR FILAS ANTERIORES A-> 1 AÑO:
        df = df.iloc[-365:]

        # Guardar los datos de nuevo en el archivo CSV en GitHub
        requests.put(github_csv_url, data=df.to_csv(index=False, sep=';'))
else:
    print('Error al obtener la página web.')

df