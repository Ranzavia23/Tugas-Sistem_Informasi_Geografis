import MapView from './components/MapView'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <header className="header">
        <h1>WebGIS Fasilitas Rajabasa</h1>
        <p>M. Zahran Dhiyaul Haq - 123140120</p>
      </header>
      <main className="map-wrapper">
        <MapView />
      </main>
    </div>
  )
}

export default App