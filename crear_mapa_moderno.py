import os
import json
import webbrowser
from datetime import datetime

def crear_mapa_html():
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zonificación POT Chía - Cundinamarca</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); overflow: hidden; }
        #container { display: flex; height: 100vh; position: relative; }
        #sidebar { width: 380px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); box-shadow: 2px 0 20px rgba(0,0,0,0.1); z-index: 1000; overflow-y: auto; transition: transform 0.3s ease; }
        #sidebar.collapsed { transform: translateX(-340px); }
        .sidebar-header { background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); color: white; padding: 25px 20px; text-align: center; }
        .sidebar-header h1 { font-size: 20px; margin-bottom: 8px; }
        .sidebar-header p { font-size: 13px; opacity: 0.9; }
        .section { padding: 20px; border-bottom: 1px solid #ecf0f1; }
        .section h3 { color: #2c3e50; font-size: 16px; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .zona-item { background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%); border-radius: 10px; padding: 15px; margin-bottom: 12px; border-left: 5px solid; box-shadow: 0 3px 12px rgba(0,0,0,0.08); cursor: pointer; transition: all 0.3s ease; }
        .zona-item:hover { transform: translateX(8px) translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
        .zona-codigo { font-weight: bold; font-size: 16px; color: #2c3e50; background: rgba(44, 62, 80, 0.1); padding: 4px 8px; border-radius: 6px; display: inline-block; margin-bottom: 8px; }
        .zona-nombre { font-size: 13px; color: #34495e; margin-bottom: 6px; font-weight: 500; }
        .zona-usos { font-size: 11px; color: #7f8c8d; line-height: 1.4; }
        .controls { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .control-btn { padding: 12px; border: none; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .control-btn.primary { background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); color: white; box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3); }
        .control-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(0,0,0,0.2); }
        #toggle-sidebar { position: absolute; left: 390px; top: 20px; z-index: 1001; background: rgba(255,255,255,0.95); border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; box-shadow: 0 4px 20px rgba(0,0,0,0.15); transition: all 0.3s ease; display: flex; align-items: center; justify-content: center; font-size: 16px; color: #2c3e50; }
        #toggle-sidebar.collapsed { left: 60px; }
        #toggle-sidebar:hover { background: white; transform: scale(1.1); color: #3498db; }
        #map { flex: 1; height: 100vh; position: relative; }
        .north-indicator { position: absolute; top: 80px; left: 20px; z-index: 1000; width: 70px; height: 70px; background: rgba(255,255,255,0.95); border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: 0 6px 20px rgba(0,0,0,0.15); border: 3px solid #3498db; }
        .north-arrow { font-size: 28px; color: #e74c3c; font-weight: bold; }
        .north-letter { font-size: 12px; color: #2c3e50; font-weight: bold; }
        #info-panel { position: absolute; bottom: 20px; right: 20px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-radius: 15px; padding: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); max-width: 320px; z-index: 1000; transform: translateY(120px); opacity: 0; transition: all 0.4s ease; }
        #info-panel.show { transform: translateY(0); opacity: 1; }
        .info-header { font-weight: bold; color: #2c3e50; margin-bottom: 12px; font-size: 15px; }
        .info-content { font-size: 13px; color: #7f8c8d; line-height: 1.5; }
        .loading { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: white; z-index: 2000; }
        .spinner { width: 50px; height: 50px; border: 5px solid rgba(255,255,255,0.3); border-radius: 50%; border-top: 5px solid white; animation: spin 1s linear infinite; margin: 0 auto 15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @media (max-width: 768px) { #sidebar { width: 100%; position: absolute; height: 100vh; transform: translateX(-100%); } #sidebar.show { transform: translateX(0); } #toggle-sidebar { left: 20px; } }
    </style>
</head>
<body>
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <h3>Cargando Zonificación de Chía</h3>
        <p>Inicializando mapa interactivo...</p>
    </div>
    <div id="container">
        <div id="sidebar">
            <div class="sidebar-header">
                <h1><i class="fas fa-map-marked-alt"></i> POT Chía 2024</h1>
                <p>Plan de Ordenamiento Territorial</p>
                <p>Cundinamarca, Colombia</p>
            </div>
            <div class="section">
                <h3><i class="fas fa-layer-group"></i> Zonas de Uso del Suelo</h3>
                <div id="zonas-list"></div>
            </div>
            <div class="section">
                <h3><i class="fas fa-tools"></i> Herramientas</h3>
                <div class="controls">
                    <button class="control-btn primary" onclick="fitAllZones()"><i class="fas fa-expand-arrows-alt"></i> Vista General</button>
                    <button class="control-btn primary" onclick="downloadData()"><i class="fas fa-download"></i> Exportar</button>
                </div>
            </div>
        </div>
        <button id="toggle-sidebar" onclick="toggleSidebar()"><i class="fas fa-bars"></i></button>
        <div id="map"></div>
        <div class="north-indicator">
            <div class="north-arrow">↑</div>
            <div class="north-letter">N</div>
        </div>
        <div id="info-panel">
            <div class="info-header">Información del Proyecto</div>
            <div class="info-content">Haga clic en cualquier zona para ver información detallada.</div>
        </div>
    </div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        const CHIA_CENTER = [4.8641, -74.0519];
        const ZOOM_LEVEL = 13;
        let map, zonasLayer;
        const zonasData = {
            "ZCH": {"nombre": "Centro Histórico", "descripcion": "Zona de conservación del centro histórico de Chía", "usos": "Comercial, Cultural, Residencial, Institucional", "altura_max": "3 pisos", "color": "#E74C3C", "border_color": "#C0392B", "coordinates": [[-74.0540, 4.8620], [-74.0500, 4.8620], [-74.0500, 4.8660], [-74.0540, 4.8660], [-74.0540, 4.8620]]},
            "ZRN": {"nombre": "Yerbabuena Norte", "descripcion": "Zona residencial consolidada de Yerbabuena", "usos": "Residencial, Comercio barrial, Servicios", "altura_max": "4 pisos", "color": "#2ECC71", "border_color": "#27AE60", "coordinates": [[-74.0420, 4.8660], [-74.0350, 4.8660], [-74.0350, 4.8720], [-74.0420, 4.8720], [-74.0420, 4.8660]]},
            "ZI": {"nombre": "Fusca Industrial", "descripcion": "Zona industrial de Fusca", "usos": "Industrial, Logística, Bodegas", "altura_max": "Sin restricción específica", "color": "#95A5A6", "border_color": "#7F8C8D", "coordinates": [[-74.0420, 4.8540], [-74.0350, 4.8540], [-74.0350, 4.8600], [-74.0420, 4.8600], [-74.0420, 4.8540]]},
            "ZVP": {"nombre": "La Balsa Ecológica", "descripcion": "Área de protección ambiental La Balsa", "usos": "Conservación, Recreación pasiva, Ecoturismo", "altura_max": "No aplica", "color": "#27AE60", "border_color": "#1E8449", "coordinates": [[-74.0600, 4.8540], [-74.0540, 4.8540], [-74.0540, 4.8600], [-74.0600, 4.8600], [-74.0600, 4.8540]]},
            "ZC": {"nombre": "Corredor Comercial", "descripcion": "Eje comercial principal de Chía", "usos": "Comercial, Servicios, Oficinas, Restaurantes", "altura_max": "5 pisos", "color": "#F39C12", "border_color": "#D68910", "coordinates": [[-74.0540, 4.8600], [-74.0460, 4.8600], [-74.0460, 4.8620], [-74.0540, 4.8620], [-74.0540, 4.8600]]},
            "ZM": {"nombre": "Fagua Mixta", "descripcion": "Zona mixta de Fagua - residencial y comercial", "usos": "Residencial, Comercial, Servicios, Mixto", "altura_max": "4 pisos", "color": "#E67E22", "border_color": "#CA6F1E", "coordinates": [[-74.0600, 4.8660], [-74.0540, 4.8660], [-74.0540, 4.8720], [-74.0600, 4.8720], [-74.0600, 4.8660]]},
            "ZR": {"nombre": "Bojacá Residencial", "descripcion": "Zona residencial de Bojacá", "usos": "Residencial, Equipamientos, Servicios básicos", "altura_max": "3 pisos", "color": "#9B59B6", "border_color": "#8E44AD", "coordinates": [[-74.0500, 4.8660], [-74.0460, 4.8660], [-74.0460, 4.8700], [-74.0500, 4.8700], [-74.0500, 4.8660]]},
            "ZRU": {"nombre": "Fonquetá Rural", "descripcion": "Zona rural de Fonquetá", "usos": "Rural, Agropecuario, Vivienda campestre", "altura_max": "2 pisos", "color": "#F1C40F", "border_color": "#F39C12", "coordinates": [[-74.0600, 4.8600], [-74.0560, 4.8600], [-74.0560, 4.8640], [-74.0600, 4.8640], [-74.0600, 4.8600]]}
        };
        function initMap() {
            map = L.map('map', { center: CHIA_CENTER, zoom: ZOOM_LEVEL, zoomControl: false });
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(map);
            L.control.zoom({ position: 'bottomleft' }).addTo(map);
            addZones(); generateZonesList(); addCenterMarker();
            setTimeout(() => { document.getElementById('loading').style.display = 'none'; }, 2000);
        }
        function addZones() {
            zonasLayer = L.layerGroup();
            Object.keys(zonasData).forEach(codigo => {
                const zona = zonasData[codigo];
                const polygon = L.polygon(zona.coordinates, { fillColor: zona.color, color: zona.border_color, weight: 3, fillOpacity: 0.75, opacity: 1 });
                const popupContent = `<div style="width: 280px;"><div style="background: ${zona.color}; color: white; padding: 12px; margin: -10px -10px 10px -10px; border-radius: 8px;"><h3 style="margin: 0;">${codigo} - ${zona.nombre}</h3></div><p><strong>Descripción:</strong><br>${zona.descripcion}</p><p><strong>Usos:</strong><br>${zona.usos}</p><p><strong>Altura máxima:</strong><br>${zona.altura_max}</p></div>`;
                polygon.bindPopup(popupContent, { maxWidth: 320 });
                polygon.on('click', () => showZoneInfo(codigo, zona));
                polygon.on('mouseover', function() { this.setStyle({ fillOpacity: 0.9, weight: 4 }); });
                polygon.on('mouseout', function() { this.setStyle({ fillOpacity: 0.75, weight: 3 }); });
                const center = polygon.getBounds().getCenter();
                const label = L.marker(center, { icon: L.divIcon({ className: 'zone-label', html: `<div style="background: rgba(0,0,0,0.7); color: white; padding: 2px 6px; border-radius: 12px; font-size: 11px; font-weight: bold; border: 1px solid white;">${codigo}</div>`, iconSize: [40, 20], iconAnchor: [20, 10] }) });
                zonasLayer.addLayer(polygon); zonasLayer.addLayer(label);
            });
            zonasLayer.addTo(map);
        }
        function addCenterMarker() { L.marker(CHIA_CENTER, { icon: L.divIcon({ html: '<div style="background: #e74c3c; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>', iconSize: [20, 20], iconAnchor: [10, 10] }) }).addTo(map).bindPopup('<div style="text-align: center; padding: 10px;"><h4 style="color: #e74c3c; margin: 0 0 8px 0;">Alcaldía Municipal</h4><p>Centro Administrativo de Chía<br>Cundinamarca, Colombia</p></div>'); }
        function generateZonesList() { const container = document.getElementById('zonas-list'); Object.keys(zonasData).forEach(codigo => { const zona = zonasData[codigo]; const item = document.createElement('div'); item.className = 'zona-item'; item.style.borderLeftColor = zona.color; item.onclick = () => zoomToZone(codigo); item.innerHTML = `<div class="zona-codigo">${codigo}</div><div class="zona-nombre">${zona.nombre}</div><div class="zona-usos">${zona.usos}</div>`; container.appendChild(item); }); }
        function zoomToZone(codigo) { const zona = zonasData[codigo]; if (zona) { const bounds = L.polygon(zona.coordinates).getBounds(); map.fitBounds(bounds, { padding: [30, 30] }); setTimeout(() => showZoneInfo(codigo, zona), 800); } }
        function showZoneInfo(codigo, zona) { const infoPanel = document.getElementById('info-panel'); const header = infoPanel.querySelector('.info-header'); const content = infoPanel.querySelector('.info-content'); header.innerHTML = `${codigo} - ${zona.nombre}`; content.innerHTML = `<strong>Descripción:</strong><br>${zona.descripcion}<br><br><strong>Usos permitidos:</strong><br>${zona.usos}<br><br><strong>Altura máxima:</strong><br>${zona.altura_max}`; infoPanel.classList.add('show'); setTimeout(() => infoPanel.classList.remove('show'), 8000); }
        function toggleSidebar() { const sidebar = document.getElementById('sidebar'); const toggle = document.getElementById('toggle-sidebar'); sidebar.classList.toggle('collapsed'); toggle.classList.toggle('collapsed'); setTimeout(() => map.invalidateSize(), 300); }
        function fitAllZones() { if (zonasLayer) { map.fitBounds(zonasLayer.getBounds(), { padding: [30, 30] }); } }
        function downloadData() { const geojson = { type: "FeatureCollection", features: Object.keys(zonasData).map(codigo => { const zona = zonasData[codigo]; return { type: "Feature", properties: { codigo, ...zona }, geometry: { type: "Polygon", coordinates: [zona.coordinates] } }; }) }; const dataStr = JSON.stringify(geojson, null, 2); const dataBlob = new Blob([dataStr], { type: 'application/json' }); const link = document.createElement('a'); link.href = URL.createObjectURL(dataBlob); link.download = 'zonificacion_chia_2024.geojson'; link.click(); }
        document.addEventListener('DOMContentLoaded', initMap);
        window.addEventListener('resize', () => map && map.invalidateSize());
    </script>
</body>
</html>'''
    return html_content

def main():
    print("Creando mapa moderno de Chía...")
    try:
        html_content = crear_mapa_html()
        filename = 'mapa_chia_moderno.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Archivo {filename} creado exitosamente")
        webbrowser.open(filename)
        print("Mapa abierto en navegador")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()