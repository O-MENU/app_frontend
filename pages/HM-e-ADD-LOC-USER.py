import folium
from folium.plugins import HeatMap
import requests
from urlback import URL

id = 'id do usuario'

# HEAT MAP !!!!!!!
locs_usuario = requests.get(f'{URL}/usuario/{id}/loc').json()['resp'] # essa url ja passa a lista de locs direto!

data = locs_usuario


m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)  # Coordenadas do centro dos EUA


HeatMap(data).add_to(m)


# ADICIONAR LOC PRO USUARIO
loc = {
  'loc': (123, 321)
}

adiciona = requests.put(f'{URL}/usuario/{id}/loc', json=loc) # adiciona a loc na lista de locs do usuario