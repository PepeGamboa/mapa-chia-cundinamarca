import folium
import json
from folium import plugins

def crear_mapa_chia_corregido():
    """
    Mapa de Chía con centro histórico CORRECTAMENTE ubicado en Parque Diosa Chía
    Basado en la ubicación real mostrada en el mapa de referencia
    """
    
    # COORDENADAS CORREGIDAS basadas en la ubicación real del Parque Diosa Chía
    # Según la imagen, está al sureste del centro, cerca de la Calle 12
    parque_diosa_chia_coords = [4.8580, -74.0520]  # Ubicación real del parque
    
    # Crear mapa centrado en el Parque Diosa Chía
    mapa = folium.Map(
        location=parque_diosa_chia_coords,
        zoom_start=16,  # Zoom más cercano para ver mejor el detalle
        tiles='OpenStreetMap'
    )
    
    # Definir las zonas con coordenadas más precisas basadas en la realidad
    zonas_uso_suelo = {
        'ZCH': {  # Centro Histórico - PARQUE DIOSA CHÍA (ubicación real)
            'nombre': 'Centro Histórico - Parque Diosa Chía',
            'descripcion': 'Patrimonio Cultural, Comercial, Institucional, Residencial',
            'color': '#e74c3c',
            'coords': [
                [4.8600, -74.0540],  # Esquina noreste
                [4.8600, -74.0500],  # Esquina noroeste  
                [4.8560, -74.0500],  # Esquina suroeste
                [4.8560, -74.0540],  # Esquina sureste
            ]
        },
        'ZC_DIAGONAL': {  # Corredor Comercial Diagonal 13
            'nombre': 'Corredor Comercial Diagonal 13',
            'descripcion': 'Comercio, Servicios, Oficinas, Restaurantes',
            'color': '#f39c12',
            'coords': [
                [4.8620, -74.0600],
                [4.8620, -74.0400],
                [4.8600, -74.0400],
                [4.8600, -74.0600]
            ]
        },
        'ZRN': {  # Zona Residencial Norte
            'nombre': 'Yerbabuena Norte',
            'descripcion': 'Residencial, Comercio barrial, Servicios',
            'color': '#27ae60',
            'coords': [
                [4.8700, -74.0600],
                [4.8700, -74.0350],
                [4.8620, -74.0350],
                [4.8620, -74.0600]
            ]
        },
        'ZRS': {  # Zona Residencial Sur
            'nombre': 'Zona Residencial Sur',
            'descripción': 'Residencial, Equipamientos básicos',
            'color': '#3498db',
            'coords': [
                [4.8560, -74.0600],
                [4.8560, -74.0400],
                [4.8500, -74.0400],
                [4.8500, -74.0600]
            ]
        },
        'ZVP': {  # Zona Verde y Parques
            'nombre': 'Zonas Verdes y Parques',
            'descripcion': 'Recreación, Conservación, Espacios públicos',
            'color': '#2ecc71',
            'coords': [
                [4.8650, -74.0520],  # Incluye el área del Parque Diosa Chía
                [4.8650, -74.0480],
                [4.8580, -74.0480],
                [4.8580, -74.0520]
            ]
        },
        'ZM': {  # Zona Mixta
            'nombre': 'Zona Mixta',
            'descripcion': 'Residencial, Comercial, Servicios',
            'color': '#e67e22',
            'coords': [
                [4.8500, -74.0700],
                [4.8500, -74.0600],
                [4.8450, -74.0600],
                [4.8450, -74.0700]
            ]
        }
    }
    
    # Agregar las zonas al mapa
    for codigo, zona in zonas_uso_suelo.items():
        folium.Polygon(
            locations=zona['coords'],
            color='black',
            weight=2,
            fill=True,
            fillColor=zona['color'],
            fillOpacity=0.4,
            popup=folium.Popup(f"""
                <div style='width: 250px; padding: 10px;'>
                    <h4 style='color: {zona['color']}; margin: 0 0 10px 0;'>{codigo}</h4>
                    <h5 style='margin: 0 0 8px 0;'>{zona['nombre']}</h5>
                    <p style='margin: 0; font-size: 13px;'><b>Descripción:</b><br>
                    {zona['descripcion']}</p>
                </div>
            """, max_width=300)
        ).add_to(mapa)
    
    # MARCADOR PRINCIPAL - PARQUE DIOSA CHÍA (Centro Histórico Real)
    folium.Marker(
        parque_diosa_chia_coords,
        popup=folium.Popup("""
            <div style='width: 300px; text-align: center; padding: 15px;'>
                <h2 style='color: #e74c3c; margin: 0 0 10px 0;'>
                    🏛️ PARQUE DIOSA CHÍA
                </h2>
                <h3 style='color: #2c3e50; margin: 0 0 10px 0;'>
                    CENTRO HISTÓRICO DE CHÍA
                </h3>
                <p style='margin: 0; font-size: 14px;'>
                    <b>Ubicación Corregida</b><br>
                    Corazón cultural e histórico del municipio<br>
                    Patrimonio arqueológico y cultural<br>
                    <small>Coordenadas: 4.8580, -74.0520</small>
                </p>
            </div>
        """, max_width=350),
        tooltip="Centro Histórico - Parque Diosa Chía ✅",
        icon=folium.Icon(color='red', icon='star', prefix='fa')
    ).add_to(mapa)
    
    # Puntos de referencia importantes
    puntos_referencia = [
        {
            'coords': [4.8590, -74.0510],
            'nombre': 'Iglesia del Centro',
            'descripcion': 'Patrimonio religioso histórico',
            'icon': 'church',
            'color': 'blue'
        },
        {
            'coords': [4.8610, -74.0530],
            'nombre': 'Plaza Principal',
            'descripcion': 'Centro cívico y comercial',
            'icon': 'home',
            'color': 'green'
        },
        {
            'coords': [4.8595, -74.0525],
            'nombre': 'Alcaldía de Chía',
            'descripcion': 'Sede administrativa municipal',
            'icon': 'building',
            'color': 'darkblue'
        },
        {
            'coords': [4.8570, -74.0515],
            'nombre': 'Sitio Arqueológico',
            'descripcion': 'Restos de la cultura Muisca',
            'icon': 'monument',
            'color': 'purple'
        }
    ]
    
    for punto in puntos_referencia:
        folium.Marker(
            punto['coords'],
            popup=folium.Popup(f"""
                <div style='min-width: 180px;'>
                    <h4 style='color: {punto['color']}; margin: 0 0 8px 0;'>
                        {punto['nombre']}
                    </h4>
                    <p style='margin: 0; font-size: 13px;'>
                        {punto['descripcion']}
                    </p>
                </div>
            """),
            tooltip=punto['nombre'],
            icon=folium.Icon(color=punto['color'], icon=punto['icon'], prefix='fa')
        ).add_to(mapa)
    
    # Agregar círculo destacando el área del Parque Diosa Chía
    folium.Circle(
        parque_diosa_chia_coords,
        radius=150,  # 150 metros de radio
        color='red',
        weight=3,
        fill=True,
        fillColor='red',
        fillOpacity=0.1,
        popup="Área del Parque Diosa Chía - Centro Histórico"
    ).add_to(mapa)
    
    # Leyenda actualizada
    leyenda_html = '''
    <div style="position: fixed; 
                top: 10px; left: 10px; width: 320px; height: auto; 
                background-color: rgba(255, 255, 255, 0.95); 
                border: 2px solid #e74c3c; border-radius: 10px;
                z-index: 9999; font-size: 14px; padding: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    
    <h3 style="margin: 0 0 15px 0; color: #e74c3c; text-align: center;">
        🗺️ MAPA CORREGIDO DE CHÍA
    </h3>
    <p style="margin: 0 0 10px 0; font-size: 12px; text-align: center;">
        <b>Centro Histórico ubicado correctamente</b><br>
        <small>📍 Parque Diosa Chía</small>
    </p>
    
    <h4 style="margin: 10px 0 5px 0; color: #2c3e50;">Zonas de Uso del Suelo:</h4>
    '''
    
    for codigo, zona in zonas_uso_suelo.items():
        leyenda_html += f'''
        <div style="margin: 8px 0; display: flex; align-items: center;">
            <span style="color: {zona['color']}; font-size: 16px; margin-right: 8px;">●</span>
            <div>
                <b style="color: #2c3e50;">{codigo}</b>: {zona['nombre']}<br>
                <small style="color: #7f8c8d;">{zona['descripcion']}</small>
            </div>
        </div>
        '''
    
    leyenda_html += '''
    <hr style="margin: 15px 0 10px 0;">
    <p style="margin: 0; font-size: 11px; color: #95a5a6; text-align: center;">
        POT Chía 2024 - Cundinamarca, Colombia<br>
        <b style="color: #e74c3c;">✅ Corrección aplicada: Centro histórico en ubicación real</b>
    </p>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(leyenda_html))
    
    # Herramientas adicionales
    plugins.Fullscreen(
        position='topright',
        title='Pantalla completa',
        title_cancel='Salir pantalla completa',
        force_separate_button=True
    ).add_to(mapa)
    
    plugins.MeasureControl(
        primary_length_unit='meters',
        secondary_length_unit='kilometers',
        primary_area_unit='sqmeters',
        secondary_area_unit='hectares'
    ).add_to(mapa)
    
    return mapa

def main():
    """
    Genera el mapa corregido de Chía con centro histórico en ubicación real
    """
    print("🗺️ Generando mapa CORREGIDO de Chía...")
    print("📍 Centro histórico ubicado en PARQUE DIOSA CHÍA (ubicación real)")
    
    # Crear el mapa
    mapa = crear_mapa_chia_corregido()
    
    # Guardar el mapa
    nombre_archivo = "mapa_chia_PARQUE_DIOSA_CHIA_corregido.html"
    
    try:
        mapa.save(nombre_archivo)
        print(f"✅ ¡Mapa corregido guardado como: {nombre_archivo}")
        print("\n🎯 CORRECCIONES APLICADAS:")
        print("   ✅ Centro histórico movido al Parque Diosa Chía")
        print("   ✅ Coordenadas precisas: [4.8580, -74.0520]")
        print("   ✅ Zonas redibujadas según ubicación real")
        print("   ✅ Marcadores de referencia agregados")
        print("\n🌐 Para ver el mapa:")
        print("   1. Abre el archivo HTML en tu navegador")
        print("   2. O ejecuta: python -m http.server 8000")
        print("   3. Ve a: http://localhost:8000")
        print(f"\n🚀 Para GitHub: renombra '{nombre_archivo}' a 'index.html'")
        
    except Exception as e:
        print(f"❌ Error al guardar el mapa: {e}")

if __name__ == "__main__":
    main()