import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'
import axios from 'axios'
import L from 'leaflet'

// Memperbaiki bug icon bawaan Leaflet di React
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

export default function MapView() {
  const [geoData, setGeoData] = useState(null)
  
  // 1. State baru khusus untuk data hasil deteksi AI
  const [aiData, setAiData] = useState(null)

  useEffect(() => {
    // Menarik data GeoJSON fasilitas dari backend FastAPI
    axios.get('http://localhost:8000/api/fasilitas/geojson')
      .then(res => setGeoData(res.data))
      .catch(err => console.error("Gagal tarik API:", err))

    // 2. Menarik data hasil deteksi AI dari folder public
    axios.get('/hasil_deteksi.geojson')
      .then(res => setAiData(res.data))
      .catch(err => console.error("Gagal load data AI:", err))
  }, [])

  // Styling beda warna berdasarkan jenis fasilitas
  const pointToLayer = (feature, latlng) => {
    let warna = '#3388ff' // default biru
    
    if (feature.properties.jenis === 'Museum') warna = '#ff9900' 
    if (feature.properties.jenis === 'Sekolah' || feature.properties.jenis === 'Kampus') warna = '#33ff55' 
    if (feature.properties.jenis === 'Masjid' || feature.properties.jenis === 'Ibadah') warna = '#9900ff' 

    return L.circleMarker(latlng, {
      radius: 8,
      fillColor: warna,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9
    })
  }

  // Interaksi: Popup saat diklik & Hover saat disentuh mouse untuk fasilitas publik
  const onEachFeature = (feature, layer) => {
    // Popup HTML
    layer.bindPopup(`
      <div style="text-align:center; min-width:150px;">
        <h3 style="margin:0 0 5px 0; color:#1e3a8a;">${feature.properties.nama}</h3>
        <p style="margin:0; font-size:14px; color:#555;">Kategori: <b>${feature.properties.jenis}</b></p>
      </div>
    `)

    // Hover Highlight
    layer.on({
      mouseover: (e) => {
        e.target.setStyle({ weight: 4, radius: 12 }) 
      },
      mouseout: (e) => {
        e.target.setStyle({ weight: 2, radius: 8 }) 
      }
    })
  }

  return (
    <MapContainer 
      center={[-5.37, 105.24]} // Titik tengah area Rajabasa
      zoom={14} 
      style={{ height: '100%', width: '100%', borderRadius: '12px' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      
      {/* Ini layer data fasilitas aslimu */}
      {geoData && (
        <GeoJSON 
          data={geoData} 
          pointToLayer={pointToLayer}
          onEachFeature={onEachFeature} 
        />
      )}

      {/* 3. Ini layer tambahan untuk menampilkan hasil AI (Titik Merah) */}
      {aiData && (
        <GeoJSON 
          data={aiData} 
          pointToLayer={(feature, latlng) => {
             return L.circleMarker(latlng, {
               radius: 10,
               fillColor: '#ef4444', // Warna merah untuk membedakan
               color: '#000',
               weight: 2,
               fillOpacity: 1
             })
          }}
          onEachFeature={(feature, layer) => {
             layer.bindPopup(`
               <div style="text-align:center;">
                 <h4 style="margin:0 0 5px 0; color:#ef4444;">Deteksi AI</h4>
                 <p style="margin:0;">Objek: <b>${feature.properties.class_name}</b></p>
                 <p style="margin:0;">Confidence: ${feature.properties.confidence}</p>
               </div>
             `)
          }}
        />
      )}
    </MapContainer>
  )
}