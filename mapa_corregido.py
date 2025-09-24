import folium

PLAZA_DIOSA_CHIA = [4.8582, -74.0588]
mapa = folium.Map(location=PLAZA_DIOSA_CHIA, zoom_start=15)
folium.Marker(PLAZA_DIOSA_CHIA, popup='Plaza Diosa Chia', icon=folium.Icon(color='red')).add_to(mapa)
mapa.save('mapa_chia_centro_corregido.html')
print('Mapa creado')
