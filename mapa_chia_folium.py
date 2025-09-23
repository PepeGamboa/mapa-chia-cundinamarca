import folium
import json
from folium import plugins
import pandas as pd

# Configuración inicial - Coordenadas de Chía, Cundinamarca
CHIA_CENTER = [4.8641, -74.0519]
ZOOM_LEVEL = 13

# Datos de ejemplo de zonas de Chía (basados en el POT real)
zonas_chia = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "nombre": "Centro Histórico",
                "codigo": "ZCH",
                "descripcion": "Zona de conservación del centro histórico",
                "usos": "Comercial, Cultural, Residencial",
                "altura_max": "3 pisos",
                "color": "#FF6B6B"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0530, 4.8641],
                    [-74.0520, 4.8641],
                    [-74.0520, 4.8651],
                    [-74.0530, 4.8651],
                    [-74.0530, 4.8641]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nombre": "Zona Residencial Norte",
                "codigo": "ZRN",
                "descripcion": "Área residencial de estratos medios-altos",
                "usos": "Residencial, Comercio barrial",
                "altura_max": "4 pisos",
                "color": "#4ECDC4"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0540, 4.8651],
                    [-74.0510, 4.8651],
                    [-74.0510, 4.8671],
                    [-74.0540, 4.8671],
                    [-74.0540, 4.8651]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nombre": "Zona Industrial",
                "codigo": "ZI",
                "descripcion": "Área destinada a actividades industriales",
                "usos": "Industrial, Logística",
                "altura_max": "Sin restricción",
                "color": "#95A5A6"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0570, 4.8611],
                    [-74.0540, 4.8611],
                    [-74.0540, 4.8631],
                    [-74.0570, 4.8631],
                    [-74.0570, 4.8611]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nombre": "Zona Verde Protegida",
                "codigo": "ZVP",
                "descripcion": "Área de conservación ambiental",
                "usos": "Conservación, Recreación pasiva",
                "altura_max": "No aplica",
                "color": "#2ECC71"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0500, 4.8611],
                    [-74.0470, 4.8611],
                    [-74.0470, 4.8641],
                    [-74.0500, 4.8641],
                    [-74.0500, 4.8611]
                ]]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "nombre": "Zona Comercial",
                "codigo": "ZC",
                "descripcion": "Corredor comercial principal",
                "usos": "Comercial, Servicios, Oficinas",
                "altura_max": "5 pisos",
                "color": "#F39C12"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.0520, 4.8611],
                    [-74.0490, 4.8611],
                    [-74.0490, 4.8621],
                    [-74.0520, 4.8621],
                    [-74.0520, 4.8611]
                ]]
            }
        }
    ]
}

def crear_mapa_chia():
    """Crear el mapa interactivo de zonificación de Chía"""
    
    # Crear el mapa base
    mapa = folium.Map(
        location=CHIA_CENTER,
        zoom_start=ZOOM_LEVEL,
        tiles='OpenStreetMap'
    )
    
    # Agregar tiles alternativos
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satelital',
        overlay=False,
        control=True
    ).add_to(mapa)
    
    folium.TileLayer(
        tiles='CartoDB positron',
        name='CartoDB Positron',
        overlay=False,
        control=True
    ).add_to(mapa)
    
    # Agregar las zonas al mapa
    for feature in zonas_chia['features']:
        propiedades = feature['properties']
        
        # Crear el popup con información detallada
        popup_content = f"""
        <div style="width: 250px;">
            <h4 style="color: {propiedades['color']};">{propiedades['nombre']}</h4>
            <hr>
            <p><strong>Código:</strong> {propiedades['codigo']}</p>
            <p><strong>Descripción:</strong> {propiedades['descripcion']}</p>
            <p><strong>Usos permitidos:</strong> {propiedades['usos']}</p>
            <p><strong>Altura máxima:</strong> {propiedades['altura_max']}</p>
        </div>
        """
        
        # Agregar polígono al mapa
        folium.GeoJson(
            feature,
            style_function=lambda x, color=propiedades['color']: {
                'fillColor': color,
                'color': 'black',
                'weight': 2,
                'fillOpacity': 0.6
            },
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=propiedades['nombre']
        ).add_to(mapa)
    
    # Agregar leyenda
    leyenda_html = '''
    <div style="position: fixed; 
                top: 10px; right: 10px; width: 200px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4 style="margin-top:0;">Zonificación Chía</h4>
    '''
    
    for feature in zonas_chia['features']:
        prop = feature['properties']
        leyenda_html += f'''
        <p><span style="color:{prop['color']}; font-size:16px;">●</span> 
        <strong>{prop['codigo']}</strong> - {prop['nombre']}</p>
        '''
    
    leyenda_html += '</div>'
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    # Agregar controles adicionales
    folium.LayerControl().add_to(mapa)
    
    # Plugin de pantalla completa
    plugins.Fullscreen().add_to(mapa)
    
    # Plugin de medición
    plugins.MeasureControl().add_to(mapa)
    
    # Agregar marcador del centro de Chía
    folium.Marker(
        CHIA_CENTER,
        popup='Centro de Chía',
        tooltip='Chía, Cundinamarca',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(mapa)
    
    return mapa

def guardar_datos_geojson():
    """Guardar los datos como archivo GeoJSON"""
    with open('zonificacion_chia.geojson', 'w', encoding='utf-8') as f:
        json.dump(zonas_chia, f, ensure_ascii=False, indent=2)
    print("Archivo GeoJSON guardado como 'zonificacion_chia.geojson'")

def crear_reporte_zonas():
    """Crear un reporte básico de las zonas"""
    zonas_data = []
    for feature in zonas_chia['features']:
        prop = feature['properties']
        zonas_data.append({
            'Código': prop['codigo'],
            'Nombre': prop['nombre'],
            'Usos': prop['usos'],
            'Altura Máxima': prop['altura_max']
        })
    
    df = pd.DataFrame(zonas_data)
    df.to_csv('reporte_zonas_chia.csv', index=False, encoding='utf-8')
    print("Reporte guardado como 'reporte_zonas_chia.csv'")
    print("\nResumen de zonas:")
    print(df.to_string(index=False))

if __name__ == "__main__":
    print("Creando mapa interactivo de zonificación de Chía...")
    
    # Crear el mapa
    mapa = crear_mapa_chia()
    
    # Guardar el mapa como HTML
    nombre_archivo = 'mapa_zonificacion_chia.html'
    mapa.save(nombre_archivo)
    
    print(f"¡Mapa creado exitosamente! Archivo: {nombre_archivo}")
    print("Abre el archivo HTML en tu navegador para ver el mapa.")
    
    # Guardar archivos adicionales
    guardar_datos_geojson()
    crear_reporte_zonas()
    
    print("\nFuncionalidades del mapa:")
    print("- Click en las zonas para ver información detallada")
    print("- Cambiar entre diferentes vistas de mapa (OpenStreetMap, Satelital, CartoDB)")
    print("- Herramienta de medición disponible")
    print("- Modo pantalla completa")
    print("- Leyenda interactiva")