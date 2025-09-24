
import folium

# Coordenadas corregidas del centro histórico (Parque Diosa Chía)
CENTRO_HISTORICO_CHIA = [4.8595, -74.0588]

# Crear el mapa centrado en el parque principal
mapa = folium.Map(
    location=CENTRO_HISTORICO_CHIA,
    zoom_start=16,
    tiles='OpenStreetMap'
)

# Agregar capa satelital como opción
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satelital',
    overlay=False,
    control=True
).add_to(mapa)

# Marcador del centro histórico con popup mejorado
folium.Marker(
    CENTRO_HISTORICO_CHIA,
    popup='''
        <div style="width: 200px;">
            <h4>Centro Histórico de Chía</h4>
            <p><strong>Parque Diosa Chía</strong></p>
            <p>Plaza Principal</p>
            <p>Zona: ZCH</p>
            <p>Uso: Comercial, Cultural, Residencial, Institucional</p>
        </div>
    ''',
    tooltip='Centro Histórico - Parque Diosa Chía',
    icon=folium.Icon(color='red', icon='home')
).add_to(mapa)

# Definir zonas de uso del suelo con colores distintivos
zonas_colores = {
    'ZCH': '#FF6B6B',  # Rojo - Centro Histórico
    'ZRN': '#4ECDC4',  # Verde agua - Yerbabuena Norte
    'ZI': '#45B7D1',   # Azul - Fusca Industrial
    'ZVP': '#96CEB4',  # Verde claro - La Balsa Ecológica
    'ZC': '#FECA57',   # Amarillo - Corredor Comercial
    'ZM': '#FF9FF3',   # Rosa - Fagua Mixta
    'ZR': '#A8E6CF',   # Verde pastel - Bojacá Residencial
    'ZRU': '#FFD93D'   # Amarillo oro - Fonquetá Rural
}

# Coordenadas aproximadas de las veredas principales
veredas_coordenadas = {
    'Fagua': [[4.8850, -74.0450], [4.8750, -74.0350], [4.8650, -74.0400], [4.8750, -74.0500]],
    'Tiquiza': [[4.8750, -74.0650], [4.8650, -74.0550], [4.8550, -74.0600], [4.8650, -74.0700]],
    'Bojacá': [[4.8450, -74.0500], [4.8350, -74.0400], [4.8250, -74.0450], [4.8350, -74.0550]],
    'Yerbabuena': [[4.8900, -74.0300], [4.8800, -74.0200], [4.8700, -74.0250], [4.8800, -74.0350]],
    'Fusca': [[4.8350, -74.0250], [4.8250, -74.0150], [4.8150, -74.0200], [4.8250, -74.0300]],
    'La Balsa': [[4.8150, -74.0450], [4.8050, -74.0350], [4.7950, -74.0400], [4.8050, -74.0500]],
    'Cerca de Piedra': [[4.8050, -74.0650], [4.7950, -74.0550], [4.7850, -74.0600], [4.7950, -74.0700]],
    'Fonquetá': [[4.7750, -74.0400], [4.7650, -74.0300], [4.7550, -74.0350], [4.7650, -74.0450]]
}

# Agregar polígonos de veredas con mejor visualización
for vereda, coords in veredas_coordenadas.items():
    # Determinar zona y color
    zona_key = 'ZRU' if 'Fonquetá' in vereda else 'ZR'
    if vereda == 'Fagua':
        zona_key = 'ZM'
    elif vereda == 'Fusca':
        zona_key = 'ZI'
    elif vereda == 'Yerbabuena':
        zona_key = 'ZRN'
    elif vereda == 'La Balsa':
        zona_key = 'ZVP'
    
    folium.Polygon(
        locations=coords,
        popup=f'Vereda {vereda} - Zona: {zona_key}',
        tooltip=f'Vereda {vereda}',
        color='#2E7D32',
        weight=2,
        fillColor=zonas_colores.get(zona_key, '#CCCCCC'),
        fillOpacity=0.3
    ).add_to(mapa)

# Agregar puntos de referencia importantes
puntos_referencia = [
    [4.8620, -74.0565, "Alcaldía Municipal"],
    [4.8605, -74.0580, "Iglesia Parroquial"],
    [4.8590, -74.0590, "Centro Comercial"],
    [4.8640, -74.0550, "Hospital"],
    [4.8610, -74.0560, "Estación Policía"]
]

for lat, lon, nombre in puntos_referencia:
    folium.Marker(
        [lat, lon],
        popup=f'{nombre} - Centro de Chía',
        tooltip=nombre,
        icon=folium.Icon(color='blue')
    ).add_to(mapa)

# Agregar control de capas
folium.LayerControl().add_to(mapa)

# Guardar el mapa
mapa.save('mapa_chia_centro_corregido.html')

print("Mapa creado correctamente")
print("Centro histórico ubicado en Plaza Diosa Chía")
print("Veredas mejoradas con mayor visibilidad")
print("Archivo guardado como: mapa_chia_centro_corregido.html")