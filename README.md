# Tugas Praktikum 10: Spatial AI & WebGIS

**Nama:** M. Zahran Dhiyaul Haq  
**NIM:** 123140120  
**Mata Kuliah:** Sistem Informasi Geografis  

## Deskripsi
Repositori ini dikerjakan untuk memenuhi Tugas Pertemuan 10 mengenai implementasi Spatial AI dan Computer Vision pada WebGIS. 

Sistem ini melakukan ekstraksi fitur/objek dari citra satelit (GeoTIFF) menggunakan model YOLOv8. Hasil koordinat piksel kemudian dikonversi menjadi koordinat spasial menggunakan `rasterio` agar bisa diekspor menjadi file `GeoJSON`. File hasil deteksi tersebut kemudian ditampilkan di atas peta pada frontend menggunakan React-Leaflet.

## Catatan Pengerjaan (Transparency Note)
1. **Prioritas Modul:** Mengingat tenggat waktu yang sangat terbatas, saya memprioritaskan pengerjaan Tugas 10 ini terlebih dahulu untuk mengamankan nilai integrasi Computer Vision. Fitur Auth dan CRUD lengkap dari Praktikum 9 belum sempat saya integrasikan di repositori ini.
2. **Penggunaan AI:** Dalam proses pengerjaan *pipeline* Python dan *debugging* integrasi ke React dalam waktu singkat ini, saya sepenuhnya menggunakan bantuan AI (LLM) sebagai *pair-programmer* untuk membimbing penulisan sintaks dan integrasi *library*.

## Tech Stack
- **Backend/AI:** Python, Ultralytics (YOLOv8 Nano), OpenCV, Rasterio
- **Frontend:** ReactJS, React-Leaflet, Axios

## Cara Menjalankan Aplikasi

**1. Eksekusi Model AI (Generate GeoJSON)**
Masuk ke folder `webgis-api` dan jalankan script pipeline:
python pipeline_ai.py
(Proses ini akan menghasilkan file hasil_deteksi.geojson yang akan dibaca oleh frontend).

2. Jalankan Backend
Di folder webgis-api:
uvicorn app.main:app --reload

3. Jalankan Frontend
Buka terminal baru, masuk ke folder webgis-frontend:
npm run dev
